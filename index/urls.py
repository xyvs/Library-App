from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name="index"),
	path('popular/', views.index, name="popular"),
	path('browse/', views.browse, name="browse"),
	path('search/', views.search, name="search"),
	path('request/', views.searchRequest, name="searchRequest"),
	
	path('category/<slug:category>/', views.category, name="category"),
	path('last/', views.last, name="last"),

	path('book/<int:book_id>/', views.book, name="book"),
	path('book/<int:book_id>/edit/', views.editBook, name="editBook"),
	path('book/<int:book_id>/rent/', views.rentBook, name="rentBook"),
	path('book/<int:book_id>/like/', views.likeBook, name="likeBook"),
	path('book/<int:book_id>/dislike/', views.dislikeBook, name="dislikeBook"),


	path('ibook/<int:ibook_id>/', views.ibook, name="ibook"),
	path('ibook/<int:ibook_id>/add/', views.addBook, name="addBook"),
	path('ibook/<int:ibook_id>/request/', views.requestBook, name="requestBook"),
	
	path('new/<int:new_id>/', views.new, name="new"),

	path('authors/', views.authors, name="authors"),
	path('author/<int:author_id>/', views.author, name="author"),

	path('series/', views.series, name="series"),
	path('serie/<int:serie_id>/', views.serie, name="serie"),

	path('account/', views.account, name="account"),

	# Admin
	path('rents/', views.rents, name="rents"),
	path('rent/<int:rent_id>/', views.rent, name="rent"),
	path('rent/<int:rent_id>/return/', views.returnRent, name="returnRent"),

	path('requests/', views.manageRequests, name="manageRequests"),
	path('request/<int:request_id>/', views.request, name="request"),

	
]
