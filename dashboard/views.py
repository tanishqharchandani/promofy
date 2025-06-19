from django.shortcuts import render
from .firebase_helper import get_sellers
from .firebase_helper import toggle_seller_verification
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from .firebase_helper import get_buyers
from .firebase_helper import *
from .forms import SellerForm, BuyerForm, ListingForm
from .firebase_helper import add_seller
import datetime
from firebase_admin import storage
import uuid
import os
import time
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from .firebase_helper import get_filtered_sorted_buyers
from .firebase_helper import get_all_listings
from .firebase_init import * 
from .forms import AdForm
from django.contrib import messages
from .firebase_helper import (
    add_ad, update_ad, delete_ad, get_ad_by_id
)
from .firebase_helper import (
    get_filtered_sorted_categories,
    add_category,
    update_category,
    delete_category,
    get_category_by_id,
)
from .forms import CategoryForm
from django.views.decorators.csrf import csrf_exempt

def categories_view(request):
    if not request.session.get("authenticated"):
        return redirect("login")
    sort = request.GET.get('sort')
    active = request.GET.get('active')
    search = request.GET.get('search', '').strip()

    filter_active = True if active == 'true' else False if active == 'false' else None

    categories = get_filtered_sorted_categories(
        filter_active=filter_active,
        sort_by=sort,
        search=search
    )

    return render(request, 'dashboard/categories.html', {
        'categories': categories,
        'current_sort': sort,
        'current_filter': active,
        'search_query': search
    })


def add_category_view(request):
    if not request.session.get("authenticated"):
        return redirect("login")
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['created_at'] = datetime.datetime.utcnow().isoformat()
            data['modified_at'] = datetime.datetime.utcnow().isoformat()
            add_category(data)
            return redirect('categories')
    else:
        form = CategoryForm()
    
    return render(request, 'dashboard/add_category.html', {'form': form})


def edit_category_view(request, category_id):
    if not request.session.get("authenticated"):
        return redirect("login")
    category_data = get_category_by_id(category_id)
    if not category_data:
        return HttpResponse("Category not found", status=404)

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['modified_at'] = datetime.datetime.utcnow().isoformat()
            update_category(category_id, data)
            return redirect('categories')
    else:
        form = CategoryForm(initial={
            'name': category_data.get('name', ''),
            'is_active': category_data.get('is_active', True)
        })

    return render(request, 'dashboard/edit_category.html', {
        'form': form,
        'category_id': category_id
    })

@csrf_exempt
@require_POST
def delete_category_view(request, category_id):
    delete_category(category_id)
    return redirect('categories')

@csrf_exempt
@require_POST
def toggle_verification_view(request, user_id):
    current_status = request.POST.get('current_status') == 'True'
    toggle_seller_verification(user_id, current_status)
    return redirect('sellers')

@csrf_exempt
@require_POST
def delete_seller_view(request, seller_id):
    delete_seller(seller_id)
    return redirect('sellers')


def add_seller_view(request):
    if not request.session.get("authenticated"):
        return redirect("login")
    if request.method == 'POST':
        form = SellerForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            now = datetime.datetime.utcnow().isoformat()
            data['created_at'] = now
            data['modified_at'] = now

            # Upload profile image
            profile_url = ''
            profile_file = request.FILES.get('profile_image')
            if profile_file:
                filename = f"{int(time.time() * 1000)}.{profile_file.name.split('.')[-1]}"
                bucket = storage.bucket('promofy-mvp.firebasestorage.app')
                blob = bucket.blob(f'profiles/{filename}')
                blob.upload_from_file(profile_file, content_type=profile_file.content_type)
                blob.make_public()
                profile_url = blob.public_url
            data['profile_image'] = profile_url

            # Upload portfolio images
            portfolio_urls = []
            for file in request.FILES.getlist('portfolio_images'):
                filename = f"{int(time.time() * 1000)}_{uuid.uuid4().hex}.{file.name.split('.')[-1]}"
                bucket = storage.bucket('promofy-mvp.firebasestorage.app')
                blob = bucket.blob(f'portfolios/{filename}')
                blob.upload_from_file(file, content_type=file.content_type)
                blob.make_public()
                portfolio_urls.append(blob.public_url)
            data['portfolio_images'] = portfolio_urls

            # Nest location
            data['location'] = {
                'lat': data.pop('location_lat'),
                'lng': data.pop('location_lng')
            }

            add_seller(data)
            return redirect('sellers')
    else:
        form = SellerForm()

    return render(request, 'dashboard/add_seller.html', {'form': form})


