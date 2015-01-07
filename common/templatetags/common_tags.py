from django import template
from django.template.loader import render_to_string


register = template.Library()

@register.tag(name='captureas')
def do_captureas(parser, token):
    try:
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("'captureas' node requires a variable name.")
    nodelist = parser.parse(('endcaptureas',))
    parser.delete_first_token()
    return CaptureasNode(nodelist, args)


class CaptureasNode(template.Node):
    def __init__(self, nodelist, varname):
        self.nodelist = nodelist
        self.varname = varname

    def render(self, context):
        output = self.nodelist.render(context)
        context[self.varname] = output  
        return ''


@register.simple_tag(name='render_formset')
def render_formset(field_formset, field_formset_id, field_formset_title, fixed=False):

    for field_form in field_formset:

        show_delete = False

        for field in field_form:
            if field.value():
                show_delete = True
                break

        if not show_delete:
            field_form['DELETE'].field.widget.attrs['class'] = 'hidden'



    return render_to_string('formset.html', {
        'field_formset': field_formset,
        'field_formset_id': field_formset_id,
        'field_formset_title': field_formset_title,
        'fixed': fixed
    })


@register.filter()
def to_int(value):
    return int(value)