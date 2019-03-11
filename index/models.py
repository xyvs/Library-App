import datetime

from django.db import models
from django.urls import reverse

from django.contrib import messages
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

###################
# Multiple Choice #
###################

BOOK_CATEGORIES = (
	('biography ', 'Biography'),
	('classic', 'Classic'),
	('comics', 'Comics/Graphic novel'),
	('crime', 'Crime/detective'),
	('essay ', 'Essay'),
	('fable', 'Fable'),
	('fairy-tailr', 'Fairy tale'),
	('fan-fiction', 'Fan fiction'),
	('fantasy', 'Fantasy'),
	('folklore', 'Folklore'),
	('historical-fiction', 'Historical fiction'),
	('horror', 'Horror'),
	('humor', 'Humor'),
	('journalism', 'Journalism'),
	('lab-report ', 'Lab report'),
	('legend', 'Legend'),
	('magical-realism', 'Magical realism'),
	('manual', 'Owner\'s manual'),
	('memoir', 'Memoir'),
	('meta-fiction', 'Meta fiction'),
	('mystery', 'Mystery'),
	('mythology', 'Mythology'),
	('mythopoeia', 'Mythopoeia'),
	('narrative-nonfiction', 'Narrative nonfiction/personal narrative'),
	('picture-book', 'Picture book'),
	('realistic-fiction', 'Realistic fiction'),
	('reference', 'Reference book'),
	('science-fiction', 'Science fiction'),
	('self-help', 'Self-help book'),
	('short-story', 'Short story'),
	('speech', 'Speech'),
	('suspense', 'Suspense/thriller'),
	('swashbuckler', 'Swashbuckler'),
	('tall-tale', 'Tall tale'),
	('textbook ', 'Textbook'),
	('western', 'Western'),
)

#################
# Profile Class #
#################

class UserDetails(models.Model):
	id_number = models.PositiveIntegerField()
	address = models.CharField(max_length=100)
	number = models.PositiveIntegerField()
	locations = models.CharField(max_length=250)
	cp = models.PositiveIntegerField()

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
	bio = models.TextField(max_length=500, blank=True)
	birth_date = models.DateField(null=True, blank=True)
	
	rents_available = models.PositiveIntegerField(default=2)
	active = models.BooleanField(default=True)

	user_details = models.ForeignKey(UserDetails, on_delete=models.CASCADE, blank=True, null=True)

	def getRentedBooks(self):
		return [x.book for x in self.rents.filter(active=True)]

	def __str__(self):
		return "{}".format(self.user)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()

################
# Staff Models #
################

class New(models.Model):
	title = models.CharField(max_length=100)
	image = models.URLField()
	body = models.TextField()

	author = models.ForeignKey(Profile, on_delete=models.CASCADE)
	date_added = models.DateTimeField(auto_now_add=True)
	date_edited = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title

	def absolute_url(self):
		return reverse('new_view', args=[self.pk])

##################
# Default Models #
##################

class Author(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	image = models.URLField()

	def __str__(self):
		return self.name

	def absolute_url(self):
		return reverse('author_view', args=[self.pk])

class BookBase(models.Model):
	name = models.CharField(max_length=100)
	isbn = models.CharField(max_length=100)
	goodreads_id = models.PositiveIntegerField()
	image = models.URLField()
	description = models.TextField(null=True, blank=True)

	author = models.ManyToManyField(Author, blank=True)
	
	release_date = models.DateField(null=True,blank=True)
	publisher = models.CharField(max_length=100)
	
	language_code = models.CharField(max_length=3)
	number_of_pages = models.PositiveIntegerField()
	format_of_release = models.CharField(max_length=100)
	
	class Meta:
		abstract = True

	def __str__(self):
		return self.name

class Request(BookBase):
	requested_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="requests")
	date_added = models.DateTimeField(auto_now_add=True)

	def absolute_url(self):
		return reverse('request', args=[self.pk])

	def add_book(self):
		return reverse('addBook', args=[self.goodreads_id])

	class Meta:
		ordering = ['-date_added']

class Book(BookBase):
	category = models.CharField(max_length=100, choices=BOOK_CATEGORIES, blank=True)
	quantity = models.PositiveIntegerField(default=1)

	added_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="books_added")
	date_added = models.DateTimeField(auto_now_add=True)
	date_edited = models.DateTimeField(auto_now=True)
	
	likes = models.ManyToManyField(User, related_name="likes", blank=True)
	bookmarks = models.ManyToManyField(User, related_name="bookmarks", blank=True)

	class Meta:
		ordering = ['-date_added']

	def absolute_url(self):
		return reverse('book', args=[self.pk])

class Set(models.Model):
	name = models.CharField(max_length=100)
	image = models.URLField()
	description = models.TextField()

	
	date_added = models.DateTimeField(auto_now_add=True)
	date_edited = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True

	def __str__(self):
		return self.name

class Serie(Set):
	books = models.ManyToManyField(Book, related_name="series")

	def absolute_url(self):
		return reverse('serie_view', args=[self.pk])

class Collection(Set):
	books = models.ManyToManyField(Book, related_name="collections")
	user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="collections")

class Rent(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="rents")
	active = models.BooleanField(default=True)

	date_rented = models.DateField(auto_now_add=True) # Maybe DateTimeField?

	returned = models.BooleanField(default=False)
	returned_to = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
	returned_date = models.DateField(null=True, blank=True)

	def return_date(self):
		return self.date_rented + datetime.timedelta(days=7)

	def return_date_str(self):

		return_date = self.return_date()

		if self.active:
			return "Return: {}".format(return_date)
		else:
			return "Returned"

	def badge_type(self):

		return_date = self.return_date()
		today = datetime.date.today()

		if not self.active:
			return "success"
		elif return_date == today:
			return "warning"
		elif return_date < today:
			return "danger"
		else:
			return "dark"

	def absolute_url(self):
		return reverse('rent', args=[self.pk])

	class Meta:
		ordering = ["-date_rented","-pk"]

	def __str__(self):
		return "{} rented {} on {}".format(self.user,self.book,self.date_rented)

class Review(models.Model):
	title = models.CharField(max_length=100, blank=True)
	review = models.TextField()
	liked = models.BooleanField()

	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	user = models.ForeignKey(Profile, on_delete=models.CASCADE)

	likes = models.ManyToManyField(User, related_name="reviews_liked", blank=True)

	def __str__(self):
		return "{} - {}".format(self.book,self.like_or_dislike)
