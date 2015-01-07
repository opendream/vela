import json
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login as auth_login, get_user_model, update_session_auth_hash, \
    REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import login, password_reset, password_reset_done
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404, resolve_url
from django.template.response import TemplateResponse
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect

from account.forms import EmailAuthenticationForm, ResetPasswordForm, AccountEditForm, InviteForm, AccountRegisterForm
from account.models import User
from common.functions import get_success_message


def account_login(request):
    if request.method == 'POST' and not request.POST.get('remember_me', None): # No unit test
        request.session.set_expiry(0) # No unit test

    if request.user.is_authenticated():
        return redirect('home')

    return login(request, authentication_form=EmailAuthenticationForm,
        template_name='account/login.html')



def account_reset_password(request):
    if request.user.is_authenticated():
        return HttpResponse('access denied', status=403)

    return password_reset(request,
        template_name='account/password_reset_form.html',
        email_template_name='account/email/password_reset_email.html',
        subject_template_name='account/email/password_reset_email_subject.txt',
        password_reset_form=ResetPasswordForm,
        post_reset_redirect=reverse('account_reset_password_done'),
    )


def account_reset_password_done(request):
    return password_reset_done(request,
        template_name='account/password_reset_done.html'
    )


def account_reset_password_confirm(request, uidb64=None, token=None, email_setting=False):
    UserModel = get_user_model()

    try:
        uid_int = urlsafe_base64_decode(uidb64)
        user = UserModel.objects.get(id=uid_int)
    except (ValueError, UserModel.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):

        user.is_active = True
        user.save()

        user_authen = authenticate(username=user.username, ignore_password=True)
        auth_login(request, user_authen)

        if email_setting:
            return redirect(reverse('account_edit') + '##email-notification-settings')

        return redirect(reverse('account_edit') + '?reset_password=True')
    else:
        return HttpResponse('invalid link', status=404)


def account_settings_confirm(request, uidb64=None, token=None):
    return account_reset_password_confirm(request, uidb64, token, email_setting=True)


@login_required
def account_edit(request, people_id=None):
    required_password = request.GET.get('reset_password')

    if people_id and request.user.is_staff:
        user_id = people_id
    elif not people_id:
        user_id = request.user.id
    else:
        user_id = people_id
        #return staff_required(request)


    UserModel = get_user_model()
    user = UserModel.objects.get(id=user_id)

    # Check permission

    if request.method == 'POST':
        form = AccountEditForm(user, UserModel, required_password, request.POST, request.FILES)
        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.description = form.cleaned_data['description']



            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)
                update_session_auth_hash(request, user)

            user.save()





            if people_id:
                message_success = get_success_message(user, False, [])
                messages.success(request, message_success)
                return redirect('people_edit', people_id)
            else:
                messages.success(request, _(
                    'Your account profile have been updated. View your profile page <a href="%s">here</a>') % reverse(
                    'account'))
                #party_activate(request, user.id)
                return redirect('account_edit')

        else:
            messages.error(request, 'Your submission error. Please, check in error fields.')

    else:

        initial = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'description': user.description,

        }
        form = AccountEditForm(user, UserModel, required_password, initial=initial)

    return render(request, 'account/edit.html', {
        'form': form,
        'reset_password': required_password,
    })


@staff_member_required
def account_invite(request):

    if request.GET.get('success'):
        messages.success(request, _('The email invitation has been send.'))
        return redirect('account_invite')

    reeturn = password_reset(request,
        template_name='account/invite_form.html',
        email_template_name='account/email/invite_email.html',
        subject_template_name='account/email/invite_email_subject.txt',
        password_reset_form=InviteForm,
        post_reset_redirect='%s?success=1' % reverse('account_invite'),
    )



@csrf_protect
def inline_password_reset(request, is_admin_site=False,
                   template_name='registration/password_reset_form.html',
                   email_template_name='registration/password_reset_email.html',
                   subject_template_name='registration/password_reset_subject.txt',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   current_app=None,
                   extra_context=None,
                   html_email_template_name=None):
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_done')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
                'html_email_template_name': html_email_template_name,
            }
            if is_admin_site:
                opts = dict(opts, domain_override=request.get_host())
            form.save(**opts)

            field_id = request.POST.get('field_id') or request.GET.get('field_id') or 'id_admins'

            user = get_user_model().objects.get(email=form.cleaned_data['email'])
            return HttpResponseRedirect('%s&user_id=%s&field_id=%s' % (post_reset_redirect, user.id, field_id))
    else:
        form = password_reset_form()
    context = {
        'form': form,
        'title': _('Password reset'),
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)

def account_inline_invite(request):
    if request.GET.get('success'):

        messages.success(request, _('The email invitation has been send.'))
        return render(request, 'account/inline_invite_form.html', {
            'form': InviteForm(),
            'success': True,
            'user_id': request.GET.get('user_id'),
            'field_id': request.POST.get('field_id') or request.GET.get('field_id') or 'id_admins'
        })

    print request.GET.get('field_id') or 'id_admins'

    return inline_password_reset(request,
        template_name='account/inline_invite_form.html',
        email_template_name='account/email/invite_email.html',
        subject_template_name='account/email/invite_email_subject.txt',
        password_reset_form=InviteForm,
        post_reset_redirect='%s?success=1' % reverse('account_inline_invite'),
        extra_context={'field_id': request.POST.get('field_id') or request.GET.get('field_id') or 'id_admins'}
    )



def account_register(request):
    if request.user.is_authenticated():
        return redirect('home')

    if request.GET.get('success'):
        messages.success(request, _('The email register has been send please check your email.'))
        return redirect('account_register')

    return password_reset(request,
        template_name='account/register.html',
        email_template_name='account/email/register_email.html',
        subject_template_name='account/email/register_email_subject.txt',
        password_reset_form=AccountRegisterForm,
        post_reset_redirect='%s?success=1' % reverse('account_register'),
    )

def account_register_confirm(request, uidb64=None, token=None, email_setting=False):

    UserModel = get_user_model()

    try:
        uid_int = urlsafe_base64_decode(uidb64)
        user = UserModel.objects.get(id=uid_int)
    except (ValueError, UserModel.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):

        user.is_active = True
        user.save()

        user_authen = authenticate(username=user.username, ignore_password=True)
        auth_login(request, user_authen)
        return redirect(reverse('account_edit') + '?reset_password=True')
    else:
        return HttpResponse('invalid link', status=404)


def account_logout(request, next_page=None,
                   template_name='registration/logged_out.html',
                   redirect_field_name=REDIRECT_FIELD_NAME,
                   current_app=None, extra_context=None):

    from django.contrib.auth.views import logout

    return logout(request, next_page=next_page, template_name=template_name, redirect_field_name=redirect_field_name,
                            current_app=current_app, extra_context=extra_context
    )


# =========================================================
# People (public pages)
# =========================================================



def account_detail(request):
    if request.user.is_authenticated():
        user = request.user
    else:
        return redirect('account_login')

    return people_detail(request, user.username)

def people_detail(request, username, people_id=None):

    # For user type name from url
    if not people_id:
        people = get_object_or_404(User, username=username)
        return redirect('people_detail', username, people.id)
    people = get_object_or_404(User, id=people_id)

    params_query = people.skills.replace(',', '+')
    params_query = params_query.replace(' ', '')
    interests = people.interests.all()
    for interest in interests:
        params_query += '+' + interest.title
    print params_query
    return render(request, 'account/detail.html', {
        'username': username,
        'people_id': people_id,
        'params_query': params_query
    })

