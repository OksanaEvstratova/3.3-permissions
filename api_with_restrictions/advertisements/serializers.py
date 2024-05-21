from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import serializers

from advertisements.models import Advertisement
from rest_framework.exceptions import PermissionDenied, ValidationError


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)


    def validate(self, data):
        qs_count = Advertisement.objects.filter(Q(creator=self.context['request'].user) & Q(status='OPEN'))
        if qs_count.count() >= 10:
            raise ValidationError('You cant have more than 10 opened advertisements')
        else:
            return data
