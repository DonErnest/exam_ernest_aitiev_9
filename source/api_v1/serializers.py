from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password','password_confirm', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, **kwargs):
        user = User(username=self.validated_data['username'],
                    first_name = self.validated_data['first_name'],
                    last_name=self.validated_data['last_name'],
                )
        password = self.validated_data['password']
        password_confirm = self.validated_data['password_confirm']

        if password != password_confirm:
            raise serializers.ValidationError({'password': 'Passwords must match!'})
        user.set_password(password)
        user.save()
    # вот здесь вставить создание какого-нибудь профиля, если такие будут в ТЗ
        return user