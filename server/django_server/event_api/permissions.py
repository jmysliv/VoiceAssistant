from rest_framework import permissions


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        return obj.username == request.user


class IsReceiver(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        return obj.receiver == request.user.username
