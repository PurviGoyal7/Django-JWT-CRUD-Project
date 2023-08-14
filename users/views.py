from http import HTTPStatus
import json
from django.http import JsonResponse
from django.conf import settings
from users.models import Users
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializer import UsersSerializer


def count_chars(str):
     upper_ctr, lower_ctr, number_ctr, special_ctr = 0, 0, 0, 0
     for i in range(len(str)):
          if str[i] >= 'A' and str[i] <= 'Z': upper_ctr += 1
          elif str[i] >= 'a' and str[i] <= 'z': lower_ctr += 1
          elif str[i] >= '0' and str[i] <= '9': number_ctr += 1
          else: special_ctr += 1
     return upper_ctr, lower_ctr, number_ctr, special_ctr
 
# Create your views here.
class Register(APIView):
    def post(self, request):
        try:
            data=json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            full_name = data.get('full_name')
            age = data.get('age')
            gender = data.get('gender')
            
            u, l, n, s = count_chars(password)
            
            response = {
                "status" : "",
                "message": "",
            }
        
            if email == '' or username == '' or password=='' or full_name=='':
                response["status"] = "error"
                response["code"] = "INVALID_REQUEST"
                response["message"] = "Invalid request. Please provide all required fields: username, email, password, full_name."
            elif Users.objects.filter(username=username).values():
                response["status"] = "error"
                response["code"] = "USERNAME_EXISTS"
                response["message"] = "The provided username is already taken. Please choose a different username."
            elif Users.objects.filter(email=email).values():
                response["status"] = "error"
                response["code"] = "EMAIL_EXISTS"
                response["message"] = "The provided email is already registered. Please use a different email address"
            elif len(password)<8 or u==0 or l==0 or n==0 or s==0:
                response["status"] = "error"
                response["code"] = "INVALID_PASSWORD"
                response["message"] = "The provided password does not meet the requirements. Password must be at least 8 characters long and contain a mix of uppercase and lowercase letters, numbers, and special characters."
            elif age<0:
                response["status"] = "error"
                response["code"] = "INVALID_AGE"
                response["message"] = "Invalid age value. Age must be a positive integer."
            elif len(gender) == 0:
                response["status"] = "error"
                response["code"] = "GENDER_REQUIRED"
                response["message"] = "Gender field is required. Please specify the gender (e.g., male, female, non-binary)."
            else:
                user = Users(email=email, username = username, password=password, full_name=full_name, age=age, gender=gender)    
                user.save() 
                response["status"] = "success"
                response["message"] = "User successfully registered!"
                data["user_id"] = Users.objects.get(email=email).user_id
                response["data"] = data
                
            
        except Exception as e:
            response["status"] = "error"
            response["code"] = "INTERNAL_SERVER_ERROR"
            response["message"] = "An internal server error occurred. Please try again later."
            
        if response["status"] == "success":
            return JsonResponse(status = HTTPStatus.OK, data=response)
        elif response["status"] == "error":
            return JsonResponse(status = HTTPStatus.BAD_REQUEST, data=response)
        
     
class Token(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)
            new_username = data.get('username', '')
            new_password = data.get('password', '')
            
            response = {
                "status" : "",
                "message": "",
            }
            
            if len(new_username) == 0 or len(new_password) == 0:
                response["status"] = "error"
                response["code"] = "MISSING_FIELDS"
                response["message"] = "Missing fields. Please provide both username and password."
                
            else: 
                user_data_raw = Users.objects.filter(username=new_username) #QuerySet
                if(len(user_data_raw) == 0):
                    response["status"] = "error"
                    response["code"] = "INVALID_CREDENTIALS"
                    response["message"] = "Invalid credentials. The provided username or password is incorrect."
                else:   
                    user_data = UsersSerializer(user_data_raw, many = True).data[0] #Dictionary items
                    user = Users(json.loads(json.dumps(user_data)))
                
                    username = user_data['username']
                    password = user_data['password']
                    user_data.pop("password")
                        
                    if username==new_username and password==new_password:
                        refresh = RefreshToken.for_user(user)
                        token = "Bearer "+ str(refresh.access_token)
                        response["status"] = "success"
                        response["message"] = "Access token generated successfully."
                        response["data"] = {
                            "access_token": token,
                            "expires_in": str(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'])  
                        }
                        
                    else:
                        response["status"] = "error"
                        response["code"] = "INVALID_CREDENTIALS"
                        response["message"] = "Invalid credentials. The provided username or password is incorrect."
            
        except Exception as e:
            response["status"] = "error"
            response["code"] = "INTERNAL_SERVER_ERROR"
            response["message"] = "An internal server error occurred. Please try again later."
            
        if response["status"] == "success":
            return JsonResponse(status = HTTPStatus.OK, data = response)
        else:
            return JsonResponse(status = HTTPStatus.BAD_REQUEST, data = response)
            
    
    

