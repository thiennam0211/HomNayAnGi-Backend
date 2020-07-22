from django.http import QueryDict
from pylint.checkers.spelling import instr
from rest_framework import serializers
from .models import Users

from dateutil import parser
import json


class UsersSerializers(serializers.ModelSerializer):

    # def validate_password(self, value):
    #     if value.isalnum():
    #         raise serializers.ValidationError('password must have at least one special character.')
    #     return value

    # def validate_email(self, value):  # to validate if the user have been used
    #     is_valid = email.validate_email(email_address=value, check_regex=True)
    #     if not is_valid:
    #         raise serializers.ValidationError("Invalid Email Address")
    #     return value

    def to_internal_value(self, value):
        if isinstance(value, QueryDict):
            if type(value['birthday']) == str:
                _mutable = value._mutable
                value._mutable = True
                value['birthday'] = parser.parse(value['birthday']).date()
                value._mutable = _mutable
        else:
            value['birthday'] = parser.parse(value['birthday']).date()
        return super().to_internal_value(value)

    class Meta:
        model = Users
        id = serializers.IntegerField()
        email = serializers.EmailField()
        fields = ('id', 'email', 'password', 'full_name', 'display_name', 'gender', 'birthday', 'avatar')

    def update(self, instance, validated_data):
        # validate_data.get(X, Y) => if X has value (new data) then return X, if X has no value then return Y

        # user_new_data = json.loads(json.dumps(validated_data))
        # instance.birthday = user_new_data['birthday']

        instance.birthday = parser.parse( str(validated_data.get('birthday', instance.birthday)) ).date()
        instance.password = validated_data.get('password', instance.password)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.display_name = validated_data.get('display_name', instance.display_name)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()

        return instance




