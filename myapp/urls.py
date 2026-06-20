from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('blog/', views.form_view, name='form_view'),
	path('menu_items/', views.menu_view, name='menu_view'),
	path('book/', views.book, name="book"),
	path('bookings/', views.bookings, name='bookings'),
	path('all-bookings/', views.all_bookings, name='all_bookings'),
]