def buyers_view(request):
    if not request.session.get("authenticated"):
        return redirect("login")
    sort = request.GET.get('sort')
    active = request.GET.get('active')
    search = request.GET.get('search', '').strip()

    filter_active = True if active == 'true' else False if active == 'false' else None

    buyers = get_filtered_sorted_buyers(filter_active=filter_active, sort_by=sort, search=search)

    return render(request, 'dashboard/buyers.html', {
        'buyers': buyers,
        'current_sort': sort,
        'current_filter': active,
        'search_query': search
    })


def listings_view(request):
    if not request.session.get("authenticated"):
        return redirect("login")
    from .firebase_helper import get_filtered_sorted_listings

    category = request.GET.get('category')
    featured = request.GET.get('featured')
    sort = request.GET.get('sort')
    search = request.GET.get('search', '').strip()

    is_featured = True if featured == 'true' else False if featured == 'false' else None

    print(">>> SEARCH VALUE:", search)  # DEBUG print

    listings = get_filtered_sorted_listings(
        category=category,
        featured=is_featured,
        sort_by=sort,
        search=search
    )

    return render(request, 'dashboard/listings.html', {
        'listings': listings,
        'current_category': category,
        'current_featured': featured,
        'current_sort': sort,
        'search_query': search
    })



def sellers_view(request):
    if not request.session.get("authenticated"):
        return redirect("login")
    sort = request.GET.get('sort')
    active = request.GET.get('active')
    search = request.GET.get('search', '').strip()

    filter_active = True if active == 'true' else False if active == 'false' else None

    sellers = get_filtered_sorted_sellers(filter_active=filter_active, sort_by=sort, search=search)

    return render(request, 'dashboard/sellers.html', {
        'sellers': sellers,
        'current_sort': sort,
        'current_filter': active,
        'search_query': search
    })



def edit_seller_view(request, seller_id):
    if not request.session.get("authenticated"):
        return redirect("login")
    seller_data = get_seller_by_id(seller_id)
    if not seller_data:
        return HttpResponse("Seller not found", status=404)

    if request.method == 'POST':
        form = SellerForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['portfolio_images'] = [img.strip() for img in data['portfolio_images'].split(',') if img.strip()]
            update_seller(seller_id, data)
            return redirect('sellers')
    else:
        initial = {
            'name': seller_data.get('name', ''),
            'profile': seller_data.get('profile', ''),
            'cover_image': seller_data.get('cover_image', ''),
            'portfolio_images': ', '.join(seller_data.get('portfolio_images', [])),
            'is_active': seller_data.get('is_active', False),
            'is_verified': seller_data.get('is_verified', False),
        }
        form = SellerForm(initial=initial)

    return render(request, 'dashboard/edit_seller.html', {
        'form': form,
        'seller_id': seller_id
    })


def upload_to_firebase(file_obj, folder="profiles"):
    storage_client = storage.Client()
    bucket = storage_client.bucket("promofy-mvp.appspot.com")

    # Use timestamp-based filename
    extension = os.path.splitext(file_obj.name)[-1].lower()  # e.g. '.jpg'
    timestamp = str(int(time.time() * 1000))
    filename = f"{folder}/{timestamp}{extension}"

    blob = bucket.blob(filename)
    blob.upload_from_file(file_obj, content_type=file_obj.content_type)
    blob.make_public()  # optional if public access is needed

    return blob.public_url

def add_buyer_view(request):
    if not request.session.get("authenticated"):
        return redirect("login")
    if request.method == 'POST':
        form = BuyerForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            now = datetime.datetime.utcnow().isoformat()
            data['created_at'] = now
            data['modified_at'] = now

            # Handle image upload
            image_file = request.FILES.get('profile_image')
            if image_file:
                # Generate unique filename like 1747770567594.jpg
                ext = image_file.name.split('.')[-1]
                timestamp_name = f"{int(time.time() * 1000)}.{ext}"
                blob_path = f"profiles/{timestamp_name}"

                # Upload to Firebase Storage
                bucket = storage.bucket()
                blob = bucket.blob(blob_path)
                blob.upload_from_file(image_file, content_type=image_file.content_type)
                blob.make_public()

                # Store public URL in Firestore
                data['profile_image'] = blob.public_url

            add_buyer(data)
            return redirect('buyers')
    else:
        form = BuyerForm()

    return render(request, 'dashboard/add_buyer.html', {'form': form})

