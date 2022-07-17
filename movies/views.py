from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status
from rest_framework.authentication import TokenAuthentication

from movies.models import Movie
from movies.serializers import MovieSerializer
from movies.permissions import MoviesPermission

class MovieView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [MoviesPermission]

    def get(self, _:Request):
        movies = Movie.objects.all()

        serialized = MovieSerializer(instance=movies, many=True)

        return Response({"Movies": serialized.data}, status.HTTP_200_OK)

    def post(self, req: Request):
        serialized = MovieSerializer(data=req.data)
        serialized.is_valid(raise_exception=True)
        serialized.save()

        return Response(serialized.data, status.HTTP_201_CREATED)

class MovieIdView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [MoviesPermission]

    def get(self, _:Request, movie_id):
        movie = get_object_or_404(Movie, pk=movie_id)
        serialized = MovieSerializer(instance=movie)

        return Response({"movie": serialized.data}, status.HTTP_200_OK)

    def patch(self, req:Request, movie_id):
        try:
            movie = get_object_or_404(Movie, pk=movie_id)
            serialized = MovieSerializer(movie, req.data, partial=True)
            serialized.is_valid()

            serialized.save()

            return Response({"movie": serialized.data}, status.HTTP_200_OK)
        except:
            return Response({"error": "Cannot update Genres property"}, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, _:Request, movie_id):
        movie = get_object_or_404(Movie, pk=movie_id)
        movie.delete()
        
        return Response("", status.HTTP_204_NO_CONTENT)
