from django.urls import path
from . import views

urlpatterns = [
    path('main/', views.MainPageView.as_view()),
    path('objects/', views.ObjectsView.as_view())
]