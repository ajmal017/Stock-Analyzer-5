from django.urls import path

from Analyze.views import indexView

app_name = 'CareerMatrix'

urlpatterns = [
    path('', indexView, name='index'),
]
