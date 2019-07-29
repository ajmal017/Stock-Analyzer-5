from django.urls import path

from Analyze.views import indexView

app_name = 'Analyze'

urlpatterns = [
    path('', indexView, name='index'),
]
