from django.urls import path

from . import views

urlpatterns = [
	# Site
	path('', views.Index, name="index"),
	path('about', views.About.as_view(), name="about"), # Add
	path('apply', views.Apply.as_view(), name="apply"), # Add
	path('test', views.Test, name='test'),	

	# Site Content
	path('blog/', views.Index, name="blog"), # Add
	path('blog/<int:new_id>/', views.New, name="new"),

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
	path('book/<int:book_id>/', views.Book, name="book"),
	path('book/<int:book_id>/edit/', views.EditBook, name="editBook"),
	path('book/<int:book_id>/rent/', views.RentBook, name="rentBook"),
	path('book/<int:book_id>/like/', views.LikeBook, name="likeBook"),
	path('book/<int:book_id>/dislike/', views.DislikeBook, name="dislikeBook"),
	path('book/<int:book_id>/bookmark/', views.BookmarkBook, name="bookmarkBook"),
	path('book/<int:book_id>/unbookmark/', views.UnbookmarkBook, name="unbookmarkBook"),

	path('ibook/<int:ibook_id>/', views.Ibook, name="ibook"),
	path('ibook/<int:ibook_id>/add/', views.AddBook, name="addBook"),
	path('ibook/<int:ibook_id>/request/', views.RequestBook, name="requestBook"),

	path('authors/', views.Authors, name="authors"),
	path('author/<int:author_id>/', views.Author, name="author"),

	path('series/', views.Series, name="series"),
	path('serie/<int:serie_id>/', views.Serie, name="serie"),

	# Account
	path('account/', views.Account, name="account"),
	path('account/rents/', views.AccountRents, name="accountRents"),
	path('account/reviews/', views.AccountReviews, name="accountReviews"),
	path('account/bookmarks/', views.AccountBookmarks, name="accountBookmarks"),
	path('account/likes/', views.AccountLikes, name="accountLikes"),
	path('account/settings/', views.Account, name="mySettings"),

	# Admin
	path('rents/', views.Rents, name="rents"),
	path('rent/<int:rent_id>/', views.Rent, name="rent"),
	path('rent/<int:rent_id>/return/', views.ReturnRent, name="returnRent"),

	path('requests/', views.ManageRequests, name="manageRequests"),
	path('request/<int:request_id>/', views.Request, name="request"),

	path('create/user/', views.CreateRandomUser, name="createRandomUser"),
]
