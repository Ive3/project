from multiprocessing import context
from .models import SubCategory, SuperCategory, About
from .cart import Cart


def categories_context(request):
    context = dict()
    context['categories'] = SubCategory.objects.all()
    context['cats'] = SuperCategory.objects.all()
    return context


def cart_context(request):
    context = dict()
    context['cart'] = Cart(request)
    return context


def contact(request):
    context = dict()
    about = About.objects.filter(show=True)
    if about:
        context['contact'] = about
    return context