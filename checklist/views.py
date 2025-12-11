from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Checklist
from .forms import ChecklistForm
import csv


# ----------------------------------------------------
# HOME – LISTADO PRINCIPAL
# ----------------------------------------------------
def home(request):
    data = Checklist.objects.all().order_by('-date')   # último primero
    return render(request, "checklist/checklist_list.html", {
        "checklist": data
    })

from django.shortcuts import render, get_object_or_404
from .models import Checklist

def detalle_checklist(request, pk):
    checklist = get_object_or_404(Checklist, pk=pk)
    return render(request, "checklist/detalle.html", {"checklist": checklist})

# ----------------------------------------------------
# CREAR NUEVO CHECKLIST
# ----------------------------------------------------
def crear_checklist(request):
    if request.method == "POST":
        form = ChecklistForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = ChecklistForm()

    return render(request, "checklist/checklist_form.html", {
        "form": form
    })


# ----------------------------------------------------
# EXPORTAR REPORTE CSV
# ----------------------------------------------------
def reporte_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte_checklist.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "ID", "Cliente", "Operador", "Placas", "Fecha",
        "Carta TIF", "Factura", "Copias TIF Porteo",
        "Orden compra", "Confirmación cita", "Control embarque",
        "Otro nombre", "Otro entregado", "Completo"
    ])

    data = Checklist.objects.all().order_by('-date')

    for c in data:
        writer.writerow([
            c.id, c.cliente, c.operador, c.placas, c.date,
            c.carta_tif, c.factura, c.copias_tif_porteo,
            c.orden_compra, c.confirmacion_cita, c.control_embarque,
            c.other_name, c.other_present, c.is_complete
        ])

    return response


# ----------------------------------------------------
# DASHBOARD
# ----------------------------------------------------
# ----------------------------------------------------
# DASHBOARD
# ----------------------------------------------------
from django.db.models import Q
from django.utils import timezone
import json

def dashboard(request):
    # Fecha de hoy
    hoy = timezone.localdate()

    # Registros totales
    total = Checklist.objects.count()

    # Incompletos (si cualquier campo está en False)
    incompletos = Checklist.objects.filter(
        Q(carta_tif=False) |
        Q(factura=False) |
        Q(copias_tif_porteo=False) |
        Q(orden_compra=False) |
        Q(confirmacion_cita=False) |
        Q(control_embarque=False) |
        Q(other_present=False)
    ).count()

    # Completos = todos los campos True
    completos = total - incompletos

    # Datos por día (últimos 7 días)
    ultimos = Checklist.objects.order_by("-created_at")[:7][::-1]

    labels = [reg.created_at.strftime("%d-%m") for reg in ultimos]
    data_registros = [1 for _ in ultimos]  # Cada registro vale 1

    context = {
        "total": total,
        "incompletos": incompletos,
        "completos": completos,
        "labels_json": json.dumps(labels),
        "data_json": json.dumps(data_registros),
    }

    return render(request, "checklist/dashboard.html", context)
