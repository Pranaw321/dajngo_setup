from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate

# User Serializer
class ExtUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = ExtUser
    fields = ('id', 'email','first_name', 'last_name','joining_date','is_active','is_email_verified','is_mobile_no_verified','mobile_no','address')


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
  class Meta:
    model = ExtUser
    fields = ('id', 'email', 'first_name', 'last_name', 'password','mobile_no')
    extra_kwargs = {'password': {'write_only': True}}

  def create(self, validated_data):
    if validated_data['email'] is not None:
      user = ExtUser.objects.create_user(email=validated_data['email'],mobile_no=validated_data['mobile_no'],first_name=validated_data['first_name'],last_name = validated_data['last_name'], password=validated_data['password'])
      return user
    else:
      user = ExtUser.objects.create_user(email=validated_data['email'],mobile_no=validated_data['mobile_no'],first_name=validated_data['first_name'],last_name = validated_data['last_name'], password=validated_data['password'])
      return user

# Login Serializer
class LoginSerializer(serializers.Serializer):
  email = serializers.CharField()
  password = serializers.CharField()

  def validate(self, data):
    user = authenticate(**data)
    if user and user.is_active:
      return user
    raise serializers.ValidationError("Incorrect Credentials")