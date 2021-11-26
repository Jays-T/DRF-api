from django.urls import path
from django.urls.resolvers import URLPattern
from profiles import views

urlpatterns = [
    path('profiles/', views.ProfileList.as_view()),
]
