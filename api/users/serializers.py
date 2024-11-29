from rest_framework import serializers
from allauth.account.models import EmailAddress
from allauth.account.adapter import get_adapter
from .models import User
import re
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'cpf', 'phone_number', 'full_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class CustomSignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    full_name = serializers.CharField(required=True)
    cpf = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    birth = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    
    def validate_full_name(self, full_name: str):
        if len(full_name.strip().split(' ')) < 2:
            raise serializers.ValidationError("Insira o nome completo.")
        return full_name
    
    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email já está em uso.")
        return get_adapter().clean_email(email)
    
    def validate_password(self, password):
        return get_adapter().clean_password(password)
    
    def validate_phone_number(self, phone_number):
        phone_number = (''.join(re.findall(r'\d', str(phone_number))))
        if len(phone_number) < 10:
            raise serializers.ValidationError("Número de telefone inválido.")
        return phone_number
    
    def validate_cpf(self, cpf):
        regex_cnpj = re.compile(r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$')
    
        if bool(regex_cnpj.match(cpf)): raise serializers.ValidationError("CPF inválido.")
        
        cpf = (''.join(re.findall(r'\d', str(cpf)))).zfill(11)
        
        if len(cpf) > 11 or len(set(cpf)) == 1: raise serializers.ValidationError("CPF inválido.")

        inteiros = list(map(int, cpf))
        novo = inteiros[:9]

        for _ in range(2):
            r = sum([(len(novo)+1-i)*v for i,v in enumerate(novo)]) % 11
            f = 11 - r if r > 1 else 0
            
            novo.append(f)

        if novo != inteiros:
            raise serializers.ValidationError("CPF inválido.")
        
        if User.objects.filter(cpf=cpf).exists():
            raise serializers.ValidationError("CPF já está em uso.")
        
        return cpf
    
    def create(self, validated_data):
        adapter = get_adapter()
        request = self.context.get('request')
        user = adapter.new_user(request=request)
        self._set_user_fields(user, validated_data)
        
        user.save()
        email_address = EmailAddress.objects.create(
            user=user, 
            email=validated_data.get('email'), 
            primary=True,
            verified=False
        )
        email_address.send_confirmation(request)
        return user

    def _set_user_fields(self, user, data):
        user.set_password(data.get('password'))
        user.email = data.get('email')
        user.full_name = data.get('full_name')
        user.cpf = data.get('cpf')
        user.phone_number = data.get('phone_number')
        user.birth = data.get('birth')
        user.username = data.get('username')