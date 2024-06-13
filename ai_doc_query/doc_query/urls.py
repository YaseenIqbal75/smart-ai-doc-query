from django.urls import path

from .import views

urlpatterns = [
    path("user/" , views.UserApis.as_view(), name="create_get_user"),
    path("user/<str:id>" , views.UserApis.as_view(), name="delete_update_user"),
    path("chat/", views.ChatApis.as_view(), name= "create_get_chat"),
    path("chat/<str:id>", views.ChatApis.as_view(), name= "update_delete_chat"),
    path("message/", views.MessageApis.as_view(), name="create_get_message"),
    path("message/<str:id>", views.MessageApis.as_view(),name="update_delete_message")
]