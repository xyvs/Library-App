import requests
import xmltodict


from . import models

def getBook(ibook_id):
	requestURL = 'https://www.goodreads.com/book/show/{}.xml?key=elWTI430BrTmVA1tCbA'.format(ibook_id)
	response = requests.get(url=requestURL)

	reponse_xml = xmltodict.parse(response.text)
	ibook = reponse_xml['GoodreadsResponse']['book']

	return ibook

def addBookToLibrary(request,ibook_id):

	ibook = getBook(ibook_id)

	book,created = models.Book.objects.get_or_create(
		name=ibook['title'],
		isbn=ibook['isbn'] or 0,
		goodreads_id=ibook_id,
		image=ibook['image_url'],
		description=ibook['description'],
		publisher=ibook['publisher'],
		language_code=ibook['language_code'],
		number_of_pages=ibook['num_pages'],
		format_of_release=ibook['format'],
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

def requestBookToLibrary(request,ibook_id):

	ibook = getBook(ibook_id)

	request,created = models.Request.objects.get_or_create(
		name=ibook['title'],
		isbn=ibook['isbn'] or 0,
		goodreads_id=ibook_id,
		image=ibook['image_url'],
		description=ibook['description'],
		publisher=ibook['publisher'],
		language_code=ibook['language_code'],
		number_of_pages=ibook['num_pages'],
		format_of_release=ibook['format'],
		requested_by=request.user.profile,
	)

	return [request,created]
