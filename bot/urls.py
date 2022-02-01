from django.urls import path
from .views import IndexPageView, DataFromJivoView, SecondPageView


urlpatterns = [
    path('', IndexPageView.as_view(), name='index_page'),
    path('q/', SecondPageView.as_view(), name='second_page'),
    path('n1G0JfmBvjnXyjA/', DataFromJivoView.as_view(), name='bot_here'),
]
