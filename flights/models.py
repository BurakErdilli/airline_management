import hashlib
import uuid
from django.db import models

class Airplane(models.Model):
    tail_number = models.CharField(max_length=10, unique=True)
    model = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()
    production_year = models.PositiveIntegerField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.model} ({self.tail_number})"


class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)
    departure = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE, related_name="flights")

    def __str__(self):
        return f"{self.flight_number}: {self.departure} -> {self.destination}"




class Reservation(models.Model):
    passenger_name = models.CharField(max_length=100)
    passenger_email = models.EmailField()
    reservation_code = models.CharField(max_length=10, unique=True, editable=False)
    flight = models.ForeignKey('Flight', on_delete=models.CASCADE, related_name="reservations")
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        from .models import Flight  # Lazy import here

        if not self.reservation_code:
            # Create a unique reservation code
            raw_string = f"{self.flight.id}-{self.passenger_email}-{uuid.uuid4().hex}"
            self.reservation_code = hashlib.sha256(raw_string.encode()).hexdigest()[:10]
        
        super().save(*args, **kwargs)


