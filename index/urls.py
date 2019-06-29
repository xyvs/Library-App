from django.urls import path

from . import views

urlpatterns = [
	# Site
	path('', views.index, name="index"),
	path('about', views.About.as_view(), name="about"), # Add
	path('apply', views.Apply.as_view(), name="apply"), # Add

	# Site Content
	path('blog/', views.index, name="blog"), # Add
	path('blog/<int:pk>/', views.NewView.as_view(), name='new_view'),

	# Browse Views
	path('browse/', views.browse, name="browse"),
	path('search/', views.search, name="search"),
	path('request/', views.search_request, name="searchRequest"),
	
	# Categories
	path('browse/popular/', views.index, name="popularBook"), # Add
	path('browse/all/', views.all_books, name="allBooks"),
	path('browse/last/', views.last_books, name="lastBooks"),
	path('category/<slug:category>/', views.category, name="category"),

	# Content
	path('books/<int:book_id>/', views.book, name="book"),
	path('books/<int:book_id>/edit/', views.edit_book, name="editBook"),
	path('books/<int:book_id>/rent/', views.rent_book, name="rentBook"),
	path('books/<int:book_id>/like/', views.like_toggle, name="LikeToggle"),
	path('books/<int:book_id>/bookmark/', views.bookmark_toggle, name="BookmarkToggle"),

	path('ibooks/<int:ibook_id>/', views.ibook, name="ibook"),
	path('ibooks/<int:ibook_id>/add/', views.add_book, name="addBook"),
	path('ibooks/<int:ibook_id>/request/', views.request_book, name="requestBook"),

	path('authors/', views.authors, name="authors"),
	path('authors/<int:pk>/', views.AuthorView.as_view(), name='author_view'),

	path('series/', views.series, name="series"),
	path('series/<int:pk>/', views.SerieView.as_view(), name='serie_view'),

	# Account
	path('account/', views.account, name="account"),
	path('account/rents/', views.account_rents, name="accountRents"),
	path('account/reviews/', views.account_reviews, name="accountReviews"),
	path('account/bookmarks/', views.account_bookmarks, name="accountBookmarks"),
	path('account/likes/', views.account_likes, name="accountLikes"),
	path('account/settings/', views.account, name="mySettings"),

	# Admin
	path('rents/', views.rents, name="rents"),
	path('rents/<int:rent_id>/', views.rent, name="rent"),
	path('rents/<int:rent_id>/return/', views.return_rent, name="returnRent"),

	path('requests/', views.manage_requests, name="manageRequests"),
	path('requests/<int:request_id>/', views.request, name="request"),

	path('create/user/', views.create_random_user, name="createRandomUser"),
]
