from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from django.http import JsonResponse

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.views.generic import TemplateView
from django.views.decorators.http import require_POST

from . import models, forms, utils

import requests
import xmltodict
import datetime
import random

########################
# Generate Random User #
########################

def CreateRandomUser(request):
	username = random.randint(100000, 999999)
	password = random.randint(1000, 9999)

	user = User.objects.create_user(username, '', password)
	messages.success(request, 'Library ID: {}, PIN: {}'.format(username,password))

	return redirect('index')

###########
# Content #
###########

def Test(request):
	username = request.GET.get('username', None)
	data = {
		'is_taken': User.objects.filter(username__iexact=username).exists()
	}
	return JsonResponse(data)

def Index(request):
	news = models.New.objects.all()[:5]
	return render(request, 'content/index.html', {'news':news})

class About(TemplateView):
	template_name = 'content/about.html'

class Apply(TemplateView):
	template_name = 'content/apply.html'

################
# Browse Views #
################

def Browse(request):

	nBooks = 8

	lastest_books = models.Book.objects.all()[:nBooks]
	fiction_books = models.Book.objects.filter(category="science-fiction")[:nBooks]
	fantasy_books = models.Book.objects.filter(category="fantasy")[:nBooks]
	mystery_books = models.Book.objects.filter(category="mystery")[:nBooks]
	crime_books = models.Book.objects.filter(category="crime")[:nBooks]

	content = {
		'lastest_books':lastest_books,
		'fiction_books':fiction_books,
		'fantasy_books':fantasy_books,
		'mystery_books':mystery_books,	
		'crime_books':crime_books,
	}

	return render(request, 'content/books.html', content)


def AllBooks(request):
	content = {
		'book_set':models.Book.objects.all(),
		'title':"All Books",
	}
	return render(request, 'content/category.html', content)

def LastBooks(request):
	content = {
		'book_set':models.Book.objects.all()[:12],
		'title':"Last Books",
	}
	return render(request, 'content/category.html', content)

def Category(request,category):
	books = models.Book.objects.filter(category=category)
	content = {
		'book_set':books,
		'title':"Category {}".format(category.capitalize()),
	}
	return render(request, 'content/category.html', content)

def Authors(request):
	authors = models.Author.objects.all()[:10]
	return render(request, 'content/authors.html', {'authors':authors})

def Series(request):
	series = models.Serie.objects.all()[:10]
	return render(request, 'content/series.html', {'series':series})

def Search(request):

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
def SearchRequest(request):

	search = request.GET.get('q')

	if search:

		page = request.GET.get('page')
		page_int = int(page) if page else 1

		requestURL = 'https://www.goodreads.com/search/index.xml?key=elWTI430BrTmVA1tCbA&q={}&page={}'.format(search,page)
		response = requests.get(url=requestURL)

		reponse_xml = xmltodict.parse(response.text)

		total_items = int(reponse_xml['GoodreadsResponse']['search']['total-results'])

	else:
		total_items = 0

	if total_items > 1:

		total_pages = round(total_items/10)
		
		books_list = reponse_xml['GoodreadsResponse']['search']['results']['work']
		
		books = [{
			'id':x['best_book']['id']['#text'],
			'name':x['best_book']['title'],
			'author':x['best_book']['author']['name'],
			'image':x['best_book']['image_url'],
		} for x in books_list ]

		pagination = {
			'total_pages':total_pages,
			'current_page':page_int,
			'previous':page_int-1,
			'next':page_int+1,
			'has_next':True if page_int < total_pages else False,
			'has_previous':True if page_int > 1 else False,
		}

	else:
		books = []
		pagination = []

	content = {'title':search, 'books':books, 'pagination':pagination}

	return render(request, 'content/searchRequests.html', content)

################
# Single Views #
################

def Book(request,book_id):
	book = get_object_or_404(models.Book, pk=book_id)
	
	books_rented = request.user.profile.getRentedBooks() if request.user.is_authenticated else []
	rented = book in books_rented

	reviewForm = forms.ReviewForm(request.POST or None)
	
	if request.method == 'POST':

		if reviewForm.has_changed() and reviewForm.is_valid():
			instance = reviewForm.save()
			return redirect('book', book_id)

	return render(request, 'content/book.html', {'book':book, 'rented':rented, 'reviewForm':reviewForm})

