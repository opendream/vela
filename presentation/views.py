from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models.loading import get_model
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _



@login_required
def presentation_delete(request, app_label, model_name, id):

    ModelClass = get_model(app_label=app_label, model_name=model_name)
    instance = get_object_or_404(ModelClass, id=id)

    # Check permission
    instance.delete()

    model_name_display = model_name
    if hasattr(ModelClass, 'REQUEST_VERB_DISPLAY'):
        model_name_display = ModelClass.REQUEST_VERB_DISPLAY.lower()

    messages.success(request, _('Your %s have been deleted.') % model_name_display)


    if request.GET.get('next'):
        if request.GET.get('next') == '.':
            next = request.META.get('HTTP_REFERER', '/')
        else:
            next = request.GET.get('next')
    else:
        next = reverse('home')

    return HttpResponseRedirect(next)




# =============================
# Home
# =============================

def home(request):

    return render(request, 'presentation/home.html')

def handler403(request):
    return render(request, '403.html')

