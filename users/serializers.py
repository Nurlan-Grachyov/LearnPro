from rest_framework import serializers

from users.models import CustomUser, Payments


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор пользователя с методом выдачи полей в зависимости от того, кто обращается,и логикой получения платежей
    """

    payments = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = "__all__"

    def to_representation(self, instance):
        """
        Метод выдачи полей в зависимости от того, кто обращается
        """

        representation = super().to_representation(instance)
        request = self.context.get("request")

        if (
            request.user == instance
            or request.user.groups.filter(name="Moderators").exists()
        ):
            return representation
        else:
            representation.pop("last_name", None)
            representation.pop("password", None)
            representation.pop("payments", None)

        return representation

    def get_payments(self, obj):
        """
        Метод получения платежей
        """

        payments = Payments.objects.filter(user=obj)
        return [payment.__str__() for payment in payments]


class RegisterSerializer(serializers.ModelSerializer):
    """
    Сериализатор регистрации с методом создания
    """

    class Meta:
        model = CustomUser
        fields = "__all__"

    def create(self, validated_data):
        """
        Метод создания аккаунта
        """

        user = CustomUser(
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.is_active = True
        user.save()
        return user


class PaymentsSerializer(serializers.ModelSerializer):
    """
    Сериализатор платежей
    """

    class Meta:
        model = Payments
        fields = "__all__"
