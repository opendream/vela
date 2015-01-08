from account.models import User
from ckeditor.widgets import CKEditorWidget
from django import forms
from common.forms import CommonForm
from keyvela.models import KeyVela

class KeyVelaForm(CommonForm):

    class Meta:
        model = KeyVela
    user_leave = forms.ModelChoiceField(required=True, queryset=User.objects.all())
    user_leave.widget.attrs['disabled'] = True
    category = forms.ChoiceField(choices=KeyVela.LEAVE_TYPE_CHOICES)
    time = forms.DecimalField()
    description = forms.CharField(required=False, widget=CKEditorWidget(config_name='minimal'))
    loss_message = forms.CharField(required=False, widget=CKEditorWidget())
