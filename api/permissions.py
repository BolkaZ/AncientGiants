import redis
from rest_framework  import permissions, exceptions
from paleo_project import settings
from app.models import *

redis = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

class IsModeratorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method != "GET":
            user = get_user_or_none(request)
            print(user)
            if not user:
                raise exceptions.PermissionDenied(detail="Ты не авторизовался!")
            elif not user.is_superuser:
                raise exceptions.PermissionDenied(detail="Ты не модератор!")
            else:
                return True
        else:
            return True


class IsCreator(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        user = get_user_or_none(request)
        if str(obj.session_id) != str(user.id):
            raise exceptions.PermissionDenied(detail="Ты не создатель!")
        else:
            return True
        
class IsAuth(permissions.BasePermission):

     def has_permission(self, request, view):
        user = get_user_or_none(request)
        if not user:
            raise exceptions.PermissionDenied(detail="Ты не авторизовался!")
        else:
            return True
        
class IsModerator(permissions.BasePermission):

     def has_permission(self, request, view):
        user = get_user_or_none(request)
        if not user:
            raise exceptions.PermissionDenied(detail="Ты не авторизовался!")
        elif not user.is_superuser:
            raise exceptions.PermissionDenied(detail="Ты не модератор!")
        else:
            return True


class IsCreatorOrModerator(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        user = get_user_or_none(request)
        if not user:
            raise exceptions.PermissionDenied(detail="Ты не авторизовался!")
        if not user.is_superuser and str(obj.session_id) != str(user.id):
            raise exceptions.PermissionDenied(detail="Ты не создатель и не модератор!")
        else:
            return True
        

    
def get_user_or_none(request):
    user = None
    session_id = request.COOKIES.get("session_id") or request.headers.get("session_id")
    print(request.headers.get("session_id"))
    print(request.COOKIES.get("session_id"))
    print(request.headers)
    if session_id:
        user_id = redis.get(session_id)
        user = User.objects.filter(id=user_id).first()
    
    return user