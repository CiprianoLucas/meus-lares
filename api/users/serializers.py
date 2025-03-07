import re
from datetime import date

from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress
from rest_framework import serializers
from soft_components.serializers import softModelSerializer

from .models import User


def validate_full_name(full_name: str):
    if len(full_name.strip().split(" ")) < 2:
        raise serializers.ValidationError({"Insert your full name"})
    return full_name


def validate_phone_number(phone_number: str):
    phone_number = "".join(re.findall(r"\d", str(phone_number)))
    if len(phone_number) < 10:
        raise serializers.ValidationError(
            {"Invalid"}
        )
    return phone_number


def validate_cpf(cpf: str):
    regex_cnpj = re.compile(r"^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$")

    if bool(regex_cnpj.match(cpf)):
        raise serializers.ValidationError("Invalid")

    cpf = ("".join(re.findall(r"\d", str(cpf)))).zfill(11)

    if len(cpf) > 11 or len(set(cpf)) == 1:
        raise serializers.ValidationError("Invalid")

    inteiros = list(map(int, cpf))
    novo = inteiros[:9]

    for _ in range(2):
        r = sum([(len(novo) + 1 - i) * v for i, v in enumerate(novo)]) % 11
        f = 11 - r if r > 1 else 0

        novo.append(f)

    if novo != inteiros:
        raise serializers.ValidationError("Invalid")

    return cpf


def validate_birth(birth: str):
    day, month, year = map(int, birth.split("/"))
    formatted_date = date(year, month, day)
    if formatted_date >= date.today():
        raise serializers.ValidationError(
            "Date of birth must be before the current year"
        )

    return formatted_date


class UserSerializer(softModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "cpf",
            "nick",
            "email",
            "phone_number",
            "full_name",
            "birth",
            "verified_status",
            "profile_photo",
            "self_photo",
            "document_front_photo",
            "document_back_photo",
            "self_with_document_photo",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "self_photo": {"write_only": True},
            "document_front_photo": {"write_only": True},
            "document_back_photo": {"write_only": True},
            "self_with_document_photo": {"write_only": True},
            "verified_status": {"read_only": True},
        }

    def to_internal_value(self, initial_data):

        data = initial_data.copy()

        if data.get("cpf", None):
            data["cpf"] = validate_cpf(data["cpf"])
        if data.get("email", None):
            data["email"] = get_adapter().clean_email(data["email"])
        if data.get("phone_number", None):
            data["phone_number"] = validate_phone_number(data["phone_number"])
        if data.get("birth", None):
            data["birth"] = validate_birth(data["birth"])
        if data.get("full_name", None):
            data["full_name"] = validate_full_name(data["full_name"])

        return super().to_internal_value(data)

    def update(self, instance: User, data):

        if instance.verified_status == "verified" and any(
            key
            in [
                "cpf",
                "email",
                "phone_number",
                "birth",
                "full_name",
                "self_photo",
                "document_front_photo",
                "document_back_photo",
                "self_with_document_photo",
            ]
            for key in data.keys()
        ):
            raise serializers.ValidationError(
                {"error": "Cannot change validated identity data"}
            )

        super().update(instance, data)

        if all(
            key
            in [
                "self_photo",
                "document_front_photo",
                "document_back_photo",
                "self_with_document_photo",
            ]
            for key in data.keys()
        ):
            instance.verified_status = "in_progress"
            instance.save()

        return instance


class CustomSignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    full_name = serializers.CharField(required=True)
    cpf = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    birth = serializers.CharField(required=True)
    nick = serializers.CharField(required=False)

    def validate_full_name(self, full_name: str):
        return validate_full_name(full_name)

    def validate_birth(self, birth: str):
        return validate_birth(birth)

    def validate_email(self, email: str):
        return get_adapter().clean_email(email)

    def validate_password(self, password: str):
        return get_adapter().clean_password(password)

    def validate_phone_number(self, phone_number: str):
        return validate_phone_number(phone_number)

    def validate_cpf(self, cpf: str):
        return validate_cpf(cpf)

    def create(self, validated_data: dict):
        adapter = get_adapter()
        request = self.context.get("request")
        if validated_data.get("nick", None) and not validated_data["nick"]:
            validated_data["nick"] = validated_data["full_name"]

        user = adapter.new_user(request=request)
        self._set_fields(user, validated_data)

        user.save(user=self.context["request"].user)
        email_address = EmailAddress.objects.create(
            user=user, email=validated_data.get("email"), primary=True, verified=False
        )
        email_address.send_confirmation(request)
        return user

    def _set_fields(self, user: User, data: dict):
        user.set_password(data.get("password"))
        user.email = data.get("email")
        user.full_name = data.get("full_name")
        user.cpf = data.get("cpf")
        user.phone_number = data.get("phone_number")
        user.birth = data.get("birth")
        user.nick = data.get("nick")
        user.username = data.get("email")
