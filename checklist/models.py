from django.db import models

class Checklist(models.Model):
    cliente = models.CharField(max_length=255)
    operador = models.CharField(max_length=255)
    placas = models.CharField(max_length=50, blank=True)

    carta_tif = models.BooleanField(default=False)
    factura = models.BooleanField(default=False)
    copias_tif_porteo = models.BooleanField(default=False)
    orden_compra = models.BooleanField(default=False)
    confirmacion_cita = models.BooleanField(default=False)
    control_embarque = models.BooleanField(default=False)

    other_name = models.CharField(max_length=255, blank=True)
    other_present = models.BooleanField(default=False)

    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_complete(self):
        docs = [
            self.carta_tif,
            self.factura,
            self.copias_tif_porteo,
            self.orden_compra,
            self.confirmacion_cita,
            self.control_embarque
        ]
        if self.other_name:
            docs.append(self.other_present)
        return all(docs)

    def __str__(self):
        return f"{self.cliente} ({self.operador})"
