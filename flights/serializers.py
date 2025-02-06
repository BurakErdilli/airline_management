from rest_framework import serializers
from .models import Airplane, Flight, Reservation

class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ['id', 'tail_number', 'model', 'capacity', 'production_year', 'status']
        read_only_fields = ['id']

class FlightSerializer(serializers.ModelSerializer):
    airplane = serializers.PrimaryKeyRelatedField(queryset=Airplane.objects.all())

    class Meta:
        model = Flight
        fields = ['id', 'flight_number', 'departure', 'destination', 'departure_time', 'arrival_time', 'airplane']
        read_only_fields = ['id']

class ReservationSerializer(serializers.ModelSerializer):
    flight = serializers.PrimaryKeyRelatedField(queryset=Flight.objects.all())
    class Meta:
        model = Reservation
        fields = ['id', 'passenger_name', 'passenger_email', 'reservation_code', 'flight', 'status', 'created_at']
        read_only_fields = ['id', 'reservation_code', 'created_at']
