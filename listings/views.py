from django.shortcuts import render , get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.core.paginator import EmptyPage, PageNotAnInteger , Paginator
from .models import Listing
from realtors.models import Realtor
from .choices import bedroom_choices, price_choices, state_choices
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from urllib.request import urlopen
def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)
    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    context = {
        'listings': paged_listings
    }
    return render(request, 'listings/listings.html', context)

def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    context = {
        'listing': listing
    }
    return render(request, 'listings/listing.html', context)

def search(request):
    query_list = Listing.objects.order_by('-list_date').filter(is_published=True)

    #keyWords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            query_list = query_list.filter(description__icontains=keywords)
        
    #City
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            query_list = query_list.filter(city__iexact=city)
    #state
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            query_list = query_list.filter(state__iexact=state)
    #bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            query_list = query_list.filter(bedrooms__lte=bedrooms)
    #price        
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            query_list = query_list.filter(price__lte=price)
    context = {
        'listings': query_list,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'state_choices': state_choices,
        'values': request.GET
    }
    return render(request, 'listings/search.html',context)
@csrf_exempt
def postListing(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        realtor_id = payload["realtor_id"]
        title = payload["title"]
        address = payload["address"]
        city = payload["city"]
        state = payload["state"]
        zipcode = payload["zipcode"]
        description = payload["description"]
        price = payload["price"]
        bedrooms = payload["bedrooms"]
        bathrooms = payload["bathrooms"]
        sqft = payload["sqft"]
        lot_size = payload["lot_size"]
        photo_main = payload["photo_main"]
        realtor_obj = Realtor.objects.get(id=realtor_id)
        img_temp = NamedTemporaryFile(delete = True)
        img_temp.write(urlopen(photo_main).read())
        img_temp.flush()
    listing = Listing(realtor=realtor_obj, title=title, address=address, city=city, state=state, zipcode=zipcode , description=description, price=price, bedrooms=bedrooms, bathrooms=bathrooms, sqft=sqft, lot_size=lot_size)    
    listing.photo_main.save(f'image_{title}', File(img_temp))
    listing.save()
    return JsonResponse([{'success':'proprty is added successfully', "title": title}], safe=False)
