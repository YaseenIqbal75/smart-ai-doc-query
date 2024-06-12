from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator



@method_decorator(csrf_exempt, name='dispatch')
class UserApis(View):

    def get(self, request, id=None):
        if id:
            try:
                user = User.objects.get(pk=id)
                user_data = {
                    "id": str(user.id),
                    "email": user.email,
                    "password": user.password
                }
                return JsonResponse(user_data, status=200)
            except User.DoesNotExist:
                return JsonResponse({"message": "User does not exist"}, status=404)
            except Exception as e:
                return JsonResponse({"message": str(e)}, status=500)
        else:
            try:
                users_list = []

                for user in User.objects:
                    user_data = {
                        "id": str(user.id),
                        "email": user.email,
                        "password": user.password
                    }
                    users_list.append(user_data)

                return JsonResponse(users_list, safe=False, status=200)
            except Exception as e:
                return JsonResponse({"message": str(e)}, status=500)

    def post(self,request):
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return JsonResponse({"message": "Email and Password are required."}, status=400)

            if User.objects(email=email).first():
                return JsonResponse({"message": "User with this email already exists"}, status=400)

            new_user = User(email=email, password=password)
            new_user.save()

            return JsonResponse({"email": email, "password": password}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)

    def put(self,request,id):
        try:
            data = json.loads(request.body)
            password = data.get('password')

            if not password:
                return JsonResponse({"message": "New password required"}, status=400)

            try:
                req_user = User.objects.get(pk=id)
            except User.DoesNotExist:
                return JsonResponse({"message": "User does not exist"}, status=404)

            req_user.password = password
            req_user.save()
            return JsonResponse({"message": "Password updated"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)
        
    def delete(self, request, id):
        try:
            try:
                req_user = User.objects.get(pk=id)
            except User.DoesNotExist:
                return JsonResponse({"message": "User does not exist"}, status=404)

            req_user.delete()
            return JsonResponse({"message": "The user was deleted"}, status=200)

        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)
# @csrf_exempt
# def create_read_user(request):
#     if request.method =='POST':
#         try:
#             data = json.loads(request.body)
#             email = data.get('email')
#             password = data.get('password')

#             if not email or not password:
#                 return JsonResponse({"message" : "Email and Password are required."}, status = 400)
            
#             if User.objects(email=email).first():
#                 return JsonResponse({"message": "User with this email already exists"}, status=400)

#             new_user = User(email=email,password=password)
#             new_user.save()

#             return JsonResponse({"email": email, "password" : password}, status = 201)
        
#         except Exception as e:
#             return JsonResponse({'message': f"{e}"}, status=400)
    
#     elif request.method == "GET":
#         try:
#             users_list = []

#             for user in User.objects:
#                 user_data = {
#                     "id": str(user.id),
#                     "email": user.email,
#                     "password": user.password
#                 }
#                 users_list.append(user_data)
            

#             return JsonResponse(users_list,safe=False, status = 200)
#         except Exception as e:
#             return JsonResponse({"message" : f"{e}"}, status = 200)
#     else:
#         return JsonResponse({"message" : "Invalid Request Method"} , status = 405)
    
# @csrf_exempt
# def delete_update_user(request, id):
    # if request.method == "DELETE":
    #     try:
    #         if not id:
    #             return JsonResponse({"message" : "Invalid user id"}, 400)
    #         req_user = None

    #         try:
    #             req_user = User.objects.get(pk=id)
    #         except User.DoesNotExist:
    #             return JsonResponse({"message": "User does not exist"}, status=404)
            
    #         req_user.delete()
    #         return JsonResponse({"message" : "The user was deleted"}, status = 200)
        
    #     except Exception as e:
    #         return JsonResponse({"message" : f"{e}"})
        
    # elif request.method == "PUT":
    #     try: 
    #         data = json.loads(request.body)
    #         password = data.get('password')
            
    #         if not password:
    #             return JsonResponse({"message" : "New password required" }, 400)
            
    #         if not id:
    #             return JsonResponse({"message" : "Invalid user id"}, 400)
            
    #         req_user = None

    #         try:
    #             req_user = User.objects.get(pk=id)
    #         except User.DoesNotExist:
    #             return JsonResponse({"message": "User does not exist"}, status=404)
            
    #         req_user.password = password
    #         req_user.save()
    #         return JsonResponse({"message" : "Password updated"}, status=200)
    #     except Exception as e:
    #         return JsonResponse({"message" : f"{e}"}, status=400)
    # else:
    #     return JsonResponse({"message" : "Invalid Request Method"} , status = 405)