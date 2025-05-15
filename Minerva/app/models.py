from django.contrib.auth.models import User
from django.db import models

class Roles(models.TextChoices):
    ADMIN = 'administrador', 'Administrador'
    PRENSA = 'prensa', 'Encargado de Prensa'
    CLASIFICACION = 'clasificacion', 'Encargado de Clasificación'
    REDACCION = 'redaccion', 'Encargado de Redacción'
    PUBLICACION = 'publicacion', 'Encargado de Publicación'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=Roles.choices)

    def __str__(self):
        return f'{self.user.username} ({self.get_rol_display()})'

# Proxy model para lógica adicional (opcional)
class UsuarioSistema(User):
    class Meta:
        proxy = True

    def is_prensa(self):
        return hasattr(self, 'userprofile') and self.userprofile.rol == Roles.PRENSA

    def is_clasificador(self):
        return hasattr(self, 'userprofile') and self.userprofile.rol == Roles.CLASIFICACION

    def is_redactor(self):
        return hasattr(self, 'userprofile') and self.userprofile.rol == Roles.REDACCION


class DiarioDigital(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    url_principal = models.URLField()

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    class CategoriaTipo(models.TextChoices):
        INDIVIDUALIZACION = 'individualizacion', 'Individualización'
        BANDAS = 'bandas criminales', 'Bandas Criminales'
        CONFLICTIVIDAD = 'conflictividad barrial', 'Conflictividad Barrial'

    nombre = models.CharField(max_length=30, choices=CategoriaTipo.choices, unique=True)

    def __str__(self):
        return self.get_nombre_display()


class EstadoLink(models.TextChoices):
    PENDIENTE = 'pendiente', 'Pendiente'
    APROBADO = 'aprobado', 'Aprobado'
    DESCARTADO = 'descartado', 'Descartado'

class LinkRelevante(models.Model):
    url = models.URLField(unique=True)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    cargado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='links_cargados')
    diario_digital = models.ForeignKey(DiarioDigital, on_delete=models.CASCADE, related_name='links')
    estado = models.CharField(max_length=20, choices=EstadoLink.choices, default=EstadoLink.PENDIENTE)
    fecha_aprobacion = models.DateTimeField(null=True, blank=True)
    categorias = models.ManyToManyField(Categoria, blank=True)

    def __str__(self):
        return self.url


class Articulo(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    generado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articulos_generados')
    links_incluidos = models.ManyToManyField(LinkRelevante)

    def __str__(self):
        return self.titulo



class TipoActividad(models.TextChoices):
    LOGIN = 'login', 'Inicio de sesión'
    LOGOUT = 'logout', 'Cierre de sesión'
    CARGA_LINK = 'carga_link', 'Carga de Link'
    CAMBIO_ESTADO = 'cambio_estado', 'Cambio de Estado'
    CLIC_LINK = 'clic_link', 'Clic en Link'
    CREACION_ARTICULO = 'creacion_articulo', 'Creación de Artículo'
    OTRO = 'otro', 'Otro'

class Actividad(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tipo = models.CharField(max_length=30, choices=TipoActividad.choices)
    descripcion = models.TextField()
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.get_tipo_display()} - {self.fecha_hora.strftime('%d/%m/%Y %H:%M')}"

