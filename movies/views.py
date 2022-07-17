from rest_framework.views import APIView, Request, Response, status

from movies.models import Movie
from movies.serializers import MovieSerializer

class MovieView(APIView):
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
    def get(self, _:Request, movie_id):
        try:
            movie = Movie.objects.get(id=movie_id)
            serialized = MovieSerializer(instance=movie)

            return Response({"movie": serialized.data}, status.HTTP_200_OK)
        except:
            return Response({"error": "movie does not exist"}, status.HTTP_404_NOT_FOUND)