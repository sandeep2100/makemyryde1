from django import template

register = template.Library()

@register.filter
def get_city_name(value):
    # Split the value by comma and get the first part (city name)
    return value.split(',')[0].strip()