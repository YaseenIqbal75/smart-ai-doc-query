from django.http import JsonResponse,HttpResponse
from .models import *
import json
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .jwt_utils import *
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os



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

            email = request.POST.get('email')
            password = request.POST.get('password')

            if not email or not password:
                return JsonResponse({"message": "Email and Password are required."}, status=400)

            if User.objects(email=email).first():
                return JsonResponse({"message": "User with this email already exists"}, status=400)

            token, exp_time = generate_jwt(email)

            new_user = User(email=email, password=password, auth_token = token)
            new_user.save()

            return JsonResponse({"id": str(new_user.id),"email": email, "password": password, "auth_token" : token}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)

    def put(self,request,id):
        try:
            headers = request.headers
            auth_header = headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return JsonResponse({"message": "Authorization token not supplied or improperly formatted"}, status=401)

            token = auth_header.split(" ")[1]
            print(token)
            response = verify_jwt(token)

            if response.get('status') == False:
                return JsonResponse({"message" : response.get('msg')}, status = 401)
            print(response.get('msg'))
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
        
    def delete(self,request,id): # not wrapped yet with JWT tokens
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
        headers = request.headers
        auth_header = headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JsonResponse({"message": "Authorization token not supplied or improperly formatted"}, status=401)

        token = auth_header.split(" ")[1]
        print(token)
        response = verify_jwt(token)
        if response.get('status') == False:
            return JsonResponse({"message" : response.get('msg')}, status = 401)
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
                return JsonResponse({"message" : str(e)}, status = 500)
        else:
            try:
                decoded = response.get('msg')
                user_email = decoded.get("email")
                chat_list = []
                for chat in Chat.objects:
                    if chat.owner.email == user_email:
                        chat_data= {
                        "id": str(chat.id),
                        "title" : chat.title,
                        "creation_timestamp": chat.creation_timestamp,
                        "owner" : chat.owner.email
                        }
                        chat_list.append(chat_data)
                chat_list.reverse()
                print(chat_list)
                return JsonResponse(chat_list,safe=False,status = 200)
            except Exception as e:
                return JsonResponse({"message" : str(e)}, status = 500)

    def post(self,request):
        try:
            headers = request.headers
            auth_header = headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return JsonResponse({"message": "Authorization token not supplied or improperly formatted"}, status=401)

            token = auth_header.split(" ")[1]
            print(token)
            response = verify_jwt(token)

            if response.get('status') == False:
                return JsonResponse({"message" : response.get('msg')}, status = 401)
            print("Authorized")
            data = json.loads(request.body)
            print("Authorized")
            title = data.get("title")
            owner_id = data.get("owner_id")

            if not title or not owner_id:
                return JsonResponse({"message" : "Chat title and owner_id required"}, status = 400)

            new_chat = Chat(title = title , owner = owner_id)
            new_chat.save()
            print("Time now is : " , datetime.datetime.now(datetime.timezone.utc))
            print(new_chat.id, new_chat.title, new_chat.owner,new_chat.creation_timestamp)

            return JsonResponse({"id" : str(new_chat.id),
                                 "creation_timestamp" : new_chat.creation_timestamp,
                                 "owner" : str(new_chat.owner),
                                 "title" : new_chat.title},status = 201)

        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"message" : str(e)}, status =500)

    def put(self,request,id):
        try:
            headers = request.headers
            auth_header = headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return JsonResponse({"message": "Authorization token not supplied or improperly formatted"}, status=401)

            token = auth_header.split(" ")[1]
            print(token)
            response = verify_jwt(token)

            if response.get('status') == False:
                return JsonResponse({"message" : response.get('msg')}, status = 401)

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
            headers = request.headers
            auth_header = headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return JsonResponse({"message": "Authorization token not supplied or improperly formatted"}, status=401)

            token = auth_header.split(" ")[1]
            print(token)
            response = verify_jwt(token)
            if response.get('status') == False:
                return JsonResponse({"message" : response.get('msg')}, status = 401)
            try:
                req_chat = Chat.objects.get(pk=id)
            except DoesNotExist:
                return JsonResponse({"message": "Chat does not exist"}, status=404)

            req_chat.delete()
            print("Chat deleted")
            return JsonResponse({"message" : "Chat deleted succesfully"}, status=200)
        except Exception as e:
            return JsonResponse({"message" : str(e)},status=500)


