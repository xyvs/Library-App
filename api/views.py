from django.contrib.auth.models import Group, User
from django.shortcuts import render
from rest_framework import viewsets

from api import serializers
from index import models


class BookViewSet(viewsets.ModelViewSet):
	queryset = models.Book.objects.all()
	serializer_class = serializers.BookSerializer
