import datetime
import random

import requests
import xmltodict
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView, TemplateView

from . import forms, models, utils

########################
# Generate Random User #
########################

def create_random_user(request):
	username = random.randint(100000, 999999)
	password = random.randint(1000, 9999)

	user = User.objects.create_user(username, '', password)
	messages.success(request, 'Library ID: {}, PIN: {}'.format(username,password))

	return redirect('index')

###########
# Content #
###########

def index(request):
	news = models.New.objects.all()[:5]
	return render(request, 'content/index.html', {'news':news})

class About(TemplateView):
	template_name = 'content/about.html'

class Apply(TemplateView):
	template_name = 'content/apply.html'

################
# Browse Views #
################

def browse(request):

	number_of_books = 8

	lastest_books = models.Book.objects.all()[:number_of_books]
	fiction_books = models.Book.objects.filter(category="science-fiction")[:number_of_books]
	fantasy_books = models.Book.objects.filter(category="fantasy")[:number_of_books]
	mystery_books = models.Book.objects.filter(category="mystery")[:number_of_books]
	crime_books = models.Book.objects.filter(category="crime")[:number_of_books]

	content = {
		'lastest_books':lastest_books,
		'fiction_books':fiction_books,
		'fantasy_books':fantasy_books,
		'mystery_books':mystery_books,	
		'crime_books':crime_books,
	}

	return render(request, 'content/books.html', content)


def all_books(request):
	content = {
		'book_set':models.Book.objects.all(),
		'title':"All Books",
	}
	return render(request, 'content/category.html', content)

def last_books(request):
	content = {
		'book_set':models.Book.objects.all()[:12],
		'title':"Last Books",
	}
	return render(request, 'content/category.html', content)

def category(request,category):
	books = models.Book.objects.filter(category=category)
	content = {
		'book_set':books,
		'title':"Category {}".format(category.capitalize()),
	}
	return render(request, 'content/category.html', content)

def authors(request):
	authors = models.Author.objects.all()[:10]
	return render(request, 'content/authors.html', {'authors':authors})

def series(request):
	series = models.Serie.objects.all()[:10]
	return render(request, 'content/series.html', {'series':series})

def search(request):

	search = request.GET.get('q')
	category = request.GET.get('c')

	if category == 'title':
		books = models.Book.objects.filter(name__icontains=search).order_by('name').distinct()
	elif category == 'isbn':
		books = models.Book.objects.filter(isbn__icontains=search).order_by('name').distinct()
	elif category == 'author':
		authors = models.Author.objects.filter(name__icontains=search)
		books = models.Book.objects.filter(author__in=authors).order_by('name').distinct()
	elif category == 'description':
		books = models.Book.objects.filter(description__icontains=search).order_by('name').distinct()
	elif category == 'series':
		series = models.Serie.objects.filter(name__icontains=search)
		books = models.Book.objects.filter(series__in=series).order_by('name').distinct()

	return render(request, 'content/searchBooks.html', {'books':books})

@login_required
def search_request(request):

	search = request.GET.get('q')
	page = request.GET.get('page')

	if search:
		content = utils.search_books(search,page)

	else:
		content = {'search':search, 'books':[], 'pagination':[]}

	return render(request, 'content/searchRequests.html', content)

################
# Single Views #
################

def book(request,book_id):
	book = get_object_or_404(models.Book, pk=book_id)
	
	books_rented = request.user.profile.getRentedBooks() if request.user.is_authenticated else []
	rented = book in books_rented

	reviewForm = forms.ReviewForm(request.POST or None)
	
	if request.method == 'POST':

		if reviewForm.has_changed() and reviewForm.is_valid():
			instance = reviewForm.save()
			return redirect('book', book_id)

	return render(request, 'content/book.html', {'book':book, 'rented':rented, 'reviewForm':reviewForm})

def ibook(request,ibook_id):
	ibook = utils.get_book(ibook_id)
	book = models.Book.objects.filter(goodreads_id=ibook_id)
	request_obj = models.Request.objects.filter(goodreads_id=ibook_id)

	content = {
		'ibook_id':ibook_id,
		'ibook':ibook,
		'book':book,
		'request_obj':request_obj,
	}

	return render(request, 'content/ibook.html', content)

class NewView(DetailView):
	model = models.New

class AuthorView(DetailView):
	model = models.Author

class SerieView(DetailView):
	model = models.Serie

##################
# Manage Account #
##################
@login_required
def account(request):
	profile = request.user.profile
	return render(request, 'content/account.html', {'profile':profile})

