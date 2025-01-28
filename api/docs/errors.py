from drf_yasg import openapi

NOT_FOUND = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties=dict(
        detail=openapi.Schema(
            type=openapi.TYPE_STRING,
            example="No Objects matches the given query."
        ),
    )
)

FORBIDDEN = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties=dict(
        detail=openapi.Schema(
            type=openapi.TYPE_STRING,
            example="Ты не авторизовался!/Ты не модератор!/Ты не создатель!"
        ),
    )
)

HTTTP_404 = openapi.Response(
            description="NOT FOUND",
            schema=NOT_FOUND
)

HTTTP_403 = openapi.Response(
            description="FORBIDDEN",
            schema=FORBIDDEN
)