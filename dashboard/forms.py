from django import forms
from django.core.exceptions import ValidationError
from PIL import Image

def validate_image(file):
    try:
        image = Image.open(file)
        file_type = image.format.lower()
        if file_type not in ['jpeg', 'png', 'jpg', 'webp', 'gif']:
            raise ValidationError("Only image files are allowed (jpg, jpeg, png, webp, gif).")
    except Exception:
        raise ValidationError("Invalid image file.")

class SellerForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2 border border-gray-300 rounded'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full px-4 py-2 border border-gray-300 rounded'
    }))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2 border border-gray-300 rounded'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-2 border border-gray-300 rounded'
    }))

    profile_image = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={
    'class': 'w-full px-4 py-2 border border-gray-300 rounded'
    }))

    # portfolio_images = forms.FileField(
    #     required=False,
    #     widget=forms.FileInput(attrs={
    #         'multiple': True,
    #         'class': 'w-full px-4 py-2 border border-gray-300 rounded'
    #     })
    # )

    category = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2 border border-gray-300 rounded',
        'placeholder': 'Category name or ID'
    }))
    location_lat = forms.FloatField(widget=forms.NumberInput(attrs={
        'class': 'w-full px-4 py-2 border border-gray-300 rounded',
        'placeholder': 'Latitude'
    }))
    location_lng = forms.FloatField(widget=forms.NumberInput(attrs={
        'class': 'w-full px-4 py-2 border border-gray-300 rounded',
        'placeholder': 'Longitude'
    }))

    is_active = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-checkbox h-5 w-5 text-blue-600'
    }))
    is_verified = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-checkbox h-5 w-5 text-green-600'
    }))
class BuyerForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2 border border-gray-300 rounded',
        'placeholder': 'Enter name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full px-4 py-2 border border-gray-300 rounded',
        'placeholder': 'Email address'
    }))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2 border border-gray-300 rounded',
        'placeholder': 'Phone number'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-2 border border-gray-300 rounded',
        'placeholder': 'Password'
    }))
    profile_image = forms.ImageField(
        required=False,
        validators=[validate_image],
        widget=forms.ClearableFileInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded'
        })
    )
    is_active = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-checkbox h-5 w-5 text-blue-600'
    }))

class ListingForm(forms.Form):
    title = forms.CharField(max_length=100)
    category = forms.CharField(max_length=50)
    price = forms.DecimalField(decimal_places=2)
    location = forms.CharField(max_length=100)
    is_featured = forms.BooleanField(required=False)


class CategoryForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2 border border-gray-300 rounded',
        'placeholder': 'Category name'
    }))
    is_active = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-checkbox h-5 w-5 text-blue-600'
    }))

class AdForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2 border border-gray-300 rounded'
    }))

    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'w-full px-4 py-2 border border-gray-300 rounded',
        'rows': 3
    }))

    price = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'w-full px-4 py-2 border border-gray-300 rounded'
    }))

    location = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2 border border-gray-300 rounded'
    }))

    category = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2 border border-gray-300 rounded'
    }))

    seller_id = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2 border border-gray-300 rounded'
    }))

    is_active = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-checkbox h-5 w-5 text-blue-600'
    }))

    is_featured = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-checkbox h-5 w-5 text-green-600'
    }))

    # cover_image = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={
    #     'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'
    # }))

    # sample_images = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={
    #     'multiple': True,
    #     'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'
    # }))