from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Venta
from .serializers import VentaSerializer

class VentaList(APIView):
    def get(self, request):
        ventas = Venta.objects.all()
        serializer = VentaSerializer(ventas, many=True)
        return Response(serializer.data)
