from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.fintech.serializers import CreditSerializer, TransactionSerializer
from apps.fintech.models import Credit, Transaction
from django.utils.dateparse import parse_date

# Vista para obtener transacciones en un período
class TransactionsAPIView(APIView):
    def post(self, request, *args, **kwargs):
        start_date = parse_date(request.data.get('start_date'))
        end_date = parse_date(request.data.get('end_date'))

        if not start_date or not end_date:
            return Response({"error": "start_date y end_date son requeridos."}, status=status.HTTP_400_BAD_REQUEST)

        # Filtrar las transacciones en el período
        transactions = Transaction.objects.filter(date__range=[start_date, end_date])

        # Usamos el serializer para todos los datos
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Vista para obtener clientes con morosidad
class ClientsWithDefaultAPIView(APIView):
    def post(self, request, *args, **kwargs):
        credits = Credit.objects.filter(
            morosidad_level__in=['mild_default', 'moderate_default', 'severe_default', 'recurrent_default', 'critical_default']
        ).distinct('user')

        # Usamos el CreditSerializer para serializar todos los datos
        serializer = CreditSerializer(credits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Vista para obtener creditos de un periodo
class CreditsAPIView(APIView):

    def post(self, request, *args, **kwargs):
        # Obtener las fechas del cuerpo
        start_date = parse_date(request.data.get('start_date'))
        end_date = parse_date(request.data.get('end_date'))

        if not start_date or not end_date:
            return Response({"error": "start_date y end_date son requeridos."}, status=status.HTTP_400_BAD_REQUEST)

        # Filtrar los créditos financieros en el período
        credits = Credit.objects.filter(created_at__range=[start_date, end_date]).order_by('-created_at')

        serialized_data = []
        for credit in credits:
            try:
                serialized_data.append(CreditSerializer(credit).data)
            except Exception as e:
                print(f"Error serializing credit {credit.id}: {str(e)}")
        
        return Response(serialized_data)

