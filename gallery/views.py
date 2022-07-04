from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
# Create your views here.
from .models import Picture, IpModel
from .forms import PictureForm


class MainPageView(TemplateView):
    template_name = 'gallery/gallery.html'


class GalleryList2DView(ListView):
    paginate_by = 8
    template_name = 'gallery/gallery_cards.html'
    queryset = Picture.objects.filter(image_type='2D')
    context_object_name = 'pictures'


class GalleryList3DView(ListView):
    paginate_by = 8
    template_name = 'gallery/gallery_cards.html'
    context_object_name = 'pictures'
    queryset = Picture.objects.filter(image_type='3D')


class GalleryDetailView(TemplateView):
    template_name = 'gallery/gallery_detail.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        picture = Picture.objects.get(pk=kwargs['pk'])
        if picture.image_type == '3D':
            context['recently'] = Picture.objects.filter(image_type='3D').order_by('-created_at')[:4]
            context['most_viewed'] = Picture.objects.filter(image_type='3D').order_by('-views')[:4]
        else:
            context['recently'] = Picture.objects.filter(image_type='2D').order_by('-created_at')[:4]
            context['most_viewed'] = Picture.objects.filter(image_type='2D').order_by('-views')[:4]
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        picture = Picture.objects.get(pk=kwargs['pk'])
        ip = get_ip(request)
        p = kwargs['pk']
        results = IpModel.objects.filter(ip=ip, picture=p)
        if results.exists():
            pass
        else:
            IpModel.objects.create(ip=ip, picture=p)
            picture.views = picture.views + 1
            picture.save()
        context['picture'] = picture
        return self.render_to_response(context)


# Get user ip for count view--------------------------------------------------------------------------
def get_ip(request):
    address = request.META.get('HTTP_X_FORWARDED_FOR')
    if address:
        ip = address.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class GalleryByTagsView(ListView):
    paginate_by = 8
    template_name = 'gallery/gallery_cards.html'
    context_object_name = 'pictures'

    def get_queryset(self):
        pictures = Picture.objects.filter(tags=self.kwargs.get('pk'))
        return pictures


class GallerySearchView(ListView):
    paginate_by = 8
    template_name = 'gallery/gallery_cards.html'
    context_object_name = 'pictures'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['keyword'] = self.request.GET.get('search')
        return context

    def get_queryset(self):
        keyword = self.request.GET.get('search')
        q = Q(name__icontains=keyword) | Q(tags__name__icontains=keyword)
        pictures = Picture.objects.filter(q)
        return pictures


@login_required()
def profile_gallery(request, pk):
    if request.GET.get('2d'):
        pictures = Picture.objects.filter(author=request.user.pk, image_type="2D")
    elif request.GET.get('3d'):
        pictures = Picture.objects.filter(author=request.user.pk, image_type="3D")   
    else:
        pictures = Picture.objects.filter(author=request.user.pk)
    paginator = Paginator(pictures, 8)
    if 'page' in request.GET:
        page_num = request.GET.get('page')
    else:
        page_num = 1
    page_obj = paginator.get_page(page_num)

    context = {'pictures': page_obj.object_list, 'page_obj': page_obj}
    return render(request, 'gallery/gallery_profile.html', context)



@login_required()
def detail_author_gallery(request, pk):
    picture = Picture.objects.get(pk=pk)
    context = {'picture': picture}
    if picture.image_type == '3D':
        context['recently'] = Picture.objects.filter(image_type='3D', author=request.user.pk).order_by('-created_at')[:4]
        context['most_viewed'] = Picture.objects.filter(image_type='3D', author=request.user.pk).order_by('-views')[:4]
    else:
        context['recently'] = Picture.objects.filter(image_type='2D', author=request.user.pk).order_by('-created_at')[:4]
        context['most_viewed'] = Picture.objects.filter(image_type='2D', author=request.user.pk).order_by('-views')[:4]
    return render(request, 'gallery/gallery_profile_detail.html', context)
    

@login_required()
def add_gallery(request):
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Picture has added')
            return HttpResponseRedirect(reverse('gallery:add_picture'))
        else:
            messages.warning(request, 'Picture has not added try again')
    else:
        form = PictureForm(initial={'author': request.user.pk})
    context = {'form': form}
    return render(request, 'gallery/gallery_profile_add.html', context)


@login_required()
def update_gallery(request, pk):
    picture = Picture.objects.get(pk=pk)
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES, instance=picture)
        if form.is_valid():
            form.save()
            messages.success(request, 'Picture has updated')
            return HttpResponseRedirect(reverse('gallery:detail_author_gallery', kwargs={'pk': picture.pk}))
    else:
        form = PictureForm(instance=picture)
    context = {'form': form}
    return render(request, 'gallery/gallery_update.html', context)  


@login_required()
def delete_picture(request, pk):
    picture = Picture.objects.get(pk=pk)
    if request.method == 'POST':
        picture.delete()
        messages.success(request, 'Picture has deleted')
        return HttpResponseRedirect(reverse('gallery:author_gallery', kwargs={'pk': request.user.pk}))
    else:
        context = {'picture': picture}
        return render(request, 'gallery/gallery_profile_delete_picture.html', context)  