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
def dashboard(request):
    data = Checklist.objects.all()  # obtener todos los registros

    total = data.count()

    # calcular completos/incompletos usando la propiedad is_complete
    completos = sum(1 for c in data if c.is_complete)
    incompletos = total - completos

    return render(request, "checklist/dashboard.html", {
        "total": total,
        "completos": completos,
        "incompletos": incompletos
    })



# ----------------------------------------------------
# VISTA DE DETALLES
# ----------------------------------------------------
def detalle_checklist(request, pk):
    checklist = Checklist.objects.get(id=pk)

    return render(request, "checklist/checklist_detalle.html", {
        "c": checklist
    })
