from django.urls import path
from . import views
from .views import analyze_file, update_total

urlpatterns = [
    path('analyze/', views.analyze_file, name='analyze_file'),
    path('update_total/', views.update_total, name='update_total'),
]
