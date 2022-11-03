from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from Baedin_app.Models.Users.users import User




class UserSerializer(serializers.Serializer):
    Id = serializers.IntegerField()
    RoleType = serializers.IntegerField()
    date_joined = serializers.ReadOnlyField()
    UserName = serializers.CharField()
    PhoneNumber = serializers.CharField()
    Country = serializers.CharField()
    RoleName = serializers.CharField()
    Email = serializers.EmailField()
    isActive = serializers.BooleanField()
    isDeleted = serializers.BooleanField()
    isVerified = serializers.BooleanField()
    isSocial = serializers.BooleanField()
    Creation_Time = serializers.DateTimeField()
    profilePic = serializers.CharField()
    address = serializers.CharField()
    language = serializers.CharField()

    class Meta:
        model = User
        app_label = 'Beadin'
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}