from http import HTTPStatus
import json
import sys
from django.http import JsonResponse
from django.shortcuts import render
from data.models import Data

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken

from rest_framework.views import APIView
from data.serializer import DataSerializer
import users

from users.models import Users

# Create your views here.


class StoreData(APIView):
    def post(self, request):
        response = {
            "status": "",
            "message": ""
        }
        try:
            authorization_header = request.META.get('HTTP_AUTHORIZATION')
            token = authorization_header.split()[1]
            access_token_obj = AccessToken(token)
            token_user = eval(access_token_obj.payload['user_id'])
        except:
            response["status"] = "error"
            response["code"] = "INVALID_TOKEN"
            response["message"] = "Invalid access token provided"
        else:
            data = json.loads(request.body)
            key = data.get('key', '')
            value = data.get('value', '')
            user = Users.objects.get(user_id=token_user['user_id'])

            if len(key) == 0:
                response["status"] = "error"
                response["code"] = "INVALID_KEY"
                response["message"] = "The provided key is not valid or missing."
            elif len(value) == 0:
                response["status"] = "error"
                response["code"] = "INVALID_VALUE"
                response["message"] = "The provided value is not valid or missing."
            elif len(Data.objects.filter(user=user, key=key)) != 0:
                response["status"] = "error"
                response["code"] = "KEY_EXISTS"
                response["message"] = "The provided key already exists in the database. To update an existing key, use the update API."
            else:
                user_data = Data(user=user, key=key, value=value)
                user_data.save()
                response["status"] = "success"
                response["message"] = "Data stored successfully."

        if response["status"] == "success":
            return JsonResponse(status=HTTPStatus.OK, data=response)
        else:
            return JsonResponse(status=HTTPStatus.BAD_REQUEST, data=response)


class ManipulateData(APIView):
    def get(self, request, *args, **kwargs):
        response = {
            "status": ""
        }
        try:
            key = self.kwargs['key']
            print(key)
            authorization_header = request.META.get('HTTP_AUTHORIZATION')
            token = authorization_header.split()[1]
            access_token_obj = AccessToken(token)
            token_user = eval(access_token_obj.payload['user_id'])
            user = Users.objects.get(user_id=token_user['user_id'])
            # print(user.user_id)
        except:
            response["status"] = "error"
            response["code"] = "INVALID_TOKEN"
            response["message"] = "Invalid access token provided"
        else:
            value_data = Data.objects.filter(user_id=user.user_id, key=key)
            if len(value_data) == 0:
                response["status"] = "error"
                response["code"] = "KEY_NOT_FOUND"
                response["message"] = "The provided key does not exist in the database."
            else:
                value = DataSerializer(value_data, many=True).data[0]['value']
                response["status"] = "success"
                response["data"] = {
                    "key": key,
                    "value": value
                }

        if response["status"] == "success":
            return JsonResponse(status=HTTPStatus.OK, data=response)
        else:
            return JsonResponse(status=HTTPStatus.BAD_REQUEST, data=response)

    def put(self, request, *args, **kwargs):
        response = {
            "status": ""
        }
        try:
            key = self.kwargs['key']
            authorization_header = request.META.get('HTTP_AUTHORIZATION')
            token = authorization_header.split()[1]
            access_token_obj = AccessToken(token)
            token_user = eval(access_token_obj.payload['user_id'])
            user = Users.objects.get(user_id=token_user['user_id'])
        except:
            response["status"] = "error"
            response["code"] = "INVALID_TOKEN"
            response["message"] = "Invalid access token provided"
        else:
            value_data = Data.objects.filter(user_id=user.user_id, key=key)
            if len(value_data) == 0:
                response["status"] = "error"
                response["code"] = "KEY_NOT_FOUND"
                response["message"] = "The provided key does not exist in the database."
            else:
                data=json.loads(request.body)   
                value = data.get('value')
                Data.objects.filter(user_id=user.user_id, key=key).update(value=value)
                response["status"] = "success"
                response["message"] = "Data updated successfully."

        if response["status"] == "success":
            return JsonResponse(status=HTTPStatus.OK, data=response)
        else:
            return JsonResponse(status=HTTPStatus.BAD_REQUEST, data=response)
        
    def delete(self, request, *args, **kwargs):
        response = {
            "status": ""
        }
        try:
            key = self.kwargs['key']
            authorization_header = request.META.get('HTTP_AUTHORIZATION')
            token = authorization_header.split()[1]
            access_token_obj = AccessToken(token)
            token_user = eval(access_token_obj.payload['user_id'])
            user = Users.objects.get(user_id=token_user['user_id'])
        except:
            response["status"] = "error"
            response["code"] = "INVALID_TOKEN"
            response["message"] = "Invalid access token provided"
        else:
            user_data = Data.objects.filter(user_id=user.user_id, key=key)
            if len(user_data) == 0:
                response["status"] = "error"
                response["code"] = "KEY_NOT_FOUND"
                response["message"] = "The provided key does not exist in the database."
            else:
                Data.objects.filter(user_id=user.user_id, key=key).delete()
                response["status"] = "success"
                response["message"] = "Data deleted successfully."

        if response["status"] == "success":
            return JsonResponse(status=HTTPStatus.OK, data=response)
        else:
            return JsonResponse(status=HTTPStatus.BAD_REQUEST, data=response)
