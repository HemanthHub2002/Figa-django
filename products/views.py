from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from .models import Product

from .forms import ProductForm, ProductImageForm


# Mixin to restrict views to staff/admin users
class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


# Create your views here.
def productsView(request):
    template = 'products/products.html'
    context = {
        'products' : Product.objects.all(),
        'current_page' : 'products'
    }
    return render(request, template, context)

# search Products
from django.db.models import Q 
def searchProducts(request):
    template = 'products/search_results.html'
    query = request.GET.get('q')
    if query:
        search_results = Product.objects.filter(
            Q(title__icontains = query) |
            Q(desc__icontains = query) 
        )
        
        # Exclude t-shirts when searching specifically for shirts
        if query.lower() == 'shirt':
            search_results = search_results.exclude(
                Q(title__icontains='t-shirt') | Q(title__icontains='tshirt') | 
                Q(desc__icontains='t-shirt') | Q(desc__icontains='tshirt')
            )
        
        context = {
            'query' : query,
            'products' : search_results
        }
   
        return render(request, template_name=template, context = context)
    else:
        return redirect(reverse_lazy('home_page'))

# CRUD Operations using Generic Class Based Views of Django

from django.views.generic import ( CreateView, DetailView,
                                   UpdateView, DeleteView )

# ListView has already been implemented using a function above : productsView()

class CreateProduct(StaffRequiredMixin, CreateView):
    model = Product
    template_name = 'products/add_product.html'
    form_class = ProductForm
    # redirection url for successful creation of resource
    success_url = '/'

# -------
from django.views.generic.edit import FormMixin
# This mixin provides ability to render forms from the `form_class`

class ProductDetail(FormMixin, DetailView):
    model = Product
    template_name = 'products/product_details.html'
    context_object_name = 'product'
    # providing form class for Product Image
    form_class = ProductImageForm

    def get_success_url(self):
        return reverse('product_details', kwargs={'pk':self.object.pk})
    
    # overriding the queryset to pre-fetch 
    # and add the product images alongside products
    def get_queryset(self):
        return Product.objects.prefetch_related('images')   
    
    def post(self, request, *args, **kwargs):
        # Only staff can upload images
        if not request.user.is_staff:
            return HttpResponseForbidden('You do not have permission to upload images.')
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            image = form.save(commit = False)
            image.Product = self.object 
            image.save()
            return redirect(self.get_success_url())



class UpdateProduct(StaffRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/update_product.html'
    success_url = '/'

class DeleteProduct(StaffRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/delete_product.html'
    success_url = '/'


# Edit Product Image
from .models import ProductImage

class EditProductImage(StaffRequiredMixin, UpdateView):
    model = ProductImage
    template_name = 'products/image_edit.html'
    form_class = ProductImageForm
    context_object_name = 'image'

    def get_success_url(self):
        return reverse('product_details', kwargs={'pk':self.object.Product.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.object.Product
        return context

# Delect prodect Image 
class DeleteProductImage(StaffRequiredMixin, DeleteView):
    model = ProductImage
    template_name = 'products/image_del.html'
    context_object_name = 'image'

    def get_success_url(self):
        return reverse('product_details', kwargs={'pk':self.object.Product.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.object.Product
        return context
    