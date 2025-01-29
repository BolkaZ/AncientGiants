from drf_yasg import openapi
from rest_framework import status

from api.serializers import (BidGetFullInfoSerializer, BidPeriodUpdateInputSerializer, BidListSerializer,
                             BidGetFullInfoSerializer, BidUpdateInputSerializer, BidGetFullInfoSerializer,
                             BidModerationInputSerializer, BidFormInputSerializer)
from api.docs.errors import HTTTP_403, HTTTP_404


PERIOD_IN_BID_CREATE_SCHEMA = {
    "operation_id": "periodInBidCreate",
    "operation_description": """
        Запрос на добавление периода в заявку.
    """,
    "manual_parameters": [
        openapi.Parameter(
            "bid_id",
            openapi.IN_FORM,
            type=openapi.TYPE_INTEGER
        )
    ],
    "responses": {
        status.HTTP_201_CREATED: BidGetFullInfoSerializer(),
        status.HTTP_403_FORBIDDEN: HTTTP_403,
        status.HTTP_404_NOT_FOUND: HTTTP_404
    },
}

PERIOD_IN_BID_DELETE_SCHEMA = {
    "operation_id": "periodInBidDelete",
    "operation_description": """
        Запрос на удаление периода из заявки.
    """,
    "manual_parameters": [
        openapi.Parameter(
            "bid_id",
            openapi.IN_FORM,
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    "responses": {
        status.HTTP_204_NO_CONTENT: openapi.Response(
            description="NO CONTENT"
        ),
        status.HTTP_403_FORBIDDEN: HTTTP_403,
        status.HTTP_404_NOT_FOUND: HTTTP_404
    },
}

PERIOD_IN_BID_UPDATE_SCHEMA = {
    "operation_id": "periodInBidUpdate",
    "operation_description": """
        Запрос на обновление периода из заявки.
    """,
    "request_body": BidPeriodUpdateInputSerializer(),
    "responses": {
        status.HTTP_200_OK: BidGetFullInfoSerializer(),
        status.HTTP_403_FORBIDDEN: HTTTP_403,
        status.HTTP_404_NOT_FOUND: HTTTP_404
    },
}


BID_LIST_SCHEMA = {
    "operation_id": "bidList",
    "operation_description": """
        Запрос на получение списка заявок.
    """,
    "manual_parameters": [
        openapi.Parameter(
            "status",
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            "date_start",
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            pattern="2024-12-16T18:14:57.834351Z"
        ),
        openapi.Parameter(
            "date_end",
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            pattern="2024-12-17T18:14:57.834351Z"
        ),
    ],
    "responses": {
        status.HTTP_200_OK: BidListSerializer(many=True),
        status.HTTP_403_FORBIDDEN: HTTTP_403,
    },
}


BID_GET_SCHEMA = {
    "operation_id": "bidGet",
    "operation_description": """
        Запрос на получение детальной информации о заявке.
    """,
    "responses": {
        status.HTTP_200_OK: BidGetFullInfoSerializer(),
        status.HTTP_403_FORBIDDEN: HTTTP_403,
        status.HTTP_404_NOT_FOUND: HTTTP_404
    },
}

BID_UPDATE_SCHEMA = {
    "operation_id": "bidUpdate",
    "operation_description": """
        Запрос на обновление заявки.
    """,
    "request_body": BidUpdateInputSerializer(),
    "responses": {
        status.HTTP_200_OK: BidGetFullInfoSerializer(),
        status.HTTP_403_FORBIDDEN: HTTTP_403,
        status.HTTP_404_NOT_FOUND: HTTTP_404
    },
}

BID_DELETE_SCHEMA = {
    "operation_id": "bidDelete",
    "operation_description": """
        Запрос на удаление заявки.
    """,
     "responses": {
        status.HTTP_204_NO_CONTENT: openapi.Response(
            description="NO CONTENT"
        ),
        status.HTTP_403_FORBIDDEN: HTTTP_403,
        status.HTTP_404_NOT_FOUND: HTTTP_404
    },
}

BID_FORM_SCHEMA ={
    "operation_id": "bidForm",
    "operation_description": """
        Запрос на формирование заявки.
    """,
    "request_body":BidFormInputSerializer(),
     "responses": {
        status.HTTP_200_OK: BidGetFullInfoSerializer(),
        status.HTTP_403_FORBIDDEN: HTTTP_403,
        status.HTTP_404_NOT_FOUND: HTTTP_404
    },
}

BID_MODERATION_SCHEMA ={
    "operation_id": "bidModeration",
    "operation_description": """
        Запрос на модерацию заявки.
    """,
    "request_body": BidModerationInputSerializer(),
     "responses": {
        status.HTTP_200_OK: BidListSerializer(),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description="BAD REQUEST",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties=dict(
                    detail=openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="Status must be REJECTED or FINISHED."
                    ),
                )
            )
        ),
        status.HTTP_403_FORBIDDEN: HTTTP_403,
        status.HTTP_404_NOT_FOUND: HTTTP_404
    },
}
