from rest_framework import serializers
from .models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'birth_date']


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'publication_date']

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        author = Author.objects.get(**author_data)
        book = Book.objects.create(author=author, **validated_data)
        return book

    def update(self, instance, validated_data):
        author_data = validated_data.pop('author')
        author = instance.author
        author.first_name = author_data.get('first_name', author.first_name)
        author.last_name = author_data.get('last_name', author.last_name)
        author.birth_date = author_data.get('birth_date', author.birth_date)
        author.save()
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.publication_date = validated_data.get('publication_date', instance.publication_date)
        instance.save()
        return instance
