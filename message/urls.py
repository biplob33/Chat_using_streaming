from django.urls import path
from message.views import chat_home,frn,post,messages
urlpatterns = [
    path('chat/', chat_home),
    path('home/', frn),
    path('post/',post),
    path('messages/',messages),
]