from rest_framework import serializers
from contact_us.models import ContactFormEntry


class ContactFormEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactFormEntry
        fields = ["email", "first_name", "last_name", "message", "created_by"]
        read_only_fields = ["created_by"]

    def create(self, validated_data):
        creator = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            creator = request.user

        validated_data["created_by"] = creator
        instance = super().create(validated_data)
        return instance