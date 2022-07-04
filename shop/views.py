from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import View, TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.
from .models import ExtraImage, Order, Product, SubCategory, SuperCategory, IpModel, IpCategory, About, Carousel
from .forms import CartAddForm, AddProductForm, ExtraImageForm
from .cart import Cart


# fist shop page -------------------------------------------
def shop(request):
    about = About.objects.get(show=True)
    carousel = about.carousel_set.all()
    products = Product.objects.order_by('-created_at')[:6]
    products_viewed = Product.objects.order_by('-views')[:4]
    cats_viewed = SubCategory.objects.order_by('-views')[:6]
    context = {'products': products,
               'products_viewed': products_viewed, 'cats_viewed': cats_viewed, 'about':about, 'carousel':carousel}
    return render(request, 'shop/shop.html', context)


# list products --------------------------------
class ProductView(ListView):
    paginate_by = 8
    model = Product
    template_name = 'shop/shop_products.html'
    context_object_name = 'products'

# product detail --------------------------------


def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    same_products = Product.objects.filter(name__icontains=product.name.split()[0])[:6]
    product_name = product.name.split()[0]
    author_products = Product.objects.filter(author=product.author)[:6]
    eis = product.extraimage_set.all()
    cart_form = CartAddForm()

    ip = get_ip(request)
    s = slug
    results = IpModel.objects.filter(ip=ip, product=s)
    if results.exists():
        print(results)
    else:
        IpModel.objects.create(ip=ip, product=s)
        product.views = product.views + 1
        product.save()
        print('user is unique', results)

    context = {'product': product, 'eis': eis, 'cart_form': cart_form,
               'same_products': same_products, 'p': product_name, 'author_products': author_products}
    return render(request, 'shop/shop_detail.html', context)


# categories page -------------------------------------
class CategoriesView(ListView):
    model = SuperCategory
    template_name = 'shop/shop_categories.html'
    context_object_name = 'cats'


# Subcategories page -------------------------------------
def sub_categories(request, pk):
    current_super_category = SuperCategory.objects.get(pk=pk)
    sub_categories = SubCategory.objects.filter(sup_category=pk)
    context = {'current_super_category': current_super_category,
               'sub_categories': sub_categories}
    return render(request, 'shop/shop_sub_categories.html', context)


# by_subcategories page -------------------------------------
def by_category(request, pk):
    products = Product.objects.filter(category=pk)
    current_cat = SubCategory.objects.get(pk=pk)
    paginator = Paginator(products, 8)

    if 'page' in request.GET:
        page_num = request.GET.get('page')
    else:
        page_num = 1
    page_obj = paginator.get_page(page_num)

    ip = get_ip(request)
    s = pk
    results = IpCategory.objects.filter(ip=ip, sub_categories=s)
    if results.exists():
        print(results)
    else:
        IpCategory.objects.create(ip=ip, sub_categories=s)
        current_cat.views = current_cat.views + 1
        current_cat.save()
        print('user is unique', results)

    context = {'products': page_obj.object_list,
               'current_cat': current_cat, 'page_obj': page_obj}
    return render(request, 'shop/shop_by_category.html', context)


# add cart ----------------------------------------------
@require_POST
def add_cart(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=pk)
    form = CartAddForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('shop:cart_detail')


def remove_cart(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=pk)
    cart.remove(product)
    messages.success(request, 'Product has removed')
    return redirect('shop:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['form'] = CartAddForm(
            initial={'quantity': item['quantity'], 'update': True})
    context = {'cart': cart}
    return render(request, 'shop/shop_cart.html', context)
# end card ------------------------------------------------


# Get user ip --------------------------------------------------------------------------
def get_ip(request):
    address = request.META.get('HTTP_X_FORWARDED_FOR')
    if address:
        ip = address.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# Check out ------------------------------------------------------
