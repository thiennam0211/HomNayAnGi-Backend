# from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import status

# Create your views here.

from FilesManager import AWS
from django.core.files.storage import default_storage
from django.core.files import File

import os
from django.http import JsonResponse
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    bucket_name = 'honayangi-bucket'


class FileAWS(object):

    def __init__(self):
        pass

    def upload_file(self, file, folder):

        file_obj = file

        file_directory_within_bucket = folder

        file_path_within_bucket = os.path.join(
            file_directory_within_bucket,
            file_obj.name
        )

        media_storage = MediaStorage()

        if not media_storage.exists(file_path_within_bucket):
            # avoid overwriting existing file
            media_storage.save(file_path_within_bucket, file_obj)
            file_url = media_storage.url(file_path_within_bucket)

            return JsonResponse({
                'message': 'OK',
                'fileUrl': file_url,
            })
        else:
            return JsonResponse({
                'message': 'Error: file {filename} already exists at {file_directory} in bucket {bucket_name}'.format(
                    filename=file_obj.name,
                    file_directory=file_directory_within_bucket,
                    bucket_name=media_storage.bucket_name
                ),
            }, status=400)

    def get_file_url(self, file, folder):

        media_storage = MediaStorage()

        file_directory_within_bucket = folder

        file_path_within_bucket = os.path.join(
            file_directory_within_bucket,
            file
        )

        if media_storage.exists(file_path_within_bucket):

            file_url = media_storage.url(file_path_within_bucket)

            return JsonResponse({
                'message': 'OK',
                'fileUrl': file_url,
            })

        else:
            return JsonResponse({
                'message': 'Error: file {filename} does not exists at {file_directory} in bucket {bucket_name}'.format(
                    filename=file,
                    file_directory=file_directory_within_bucket,
                    bucket_name=media_storage.bucket_name
                ),
            }, status=400)

    def remove_file(self, file, folder):

        media_storage = MediaStorage()

        file_directory_within_bucket = folder

        file_path_within_bucket = os.path.join(
            file_directory_within_bucket,
            file
        )

        if media_storage.exists(file_path_within_bucket):

            file_url = media_storage.delete(file_path_within_bucket)

            return JsonResponse({
                'message': 'OK',
            })

        else:
            return JsonResponse({
                'message': 'Error: file {filename} does not exists at {file_directory} in bucket {bucket_name}'.format(
                    filename=file,
                    file_directory=file_directory_within_bucket,
                    bucket_name=media_storage.bucket_name
                ),
            }, status=400)

# class FileUploadView(generics.CreateAPIView):
#     """
#     POST file/upload/
#     """
#
#     parser_classes = (MultiPartParser,)
#     permission_classes = [permissions.AllowAny]
#
#     def post(self, request, *args, **kwargs):
#         file_obj = request.data['images']
#
#         # print(file_obj)
#
#         # do your validation here e.g. file size/type check
#         # organize a path for the file in bucket
#         file_directory_within_bucket = 'recipes-img'
#
#         # synthesize a full file path; note that we included the filename
#         file_path_within_bucket = os.path.join(
#             file_directory_within_bucket,
#             file_obj.name
#         )
#
#         media_storage = MediaStorage()
#
#         if not media_storage.exists(file_path_within_bucket):
#             # avoid overwriting existing file
#             media_storage.save(file_path_within_bucket, file_obj)
#             file_url = media_storage.url(file_path_within_bucket)
#
#             return JsonResponse({
#                 'message': 'OK',
#                 'fileUrl': file_url,
#             })
#         else:
#             return JsonResponse({
#                 'message': 'Error: file {filename} already exists at {file_directory} in bucket {bucket_name}'.format(
#                     filename=file_obj.name,
#                     file_directory=file_directory_within_bucket,
#                     bucket_name=media_storage.bucket_name
#                 ),
#             }, status=400)
#
#
# class FileDetailView(generics.RetrieveUpdateDestroyAPIView):
#     """
#     POST file/get-url
#     """
#
#     # parser_classes = (MultiPartParser, )
#     permission_classes = [permissions.AllowAny]
#
#     def put(self, request, *args, **kwargs):
#
#         file_directory = request.data["folder"]
#
#         file = str(request.data['file_name']).split(".")
#
#         file_name = file[0]
#         file_type = str("." + file[1])
#
#         media_storage = MediaStorage()
#
#         file_directory_within_bucket = file_directory
#
#         file_path_within_bucket = os.path.join(
#             file_directory_within_bucket,
#             file_name + file_type
#         )
#
#         if media_storage.exists(file_path_within_bucket):
#
#             file_url = media_storage.url(file_path_within_bucket)
#
#             return JsonResponse({
#                 'message': 'OK',
#                 'fileUrl': file_url,
#             })
#
#         else:
#             return JsonResponse({
#                 'message': 'Error: file {filename} does not exists at {file_directory} in bucket {bucket_name}'.format(
#                     filename=file_name + file_type,
#                     file_directory=file_directory_within_bucket,
#                     bucket_name=media_storage.bucket_name
#                 ),
#             }, status=400)
#
#
# class FileRemoveView(generics.DestroyAPIView):
#     """
#     DELETE file/remove
#     """
#
#     def delete(self, request, *args, **kwargs):
#
#         file_directory = request.data["folder"]
#
#         file = str(request.data['file_name']).split(".")
#
#         file_name = file[0]
#         file_type = str("." + file[1])
#
#         media_storage = MediaStorage()
#
#         file_directory_within_bucket = file_directory
#
#         file_path_within_bucket = os.path.join(
#             file_directory_within_bucket,
#             file_name + file_type
#         )
#
#         if media_storage.exists(file_path_within_bucket):
#             media_storage.delete(file_path_within_bucket)
#             return JsonResponse({
#                 'message': 'OK',
#             })
#         else:
#             return JsonResponse({
#                 'message': 'Error: file {filename} does not exists at {file_directory} in bucket {bucket_name}'.format(
#                     filename=file_name + file_type,
#                     file_directory=file_directory_within_bucket,
#                     bucket_name=media_storage.bucket_name
#                 ),
#             }, status=400)
