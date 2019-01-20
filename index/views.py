from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.views.decorators.http import require_POST

from . import models, forms, functions

import requests
import xmltodict
import datetime

###########
# Content #
###########

def index(request):
	news = models.New.objects.all()[:5]
	return render(request, 'content/index.html', {'news':news})

def about(request):
	return render(request, 'content/about.html', {})

################
# Browse Views #
################

def browse(request):

	nBooks = 8

	lastest_books = models.Book.objects.all()[:nBooks]
	adventure_books = models.Book.objects.filter(category="adventure")[:nBooks]
	drama_books = models.Book.objects.filter(category="drama")[:nBooks]
	crime_books = models.Book.objects.filter(category="crime")[:nBooks]
	fantasy_books = models.Book.objects.filter(category="fantasy")[:nBooks]

	content = {
		'lastest_books':lastest_books,
		'adventure_books':adventure_books,
		'drama_books':drama_books,
		'crime_books':crime_books,
		'fantasy_books':fantasy_books,
		'lastest_books':lastest_books,
	}

	return render(request, 'content/books.html', content)


def lastBooks(request):
	content = {
		'book_set':models.Book.objects.all(),
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
		books = models.Book.objects.filter(name__icontains=search).order_by('name')
	elif category == 'isbn':
		books = models.Book.objects.filter(isbn__icontains=search).order_by('name')
	elif category == 'author':
		authors = models.Author.objects.filter(name__icontains=search)
		books = models.Book.objects.filter(author__in=authors).order_by('name')
	elif category == 'description':
		books = models.Book.objects.filter(description__icontains=search).order_by('name')
	elif category == 'series':
		series = models.Serie.objects.filter(name__icontains=search)
		books = models.Book.objects.filter(series__in=series).order_by('name')

	return render(request, 'content/searchBooks.html', {'books':books})

@login_required
def searchRequest(request):

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

def book(request,book_id):
	book = get_object_or_404(models.Book, pk=book_id)
	books_rented = request.user.profile.getRentedBooks() if request.user.is_authenticated else []
	rented = book in books_rented
	return render(request, 'content/book.html', {'book':book, 'rented':rented})

def ibook(request,ibook_id):
	ibook = functions.getBook(ibook_id)
	book = models.Book.objects.filter(goodreads_id=ibook_id)
	request_obj = models.Request.objects.filter(goodreads_id=ibook_id)

	content = {
		'ibook_id':ibook_id,
		'ibook':ibook,
		'book':book,
		'request_obj':request_obj,
	}

	return render(request, 'content/ibook.html', content)

def new(request,new_id):
	new = get_object_or_404(models.New, pk=new_id)
	return render(request, 'content/new.html', {'new':new })

def author(request,author_id):
	author = get_object_or_404(models.Author, pk=author_id)
	content = {
		'author':author,
		'title':"Books by {}".format(author)
	}
	return render(request, 'content/author.html', content)

def serie(request,serie_id):
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
def account(request):
	profile = request.user.profile
	return render(request, 'content/account.html', {'profile':profile})

@login_required
def accountRents(request):
	rents = request.user.profile.rents.all()
	return render(request, 'content/accountRents.html', {'rents':rents})

@login_required
def accountBookmarks(request):
	books = request.user.bookmarks.all()
	return render(request, 'content/accountBookmarks.html', {'book_set':books})

@login_required
def accountLikes(request):
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
def manageRequests(request):
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
def editBook(request,book_id):

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
def addBook(request,ibook_id):

	book,created = functions.addBookToLibrary(request,ibook_id)

	if not created:
		messages.warning(request, 'This book was already added.')

	return redirect('book', book.pk)

@login_required
def requestBook(request,ibook_id):

	request_obj,created = functions.requestBookToLibrary(request,ibook_id)

	if not created:
		messages.warning(request, 'This book was already requested.')
	else: 
		messages.success(request, 'You have requested this book.')

	return redirect('ibook', ibook_id)

@login_required
def rentBook(request,book_id):

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
			messages.warning(request, 'The rent of this book isn\'t available for now.')
	
	else:
		messages.warning(request, 'You cannot rent more that {} books.'.format(rents_available))
	
	return redirect('book', book_id)

@login_required
@staff_member_required
def returnRent(request,rent_id):
	
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
def likeBook(request,book_id):
	
	book = get_object_or_404(models.Book, pk=book_id)

	if request.user not in book.likes.all():
		book.likes.add(request.user)
		messages.success(request, 'You liked this book.')
	else:
		messages.warning(request, 'You already liked this book.')

	return redirect('book', book_id)

@login_required
def dislikeBook(request,book_id):
	
	book = get_object_or_404(models.Book, pk=book_id)
	
	if request.user in book.likes.all():
		book.likes.remove(request.user)
		messages.warning(request, 'You unliked this book.')
	else:
		messages.warning(request, 'You already unliked this book.')

	return redirect('book', book_id)

@login_required
def bookmarkBook(request,book_id):
	
	book = get_object_or_404(models.Book, pk=book_id)

	if request.user not in book.bookmarks.all():
		book.bookmarks.add(request.user)
		messages.success(request, 'You bookmarked this book.')
	else:
		messages.warning(request, 'You already bookmarked this book.')

	return redirect('book', book_id)

@login_required
def unbookmarkBook(request,book_id):
	
	book = get_object_or_404(models.Book, pk=book_id)
	
	if request.user in book.bookmarks.all():
		book.bookmarks.remove(request.user)
		messages.warning(request, 'You unbookmarked this book.')
	else:
		messages.warning(request, 'You already unbookmarked this book.')

	return redirect('book', book_id)
