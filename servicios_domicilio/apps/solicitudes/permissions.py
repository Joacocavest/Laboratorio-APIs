from rest_framework.permissions import BasePermission, SAFE_METHODS

class EsClienteYDueñoSolicitud(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.tipo == 'cliente' and obj.cliente == request.user

class EsTrabajadorAsignado(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.tipo == 'trabajador' and obj.trabajador == request.user
