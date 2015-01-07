from django.utils.translation import ugettext_lazy as _

STATUS_PUBLISHED = 1
STATUS_PENDING = -1
STATUS_DRAFT = 0
STATUS_DELETED = -2
STATUS_REJECTED = -3

STATUS_CHOICES = (
    (STATUS_PUBLISHED, _('Published')),
    (STATUS_PENDING, _('Request for Approval')),
    (STATUS_DRAFT, _('Draft')),
)

NO_IP = '127.0.0.1'

SHORT_UUID_ALPHABETS = '23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

SUMMARY_MAX_LENGTH = 80