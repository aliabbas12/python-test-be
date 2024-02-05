from rest_framework.viewsets import ModelViewSet

from contact_us.models import ContactFormEntry
from accounts.permissions import AllowAny
from contact_us.serializers import ContactFormEntrySerializer


class ContactFormEntryViewSet(ModelViewSet):
    queryset = ContactFormEntry.objects.all()
    serializer_class = ContactFormEntrySerializer
    permission_classes = [AllowAny]
    http_method_names = ["post"]
