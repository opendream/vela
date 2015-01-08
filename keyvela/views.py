from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
# Create your views here.
from common.functions import get_success_message
from keyvela.form import KeyVelaForm
from keyvela.models import KeyVela

@login_required
def keyvela_create(request, instance=None):

    # Config for reuse
    ModelClass = KeyVela
    instance = instance or ModelClass()

    form = KeyVelaForm(instance, ModelClass, request.POST)
    is_new = form.is_new()
    if request.method == 'POST':

        form = KeyVelaForm(instance, ModelClass, request.POST)

        is_new = form.is_new()

        if form.is_valid():

            # Relation
            if not instance.created_by_id:
                instance.created_by = request.user
            instance.user_leave = form.cleaned_data['user_leave']
            instance.category = form.cleaned_data['category']
            instance.time = form.cleaned_data['time']
            instance.description = form.cleaned_data['description']
            instance.loss_message = form.cleaned_data['loss_message']

            instance.changed = timezone.now()

            instance.save()

            message_success = get_success_message(instance, is_new, [])
            messages.success(request, message_success)
            return redirect('keyvela_edit', instance.id)
        else:
            messages.error(request, 'Your submission error. Please, check in error fields.')

    else:
        initial = {
            'category': instance.category,
            'time': instance.time,
            'description': instance.description,
            'loss_message': instance.loss_message,
        }

        if instance.id:
            initial['user_leave'] = instance.user_leave

        form = KeyVelaForm(instance, ModelClass, initial=initial)
    return render(request, 'keyvela/form.html', {'form': form})

def keyvela_detail(request, keyvela_id):
    # Todo redirect if no keyvela_id
    return render(request, 'keyvela/detail.html',{
        'keyvela_id': keyvela_id,
    })
def keyvela_edit(request, keyvela_id=None):

    keyvela = get_object_or_404(KeyVela, id=keyvela_id)



    return keyvela_create(request, keyvela)
