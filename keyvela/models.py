from django.db import models

# Create your models here.
from ckeditor.fields import RichTextField
from django.conf import settings
from common.models import CommonModel

USER_MODEL = settings.AUTH_USER_MODEL
class KeyVela(CommonModel):

    user_leave = models.ForeignKey(USER_MODEL, related_name='keyvela_user_leave')
    LEAVE_TYPE_CHOICES = (
        ('leave', 'Leave'),
        ('vacation', 'Vacation'),
        ('sick', 'Sick'),
    )
    category = models.CharField(max_length=255, choices=LEAVE_TYPE_CHOICES, default='news')

    time = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
    )
    description = RichTextField(null=True, blank=True, config_name='minimal')
    loss_message = RichTextField(null=True, blank=True, config_name='minimal')
    created_by = models.ForeignKey(USER_MODEL, related_name='keyvela_created_by')
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    changed = models.DateTimeField(auto_now_add=True, null=True, blank=True)