def edit_buyer_view(request, buyer_id):
    if not request.session.get("authenticated"):
        return redirect("login")
    buyer_data = get_buyer_by_id(buyer_id)
    if not buyer_data:
        return HttpResponse("Buyer not found", status=404)

    if request.method == 'POST':
        form = BuyerForm(request.POST)
        if form.is_valid():
            update_buyer(buyer_id, form.cleaned_data)
            return redirect('buyers')
    else:
        initial = {
            'name': buyer_data.get('name', ''),
            'profile': buyer_data.get('profile', ''),
            'number': buyer_data.get('number', ''),
            'is_active': buyer_data.get('is_active', False),
        }
        form = BuyerForm(initial=initial)

    return render(request, 'dashboard/edit_buyer.html', {
        'form': form,
        'buyer_id': buyer_id
    })

@csrf_exempt
@require_POST
def delete_buyer_view(request, buyer_id):
    delete_buyer(buyer_id)
    return redirect('buyers')

@csrf_exempt
@require_POST
def delete_listing_view(request, listing_id):
    delete_listing(listing_id)
    return redirect('listings')

@csrf_exempt
@require_POST
def toggle_featured_view(request, listing_id):
    current_status = request.POST.get('current_status') == 'True'
    toggle_featured_status(listing_id, current_status)
    return redirect('listings')

def edit_listing_view(request, listing_id):
    if not request.session.get("authenticated"):
        return redirect("login")
    listing = get_listing_by_id(listing_id)
    if not listing:
        return HttpResponse("Listing not found", status=404)

    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            update_listing(listing_id, form.cleaned_data)
            return redirect('listings')
    else:
        form = ListingForm(initial={
            'title': listing.get('title', ''),
            'category': listing.get('category', ''),
            'price': listing.get('price', 0),
            'location': listing.get('location', ''),
            'is_featured': listing.get('is_featured', False),
        })

    return render(request, 'dashboard/edit_listing.html', {'form': form, 'listing_id': listing_id})


def ads_view(request):
    if not request.session.get('authenticated'):
        return redirect('login')
    sort = request.GET.get('sort')
    active = request.GET.get('active')
    search = request.GET.get('search', '').strip()

    filter_active = True if active == 'true' else False if active == 'false' else None

    ads = get_filtered_sorted_ads(filter_active=filter_active, sort_by=sort, search=search)

    return render(request, 'dashboard/ads.html', {
        'ads': ads,
        'current_sort': sort,
        'current_filter': active,
        'search_query': search
    })


# Add new ad
def add_ad_view(request):
    if not request.session.get("authenticated"):
        return redirect("login")
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            bucket = storage.bucket()
            # Upload cover image
            cover_file = request.FILES.get('cover_image')
            if cover_file:
                cover_filename = f"cover_images/{int(time.time() * 1000)}_{cover_file.name}"
                cover_blob = bucket.blob(f"ads/{cover_filename}")
                cover_blob.upload_from_file(cover_file, content_type=cover_file.content_type)
                data['cover_image'] = cover_blob.generate_signed_url(datetime.timedelta(days=365))

            # Upload sample images
            sample_files = request.FILES.getlist('sample_images')
            sample_urls = []
            for file in sample_files:
                filename = f"sample_images/{int(time.time() * 1000)}_{file.name}"
                blob = bucket.blob(f"ads/{filename}")
                blob.upload_from_file(file, content_type=file.content_type)
                sample_urls.append(blob.generate_signed_url(datetime.timedelta(days=365)))

            data['sample_images'] = sample_urls
            now = datetime.datetime.utcnow().isoformat()
            data['created_at'] = now
            data['modified_at'] = now
            data['posted_at'] = now

            add_ad(data)
            return redirect('ads')
    else:
        form = AdForm()

    return render(request, 'dashboard/add_ad.html', {'form': form})

