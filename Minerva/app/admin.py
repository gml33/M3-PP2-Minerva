from django.contrib import admin
from django.contrib.auth.models import User
from .models import (
    UserProfile, UsuarioSistema,
    DiarioDigital, Categoria,
    LinkRelevante, Articulo,
    Actividad
)

# UserProfile en línea dentro del User admin
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfil de Usuario'

class CustomUserAdmin(admin.ModelAdmin):
    inlines = (UserProfileInline,)

# Registrar el modelo User con el perfil inline
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Registrar otros modelos
@admin.register(DiarioDigital)
class DiarioDigitalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'url_principal')
    search_fields = ('nombre',)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(LinkRelevante)
class LinkRelevanteAdmin(admin.ModelAdmin):
    list_display = ('url', 'estado', 'fecha_carga', 'cargado_por')
    list_filter = ('estado', 'fecha_carga', 'diario_digital')
    search_fields = ('url',)
    filter_horizontal = ('categorias',)

@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_generacion', 'generado_por')
    search_fields = ('titulo', 'descripcion')
    filter_horizontal = ('links_incluidos',)

@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ('fecha_hora', 'usuario', 'tipo', 'descripcion')
    list_filter = ('tipo', 'fecha_hora', 'usuario')
    search_fields = ('descripcion', 'usuario__username')
    ordering = ('-fecha_hora',)