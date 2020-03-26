from rest_framework import serializers
from event_api.models import Event, Task


class EventSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True)
    event_name = serializers.CharField(max_length=100)
    date = serializers.DateTimeField(required=True)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        print(validated_data)
        return Event.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.event_name = validated_data.get('event_name', instance.event_name)
        instance.date = validated_data.get('date', instance.date)
        instance.save()
        return instance


class TaskSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True)
    task_name = serializers.CharField(max_length=100)
    date = serializers.DateTimeField(required=False)
    is_done = serializers.BooleanField(default=False)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.task_name = validated_data.get('task_name', instance.task_name)
        instance.date = validated_data.get('date', instance.date)
        instance.is_done = validated_data.get('is_done', instance.is_done)
        instance.save()
        return instance