'''
@register.simple_tag
def field(*args, **kwargs):
    tpl = get_template(kwargs.get('template', "forms/field.html"))
    width = 12 / len(args)
    fields = []
    for field in args:
        label  = "forms/label.html"
        hlp    = "forms/help.html"
        errors = "forms/errors.html"
        if isinstance(field.field.widget, forms.CheckboxInput):
            fields.append((field, width, None, hlp, errors, True))
        else:
            fields.append((field, width, label, hlp, errors, False))

    return tpl.render(context={
        'fields': fields,
        'cr_inline': kwargs.get('inline', False)})
'''