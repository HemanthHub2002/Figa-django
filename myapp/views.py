from django.shortcuts import render

from .models import CarouselImage
from products.models import Product

# Create your views here.

def homeView(request):
    template = 'mainapp/home.html'
    context  = {
        'current_page' : 'home',

        # Let's collect all existing records of carousel image table to be sent to template
        'carousel_images': CarouselImage.objects
            .filter(active=True)
            .order_by('id'),
            
        'products' : Product.objects.all()
    }

    return render(request, template_name= template, context= context)


    

def aboutView(request):
    template = 'mainapp/about.html'
    context = {
        'current_page' : 'about'
    }
    return render(request, template, context)


def contactView(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Later you can save to DB or send email
        print(name, email, message)

    return render(request, "mainapp/contact.html")


from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import CarouselImage


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class CarouselImageListView(StaffRequiredMixin, ListView):
    model = CarouselImage
    template_name = 'mainapp/carousel_list.html'
    context_object_name = 'images'

class CarouselImageCreateView(StaffRequiredMixin, CreateView):
    model = CarouselImage
    fields = '__all__'
    template_name = 'mainapp/carousel_form.html'
    success_url = reverse_lazy('carousel_list')

class CarouselImageUpdateView(StaffRequiredMixin, UpdateView):
    model = CarouselImage
    fields = '__all__'
    template_name = 'mainapp/carousel_form.html'
    success_url = reverse_lazy('carousel_list')

class CarouselImageDeleteView(StaffRequiredMixin, DeleteView):
    model = CarouselImage
    template_name = 'mainapp/carousel_delete.html'
    success_url = reverse_lazy('carousel_list')