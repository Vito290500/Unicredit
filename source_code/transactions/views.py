"""
Transaction views configuration. 
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Transaction
from .serializers import TransactionSerializer, TransactionDetailSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TransferSerializer
from accounts.models import BankAccount
from .pagination import TransactionPageNumberPagination

@extend_schema_view(
    list=extend_schema(
        summary="Elenca le transazioni",
        description="Restituisce paginazione di tutte le transazioni dell’utente."
    ),
    retrieve=extend_schema(
        summary="Dettaglio transazione",
        description="Restituisce i dettagli di una singola transazione per `id`."
    ),
)
class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.all().order_by('-created_at')
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    ordering_fields = ['created_at', 'date', 'amount', 'category', 'destinatario_nome', 'mittente_nome']
    pagination_class = TransactionPageNumberPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TransactionDetailSerializer
        return TransactionSerializer

    def get_queryset(self):
        return super().get_queryset().filter(account__user=self.request.user)

class TransferView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TransferSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            from_account = serializer.validated_data['from_account']
    
            if from_account.user != request.user:
                return Response({'detail': 'Non puoi disporre bonifici da un conto che non ti appartiene.'}, status=status.HTTP_403_FORBIDDEN)

            transfer = serializer.save()
            
            return Response({
                'success': True,
                'tx_out_id': str(transfer['tx_out'].id),
                'tx_in_id': str(transfer['tx_in'].id),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
