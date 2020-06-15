from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='listings'),
    path('<int:listing_id>', views.listing, name='listing'),
        path('search', views.search, name='search'),
        path('api', views.postListing, name='listing_api'),
        path('api_class', views.ListingView.as_view(), name='listing_api_class'),
]
