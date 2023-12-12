import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    nc = models.CharField(max_length=10, unique=True)
    role = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    initial_test= models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role', 'nc', 'password']

    @property
    def is_anonymous(self):
        return False

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        names = self.first_name.split()
        return names[0] if names else ''
    
class CuestionarioInicial(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    nivel_experiencia = models.CharField(
        max_length=20,
        choices=[
            ('Principiante', 'Principiante'),
            ('Intermedio', 'Intermedio'),
            ('Avanzado', 'Avanzado')
        ]
    )
    estilo_aprendizaje = models.CharField(
        max_length=20,
        choices=[
            ('Visual', 'Visual'),
            ('Auditivo', 'Auditivo'),
            ('Kinestésico', 'Kinestésico')
        ]
    )
    contenido_preferido = models.CharField(
        max_length=20,
        choices=[
            ('Videos', 'Videos'),
            ('Lecturas', 'Lecturas'),
            ('Prácticas', 'Prácticas')
        ]
    )
    horarios_estudio = models.CharField(
        max_length=20,
        choices=[
            ('Mañana', 'Mañana'),
            ('Tarde', 'Tarde'),
            ('Noche', 'Noche')
        ]
    )
    duracion_sesiones = models.CharField(
        max_length=20,
        choices=[
            ('Cortas', 'Cortas'),
            ('Moderadas', 'Moderadas'),
            ('Largas', 'Largas')
        ]
    )
    formato_evaluacion = models.CharField(
        max_length=20,
        choices=[
            ('Cuestionarios', 'Cuestionarios'),
            ('Proyectos', 'Proyectos'),
            ('Discusiones', 'Discusiones')
        ]
    )
    recibir_recomendaciones = models.BooleanField(default=True)

    def __str__(self):
        return f"Cuestionario de {self.user.username}"

class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    profesor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    alumnos = models.ManyToManyField(CustomUser, related_name='materias_inscritas', blank=True, default="")

    def __str__(self):
        return self.nombre
    
    def is_user_registered(self, user):
        return self.alumnos.filter(id=user.id).exists()
    
class Tema(models.Model):
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
class Subtema(models.Model):
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200, default="")
    tipo = models.CharField(max_length=50, choices=[('Material didáctico', 'Material didáctico'), ('Evaluación', 'Evaluación'), ('Video', 'Video')])

    def __str__(self):    
        return self.nombre
    
class SubtemaDoc(models.Model):
    subtema = models.ForeignKey(Subtema, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    file = models.FileField(upload_to='docs/')

    def __str__(self):    
        return self.name

class Video(models.Model):
    subtema = models.ForeignKey(Subtema, on_delete=models.CASCADE)
    video = models.CharField(max_length=100)

class Evaluacion(models.Model):
    subtema = models.ForeignKey(Subtema, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50, choices=[('Cuestionarios', 'Cuestionarios'), ('Proyectos', 'Proyectos'), ('Discusiones', 'Discusiones')])
    valor = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)

class Pregunta(models.Model):
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE)
    preg = models.CharField(max_length=100)
    correcta = models.CharField(max_length=100)
    opc_a = models.CharField(max_length=100)
    opc_b = models.CharField(max_length=100)
    opc_c = models.CharField(max_length=100)

class Calificacion(models.Model):
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE)
    alumno = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class RegistroTiempo(models.Model):
    alumno = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subtema = models.ForeignKey(Subtema, on_delete=models.CASCADE)
    tiempo_dedicado = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Registro de tiempo para {self.alumno} en {self.subtema}"