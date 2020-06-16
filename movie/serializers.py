from rest_framework import serializers

from .models import Movies, Review, Rating, Actor


class MoviesSerializer(serializers.ModelSerializer):
    """movie list"""
    rating_user = serializers.BooleanField()
    middle_star = serializers.IntegerField()

    class Meta:
        model = Movies
        fields = ('id', 'title', 'tagline', 'category', 'rating_user', 'middle_star')


class FilterReviewSerializer(serializers.ListSerializer):
    """filter reviews omly parents"""
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """recursive children"""
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ActorSerializer(serializers.ModelSerializer):
    """view actor and directors detail """
    class Meta:
        model = Actor
        fields = ('id', 'name', 'image')


class ActorDetailSerializer(serializers.ModelSerializer):
    """view actor and directors list """
    class Meta:
        model = Actor
        fields = ('id', 'name', 'age', 'image')


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Add review"""

    class Meta:
        model = Review
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Output reviews"""
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewSerializer
        model = Review
        fields = ('name', 'message', 'parent', 'children')


class MoviesDetailSerializer(serializers.ModelSerializer):
    """movie detail"""
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    directors = ActorSerializer(read_only=True, many=True)
    actors = ActorSerializer(read_only=True, many=True)
    genre = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movies
        exclude = ('draft',)


class CreateRatingSerializer(serializers.ModelSerializer):
    """add rating"""
    class Meta:
        model = Rating
        fields = ('star', 'movie')

    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={'star': validated_data.get('star')}
        )
        return rating
