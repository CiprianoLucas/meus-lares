from rest_framework import serializers
from rest_framework.utils import model_meta


class softModelSerializer(serializers.ModelSerializer):
    def create(self, data):
        user = self.context["request"].user
        if not user:
            raise AttributeError("User is not defined")

        serializers.raise_errors_on_nested_writes("create", self, data)

        ModelClass = self.Meta.model

        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in data):
                many_to_many[field_name] = data.pop(field_name)

        instance = ModelClass(**data)
        instance.save(user=user)
        return instance

    def update(self, instance, data):
        user = self.context["request"].user
        if not user:
            raise AttributeError("User is not defined")

        serializers.raise_errors_on_nested_writes("update", self, data)
        info = model_meta.get_field_info(instance)
        m2m_fields = []
        for attr, value in data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        instance.save(user=user)

        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        return instance
