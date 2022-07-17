from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView, Request, Response, status

from reviews.models import Review
from reviews.serializers import ReviewSerializer
from reviews.permissions import ReviewPermission

from movies.serializers import MovieSerializer
from movies.models import Movie

class ReviewView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [ReviewPermission]

    def get(self, _:Request, movie_id):
        movie = get_object_or_404(Movie, pk=movie_id)
        serialized = MovieSerializer(instance=movie)

        return Response({"reviews": serialized.data['reviews']}, status.HTTP_200_OK)

    def post(self, req:Request, movie_id):
        req.data["movie"] = movie_id
        req.data["critic"] = req.user.id

        serialized = ReviewSerializer(data=req.data)
        serialized.is_valid(raise_exception=True)
        serialized.save()

        return Response(serialized.data, status.HTTP_201_CREATED)

class ReviewIdView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [ReviewPermission]
    
    def delete(self, _:Request, review_id):
        serialized = get_object_or_404(Review, pk=review_id)
        serialized.delete()

        return Response("", status.HTTP_204_NO_CONTENT)

class ReviewGetView(APIView):
    def get(self, _:Request):
        reviews = Review.objects.all()
        serialized = ReviewSerializer(instance=reviews, many=True)

        return Response({"reviews": serialized.data}, status.HTTP_200_OK)