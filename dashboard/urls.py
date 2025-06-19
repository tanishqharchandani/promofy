from django.urls import path
from . import views
from .views import (
    categories_view,
    add_category_view,
    edit_category_view,
    delete_category_view,
)

urlpatterns = [
    path('sellers/', views.sellers_view, name='sellers'),
    path('sellers/<str:user_id>/verify/', views.toggle_verification_view, name='toggle_verification'),
    path('buyers/', views.buyers_view, name='buyers'),
    path('listings/', views.listings_view, name='listings'),
    path('sellers/add/', views.add_seller_view, name='add_seller'),
    path('sellers/<str:seller_id>/edit/', views.edit_seller_view, name='edit_seller'),
    path('sellers/<str:seller_id>/delete/', views.delete_seller_view, name='delete_seller'),
    path('buyers/add/', views.add_buyer_view, name='add_buyer'),
    path('buyers/<str:buyer_id>/edit/', views.edit_buyer_view, name='edit_buyer'),
    path('buyers/<str:buyer_id>/delete/', views.delete_buyer_view, name='delete_buyer'),
    path('listings/<str:listing_id>/edit/', views.edit_listing_view, name='edit_listing'),
    path('listings/<str:listing_id>/delete/', views.delete_listing_view, name='delete_listing'),
    path('listings/<str:listing_id>/toggle-featured/', views.toggle_featured_view, name='toggle_featured'),
    path('categories/', categories_view, name='categories'),
    path('categories/add/', add_category_view, name='add_category'),
    path('categories/edit/<str:category_id>/', edit_category_view, name='edit_category'),
    path('categories/delete/<str:category_id>/', delete_category_view, name='delete_category'),
    path('ads/', views.ads_view, name='ads'),
    path('ads/add/', views.add_ad_view, name='add_ad'),
    path('ads/edit/<str:ad_id>/', views.edit_ad_view, name='edit_ad'),
    path('ads/delete/<str:ad_id>/', views.delete_ad_view, name='delete_ad'),
    path('sellers/<str:seller_id>/ads/', views.seller_ads_view, name='seller_ads'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.login_view, name='home'),
    path('sellers/<str:seller_id>/view/', views.view_seller_view, name='view_seller'),
    path('inquiries/', views.inquiries_view, name='inquiries'),
    path('inquiries/<str:inquiry_id>/delete/', views.delete_inquiry_view, name='delete_inquiry'),
    path('sellers/<str:seller_id>/inquiries/', views.seller_inquiries_view, name='seller_inquiries'),

]
