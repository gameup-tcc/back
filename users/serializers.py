from rest_framework import serializers
from users.models import Person

class PersonSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Person
        fields = ('password', 'first_name', 'last_name', 'email', 'username',
                  'role')

    def create(self, validated_data):
        user = Person.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
