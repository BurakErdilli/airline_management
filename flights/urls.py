from django.urls import path
from . import views

urlpatterns = [
    # Airplane Endpoints
    path('airplanes/', views.AirplaneListView.as_view(), name='airplane-list'),
    path('airplanes/<int:id>/', views.AirplaneDetailView.as_view(), name='airplane-detail'),
    path('airplanes/<int:id>/flights/', views.AirplaneFlightsView.as_view(), name='airplane-flights'),
    path('airplanes/create/', views.create_airplane, name='create-airplane'),
    path('airplanes/<int:id>/update/', views.AirplaneUpdateView.as_view(), name='update-airplane'),
    path('airplanes/<int:id>/delete/', views.AirplaneDeleteView.as_view(), name='delete-airplane'),

    # Flight Endpoints
    path('flights/', views.FlightListView.as_view(), name='flight-list'),
    path('flights/<int:id>/', views.FlightDetailView.as_view(), name='flight-detail'),
    path('flights/<int:id>/reservations/', views.FlightReservationsView.as_view(), name='flight-reservations'),
    path('flights/create/', views.create_flight, name='create-flight'),
    path('flights/<int:id>/update/', views.FlightUpdateView.as_view(), name='update-flight'),
    path('flights/<int:id>/delete/', views.FlightDeleteView.as_view(), name='delete-flight'),

    # Reservation Endpoints
    path('reservations/', views.ReservationListView.as_view(), name='reservation-list'),
    path('reservations/<int:id>/', views.ReservationDetailView.as_view(), name='reservation-detail'),
    path('reservations/create/', views.create_reservation, name='create-reservation'),
    path('reservations/<int:id>/update/', views.ReservationUpdateView.as_view(), name='update-reservation'),
]
