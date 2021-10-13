from django.urls import path
from .views import IndexPageView, DataFromJivoView


urlpatterns = [
    path('', IndexPageView.as_view(), name='index_page'),
    path('bot_here/', DataFromJivoView.as_view(), name='bot_here'),
]
