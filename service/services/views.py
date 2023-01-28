from rest_framework.viewsets import ReadOnlyModelViewSet

from services.models import Subscription
from services.serializer import SubscriptionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
