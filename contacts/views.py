from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Contact
from .tasks import sleeps
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse


def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']
# check if uerer already has made inquiry 
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'you have already made an inquiry for this listing')
                return redirect('/listings/'+listing_id)

        contact = Contact(listing_id=listing_id, listing=listing, name=name, email=email, phone=phone, message=message, user_id=user_id)
        contact.save()
        #send mail
        # send_mail(
        #     'property listing inquiry',
        #     'There has been an inquiry for'+ listing + '. sign into admin panel for more info',
        #     'abdullahmafuz1@gmail.com',
        #     [realtor_email],
        #     fail_silently=False
        # )
        sleeps.delay(5)
        messages.success(request, 'Your request has been submitted, a realtor will get back to you soon ')
        return redirect('/listings/'+listing_id)
@csrf_exempt
def contactApi(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        listing_id = payload['listing_id']
        listing = payload['listing']
        name = payload['name']
        email = payload['email']
        phone = payload['phone']
        message = payload['message']
        user_id = payload['user_id']
        realtor_email = payload['realtor_email']
# check if uerer already has made inquiry 
        if not user_id is None:
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                response = json.dumps([{'fail':'you have already made an inquiry for this listing'}])
                return HttpResponse(response, content_type = 'text/json')

        contact = Contact(listing_id=listing_id, listing=listing, name=name, email=email, phone=phone, message=message, user_id=user_id)
        contact.save()
        response = json.dumps([{'success':'will contact you soon'}])
        return HttpResponse(response, content_type = 'text/json')
