from django import template
register = template.Library()

@register.filter
def ru_pluralize(value, endings):
    try:
        endings = endings.split(',')
        value = int(value)
        if value % 100 in (11, 12, 13, 14):
            return endings[2]
        if value % 10 == 1:
            return endings[0]
        if value % 10 in (2, 3, 4):
            return endings[1]
        return endings[2]
    except:
        return endings[2]