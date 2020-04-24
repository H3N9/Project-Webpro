import six
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test


def group_required(group, login_url=None, raise_exception=False):
    def check_perms(user):
        if isinstance(group, six.string_types):
            groups = (group, )
        else:
            groups = group

        if user.groups.filter(name__in=groups).exists() or user.is_superuser:
            return True
            
        if raise_exception:
            raise PermissionDenied
        
        return False
    return user_passes_test(check_perms, login_url=login_url)