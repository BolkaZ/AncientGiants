from django.conf import settings
from minio import Minio
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.response import *

def process_file_upload(file_object: InMemoryUploadedFile, client, image_name):
    try:
        client.put_object(settings.AWS_STORAGE_BUCKET_NAME, image_name, file_object, file_object.size)
        return f"http://localhost:9000/{settings.AWS_STORAGE_BUCKET_NAME}/{image_name}"
    except Exception as e:
        return {"error": str(e)}

def add_pic(period, image):
    client = Minio(           
        endpoint=settings.AWS_S3_ENDPOINT_URL,
        access_key=settings.AWS_ACCESS_KEY_ID,
        secret_key=settings.AWS_SECRET_ACCESS_KEY,
        secure=settings.MINIO_USE_SSL
    )
    period_id = period.id
    image_name = f"{period_id}.png"

    if not image:
        return Response({"error": "Нет файла для изображения логотипа."})
    result = process_file_upload(image, client, image_name)

    if 'error' in result:
        return Response(result)

    period.image = result
    period.save()

    return Response({"message": "success"})

def delete_pic(period):
    client = Minio(           
        endpoint=settings.AWS_S3_ENDPOINT_URL,
        access_key=settings.AWS_ACCESS_KEY_ID,
        secret_key=settings.AWS_SECRET_ACCESS_KEY,
        secure=settings.MINIO_USE_SSL
    )

    image_name = f"{period.id}.png"

    try:
        # image = client.get_object(
        #     bucket_name=settings.AWS_STORAGE_BUCKET_NAME,
        #     object_name=image_name
        # )

        # if image.data:
        client.remove_object(
                bucket_name=settings.AWS_STORAGE_BUCKET_NAME,
                object_name=image_name
        )
            
        return {'message':'success'}
    except Exception as e:
        return {'error':str(e)}