from django.forms import ModelForm

from . import models

class BookForm(ModelForm):
	class Meta:
		model = models.Book
		exclude = ['added_by', 'likes']

class ReviewForm(ModelForm):
	class Meta:
		model = models.Review
		fields = ['title','review','liked']

class ApplyForm(ModelForm):
	pass