from drf_yasg import openapi
from rest_framework import status

from api.serializers import (UserCreateInputSerializer, UserListSerializer, UserUpdateInputSerializer,
                             UserListSerializer, UserLoginInputSerializer, UserListSerializer)
from api.docs.errors import HTTTP_403, HTTTP_404


USER_CREATE_SCHEMA = {
    "operation_id": "userRegister",
    "operation_description": """
        Запрос на регистрацию пользователя.
    """,
    "request_body": UserCreateInputSerializer(),
     "responses": {
        status.HTTP_201_CREATED: UserListSerializer(),
    },
}

USER_UPDATE_SCHEMA = {
    "operation_id": "userUpdate",
    "operation_description": """
        Запрос на обновление пользователя.
    """,
    "request_body": UserUpdateInputSerializer(),
     "responses": {
        status.HTTP_200_OK: UserListSerializer(),
        status.HTTP_403_FORBIDDEN: HTTTP_403,
        status.HTTP_404_NOT_FOUND: HTTTP_404
    },
}

USER_LOGIN_SCHEMA = {
    "operation_id": "userLogin",
    "operation_description": """
        Запрос на авторизацию пользователя.
    """,
    "request_body": UserLoginInputSerializer(),
     "responses": {
        status.HTTP_200_OK: UserListSerializer(),
        status.HTTP_403_FORBIDDEN: openapi.Response(
            description="FORBIDDEN",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties=dict(
                    detail=openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="Invalid credentianls."
                    ),
                )
            )
        ),
    },
}

USER_LOGOUT_SCHEMA = {
    "operation_id": "userLogout",
    "operation_description": """
        Запрос на деавторизацию пользователя.
    """,
     "responses": {
        status.HTTP_200_OK:  openapi.Response(
            description="FORBIDDEN",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties=dict(
                    detail=openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="success"
                    ),
                )
            )
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description="FORBIDDEN",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties=dict(
                    detail=openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="You must authorize before."
                    ),
                )
            )
        ),
    },
}