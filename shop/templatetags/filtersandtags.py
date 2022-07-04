from django import template

register = template.Library()


def total_price(price, quantity):
    return price * quantity


register.filter('total_price', total_price)