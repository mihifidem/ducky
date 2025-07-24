<<<<<<< HEAD
# jobs/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone # Importar para usar timezone.now() o manejar TimeZone


# Oferta de empleo creada por un headhunter
class JobOffer(models.Model):
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='job_offers_created',
        verbose_name="Creada por"
    )
    company_name = models.CharField(max_length=200, verbose_name="Nombre de la empresa")
    title = models.CharField(max_length=200, verbose_name="Título del puesto")
    description = models.TextField(verbose_name="Descripción")
    location = models.CharField(max_length=100, blank=True, verbose_name="Ubicación")
    
    class ModalityChoices(models.TextChoices):
        REMOTE = 'remote', 'Remoto'
        ONSITE = 'onsite', 'Presencial'
        HYBRID = 'hybrid', 'Híbrido'

    modality = models.CharField(
        max_length=20,
        choices=ModalityChoices.choices,
        default=ModalityChoices.ONSITE,
        verbose_name="Modalidad"
    )
    salary = models.CharField(max_length=100, blank=True, verbose_name="Salario")
    category = models.CharField(max_length=100, blank=True, verbose_name="Categoría")
    requirements = models.TextField(blank=True, verbose_name="Requisitos")
    benefits = models.TextField(blank=True, verbose_name="Beneficios")
    is_active = models.BooleanField(default=True, verbose_name="Activa")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última actualización")    

    class Meta:
        verbose_name = "Oferta de Empleo"
        verbose_name_plural = "Ofertas de Empleo"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} en {self.company_name}"

# Candidatura de un usuario a una oferta
class CandidatureStatus(models.TextChoices):
    PENDING = 'pendiente', 'Pendiente'
    ACCEPTED = 'aceptado', 'Aceptado'
    REJECTED = 'rechazado', 'Rechazado'

class Candidatura(models.Model):
    offer = models.ForeignKey(
        JobOffer, on_delete=models.CASCADE, related_name='applications', verbose_name="Oferta de Empleo"
    )
    # ELIMINADO: El campo 'candidatura' que estaba aquí fue movido a AgendaAccion
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='my_applications', verbose_name="Candidato"
    )
    estado = models.CharField(
        max_length=20, choices=CandidatureStatus.choices, default=CandidatureStatus.PENDING, verbose_name="Estado"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    mensaje_personalizado = models.TextField(blank=True, null=True, verbose_name="Mensaje personalizado")
    fecha_aplicacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de aplicación")

    class Meta:
        verbose_name = "Candidatura"
        verbose_name_plural = "Candidaturas"
        unique_together = ('offer', 'user')
        ordering = ['-fecha_aplicacion']

    def __str__(self):
        return f"{self.user.username} - {self.offer.title} ({self.get_estado_display()})"
=======
from django.db import models
from django.contrib.auth.models import User

# Oferta de empleo creada por un headhunter
class JobOffer(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_offers')
    company_name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100, blank=True)
    modality = models.CharField(
        max_length=20,
        choices=[
            ('remote', 'Remote'),
            ('onsite', 'On Site'),
            ('hybrid', 'Hybrid')
        ],
        default='onsite'
    )
    salary = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100, blank=True)
    requirements = models.TextField(blank=True)
    benefits = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    headhunter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_offers_as_headhunter', null=True, blank=True)

    def __str__(self):
        return f"{self.title} at {self.company_name}"

# Candidatura de un usuario a una oferta
class JobApplication(models.Model):
    offer = models.ForeignKey(
        JobOffer,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    applicant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='job_applications'
    )
    applied_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=True)

    class Meta:
        unique_together = ('offer', 'applicant')

    def __str__(self):
        return f"{self.applicant.username} → {self.offer.title}"
    
class Candidature(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
    ]

    offer = models.ForeignKey(
        JobOffer, on_delete=models.CASCADE, related_name='candidatures'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='candidatures'
    )
    estado = models.CharField(
        max_length=20, choices=ESTADO_CHOICES, default='pendiente'
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.offer.title} ({self.estado})"
>>>>>>> e083518c28dbe2d325c3d2683f4c84a9cc6209d7
    
class StatusMessageTemplate(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
<<<<<<< HEAD
        related_name="status_templates",
        verbose_name="Usuario (Headhunter)"
    )
    estado = models.CharField(
        max_length=20,
        choices=CandidatureStatus.choices,
        default=CandidatureStatus.PENDING,
        verbose_name="Estado de Candidatura"
    )
    mensaje = models.TextField(verbose_name="Plantilla de Mensaje")

    class Meta:
        unique_together = ('user', 'estado')
        verbose_name = "Plantilla de Mensaje de Estado"
        verbose_name_plural = "Plantillas de Mensajes de Estado"

    def __str__(self):
        return f"Plantilla de {self.user.username} para {self.get_estado_display()}"
    
