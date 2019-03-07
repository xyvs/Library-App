from rest_framework import serializers

from index import models

class BookSerializer(serializers.HyperlinkedModelSerializer):
	author = serializers.StringRelatedField(many=True)
	likes = serializers.StringRelatedField(many=True)
	bookmarks = serializers.StringRelatedField(many=True)
	
	class Meta:
		model = models.Book
		exclude = ('added_by',)