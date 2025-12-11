from django.urls import path
from . import views
from .views import exportar_pdf   # 👈 importar la función

urlpatterns = [
    path('', views.home, name="home"),
    path('nuevo/', views.crear_checklist, name="nuevo"),
    path('reporte/', views.reporte_csv, name="reporte"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('detalle/<int:pk>/', views.detalle_checklist, name="detalle"),
    path('pdf/<int:checklist_id>/', exportar_pdf, name='exportar_pdf'),
]