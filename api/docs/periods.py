from drf_yasg import openapi
from rest_framework import status

from api.serializers import (PeriodGetSerializers, PeriodUpdateInputSerializer, PeriodGetSerializers,
                            PeriodInputSerializer, PeriodGetSerializers)
from api.docs.errors import HTTTP_403, HTTTP_404

PERIOD_GET_SCHEMA = {
    "operation_id": "periodGet",
    "operation_description": """
        Выводит детальную информацию о периооде.
    """,
    "responses": {
        status.HTTP_200_OK: PeriodGetSerializers(),
        status.HTTP_403_FORBIDDEN: HTTTP_403,
        status.HTTP_404_NOT_FOUND: HTTTP_404
    },
}

PERIOD_UPDATE_SCHEMA = {
    "operation_id": "periodUpdate",
    "operation_description": """
        Запрос на обновление периода.
    """,
    "request_body": PeriodUpdateInputSerializer(),
    "responses": {
        status.HTTP_200_OK: PeriodGetSerializers(),
        status.HTTP_403_FORBIDDEN: HTTTP_403,
        status.HTTP_404_NOT_FOUND: HTTTP_404
    },
}

PERIOD_DELETE_SCHEMA = {
    "operation_id": "periodDelete",
    "operation_description": """
        Запрос на удаление периода.
    """,
    "responses": {
        status.HTTP_204_NO_CONTENT: openapi.Response(
            description="NO CONTENT"
        ),
        status.HTTP_403_FORBIDDEN: HTTTP_403,
        status.HTTP_404_NOT_FOUND: HTTTP_404
    },
}

PERIOD_IMAGE_CREATE_SCHEMA = {
    "operation_id": "periodImageCreate",
    "operation_description": """
        Запрос на добавление изображения к периоду.
    """,
    "manual_parameters": [
        openapi.Parameter(
            "image",
            openapi.IN_FORM,
            type=openapi.TYPE_FILE,
            required=True
        )
    ],
    "responses": {
        status.HTTP_200_OK: openapi.Response(
            description="SUCCESS",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties=dict(
                    message=openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="Success"
                    ),
                )
            )
        ),
        status.HTTP_403_FORBIDDEN: HTTTP_403,
        status.HTTP_404_NOT_FOUND: HTTTP_404
    },
}

PERIOD_LIST_SCHEMA = {
    "operation_id": "periodList",
    "operation_description": """
        Запрос на получение списка периодов.
    """,
    "manual_parameters": [
        openapi.Parameter(
            "search",
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            required=False
        )
    ],
    "responses": {
        status.HTTP_200_OK: openapi.Response(
            description="SUCCESS",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties=dict(
                    periods=openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties=dict(
                                id=openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                ),
                                name=openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                ),
                                start=openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                ),
                                end=openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                ),
                                image=openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                ),
                            ),
                            required=["id", "name", "start", "end", "image"]
                        )

                    ),
                    bid_info=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties=dict(
                            bid_id=openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                            ),
                            count_of_periods=openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                            ),
                            detail=openapi.Schema(
                                type=openapi.TYPE_STRING,
                            ),
                        ),
                    ),
                ),
                required=["periods", "bid_info"]
            ),
        ),
        status.HTTP_403_FORBIDDEN: HTTTP_403,
    },
}


PERIOD_CREATE_SCHEMA = {
    "operation_id": "periodCreate",
    "operation_description": """
        Запрос на создание периода.
    """,
    "request_body": PeriodInputSerializer(),
    "responses": {
        status.HTTP_201_CREATED: PeriodGetSerializers(),
        status.HTTP_403_FORBIDDEN: HTTTP_403,
    },
}
