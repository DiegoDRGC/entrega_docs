from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('nuevo/', views.crear_checklist, name="nuevo"),
    path('reporte/', views.reporte_csv, name="reporte"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('detalle/<int:pk>/', views.detalle_checklist, name="detalle"),
]



