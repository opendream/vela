from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.core.urlresolvers import resolve

from django.utils.decorators import decorator_from_middleware_with_args
from django.middleware.cache import CacheMiddleware

from common.models import StatisitcAccess

from functools import wraps


def statistic(view_func=None):

    def _decorator(request, *args, **kwargs):

        content_type = ''.join([c.title() for c in view_func.__name__.split('_')[0:-1]])

        content_type = ContentType.objects.get_by_natural_key(resolve(request.path).app_name, content_type.lower())
        content_type_id_key = request.resolver_match.kwargs.keys()

        if len(content_type_id_key):
            for k in content_type_id_key:
                if content_type.name.lower() in k:
                    content_type_id_key = k

            if type(content_type_id_key) == list:
                content_type_id_key = content_type_id_key[0]

        else:
            return view_func(request, *args, **kwargs)

        object_id = request.resolver_match.kwargs[content_type_id_key]

        if 'permalink' in content_type_id_key:
            object_id = content_type.model_class().objects.get(permalink=object_id).id


        StatisitcAccess.objects.create(content_type=content_type, object_id=object_id)
        response = view_func(request, *args, **kwargs)

        return response

    return wraps(view_func)(_decorator)


def scache(view_func=None):

    def _decorator(request, *args, **kwargs):

        path = request.get_full_path()
        user_id = request.user.id or 0

        key = '%s--%s' % (user_id, path)

        print key

        response = cache.get(key)
        if response is not None:
            print 'CACHE HIT'
            return response

        response = view_func(request, *args, **kwargs)
        cache.set(key, response, None)

        return response


    return wraps(view_func)(_decorator)