@login_required
def account_rents(request):
	rents = request.user.profile.rents.all()
	return render(request, 'content/accountRents.html', {'rents':rents})

@login_required
def account_reviews(request):
	return render(request, 'content/accountReviews.html')

@login_required
def account_bookmarks(request):
	books = request.user.bookmarks.all()
	return render(request, 'content/accountBookmarks.html', {'book_set':books})

@login_required
def account_likes(request):
	books = request.user.likes.all()
	return render(request, 'content/accountLikes.html', {'book_set':books})

###############
# Admin Views #
###############

@login_required
@staff_member_required
def rents(request):
	rents = models.Rent.objects.all()
	return render(request, 'content/rents.html', {'rents':rents})

@login_required
@staff_member_required
def rent(request,rent_id):
	rent = get_object_or_404(models.Rent, pk=rent_id)
	return render(request, 'content/rent.html', {'rent':rent})

@login_required
@staff_member_required
def manage_requests(request):
	requests = models.Request.objects.all()
	return render(request, 'content/requests.html', {'requests':requests})

@login_required
@staff_member_required
def request(request,request_id):
	request_obj = models.Request.objects.get(pk=request_id)
	book = models.Book.objects.filter(goodreads_id=request_obj.goodreads_id)
	return render(request, 'content/request.html', {'request_obj':request_obj,'book':book})

#########
# Forms #
#########

@login_required
@staff_member_required
def edit_book(request,book_id):

	book = get_object_or_404(models.Book, pk=book_id)
	form = forms.BookForm(request.POST or None, instance=book)
	
	if request.method == 'POST':

		if form.has_changed() and form.is_valid():
			instance = form.save()
			return redirect('book', instance.pk)

	return render(request, 'forms/edit_book.html', {'form':form})

###########
# Actions #
###########

@login_required
@staff_member_required
def add_book(request,ibook_id):

	book,created = utils.add_book_to_library(request,ibook_id)

	if not created:
		messages.warning(request, 'This book was already added.')
	else:
		messages.success(request, 'Book added succesfully.')
	
	return redirect('book', book.pk)

@login_required
def request_book(request,ibook_id):

	request_obj,created = utils.request_book_to_library(request,ibook_id)

	if not created:
		messages.warning(request, 'This book was already requested.')
	else: 
		messages.success(request, 'You have requested this book.')

	return redirect('ibook', ibook_id)

@login_required
def rent_book(request,book_id):

	rents_available = request.user.profile.rents_available

	rents = request.user.profile.rents.filter(active=True)
	book = models.Book.objects.get(pk=book_id)

	if len(rents) < rents_available:

		if not book.quantity < 1:

			rent, created = models.Rent.objects.get_or_create(book=book, user=request.user.profile, active=True)

			if not created:
				messages.warning(request, 'You have an active rent for this item, that ends on {}.'.format(rent.return_date()))
			else:
				messages.success(request, 'You have succesfully rented this book. You can pick it up at the library.')
				messages.info(request, 'You have until {} to return this book!'.format(rent.return_date()))

				book.quantity -= 1
				book.save()
		else:
			messages.warning(request, 'The rent of this book isn\'t available now.')
	
	else:
		messages.warning(request, 'You cannot rent more that {} books.'.format(rents_available))
	
	return redirect('book', book_id)

@login_required
@staff_member_required
def return_rent(request,rent_id):
	
	rent = get_object_or_404(models.Rent, pk=rent_id)

	rent.active = False
	rent.returned = True
	rent.returned_to = request.user.profile
	rent.returned_date = datetime.datetime.now()
	
	rent.book.quantity += 1
	rent.book.save()

	rent.save()

	messages.success(request, 'Book returned succesfully!')

	return redirect('rent', rent_id)


@login_required
def like_toggle(request,book_id):
	
	book = get_object_or_404(models.Book, pk=book_id)

	if request.user not in book.likes.all():
		book.likes.add(request.user)
		messages.success(request, 'You liked this book.')
	else:
		book.likes.remove(request.user)
		messages.warning(request, 'You unliked this book.')

	return redirect('book', book_id)

@login_required
def bookmark_toggle(request,book_id):
	
	book = get_object_or_404(models.Book, pk=book_id)

	if request.user not in book.bookmarks.all():
		book.bookmarks.add(request.user)
		messages.success(request, 'You bookmarked this book.')
	else:
		book.bookmarks.remove(request.user)
		messages.warning(request, 'You unbookmarked this book.')

	return redirect('book', book_id)
