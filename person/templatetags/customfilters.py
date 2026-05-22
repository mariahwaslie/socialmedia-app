from django import template

register = template.Library()

@register.filter
def unique_values(queryset, attribute):
    seen = set()
    unique_items = []
    for item in queryset:
        value = getattr(item, attribute, None)
        if value not in seen:
            unique_items.append(item)
            seen.add(value)
    return unique_items
