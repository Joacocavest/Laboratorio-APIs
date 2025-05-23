from rest_framework import viewsets, permissions, status
from .models import Usuario
from .serializers import UsuarioSerializer, RegistroSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


# CRUD de usuario
class UsuarioViewSet(viewsets.ModelViewSet):
    def list(self):
        queryset = Usuario.objects.all()
        serializer_class = UsuarioSerializer(queryset, many=True)
        # permission_classes = [permissions.IsAuthenticated]
        return Response({"mensaje": "Lista de usuarios - Versión 1", "usuarios": serializer_class.data})

# class RegistroAPIView(APIView):
#     def post(self, request):
#         serializer = RegistroSerializer(data=request.data)
#         if serializer.is_valid():
#             usuario = serializer.save()
#             return Response({'mensaje': 'Usuario creado correctamente'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




