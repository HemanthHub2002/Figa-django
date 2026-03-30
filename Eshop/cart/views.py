from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse

from .models import CartItem
from products.models import Product

# Create your views here.

class AddToCart(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                'error' : 'login_required',
                'redirect_url' : reverse('signin')
            }, status = 401)
        
        # When user is logged in...
        product_id = request.POST.get('product_id')
        size = request.POST.get('size')
        if not size:
            size = 'M'
            
        this_product = get_object_or_404(Product, id = product_id)

        # get cartitem for this product-user combination or create if it doesn't exist.
        item, created = CartItem.objects.get_or_create(
            user = request.user,
            product = this_product,
            size = size
        )

        item.quantity += 1
        item.save()
        cart_count = CartItem.objects.filter(user = request.user).count()

        return JsonResponse({
            'message': f'{this_product.title.capitalize()} was added to cart',
            'cart_count' : cart_count
        })

# Increase Quantity
class IncreaseCartItem(View):
    def post(self, request):
        size = request.POST.get('size')
        if not size:
            size = 'M'
            
        item = get_object_or_404(
            CartItem,
            user=request.user,
            product_id=request.POST.get('product_id'),
            size=size
        )

        item.quantity += 1
        item.save()

        return JsonResponse({
            'quantity': item.quantity,
            'subtotal': item.subtotal
        })

# Decrease Quantity
class DecreaseCartItem(View):
    def post(self, request):
        size = request.POST.get('size')
        if not size:
            size = 'M'
            
        item = get_object_or_404(
            CartItem,
            user=request.user,
            product_id=request.POST.get('product_id'),
            size=size
        )

        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()

        return JsonResponse({'success': True})
    
# Remove item
class RemoveCartItem(View):
    def post(self, request):
        size = request.POST.get('size')
        if not size:
            size = 'M'
            
        item = get_object_or_404(
            CartItem,
            user=request.user,
            product_id=request.POST.get('product_id'),
            size=size
        )
        item.delete()

        return JsonResponse({'success': True})


    
# View Cart
from django.contrib.auth.decorators import login_required

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user = request.user)
    total_quantity = sum(item.quantity for item in cart_items)
    total_price = sum(item.subtotal for item in cart_items)
    context = {
        'cart_items' : cart_items,
        'total_quantity' : total_quantity,
        'total_price' : total_price,
    }
    template = 'cart/cart.html'
    return render(request,template, context)

def get_cart_item_count(request):
    if not request.user.is_authenticated:
        return JsonResponse({'cart_count': 0})
    return JsonResponse({
        'cart_count' : CartItem.objects.filter(user = request.user).count()
    })