@method_decorator(csrf_exempt, name="dispatch")
class MessageApis(View):
    def get(self, request, id):
        headers = request.headers
        auth_header = headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JsonResponse({"message": "Authorization token not supplied or improperly formatted"}, status=401)

        token = auth_header.split(" ")[1]
        print(token)
        response = verify_jwt(token)

        if response.get('status') == False:
            return JsonResponse({"message" : response.get('msg')}, status = 401)

        if id:
            try:
                print(id)
                chat_messages =[]
                for msg in Message.objects:
                    if str(msg.chat.id) == id:
                        curr_msg = {
                            "id" : str(msg.id),
                            "chat": msg.chat.title,
                            "type": str(msg.type),
                            "msg_txt": str(msg.msg_txt),
                            "creation_timestamp": msg.creation_timestamp
                        }
                        chat_messages.append(curr_msg)

                return JsonResponse(chat_messages,safe=False ,status = 200)
            except DoesNotExist:
                return JsonResponse({"message" : "No message found for the Chat"}, status = 404)
            except Exception as e:
                return JsonResponse({"message" : str(e)}, status= 500)
        else:
            return JsonResponse({"message" : "Chat id not found in query param"},status =400)

    def post(self, request):
        try:
            headers = request.headers
            auth_header = headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return JsonResponse({"message": "Authorization token not supplied or improperly formatted"}, status=401)

            token = auth_header.split(" ")[1]
            print(token)
            response = verify_jwt(token)

            if response.get('status') == False:
                return JsonResponse({"message" : response.get('msg')}, status = 401)

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
            return JsonResponse({"id" : str(new_msg.id),
                                 "msg_txt" : new_msg.msg_txt,
                                 "creation_timestamp" : new_msg.creation_timestamp},status = 201)
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status= 500)

    def put(self, request, id):
        try:
            headers = request.headers
            auth_header = headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return JsonResponse({"message": "Authorization token not supplied or improperly formatted"}, status=401)

            token = auth_header.split(" ")[1]
            print(token)
            response = verify_jwt(token)

            if response.get('status') == False:
                return JsonResponse({"message" : response.get('msg')}, status = 401)

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
            headers = request.headers
            auth_header = headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return JsonResponse({"message": "Authorization token not supplied or improperly formatted"}, status=401)

            token = auth_header.split(" ")[1]
            print(token)
            response = verify_jwt(token)

            if response.get('status') == False:
                return JsonResponse({"message" : response.get('msg')}, status = 401)

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
        headers = request.headers
        auth_header = headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JsonResponse({"message": "Authorization token not supplied or improperly formatted"}, status=401)

        token = auth_header.split(" ")[1]
        print(token)
        response = verify_jwt(token)

        if response.get('status') == False:
            return JsonResponse({"message" : response.get('msg')}, status = 401)

        if id:
            try:
                file_list = []
                for file in File.objects:
                    if str(file.chat.id) == id:
                        print("inside if loop")
                        file_obj = {
                        "id": str(file.id),
                        "name": file.name,
                        "chat": file.chat.title
                        }
                        file_list.append(file_obj)
                return JsonResponse(file_list,safe=False,status=200)
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
            headers = request.headers
            auth_header = headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return JsonResponse({"message": "Authorization token not supplied or improperly formatted"}, status=401)

            token = auth_header.split(" ")[1]
            print(token)
            response = verify_jwt(token)
            print('here!')
            if response.get('status') == False:
                return JsonResponse({"message": response.get('msg')}, status=401)
            chat_id = request.POST.get("chat_id") # should be passed in the form data
            print(chat_id)
            if not chat_id:
                return JsonResponse({"message": "Chat ID is required"}, status=400)

            if 'files[]' not in request.FILES:
                return JsonResponse({"message": "No file uploaded"}, status=400)
            uploaded_files = request.FILES.getlist('files[]')
            for uploaded_file in uploaded_files:
                file_name = uploaded_file.name
                file_path = default_storage.save(os.path.join('uploads', file_name), ContentFile(uploaded_file.read()))

                # Assuming your File model has a FileField to store the uploaded file
                new_file = File(name=file_name, chat=chat_id)
                with open(file_path, "rb") as f:
                    new_file.file.put(f, content_type = "application/pdf")
                new_file.save()

            return JsonResponse({"message": "Files uploaded successfully"}, status=201)

        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)

    def delete(self,request,id):
        try:
            headers = request.headers
            auth_header = headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return JsonResponse({"message": "Authorization token not supplied or improperly formatted"}, status=401)

            token = auth_header.split(" ")[1]
            print(token)
            response = verify_jwt(token)

            if response.get('status') == False:
                return JsonResponse({"message" : response.get('msg')}, status = 401)
            req_file = File.objects.get(pk=id)
            req_file.file.delete()
            req_file.save()
            req_file.delete()
            return  JsonResponse({"message": "File deleted successfully"} , status=204)
        except DoesNotExist as d:
            return JsonResponse({"message": "File does not exist"}, status = 404)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status = 500)

@method_decorator(csrf_exempt, name="dispatch")
class Login(View):
    def post(self,request):
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = User.objects(email=email).first()
            if user:
                if user.password == password:
                    print("inside pass")
                    verified = verify_jwt(str(user.auth_token))
                    print(verified)
                    if verified.get('status'):
                        return JsonResponse({"id": str(user.id),"email": user.email, "password": user.password, "auth_token" : user.auth_token},status=200)
                    else:
                        return JsonResponse({"message" : verified.get('msg')},status = 400)
                else:
                    return JsonResponse({"message" : "Invalid Password"},status = 400)
            else:
                return JsonResponse({"message": "Invalid Email"}, status= 400)
        except Exception as e:
            return JsonResponse({"message" : str(e)}, status=500)