class CartOrder(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        cart = request.session.get('cart')
        products = Product.objects.filter(pk__in=list(cart.keys()))
        for product in products:
            order = Order(
                product=Product.objects.get(pk=product.pk),
                customer=product.author,
                price=product.price,
                address=address,
                phone=phone,
                quantity=cart[str(product.id)]['quantity'],
            )
            order.place_order()
            request.session['cart'] = dict()
        messages.success(request, 'Your order has sent.')
        return redirect('shop:order_list')


# Order page ----------------------------------------
class OrderView(View):
    def get(self, request):
        customer = request.user.id
        orders = Order.customer_orders(customer)
        qs = []
        qp = []
        for s in orders:
            qs.append(s.quantity)
            q = s.quantity
            p = s.price
            qp.append(q*p)
        qs = sum(qs)
        qp = sum(qp)
        context = {'orders': orders, 'total_q': qs, 'total_p': qp}
        return render(request, 'shop/shop_order.html', context)


# shear list ---------------------------------------------------------
class Search(View):
    def get(self, request):
        keyword = request.GET.get('search')
        products = Product.objects.filter(name__icontains=keyword)
        paginator = Paginator(products, 4)
        if 'page' in request.GET:
            page_num = request.GET.get('page')
        else:
            page_num = 1
        page_obj = paginator.get_page(page_num)
        context = {'keyword': keyword,
                   'products': page_obj.object_list, 'page_obj': page_obj}
        return render(request, 'shop/shop_search_list.html', context)


# Add Product Form ----------------------------------------------
def add_product(request):
    form = AddProductForm()
    formset = ExtraImageForm()
    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            formset = ExtraImageForm(
                request.POST, request.FILES, instance=product)
            if formset.is_valid():
                formset.save()
                messages.success(
                    request, 'The product has added successfully!')
                return redirect('shop:add_product')
        else:
            messages.warning(request, 'The product has not added try again!')

    else:
        form = AddProductForm(initial={'author': request.user.pk})
        formset = ExtraImageForm()
    context = {'form': form, 'formset': formset}
    return render(request, 'shop/shop_add_product.html', context)


# products by author-------------------------------------------------------------
def author_product(request, pk):
    products = Product.objects.filter(author=pk)
    paginator = Paginator(products, 4)
    if 'page' in request.GET:
        page_num = request.GET.get('page')
    else:
        page_num = 1
    page_obj = paginator.get_page(page_num)
    context = {'products': page_obj.object_list, 'page_obj': page_obj}
    return render(request, 'shop/author_products.html', context)


# user products --------------------------------------------------
class UserProductsView(ListView):
    paginate_by = 8
    template_name = 'shop/shop_user.html'
    context_object_name = 'products'

    def get_queryset(self):
        products = Product.objects.filter(author=self.request.user.pk)
        return products

# user detail product --------------------------------------------------
class UserDetailProductView(DetailView):
    template_name = 'shop/shop_user_detail_product.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = DetailView.get_context_data(self, **kwargs)
        eis = self.product.extraimage_set.all()
        context['eis'] = eis
        return context

    def setup(self, request, *args, **kwargs):
        self.pk = kwargs['pk']
        return super().setup(request, *args, **kwargs)

    def get_object(self):
        self.product = Product.objects.get(pk=self.pk)
        return self.product


# update user product --------------------------------------------------
def update_user_product(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            formset = ExtraImageForm(
                request.POST, request.FILES, instance=product)
            if formset.is_valid():
                formset.save()
                messages.success(
                    request, 'The product has updated successfully!')
                return HttpResponseRedirect(reverse('shop:user_detail_product', kwargs={'pk': pk}))
        else:
            messages.warning(request, 'The product has not updated try again!')
    else:
        form = AddProductForm(instance=product)
        formset = ExtraImageForm(instance=product)
    context = {'form': form, 'formset': formset}
    return render(request, 'shop/user_update_product.html', context)


# update user product --------------------------------------------------
class DelUserProductView(DeleteView):
    template_name = 'shop/user_del_product.html'
    context_object_name = 'product'
    success_message = "Product has removed successfully"

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        success_url = reverse_lazy('shop:user_products', kwargs={
                                   'pk': self.request.user.pk})
        return success_url

    def get_context_data(self, **kwargs):
        context = DeleteView.get_context_data(self, **kwargs)
        eis = self.product.extraimage_set.all()
        context['eis'] = eis
        return context

    def setup(self, request, *args, **kwargs):
        self.pk = kwargs['pk']
        return super().setup(request, *args, **kwargs)

    def get_object(self):
        self.product = Product.objects.get(pk=self.pk)
        return self.product

# most viewed products -------------------------------------------------------------


def viewed_product(request):
    products = Product.objects.order_by('-views')
    paginator = Paginator(products, 8)
    if 'page' in request.GET:
        page_num = request.GET.get('page')
    else:
        page_num = 1
    page_obj = paginator.get_page(page_num)
    context = {'products': page_obj.object_list, 'page_obj': page_obj}
    return render(request, 'shop/shop_viewed_products.html', context)


# most viewed categories -------------------------------------------------------------
def viewed_category(request):
    categories = SubCategory.objects.order_by('-views')
    context = {'cats_viewed': categories}
    return render(request, 'shop/shop_viewed_categories.html', context)


# filtered products -------------------------------------------------------------
def filter_product(request):
    hp = request.GET.get('high_price')
    lp = request.GET.get('low_price')
    nw = request.GET.get('new')
    vs = request.GET.get('viewed')
    context = {}
    print(request.GET)
    if hp:
        products = Product.objects.order_by('-price')
        context['high_price'] = hp
    if lp:
        products = Product.objects.order_by('price')
        context['low_price'] = lp
    if nw:
        products = Product.objects.order_by('-created_at')
        context['new'] = nw
    if vs:
        products = Product.objects.order_by('-views')
        context['viewed'] = vs

    paginator = Paginator(products, 4)
    if 'page' in request.GET:
        page_num = request.GET.get('page')
    else:
        page_num = 1
    page_obj = paginator.get_page(page_num)
    context['products'] = page_obj.object_list
    context['page_obj'] = page_obj
    return render(request, 'shop/shop_filter.html', context)


# About shop ---------------------------------------------------------
class AboutView(TemplateView):
    template_name = 'shop/shop_about.html'

    def get_context_data(self, *args, **kwargs):
        context = TemplateView.get_context_data(self, kwargs=kwargs)
        about = About.objects.get(show=True)
        if about:
            context['about'] = about
        return context
