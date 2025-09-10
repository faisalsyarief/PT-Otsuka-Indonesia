from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from .models import CustomUser


class EmployeeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "nama",
            "email",
            "jabatan",
            "tanggal_masuk",
            "status_aktif",
            "username",
            "password",
        ]
        read_only_fields = ["id"]


    def create(self, validated_data):
        pw = validated_data.pop("password", None)
        user = CustomUser(**validated_data)
        if pw:
            validate_password(pw, user)
            user.set_password(pw)
        else:
            user.set_unusable_password()
        user.save()
        return user


    def update(self, instance, validated_data):
        pw = validated_data.pop("password", None)
        for k, v in validated_data.items():
            setattr(instance, k, v)
        if pw:
            validate_password(pw, instance)
            instance.set_password(pw)
        instance.save()
        return instance
