from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    UserProfile, DiarioDigital, Categoria,
    LinkRelevante, Articulo
)

from .utils.actividad import log_actividad
from .models import TipoActividad

from rest_framework import serializers
from .models import LinkRelevante, Categoria, DiarioDigital, Actividad

# Serializer para perfil de usuario
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['rol']

# Usuario con perfil anidado
class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'userprofile']

# DiarioDigital
class DiarioDigitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiarioDigital
        fields = '__all__'

# Categoria
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

# LinkRelevante
class LinkRelevanteSerializer(serializers.ModelSerializer):
    cargado_por = serializers.StringRelatedField()
    diario_digital = DiarioDigitalSerializer()
    categorias = CategoriaSerializer(many=True)

    class Meta:
        model = LinkRelevante
        fields = [
            'id', 'url', 'fecha_carga', 'cargado_por',
            'diario_digital', 'estado', 'fecha_aprobacion', 'categorias'
        ]

        def update(self, instance, validated_data):
            estado_anterior = instance.estado
            instance = super().update(instance, validated_data)

            if 'estado' in validated_data and validated_data['estado'] != estado_anterior:
                log_actividad(
                    self.context['request'],
                    TipoActividad.CAMBIO_ESTADO,
                    f"Se cambió el estado del link ID {instance.id} de '{estado_anterior}' a '{instance.estado}'."
                )

            return instance


class LinkRelevanteCreateSerializer(serializers.ModelSerializer):
    diario_digital = serializers.PrimaryKeyRelatedField(queryset=DiarioDigital.objects.all())
    categorias = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all(), many=True)

    def create(self, validated_data):
        user = self.context['request'].user
        categorias = validated_data.pop('categorias', [])
        link = LinkRelevante.objects.create(cargado_por=user, **validated_data)
        link.categorias.set(categorias)

        # Registro de actividad (debe estar aquí)
        log_actividad(
            self.context['request'],
            TipoActividad.CARGA_LINK,
            f"Se cargó el link: {link.url}"
        )

        return link
    
    class Meta:
        model = LinkRelevante
        fields = ['url', 'diario_digital', 'categorias']


# Articulo
class ArticuloSerializer(serializers.ModelSerializer):
    links_incluidos = serializers.PrimaryKeyRelatedField(queryset=LinkRelevante.objects.all(), many=True)

    class Meta:
        model = Articulo
        fields = ['id', 'titulo', 'descripcion', 'fecha_generacion', 'generado_por', 'links_incluidos']
        read_only_fields = ['fecha_generacion', 'generado_por']

    def create(self, validated_data):
        user = self.context['request'].user
        links = validated_data.pop('links_incluidos', [])
        articulo = Articulo.objects.create(generado_por=user, **validated_data)
        articulo.links_incluidos.set(links)

        log_actividad(
            self.context['request'],
            TipoActividad.CREACION_ARTICULO,
            f"Creó el artículo: '{articulo.titulo}' con {len(links)} link(s)."
        )

        return articulo
    
class ActividadSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField()

    class Meta:
        model = Actividad
        fields = ['id', 'usuario', 'tipo', 'descripcion', 'fecha_hora']