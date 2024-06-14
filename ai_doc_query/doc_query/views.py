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
            except DoesNotExist:
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
            except DoesNotExist:
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
                    "owner" : chat.owner.email
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
                    "owner" : chat.owner.email
                    }
                    chat_list.append(chat_data)
                return JsonResponse(chat_list,safe=False,status = 200)
            except Exception as e:
                return JsonResponse({"message" : str(e)}, status = 400)

    def post(self,request):
        try:
            data = json.loads(request.body)

            title = data.get("title")
            owner_id = data.get("owner_id")

            if not title or not owner_id:
                return JsonResponse({"message" : "Chat title and owner_id required"}, status = 400)

            new_chat = Chat(title = title , owner = owner_id)
            new_chat.save()

            return JsonResponse({"message" : "Chat created successfully"},status = 201)

        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON"}, status=400)
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

            except json.JSONDecodeError:
                return JsonResponse({"message": "Invalid JSON"}, status=400)
            except DoesNotExist:
                return JsonResponse({"message" : "Chat does not exist"}, status = 404)

        except Exception as e:
            return JsonResponse({"message" : str(e)}, status = 500)

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


@method_decorator(csrf_exempt, name="dispatch")
class MessageApis(View):
    def get(self, request, id=None):
        if id:
            try:
                req_msg = Message.objects.get(pk=id)
                msg = {
                    "id" : str(req_msg.id),
                    "chat": req_msg.chat.title,
                    "type": str(req_msg.type)
                }

                return JsonResponse(msg ,status = 200)
            except DoesNotExist:
                return JsonResponse({"message" : "Message does not exist"}, status = 404)
            except Exception as e:
                return JsonResponse({"message" : str(e)}, status= 500)
        else:
            try:
                msg_list = []

                for msg in Message.objects:
                    data = {
                    "id" : str(msg.id),
                    "msg_txt" : msg.msg_txt,
                    "chat": msg.chat.title,
                    "type":str(msg.type)
                }
                    msg_list.append(data)

                return JsonResponse(msg_list, safe=False, status=200)
            except Exception as e:
                return  JsonResponse({"message": str(e)}, status=500)

    def post(self, request):
        try:
            data = json.loads(request.body)

            msg_txt = data.get("msg_txt")
            type = data.get("type")
            chat_id = data.get("chat_id")

            if not msg_txt or not type or not chat_id:
                return JsonResponse({"message": "Message text , type and chat are required"}, status =400)

            if type == "bot":
                type = MessageType.BOT
            elif type == "user":
                type = MessageType.USER
            else:
                return JsonResponse({"message":"Message type can either be 'user' or 'bot' "},status= 400)

            new_msg = Message(msg_txt=msg_txt , type=type , chat=chat_id)
            new_msg.save()
            return JsonResponse({"message" : "Message created successfully"},status = 201)
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON"}, status=400)
        except DoesNotExist as d:
            return JsonResponse({"message": "Message does not exist"},status = 404)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status= 500)

    def put(self, request, id):
        try:
            data = json.loads(request.body)

            new_txt = data.get("new_txt")

            if not new_txt:
                return JsonResponse({"message": "New text is required"}, status= 400)

            req_msg = Message.objects.get(pk=id)
            req_msg.msg_txt = new_txt
            req_msg.save()
            return JsonResponse({"message": "Message updated succesfully"}, status = 200)

        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON"}, status=400)
        except DoesNotExist as d:
            return JsonResponse({"message" : "Message does not exist"}, status = 404)
        except Exception as e:
            return JsonResponse({"message" : str(e)}, status = 500)

    def delete(self,request,id):
        try:
            req_msg = Message.objects.get(pk = id)
            req_msg.delete()
            return JsonResponse({"message":"Message deleted successfully"}, status= 204)
        except DoesNotExist as d:
            return JsonResponse({"message": "Message does not exist"}, status = 404)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status = 500)

@method_decorator(csrf_exempt, name="dispatch")
class FileApis(View):
    def get(self,request,id=None):
        if id:
            try:
                req_file = File.objects.get(pk=id)
                file_obj = {
                    "id": str(req_file.id),
                    "name": req_file.name,
                    "chat": req_file.chat.title
                }
                return JsonResponse(file_obj,status=200)
            except DoesNotExist as d:
                return JsonResponse({"message": "File does not exist"} , status=404)
            except Exception as e:
                return JsonResponse({"message" : str(e)}, status = 500)
        else:
            try:
                file_list = []

                for file in File.objects:
                    file_obj = {
                    "id": str(file.id),
                    "name": file.name,
                    "chat": file.chat.title
                    }
                    file_list.append(file_obj)

                return JsonResponse(file_list, safe=False, status= 200)
            except Exception as e:
                return JsonResponse({"message" : str(e)}, status = 500)

    def post(self, request):
        try:
            data = json.loads(request.body)

            path = data.get("path")
            chat_id = data.get("chat_id") # would be static currently

            if not path or not chat_id:
                return JsonResponse({"message" : "File path and chat id required"}, status= 400)

            file_name = path.split("/")[-1]
            file_name = file_name.split(".")[0]
            print(file_name)

            new_file = File(name= file_name, chat = chat_id)
            with open(path, "rb") as f:
                new_file.file.put(f, content_type = "application/pdf")
            new_file.save()

            return JsonResponse({"message":"File created successfuly"}, status = 201)

        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status = 500)

    def delete(self,request,id):
        try:
            req_file = File.objects.get(pk=id)
            req_file.file.delete()
            req_file.save()
            req_file.delete()
            return  JsonResponse({"message": "File deleted successfully"} , status=204)
        except DoesNotExist as d:
            return JsonResponse({"message": "File does not exist"}, status = 404)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status = 500)