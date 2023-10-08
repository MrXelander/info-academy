from django.db import models
from app.models import CustomUser

class RegistroEstudiante(models.Model):
    estudiante = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tipo_contenido = models.CharField(
        max_length=50,
        choices=[
            ('Videos', 'Videos'),
            ('Lecturas', 'Lecturas'),
            ('Prácticas', 'Prácticas')
        ]
    )
    tiempo_dedicado_minutos = models.PositiveIntegerField()
    calificacion = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Registro de {self.estudiante.get_full_name()} - {self.tipo_contenido}"