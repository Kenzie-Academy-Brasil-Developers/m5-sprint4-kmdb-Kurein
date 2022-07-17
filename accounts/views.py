from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView, Request, Response, status

from accounts.models import User
from accounts.serializers import LoginSerializer, UserSerializer


class UserView(APIView):
    def post(self, request: Request):
        serialized = UserSerializer(data=request.data)
        try:
            serialized.is_valid(raise_exception=True)
            serialized.save()

            return Response(serialized.data, status.HTTP_201_CREATED)

        except ValueError as err:
            return Response(*err.args)


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