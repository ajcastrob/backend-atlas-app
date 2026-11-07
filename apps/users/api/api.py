from rest_framework import viewsets
from rest_framework.views import Response, status
from django.shortcuts import get_object_or_404
from apps.users.models import User
from apps.users.api.serialazer import (
    UpdateUserSerializer,
    UserSerializer,
    UserListSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    model = User
    serializer_class = UserSerializer
    list_serializer_class = UserListSerializer
    queryset = None

    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)

    def get_queryset(self):
        if self.queryset == None:
            return self.model.objects.filter(
                is_active=True,
            ).values("id", "username", "email", "name")
        return self.queryset

    # GET
    def list(self, request):
        users = self.get_queryset()
        users_serializer = self.list_serializer_class(users, many=True)
        return Response(users_serializer.data, status=status.HTTP_200_OK)

    # Get by id
    def retrieve(self, request, pk=None):
        user = self.get_object(pk)
        users_serializer = self.serializer_class(user)
        return Response(users_serializer.data, status=status.HTTP_200_OK)

    # POST
    def create(self, request):
        users_serializer = self.serializer_class(data=request.data)
        if users_serializer.is_valid():
            users_serializer.save()
            return Response(
                {
                    "message": "Usuario creado correctamente",
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(
            {
                "message": "Usuario se creó incorrectamente",
                "errors": users_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # PUT
    def update(self, request, pk=None):
        user = self.get_object(pk)
        user_serializer = UpdateUserSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(
                {"message": "Usuario actualizado con éxito"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "message": "Hubo un error al actualizar",
                "errors": user_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # DELETE
    def destroy(self, request, pk=None):
        user_destroy = self.model.objects.filter(id=pk).update(is_active=False)
        if user_destroy == 1:
            return Response(
                {
                    "message": "Usuario eliminado correctamente",
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(
            {
                "message": "Usuario no se encontró",
            },
            status=status.HTTP_404_NOT_FOUND,
        )
