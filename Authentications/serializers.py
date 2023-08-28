from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username','password','is_claimAssure_admin' , 'is_support_staff' , 'is_document_manager')
        extra_kwargs = {'password': {'write_only': True}}
    
    def validate(self, data):
        username = data.get('username')
        if username == "" or username == None:
            raise serializers.ValidationError({'message':'Username can not be empty'})
        if username[0].islower():
            raise serializers.ValidationError('Username First letter must be uppercase')

        password = data.get('password')
        if len(password) < 8:
            raise serializers.ValidationError({ 'message':'Password must be at least 8 characters'})

        return data


    def create(self,validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ("email", "password")
        extra_kwargs ={'password':{'write_only':True}}


    def validate(self,data):
        if 'email' not in data or data['email'] == "":
           raise serializers.ValidationError('Email can not be empty !!')

        if 'password' not in data or data['password'] == "":
           raise serializers.ValidationError('Password can not be blank')
        return authenticate(**data)



class ChangePasswordSerializer(serializers.Serializer):
   password = serializers.CharField(max_length=255 , style={'input_type':'password'}, write_only =True)
   class Meta:
    Feilds = ["password"]
   
   def validate(self, data):
    password = data.get('password')
    if len(password) < 8:
       raise serializers.ValidationError('Password must be at least 8 characters')
    user = self.context.get('user')
    user.set_password(password)
    user.save()
    return data
