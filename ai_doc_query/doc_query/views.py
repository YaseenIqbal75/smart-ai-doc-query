from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator



@method_decorator(csrf_exempt, name='dispatch')
class UserApis(View):

    def get(self,request,id=None):
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
                return JsonResponse({"message": str(e)}, status=400)
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
                return JsonResponse({"message": str(e)}, status=400)

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
            return JsonResponse({"message": str(e)}, status=400)
        
    def delete(self,request,id):
        try:
            try:
                req_user = User.objects.get(pk=id)
            except User.DoesNotExist:
                return JsonResponse({"message": "User does not exist"}, status=404)

            req_user.delete()
            return JsonResponse({"message": "The user was deleted"}, status=204)

        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class ChatApis(View):
    def get(self,request, id=None):
        if id:
            try:
                chat = Chat.objects.get(pk=id)
                chat_data= {
                    "id": str(chat.id),
                    "title" : chat.title,
                    "creation_timestamp": chat.creation_timestamp,
                    "owner" : User.objects.get(pk=chat.owner.id).email
                }
                return JsonResponse(chat_data, status = 200)
            except Exception as e:
                return JsonResponse({"message" : str(e)}, status = 400)
        else:
            try:
                chat_list = []
                for chat in Chat.objects:
                    chat_data= {
                    "id": str(chat.id),
                    "title" : chat.title,
                    "creation_timestamp": chat.creation_timestamp,
                    "owner" : User.objects(pk = chat.owner.id).first().email
                    }
                    chat_list.append(chat_data)
                return JsonResponse(chat_list,safe=False,status = 200)
            except Exception as e:
                return JsonResponse({"message" : str(e)}, status = 400)

    def post(self,request):
        try:
            data = json.loads(request.body)
            title = data.get("title")
            owner = User.objects(email="arslanwaqar421@gmail.com").first() # static user

            if not title or not owner:
                return JsonResponse({"message" : "Chat title and Owner required"}, status = 400)

            new_chat = Chat(title = title , owner = owner)
            new_chat.save()

            return JsonResponse({"message" : "Chat created successfully"},status = 201)

        except Exception as e:
            return JsonResponse({"message" : str(e)}, status = 400)

    def put(self,request,id):
        try:
            data = json.loads(request.body)
            title = data.get("title")

            if not title:
                return JsonResponse({"message" : "Title is required"}, status= 400)

            try:
                req_chat = Chat.objects.get(pk=id)
                req_chat.title = title
                req_chat.save()
                return JsonResponse({"message": "Title updated"}, status=200)
            except DoesNotExist:
                JsonResponse({"message" : "Chat does not exist"}, status = 404)

        except Exception as e:
            return JsonResponse({"message" : str(e)}, status = 400)

    def delete(self, request, id):
        try:
            try:
                req_chat = Chat.objects.get(pk=id)
            except DoesNotExist:
                return JsonResponse({"message": "Chat does not exist"}, status=404)

            req_chat.delete()
            return JsonResponse({"message" : "Chat deleted succesfully"}, status=204)
        except Exception as e:
            return JsonResponse({"message" : str(e)})