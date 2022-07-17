from rest_framework import serializers

from movies.models import Movie
from genres.models import Genre

from genres.serializers import GenreSerializer

class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10)
    premiere = serializers.DateField()
    classification = serializers.IntegerField()
    synopsis = serializers.CharField()

    genres = GenreSerializer(many=True)

    def create(self, validated_data):
        genres = validated_data.pop("genres")

        movie = Movie.objects.create(**validated_data)

        for item in genres:
            item, _ = Genre.objects.get_or_create(**item)
            movie.genres.add(item)

        return movie