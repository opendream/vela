import re

from ckeditor.fields import RichTextField
from django.core import validators
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from common.models import PriorityModel



class AbstractPeopleField(models.Model):

    # Internal
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)

    description = RichTextField(null=True, blank=True)


    class Meta:
        abstract = True

    def get_full_name(self):
        try:
            full_name = '%s %s' % (self.first_name or '', self.last_name or '')
            return full_name.strip()
        except:
            return ''

    def get_short_name(self):
        output = ''
        try:
            if self.first_name.strip() and self.last_name.strip():
                output = '%s.%s' % (self.first_name.strip(), self.last_name.strip()[0])

            elif self.first_name.strip():
                output = self.first_name.strip()

            elif self.last_name.strip():
                output = self.last_name.strip()

            output = ''
        except:
            output = ''

        if not output:
            output = self.username

        return output

    def get_display_name(self, allow_email=False):
        if allow_email:
            return self.get_full_name() or self.email or self.username

        return self.get_full_name() or self.username


    def __unicode__(self):
        return self.get_full_name()



class User(AbstractPeopleField, AbstractBaseUser, PermissionsMixin, PriorityModel):


    username = models.CharField(_('username'), max_length=30, unique=True,
        help_text=_('Required 30 characters or fewer. Letters, numbers and @/./+/-/_ characters'),
        validators=[
            validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'), 'invalid')
        ])

    email = models.EmailField(
        verbose_name=_('email address'),
        max_length=255,
        unique=True,
    )
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    # Deprecated

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    @property
    def inst_name(self):
        return 'people'
