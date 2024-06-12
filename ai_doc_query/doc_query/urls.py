from django.urls import path

from .import views

urlpatterns = [
    path("user/" , views.UserApis.as_view(), name="create_user"),
    path("user/<str:id>" , views.UserApis.as_view(), name="delete_update_user")
]