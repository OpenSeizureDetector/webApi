from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    only the owner of an object or an admin user can view and edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Only the owner can use it.
        hasPermission = obj.user == request.user or request.user.is_superuser
        print("IsOwnerOrAdmin:  owner = "+str(obj.user)+", request="+str(request.user)+": Admin="+str(request.user.is_superuser)+" : haspermission="+str(hasPermission))
        return hasPermission


class IsOwnerOrStaff(permissions.BasePermission):
    """
    only the owner of an object, staff or admin user can view and edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Only the owner can use it.
        hasPermission = obj.user == request.user or request.user.is_superuser or request.user.is_staff
        print("IsOwnerOrAdmin:  owner = "+str(obj.user)+", request="+str(request.user)+": Admin="+str(request.user.is_superuser)+", Staff="+str(request.user.is_staff)+" : haspermission="+str(hasPermission))
        return hasPermission
