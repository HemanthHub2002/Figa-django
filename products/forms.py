from django import forms 

from .models import Product, ProductImage

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'desc', 'price', 'stock', 'thumbnail', 'color', 'is_new']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Product title'
            }),
            'desc': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Product description',
                'rows': 4
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Price'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Stock quantity'
            }),
            'thumbnail': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Product color (e.g. Red, Blue)'
            }),
            'is_new': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'width: 20px; height: 20px;'
            }),
        }


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['img', 'caption']
        widgets = {
            'img': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'caption': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Optional caption'
            }),
        }