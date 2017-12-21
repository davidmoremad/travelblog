from django import template

register = template.Library()

@register.filter
def price_color(price):
    if price >= '500': return 'warning'
    elif price <= '300': return 'success'
    else: return None

@register.filter
def score_color(score):
    if score < 5: return 'warning'
    elif score > 8: return 'success'
    else: return None