class AgendaAccion(models.Model):
    class AccionTipoChoices(models.TextChoices):
        INTERVIEW = 'entrevista', 'Entrevista'
        CALL = 'llamada', 'Llamada'
        REMINDER = 'recordatorio', 'Recordatorio'
        DELIVERY = 'entrega', 'Entrega'
        OTHER = 'otro', 'Otro'

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='agenda_acciones',
        verbose_name="Realizada por"
    )
    oferta = models.ForeignKey(
        JobOffer, 
        null=True, blank=True, 
        on_delete=models.SET_NULL, 
        related_name='acciones_agendadas',
        verbose_name="Oferta asociada"
    )
    # ESTE ES EL CAMPO 'candidatura' que estaba en Candidatura y AHORA ESTÁ AQUÍ
    candidatura = models.ForeignKey(
        Candidatura, # Referencia al modelo Candidatura (sin comillas porque ya está definido arriba)
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='acciones_agendadas_candidatura',
        verbose_name="Candidatura asociada"
    )
    titulo = models.CharField(max_length=255, verbose_name="Título de la acción")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    
    fecha_hora_inicio = models.DateTimeField(
        verbose_name="Fecha y Hora de Inicio",
    )
    duracion_minutos = models.PositiveIntegerField(default=30, verbose_name="Duración (minutos)")
    
    tipo = models.CharField(
        max_length=20, 
        choices=AccionTipoChoices.choices, 
        default=AccionTipoChoices.OTHER, 
        verbose_name="Tipo de acción"
    )
    finished = models.BooleanField(default=False, verbose_name="Finalizada")
    fecha_finalizacion = models.DateTimeField(
        null=True, blank=True, verbose_name="Fecha de finalización"
    )

    class Meta:
        verbose_name = "Acción de Agenda"
        verbose_name_plural = "Acciones de Agenda"
        ordering = ['fecha_hora_inicio']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['fecha_hora_inicio']),
            models.Index(fields=['oferta']),
            models.Index(fields=['candidatura']), # Añadido el índice para el nuevo campo en AgendaAccion
        ]

    def __str__(self):
        return f"{self.titulo} ({self.fecha_hora_inicio.strftime('%Y-%m-%d %H:%M')})"
    
    @property
    def fecha_hora_fin(self):
        if self.fecha_hora_inicio and self.duracion_minutos:
            return self.fecha_hora_inicio + timezone.timedelta(minutes=self.duracion_minutos)
        return None
=======
        related_name="status_templates"
    )
    estado = models.CharField(
        max_length=20,
        choices= Candidature.ESTADO_CHOICES,
        default='pendiente'
    )
    mensaje = models.TextField()

    class Meta:
        unique_together = ('user', 'estado')

    def __str__(self):
        return f"{self.user.username} - {self.estado}"
    


class AccionOferta(models.Model):
    TIPO_ACCION_CHOICES = [
        ('llamada', 'Llamada'),
        ('entrevista', 'Entrevista'),
        ('nota', 'Nota Interna'),
        ('seguimiento', 'Seguimiento'),
        ('otro', 'Otro'),
    ]

   
    oferta = models.ForeignKey('jobs.JobOffer', on_delete=models.CASCADE, related_name='acciones')
    fecha = models.DateTimeField()
    tipo = models.CharField(max_length=20, choices=TIPO_ACCION_CHOICES)
    descripcion = models.TextField()
    realizada_por = models.ForeignKey(User, on_delete=models.CASCADE)

class Oferta(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ofertas')
    titulo = models.CharField(max_length=255)
    empresa = models.CharField(max_length=255, help_text="Nombre de la empresa asociada")
    descripcion = models.TextField()
    fecha_publicacion = models.DateField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['fecha_publicacion']),
        ]

    def __str__(self):
        return f"{self.titulo} - {self.empresa}"


class AgendaAccion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='acciones')
    oferta = models.ForeignKey(Oferta, null=True, blank=True, on_delete=models.SET_NULL, related_name='acciones')
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    fecha = models.DateField()
    hora = models.TimeField()
    duracion_minutos = models.PositiveIntegerField(default=30)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['fecha']),
            models.Index(fields=['oferta']),
        ]

    def __str__(self):
        return f"{self.titulo} ({self.fecha} {self.hora})"
>>>>>>> e083518c28dbe2d325c3d2683f4c84a9cc6209d7