# Edit ad
def edit_ad_view(request, ad_id):
    ad = get_ad_by_id(ad_id)
    if not ad:
        return HttpResponse("Ad not found", status=404)

    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            data['modified_at'] = datetime.datetime.utcnow().isoformat()
            bucket = storage.bucket()
            # Optional new cover image
            cover_file = request.FILES.get('cover_image')
            if cover_file:
                cover_filename = f"cover_images/{int(time.time() * 1000)}_{cover_file.name}"
                cover_blob = bucket.blob(f"ads/{cover_filename}")
                cover_blob.upload_from_file(cover_file, content_type=cover_file.content_type)
                data['cover_image'] = cover_blob.generate_signed_url(datetime.timedelta(days=365))
            else:
                data['cover_image'] = ad.get('cover_image')

            # Optional new sample images
            sample_files = request.FILES.getlist('sample_images')
            sample_urls = []
            for file in sample_files:
                filename = f"sample_images/{int(time.time() * 1000)}_{file.name}"
                blob = bucket.blob(f"ads/{filename}")
                blob.upload_from_file(file, content_type=file.content_type)
                sample_urls.append(blob.generate_signed_url(datetime.timedelta(days=365)))

            if sample_urls:
                data['sample_images'] = sample_urls
            else:
                data['sample_images'] = ad.get('sample_images', [])

            update_ad(ad_id, data)
            return redirect('ads')
    else:
        form = AdForm(initial={
            'title': ad.get('title', ''),
            'description': ad.get('description', ''),
            'price': ad.get('price', 0),
            'location': ad.get('location', ''),
            'category': ad.get('category', ''),
            'seller_id': ad.get('seller_id', ''),
            'is_active': ad.get('is_active', False),
            'is_featured': ad.get('is_featured', False)
        })

    return render(request, 'dashboard/edit_ad.html', {'form': form, 'ad_id': ad_id})

# Delete ad
@csrf_exempt
@require_POST
def delete_ad_view(request, ad_id):
    if not request.session.get("authenticated"):
        return redirect("login")
    delete_ad(ad_id)
    return redirect('ads')

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "promofy123"

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            request.session['authenticated'] = True
            return redirect('buyers')  # Make sure this name matches your urls.py
        else:
            return render(request, 'dashboard/login.html', {
                'error': 'Invalid credentials'
            })

    return render(request, 'dashboard/login.html')


def logout_view(request):
    request.session.flush()
    return redirect('login')

def seller_ads_view(request, seller_id):
    if not request.session.get("authenticated"):
        return redirect("login")

    ads = get_filtered_sorted_ads(filter_active=None, sort_by=None, search=None)
    seller_ads = [ad for ad in ads if ad.get("seller_id") == seller_id]

    # ✅ Get seller name
    seller = get_seller_by_id(seller_id)
    seller_name = seller.get("name", "Unknown Seller") if seller else "Unknown Seller"

    return render(request, 'dashboard/seller_ads.html', {
        'ads': seller_ads,
        'seller_name': seller_name,
    })

def view_seller_view(request, seller_id):
    if not request.session.get("authenticated"):
        return redirect("login")
    seller_data = get_seller_by_id(seller_id)
    if not seller_data:
        return HttpResponse("Seller not found", status=404)

    return render(request, 'dashboard/view_seller.html', {
        'seller': seller_data
    })


def inquiries_view(request):
    if not request.session.get("authenticated"):
        return redirect("login")
    inquiries = get_all_inquiries()

    # Attach related names
    for inquiry in inquiries:
        ad = get_ad_by_id(inquiry['ad_id']) or {}
        buyer = get_buyer_by_id(inquiry['buyer_id']) or {}
        seller = get_seller_by_id(inquiry['seller_id']) or {}
        inquiry['ad_title'] = ad.get('title', 'N/A')
        inquiry['buyer_name'] = buyer.get('name', 'N/A')
        inquiry['buyer_phone'] = buyer.get('phone_number', 'N/A')
        inquiry['seller_name'] = seller.get('name', 'N/A')

    return render(request, 'dashboard/inquiries.html', {'inquiries': inquiries})


def seller_inquiries_view(request, seller_id):
    if not request.session.get("authenticated"):
        return redirect("login")
    seller = get_seller_by_id(seller_id)
    if not seller:
        return HttpResponse("Seller not found", status=404)

    inquiries = get_inquiries_by_seller(seller_id)
    for inquiry in inquiries:
        ad = get_ad_by_id(inquiry['ad_id']) or {}
        buyer = get_buyer_by_id(inquiry['buyer_id']) or {}
        inquiry['ad_title'] = ad.get('title', 'N/A')
        inquiry['buyer_name'] = buyer.get('name', 'N/A')
        inquiry['buyer_phone'] = buyer.get('phone_number', 'N/A')
        inquiry['seller_name'] = seller.get('name', 'N/A')

    return render(request, 'dashboard/seller_inquiries.html', {
        'inquiries': inquiries,
        'seller_name': seller.get('name')
    })

@csrf_exempt
@require_POST
def delete_inquiry_view(request, inquiry_id):
    delete_inquiry(inquiry_id)
    return redirect('inquiries')
