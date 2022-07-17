from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView, Request, Response, status
from rest_framework.authentication import TokenAuthentication

from accounts.models import User
from accounts.serializers import LoginSerializer, UserSerializer
from accounts.permissions import UserPermission


class UserView(APIView):
    def post(self, request: Request):
        serialized = UserSerializer(data=request.data)
        try:
            serialized.is_valid(raise_exception=True)
            serialized.save()

            return Response(serialized.data, status.HTTP_201_CREATED)

        except ValueError as err:
            return Response(*err.args)

class UserGetView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [UserPermission]

    def get(self, _:Request):
        users = User.objects.all()
        serialized = UserSerializer(instance=users, many=True)

        return Response({"users": serialized.data}, status.HTTP_200_OK)

class UserIdView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [UserPermission]

    def get(self, _:Request, user_id):
        try:
            user = User.objects.get(id=user_id)
            serialized = UserSerializer(instance=user)

            return Response({"user": serialized.data}, status.HTTP_200_OK)
        except:
            return Response({"error": "user does not exist"}, status.HTTP_404_NOT_FOUND)



class LoginView(APIView):
    def post(self, request: Request):
        serialized = LoginSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)

        user: User = authenticate(**serialized.validated_data)

        if not user:
            return Response(
                {"detail": "invalid email or password"}, status.HTTP_401_UNAUTHORIZED
            )

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key})