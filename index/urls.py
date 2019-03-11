from django.urls import path

from . import views

urlpatterns = [
	# Site
	path('', views.Index, name="index"),
	path('about', views.About.as_view(), name="about"), # Add
	path('apply', views.Apply.as_view(), name="apply"), # Add

	# Site Content
	path('blog/', views.Index, name="blog"), # Add
	path('blog/<int:pk>/', views.NewView.as_view(), name='new_view'),

	# Browse Views
	path('browse/', views.Browse, name="browse"),
	path('search/', views.Search, name="search"),
	path('request/', views.SearchRequest, name="searchRequest"),
	
	# Categories
	path('browse/popular/', views.Index, name="popularBook"), # Add
	path('browse/all/', views.AllBooks, name="allBooks"),
	path('browse/last/', views.LastBooks, name="lastBooks"),
	path('category/<slug:category>/', views.Category, name="category"),

	# Content
	path('books/<int:book_id>/', views.Book, name="book"),
	path('books/<int:book_id>/edit/', views.EditBook, name="editBook"),
	path('books/<int:book_id>/rent/', views.RentBook, name="rentBook"),
	path('books/<int:book_id>/like/', views.LikeToggle, name="LikeToggle"),
	path('books/<int:book_id>/bookmark/', views.BookmarkToggle, name="BookmarkToggle"),

	path('ibooks/<int:ibook_id>/', views.Ibook, name="ibook"),
	path('ibooks/<int:ibook_id>/add/', views.AddBook, name="addBook"),
	path('ibooks/<int:ibook_id>/request/', views.RequestBook, name="requestBook"),

	path('authors/', views.Authors, name="authors"),
	path('authors/<int:pk>/', views.AuthorView.as_view(), name='author_view'),

	path('series/', views.Series, name="series"),
	path('series/<int:pk>/', views.SerieView.as_view(), name='serie_view'),

	# Account
	path('account/', views.Account, name="account"),
	path('account/rents/', views.AccountRents, name="accountRents"),
	path('account/reviews/', views.AccountReviews, name="accountReviews"),
	path('account/bookmarks/', views.AccountBookmarks, name="accountBookmarks"),
	path('account/likes/', views.AccountLikes, name="accountLikes"),
	path('account/settings/', views.Account, name="mySettings"),

	# Admin
	path('rents/', views.Rents, name="rents"),
	path('rents/<int:rent_id>/', views.Rent, name="rent"),
	path('rents/<int:rent_id>/return/', views.ReturnRent, name="returnRent"),

	path('requests/', views.ManageRequests, name="manageRequests"),
	path('requests/<int:request_id>/', views.Request, name="request"),

	path('create/user/', views.CreateRandomUser, name="createRandomUser"),
]
