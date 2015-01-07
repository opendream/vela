import json
from django.conf import settings
from django.core.urlresolvers import reverse
from account.forms import EmailAuthenticationForm, AccountRegisterForm, ResetPasswordForm
from common.constants import STATUS_PENDING, STATUS_PUBLISHED, STATUS_DRAFT, STATUS_DELETED, STATUS_REJECTED

def helper(request):

    context = {
        'request_popup': bool(request.GET.get('_popup') or request.POST.get('_popup')),
        'request_inline': bool(request.GET.get('_inline') or request.POST.get('_inline')),
        'request_pagination': request.GET.get('page'),
        'show_modal_login': request.user.is_anonymous() and request.path not in [reverse('account_login')],
        'show_modal_register': request.user.is_anonymous() and request.path not in [reverse('account_register')],
        'show_modal_password_reset': request.user.is_anonymous() and request.path not in [reverse('account_reset_password')],
        'login_form': AccountRegisterForm,
        'password_reset_form': ResetPasswordForm,
        'BASE_URL': request.build_absolute_uri('/')[0:-1],
        'SITE_LOGO_URL': settings.SITE_LOGO_URL,
        'SITE_NAME': settings.SITE_NAME,
        'SITE_SLOGAN': settings.SITE_SLOGAN,
        'SITE_FAVICON_URL': settings.SITE_FAVICON_URL,
        'STATUS_PUBLISHED': STATUS_PUBLISHED,
        'STATUS_PENDING': STATUS_PENDING,
        'STATUS_DRAFT': STATUS_DRAFT,
        'STATUS_DELETED': STATUS_DELETED,
        'STATUS_REJECTED': STATUS_REJECTED,
        'GOOGLE_ANALYTICS_KEY': settings.GOOGLE_ANALYTICS_KEY,
        #'FACEBOOK_APP_ID': settings.FACEBOOK_APP_ID,
        'SITE_URL': settings.SITE_URL,

        'DEBUG': int(settings.DEBUG)
    }

    return context
