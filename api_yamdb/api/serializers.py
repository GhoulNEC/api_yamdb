from rest_framework import serializers

from reviews.models import Categories, Genres, Titles, Review, Comments


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('name', 'slug')


class TitlesReadOnlySerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = Titles
        fields = '__all__'


class TitleCreateSerializer(TitlesReadOnlySerializer):
    category = serializers.SlugRelatedField(queryset=Categories.objects.all(),
                                            slug_field='slug')
    genre = serializers.SlugRelatedField(queryset=Genres.objects.all(),
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
        model = Comments
        exclude = ('review',)
