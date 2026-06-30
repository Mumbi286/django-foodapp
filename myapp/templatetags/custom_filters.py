# creating our own custome file 
from django import template

register = template.Library()

@register.filter
def currency(value):
    return f"${value}"


# python function to calculate the discount
@register.filter
def discount(value,percentage):
    return int(value) - (int(value) * (int(percentage)/100))