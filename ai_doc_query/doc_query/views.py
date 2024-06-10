from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.
def signUp(request):
    # for user in User.objects:
    #     user.delete()
    # # Assuming you have a User and a Chat instance already created
    # user = User(email="example@example.com", password="password123").save()
    # chat = Chat(title="Sample Chat", owner=user).save()

    # # Sample PDF file path
    # pdf_file_path = "/home/eritheia/Downloads/sample.pdf"

    # # Create a new File instance
    # with open(pdf_file_path, 'rb') as pdf_file:
    #     file_doc = File(
    #         name="Sample PDF",
    #         chat=chat,
    #     )
    #     file_doc.file.put(pdf_file, content_type='application/pdf')
    #     file_doc.save()

    # print("PDF file saved successfully in the File table!")
    file_doc = File.objects(name="Sample PDF").first()

    if file_doc and file_doc.file:
        # Read the file content from GridFS
        file_data = file_doc.file.read()
        
        # Save the file data to a local file (optional)
        output_file_path = "/home/eritheia/Downloads/retrieved_sample.pdf"
        with open(output_file_path, 'wb') as output_file:
            output_file.write(file_data)
        
        print(f"PDF file retrieved successfully and saved to {output_file_path}!")
    else:
        print("File not found.")
    return HttpResponse("Signup")

def logIn(request):
    for chat in Chat.objects:
        print(chat.title)
    return HttpResponse("Login")