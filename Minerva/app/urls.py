from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, DiarioDigitalViewSet, CategoriaViewSet,
    LinkRelevanteViewSet, ArticuloViewSet, prensa_view, login_view, logout_view,
    clasificacion_view, redaccion_view, actividad_view, ActividadViewSet, exportar_actividades_excel,
    exportar_actividades_pdf, actividad_debug_view
)


router = DefaultRouter()
router.register(r'usuarios', UserViewSet, basename='usuario')
router.register(r'diarios', DiarioDigitalViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'links', LinkRelevanteViewSet)
router.register(r'articulos', ArticuloViewSet)
router.register(r'actividades', ActividadViewSet, basename='actividad')

urlpatterns = [
    path('api/', include(router.urls)),
    path('actividades/exportar_excel/', exportar_actividades_excel, name='exportar_actividades_excel'),
    path('actividades/exportar_pdf/', exportar_actividades_pdf, name='exportar_actividades_pdf'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', prensa_view, name='prensa'),
    path('clasificacion/', clasificacion_view, name='clasificacion'),
    path('redaccion/', redaccion_view, name='redaccion'),
    path('actividad/', actividad_view, name='actividad'),
    path('actividad_debug/', actividad_debug_view, name='actividad_debug'),
]