def Ibook(request,ibook_id):
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

def New(request,new_id):
	new = get_object_or_404(models.New, pk=new_id)
	return render(request, 'content/new.html', {'new':new })

def Author(request,author_id):
	author = get_object_or_404(models.Author, pk=author_id)
	content = {
		'author':author,
		'title':"Books by {}".format(author)
	}
	return render(request, 'content/author.html', content)

def Serie(request,serie_id):
	serie = get_object_or_404(models.Serie, pk=serie_id)
	content = {
		'serie':serie,
		'title':"Books from {}".format(serie)
	}
	return render(request, 'content/serie.html', content)

##################
# Manage Account #
##################

@login_required
def Account(request):
	profile = request.user.profile
	return render(request, 'content/account.html', {'profile':profile})

@login_required
def AccountRents(request):
	rents = request.user.profile.rents.all()
	return render(request, 'content/accountRents.html', {'rents':rents})


@login_required
def AccountReviews(request):
	return render(request, 'content/accountReviews.html')

@login_required
def AccountBookmarks(request):
	books = request.user.bookmarks.all()
	return render(request, 'content/accountBookmarks.html', {'book_set':books})

@login_required
def AccountLikes(request):
	books = request.user.likes.all()
	return render(request, 'content/accountLikes.html', {'book_set':books})

###############
# Admin Views #
###############

@login_required
@staff_member_required
def Rents(request):
	rents = models.Rent.objects.all()
	return render(request, 'content/rents.html', {'rents':rents})

@login_required
@staff_member_required
def Rent(request,rent_id):
	rent = get_object_or_404(models.Rent, pk=rent_id)
	return render(request, 'content/rent.html', {'rent':rent})

@login_required
@staff_member_required
def ManageRequests(request):
	requests = models.Request.objects.all()
	return render(request, 'content/requests.html', {'requests':requests})

@login_required
@staff_member_required
def Request(request,request_id):
	request_obj = models.Request.objects.get(pk=request_id)
	book = models.Book.objects.filter(goodreads_id=request_obj.goodreads_id)
	return render(request, 'content/request.html', {'request_obj':request_obj,'book':book})

#########
# Forms #
#########

@login_required
@staff_member_required
def EditBook(request,book_id):

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
def AddBook(request,ibook_id):

	book,created = utils.add_book_to_library(request,ibook_id)

	if not created:
		messages.warning(request, 'This book was already added.')
	else:
		messages.success(request, 'Book added succesfully.')
	
	return redirect('book', book.pk)

@login_required
def RequestBook(request,ibook_id):

	request_obj,created = utils.request_book_to_library(request,ibook_id)

	if not created:
		messages.warning(request, 'This book was already requested.')
	else: 
		messages.success(request, 'You have requested this book.')

	return redirect('ibook', ibook_id)

@login_required
def RentBook(request,book_id):

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
def ReturnRent(request,rent_id):
	
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
def LikeBook(request,book_id):
	
	book = get_object_or_404(models.Book, pk=book_id)

	if request.user not in book.likes.all():
		book.likes.add(request.user)
		messages.success(request, 'You liked this book.')
	else:
		messages.warning(request, 'You already liked this book.')

	return redirect('book', book_id)

@login_required
def DislikeBook(request,book_id):
	
	book = get_object_or_404(models.Book, pk=book_id)
	
	if request.user in book.likes.all():
		book.likes.remove(request.user)
		messages.warning(request, 'You unliked this book.')
	else:
		messages.warning(request, 'You already unliked this book.')

	return redirect('book', book_id)

@login_required
def BookmarkBook(request,book_id):
	
	book = get_object_or_404(models.Book, pk=book_id)

	if request.user not in book.bookmarks.all():
		book.bookmarks.add(request.user)
		messages.success(request, 'You bookmarked this book.')
	else:
		messages.warning(request, 'You already bookmarked this book.')

	return redirect('book', book_id)

@login_required
def UnbookmarkBook(request,book_id):
	
	book = get_object_or_404(models.Book, pk=book_id)
	
	if request.user in book.bookmarks.all():
		book.bookmarks.remove(request.user)
		messages.warning(request, 'You unbookmarked this book.')
	else:
		messages.warning(request, 'You already unbookmarked this book.')

	return redirect('book', book_id)
