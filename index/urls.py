from django.urls import path

from . import views

urlpatterns = [
	# Site
	path('', views.index, name="index"),
	path('about', views.about, name="about"), # Add
	path('apply', views.apply, name="apply"), # Add
	path('test', views.test, name='test'),	

	# Site Content
	path('blog/', views.index, name="blog"), # Add
	path('blog/<int:new_id>/', views.new, name="new"),

	# Browse Views
	path('browse/', views.browse, name="browse"),
	path('search/', views.search, name="search"),
	path('request/', views.searchRequest, name="searchRequest"),
	
	# Categories
	path('browse/popular/', views.index, name="popularBook"), # Add
	path('browse/all/', views.allBooks, name="allBooks"),
	path('browse/last/', views.lastBooks, name="lastBooks"),
	path('category/<slug:category>/', views.category, name="category"),

	# Content
	path('book/<int:book_id>/', views.book, name="book"),
	path('book/<int:book_id>/edit/', views.editBook, name="editBook"),
	path('book/<int:book_id>/rent/', views.rentBook, name="rentBook"),
	path('book/<int:book_id>/like/', views.likeBook, name="likeBook"),
	path('book/<int:book_id>/dislike/', views.dislikeBook, name="dislikeBook"),
	path('book/<int:book_id>/bookmark/', views.bookmarkBook, name="bookmarkBook"),
	path('book/<int:book_id>/unbookmark/', views.unbookmarkBook, name="unbookmarkBook"),

	path('ibook/<int:ibook_id>/', views.ibook, name="ibook"),
	path('ibook/<int:ibook_id>/add/', views.addBook, name="addBook"),
	path('ibook/<int:ibook_id>/request/', views.requestBook, name="requestBook"),

	path('authors/', views.authors, name="authors"),
	path('author/<int:author_id>/', views.author, name="author"),

	path('series/', views.series, name="series"),
	path('serie/<int:serie_id>/', views.serie, name="serie"),

	# Account
	path('account/', views.account, name="account"),
	path('account/rents/', views.accountRents, name="accountRents"),
	path('account/reviews/', views.accountReviews, name="accountReviews"),
	path('account/bookmarks/', views.accountBookmarks, name="accountBookmarks"),
	path('account/likes/', views.accountLikes, name="accountLikes"),
	path('account/settings/', views.account, name="mySettings"),

	# Admin
	path('rents/', views.rents, name="rents"),
	path('rent/<int:rent_id>/', views.rent, name="rent"),
	path('rent/<int:rent_id>/return/', views.returnRent, name="returnRent"),

	path('requests/', views.manageRequests, name="manageRequests"),
	path('request/<int:request_id>/', views.request, name="request"),

	path('create/user/', views.createRandomUser, name="createRandomUser"),
]
