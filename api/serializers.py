from rest_framework import serializers
from hunt.models import Product
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email']


class ProductSerializer(serializers.ModelSerializer):
    creator = UserSerializer()
    vote_users = serializers.SerializerMethodField()
    details = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_vote_users(self, obj):
        User = get_user_model()
        user_ids = [int(x) for x in obj.vote_users.split(',')]  # "2,3" -> [2, 3]
        users = User.objects.filter(id__in=user_ids)  # [user1, u]
        return [user.username for user in users]

    def get_details(self, obj):
        return f"http://127.0.0.1:8002/api/products/{obj.pk}/"