from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from django.db.models import Q
from django.utils import timezone
import csv
import json

from .models import Checklist
from .forms import ChecklistForm

# ----------------------------------------------------
# HOME – LISTADO PRINCIPAL
# ----------------------------------------------------
def home(request):
    data = Checklist.objects.all().order_by('-date')   # último primero
    return render(request, "checklist/checklist_list.html", {
        "checklist": data
    })


# ----------------------------------------------------
# DETALLE DE CHECKLIST
# ----------------------------------------------------
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


# ----------------------------------------------------
# EXPORTAR PDF
# ----------------------------------------------------
from xhtml2pdf import pisa

def exportar_pdf(request, checklist_id):
    checklist = get_object_or_404(Checklist, id=checklist_id)

    template_path = 'checklist/pdf_template.html'
    context = {'checklist': checklist}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Checklist_{checklist_id}.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("Error al generar PDF", status=500)

    return response
