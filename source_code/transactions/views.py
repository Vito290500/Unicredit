"""
Transaction views configuration. 
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Transaction
from .serializers import TransactionSerializer

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
    queryset = Transaction.objects.all().order_by('-date')
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Se vuoi filtrare solo quelle dell'account corrente:
        return super().get_queryset().filter(account__user=self.request.user)
