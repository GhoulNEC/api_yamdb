from rest_framework import serializers

from reviews.models import (
    Categorie,
    Genre,
    Title,
    Review,
    Comment
)


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitlesReadOnlySerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = Title
        fields = '__all__'


class TitleCreateSerializer(TitlesReadOnlySerializer):
    category = serializers.SlugRelatedField(queryset=Categorie.objects.all(),
                                            slug_field='slug')
    genre = serializers.SlugRelatedField(queryset=Genre.objects.all(),
                                         slug_field='slug', many=True)


class ReviewSerializers(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username'
                                          )

    class Meta:
        model = Review
        exclude = ('titles',)


class CommentSerializers(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username'
                                          )

    class Meta:
        model = Comment
        exclude = ('review',)
