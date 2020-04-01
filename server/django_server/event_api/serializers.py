from rest_framework import serializers
from event_api.models import Event, Task, Message
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'username', 'password']


class EventSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='username.username')

    class Meta:
       model = Event
       fields = ['username', 'event_name', 'date', 'id']

    def create(self, validated_data):

        return Event.objects.create(**validated_data)

    def update(self, instance, validated_data):

       instance.event_name = validated_data.get('event_name', instance.event_name)
       instance.date = validated_data.get('date', instance.date)
       instance.save()
       return instance


class TaskSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='username.username')

    class Meta:
        model = Task
        fields = ['username', 'task_name', 'date', 'is_done', 'id']

    def create(self, validated_data):

        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.task_name = validated_data.get('task_name', instance.task_name)
        instance.date = validated_data.get('date', instance.date)
        instance.is_done = validated_data.get('is_done', instance.is_done)
        instance.save()
        return instance


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.username')

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'date', 'is_read', 'id', 'content']

    def create(self, validated_data):

        return Message.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.is_read = validated_data.get('is_read', instance.is_read)
        instance.save()
        return instance
