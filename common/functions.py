import random
import shutil
import datetime
from django.conf import settings
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login
from django.core.urlresolvers import reverse
from django.template import loader, Context
from django.utils.translation import ugettext_lazy as _


from django import template
from django.utils.safestring import mark_safe
from django.utils.text import normalize_newlines, slugify
from django.template.loader_tags import BlockNode, ExtendsNode
from common.constants import STATUS_PUBLISHED, STATUS_PENDING

import os
import re
import urllib

register = template.Library()

def camelcase_to_underscore(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def underscore_to_camelcase(name):
    return ''.join([c.title() for c in name.split('_')])

def remove_newlines(text):
    """
    Removes all newline characters from a block of text.
    """
    # First normalize the newlines using Django's nifty utility
    normalized_text = normalize_newlines(text)
    # Then simply remove the newlines like so.
    return mark_safe(normalized_text.replace('\n', ' '))

def process_status(user, status, default=False):

    if default:
        return STATUS_PUBLISHED if user.is_staff else STATUS_PENDING

    status = int(status)
    if not user.is_staff and status == STATUS_PUBLISHED:
        status = STATUS_PENDING

    return status

def get_success_message(inst=False, is_new=False, args=[]):

    if not inst:
        return _('Complete created')


    inst_name = inst.inst_name.lower()
    if hasattr(inst, 'permalink'):
        args.append(inst.permalink)
    elif hasattr(inst, 'username'):
        args.append(inst.username)

    args.append(inst.id)

    if is_new:
        return  _('New %s have been created. View this %s <a href="%s">here</a>.') % (
            _(inst_name),
            _(inst_name),
            reverse('%s_detail' % inst_name, args=args)
        )
    else:
        return _('Your %s settings have been updated. View this %s <a href="%s">here</a>.') % (
            _(inst_name),
            _(inst_name),
            reverse('%s_detail' % inst_name, args=args)
        )

def get_template(template):
    if isinstance(template, (tuple, list)):
        return loader.select_template(template)
    return loader.get_template(template)


class BlockNotFound(Exception):
    pass


def render_template_block(template, block, context):
    """
    Renders a single block from a template. This template should have previously been rendered.
    """
    return render_template_block_nodelist(template.nodelist, block, context)


def render_template_block_nodelist(nodelist, block, context):
    for node in nodelist:
        if isinstance(node, BlockNode) and node.name == block:
            return node.render(context)
        for key in ('nodelist', 'nodelist_true', 'nodelist_false'):
            if hasattr(node, key):
                try:
                    return render_template_block_nodelist(getattr(node, key), block, context)
                except:
                    pass
    for node in nodelist:
        if isinstance(node, ExtendsNode):
            try:
                return render_template_block(node.get_parent(context), block, context)
            except BlockNotFound:
                pass
    raise BlockNotFound


def render_block_to_string(template_name, block, dictionary=None, context_instance=None):
    """
    Loads the given template_name and renders the given block with the given dictionary as
    context. Returns a string.
    """
    dictionary = dictionary or {}
    t = get_template(template_name)
    if context_instance:
        context_instance.update(dictionary)
    else:
        context_instance = Context(dictionary)
    t.render(context_instance)
    return render_template_block(t, block, context_instance)

def staff_required(request):
    defaults = {
        'template_name': 'admin/login.html',
        'authentication_form': AdminAuthenticationForm,
        'extra_context': {
            'title': _('Log in'),
            'app_path': request.get_full_path(),
            REDIRECT_FIELD_NAME: request.get_full_path(),
        },
    }
    return login(request, **defaults)

def instance_set_permalink(instance, title, field_name='permalink'):
    ModelClass = instance.__class__

    permalink = slugify(title)

    increment_number = 1

    while True:
        try:
            ModelClass.objects.get(**{field_name: permalink})
        except ModelClass.DoesNotExist:
            setattr(instance, field_name, permalink)
            break

        permalink = "%s-%s" % (permalink, increment_number)
        increment_number = increment_number + 1


def generate_year_range(prev_years=30, choices=False, required=False, empty_label='Year', next_years=None):
    this_year = datetime.date.today().year
    if next_years:
        this_year += next_years
    years = range(this_year - prev_years, this_year)
    years.reverse()

    if choices:
        years = zip(years, years)

        if not required:
            years.insert(0, (None, empty_label))

    return years
