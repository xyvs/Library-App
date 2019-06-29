import requests
import xmltodict

from . import models
from django.conf import settings


def search_books(search,page):
	page_int = int(page) if page else 1

	request_url = f'https://www.goodreads.com/search/index.xml?key={settings.GOODREADS_API_KEY}&q={search}&page={page}'
	response = requests.get(url=request_url)
	reponse_xml = xmltodict.parse(response.text)

	total_items = int(reponse_xml['GoodreadsResponse']['search']['total-results'])

	if total_items > 1:

		total_pages = round(total_items/10)
		
		books_list = reponse_xml['GoodreadsResponse']['search']['results']['work']
		
		books = [{
			'id':book['best_book']['id']['#text'],
			'name':book['best_book']['title'],
			'author':book['best_book']['author']['name'],
			'image':book['best_book']['image_url'],
		} for book in books_list ]

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

	return {'search':search, 'books':books, 'pagination':pagination}


def get_book(ibook_id):
	request_url = f'https://www.goodreads.com/book/show/{ibook_id}.xml?key={settings.GOODREADS_API_KEY}'
	response = requests.get(url=request_url)

	reponse_xml = xmltodict.parse(response.text)
	ibook = reponse_xml['GoodreadsResponse']['book']

	return ibook


def add_book_to_library(request,ibook_id):

	ibook = get_book(ibook_id)

	book,created = models.Book.objects.get_or_create(
		name=ibook['title'],
		isbn=ibook['isbn'] or 0,
		goodreads_id=ibook_id,
		image=ibook['image_url'],
		description=ibook['description'],
		publisher=ibook['publisher'] or "None",
		language_code=ibook['language_code'],
		number_of_pages=ibook['num_pages'],
		format_of_release=ibook['format'] or "None",
		added_by=request.user.profile,
	)

	authors = ibook['authors']['author']

	try:
		author,x = models.Author.objects.get_or_create(name=authors['name'])
		book.author.add(author)

	except:
		for author in authors:
			if not author['role']:
				author,x = models.Author.objects.get_or_create(name=author['name'])
				book.author.add(author)


	if ibook['series_works'] != None:
		
		series = ibook['series_works']['series_work']

		try:
			series,x = models.Serie.objects.get_or_create(name=series['series']['title'])
			series.books.add(book)

		except:
			for serie in series:
				series,x = models.Serie.objects.get_or_create(name=serie['series']['title'])
				series.books.add(book)

	return [book,created]

def request_book_to_library(request,ibook_id):

	ibook = get_book(ibook_id)

	request,created = models.Request.objects.get_or_create(
		name=ibook['title'],
		isbn=ibook['isbn'] or 0,
		goodreads_id=ibook_id,
		image=ibook['image_url'],
		description=ibook['description'],
		publisher=ibook['publisher'] or "None",
		language_code=ibook['language_code'],
		number_of_pages=ibook['num_pages'],
		format_of_release=ibook['format'] or "None",
		requested_by=request.user.profile,
	)

	return [request,created]
