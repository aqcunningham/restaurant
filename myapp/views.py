from django.shortcuts import render
from .forms import CommentForm, MenuForm, BookingForm
from .models import UserComments, Menu, Booking
from django.http import JsonResponse
from datetime import datetime
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse



def home(request):
	return render(request, 'index.html')

def form_view(request):
	form = CommentForm()
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			# can skip?
			# cldt = form.cleaned_data
			# uc = UserComments(
			# 	first_name = cldt['first_name'],
			# 	last_name = cldt['last_name'],
			# 	comment = cldt['comment']
			# )
			form.save()
			return JsonResponse({'message': 'success'})
	return render(request, 'blog.html', {'form': form})

def menu_view(request):
	form = MenuForm()
	if request.method == "POST":
		form = MenuForm(request.POST)
		if form.is_valid():
			# cleanD = form.cleaned_data
			# mf = Menu(
			# 	item_name = cleanD['item_name'],
			# 	category = cleanD['category'],
			# 	description = cleanD['description']
			# )
			form.save()
			return JsonResponse({'message': 'success'})
	return render(request, 'menu_items.html', {'form': form})

def book(request):
	form = BookingForm()
	if request.method == 'POST':
		form = BookingForm(request.POST)
		if form.is_valid():
			form.save()
			return JsonResponse({'message': 'success'})
	return render(request, 'book.html', {'form': form})

@csrf_exempt	
def bookings(request):
	# this version from prev lab:
	# show map and  a header All Reservations
	# date = request.GET.get('date', datetime.today().date())
	# bookings = Booking.objects.all()
	# booking_json = serializers.serialize('json', bookings)
	# return render(request, 'bookings.html', {'bookings': booking_json})
	if request.method == 'POST':
		data = json.load(request)
		exist = Booking.objects.filter(
			reservation_date=data['reservation_date']
			).filter(
				reservation_slot= data['reservation_slot']
				).exists()
		if exist == False:
			booking = Booking(
				first_name=data['first_name'],
				reservation_date=data['reservation_date'],
				reservation_slot=data['reservation_slot']
				)
			booking.save()
		else:
			return HttpResponse("{'error': 1}", content_type='application/json')
				
	date = request.GET.get('date', datetime.today().date())
	if date == '':
		date = datetime.today().date()
	bookings = Booking.objects.all().filter(reservation_date=date)
	booking_json = serializers.serialize('json', bookings)
	return HttpResponse(booking_json, content_type='application/json') 

def all_bookings(request):
	date = request.GET.get('date', datetime.today().date())
	if date == '':
		date = datetime.today().date()
	bookings = Booking.objects.all().filter(reservation_date=date)
	booking_json = serializers.serialize('json', bookings)
	return render(request, 'bookings.html', {'bookings': booking_json})