# Django & DRF Imports
from django.utils.dateparse import parse_datetime

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

# Standard Library Imports
import hashlib
import uuid

# Local Imports
from . import utils
from .models import Airplane, Flight, Reservation
from .serializers import AirplaneSerializer, FlightSerializer, ReservationSerializer



# Airplane API Endpoints

class AirplaneListView(APIView):
    def get(self, request: Request) -> Response:
        airplanes = Airplane.objects.all()
        serializer = AirplaneSerializer(airplanes, many=True)
        
        # Log the API traffic
        response = Response(serializer.data)
        utils.log_traffic(request, response)

        return response


class AirplaneDetailView(APIView):
    def get(self, request: Request, id: int) -> Response:
        try:
            airplane = Airplane.objects.get(id=id)
        except Airplane.DoesNotExist:
            response = Response({"error": "Airplane not found"}, status=status.HTTP_404_NOT_FOUND)
            utils.log_traffic(request, response)
            return response
        
        serializer = AirplaneSerializer(airplane)
        response = Response(serializer.data)
        utils.log_traffic(request, response)
        
        return response



class AirplaneFlightsView(APIView):
    def get(self, request: Request, id: int) -> Response:
        try:
            airplane = Airplane.objects.get(id=id)
        except Airplane.DoesNotExist:
            response = Response({"error": "Airplane not found"}, status=status.HTTP_404_NOT_FOUND)
            utils.log_traffic(request, response)
            return response

        flights = airplane.flights.all()
        flight_serializer = FlightSerializer(flights, many=True)
        
        response = Response(flight_serializer.data)
        utils.log_traffic(request, response)

        return response


@api_view(['POST'])
def create_airplane(request: Request) -> Response:
    tail_number = request.data.get('tail_number')

    if Airplane.objects.filter(tail_number=tail_number).exists():
        response = Response({"error": f"An airplane with tail number {tail_number} already exists."}, 
                            status=status.HTTP_400_BAD_REQUEST)
        utils.log_traffic(request, response)
        return response

    serializer = AirplaneSerializer(data=request.data)
    if serializer.is_valid():
        airplane = serializer.save()
        response = Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    utils.log_traffic(request, response)
    return response


class AirplaneUpdateView(APIView):
    def patch(self, request: Request, id: int) -> Response:
        try:
            airplane = Airplane.objects.get(id=id)
        except Airplane.DoesNotExist:
            response = Response({"error": "Airplane not found"}, status=status.HTTP_404_NOT_FOUND)
            utils.log_traffic(request, response)
            return response

        serializer = AirplaneSerializer(airplane, data=request.data, partial=True)
        if serializer.is_valid():
            updated_airplane = serializer.save()
            response = Response(serializer.data)
        else:
            response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        utils.log_traffic(request, response)
        return response


class AirplaneDeleteView(APIView):
    def delete(self, request: Request, id: int) -> Response:
        try:
            airplane = Airplane.objects.get(id=id)
        except Airplane.DoesNotExist:
            response = Response({"error": "Airplane not found"}, status=status.HTTP_404_NOT_FOUND)
            utils.log_traffic(request, response)
            return response

        airplane.delete()
        response = Response(status=status.HTTP_204_NO_CONTENT)
        utils.log_traffic(request, response)

        return response


# Flight API Endpoints

class FlightListView(APIView):
    def get(self, request: Request) -> Response:
        departure_location = request.query_params.get('departure', None)
        arrival_location = request.query_params.get('destination', None)
        departure_date = request.query_params.get('departure_time', None)
        arrival_date = request.query_params.get('arrival_time', None)

        flights = Flight.objects.all()

        # Apply filters if any
        if departure_location:
            flights = flights.filter(departure__icontains=departure_location)
        if arrival_location:
            flights = flights.filter(destination__icontains=arrival_location)
        
        if departure_date:
            try:
                departure_date = parse_datetime(departure_date).date()
            except ValueError:
                return Response({"error": "Invalid date format, please use yyyy-mm-dd"}, status=400)
            flights = flights.filter(departure_time__date=departure_date)

        if arrival_date:
            try:
                arrival_date = parse_datetime(arrival_date).date()
            except ValueError:
                return Response({"error": "Invalid date format, please use yyyy-mm-dd"}, status=400)
            flights = flights.filter(arrival_time__date=arrival_date)

        flight_serializer = FlightSerializer(flights, many=True)

        # Log the API traffic
        response = Response(flight_serializer.data)
        utils.log_traffic(request, response)

        return response


class FlightDetailView(APIView):
    def get(self, request: Request, id: int) -> Response:
        try:
            flight = Flight.objects.get(id=id)
        except Flight.DoesNotExist:
            response = Response({"error": "Flight not found"}, status=status.HTTP_404_NOT_FOUND)
            utils.log_traffic(request, response)
            return response

        serializer = FlightSerializer(flight)
        response = Response(serializer.data)
        utils.log_traffic(request, response)

        return response


class FlightReservationsView(APIView):
    def get(self, request: Request, id: int) -> Response:
        try:
            flight = Flight.objects.get(id=id)
        except Flight.DoesNotExist:
            response = Response({"error": "Flight not found"}, status=status.HTTP_404_NOT_FOUND)
            utils.log_traffic(request, response)
            return response

        reservations = Reservation.objects.filter(flight=flight)
        reservation_serializer = ReservationSerializer(reservations, many=True)

        response = Response(reservation_serializer.data)
        utils.log_traffic(request, response)

        return response



@api_view(['POST'])
def create_flight(request: Request) -> Response:
    serializer = FlightSerializer(data=request.data)
    if serializer.is_valid():
        flight = serializer.save()
        
        response = Response(serializer.data, status=status.HTTP_201_CREATED)
        utils.log_traffic(request, response)
        
        return response

    response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    utils.log_traffic(request, response)
    return response


class FlightUpdateView(APIView):
    def patch(self, request: Request, id: int) -> Response:
        try:
            flight = Flight.objects.get(id=id)
        except Flight.DoesNotExist:
            response = Response({"error": "Flight not found"}, status=status.HTTP_404_NOT_FOUND)
            utils.log_traffic(request, response)
            return response

        serializer = FlightSerializer(flight, data=request.data, partial=True)
        if serializer.is_valid():
            updated_flight = serializer.save()
            response = Response(serializer.data)
        else:
            response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        utils.log_traffic(request, response)
        return response


class FlightDeleteView(APIView):
    def delete(self, request: Request, id: int) -> Response:
        try:
            flight = Flight.objects.get(id=id)
        except Flight.DoesNotExist:
            response = Response({"error": "Flight not found"}, status=status.HTTP_404_NOT_FOUND)
            utils.log_traffic(request, response)
            return response

        flight.delete()

        response = Response(status=status.HTTP_204_NO_CONTENT)
        utils.log_traffic(request, response)

        return response



# Reservation API Endpoints

class ReservationListView(APIView):
    def get(self, request: Request) -> Response:
        reservations = Reservation.objects.all()
        serializer = ReservationSerializer(reservations, many=True)
        response = Response(serializer.data)
        utils.log_traffic(request, response)

        return response


class ReservationDetailView(APIView):
    def get(self, request: Request, id: int) -> Response:
        try:
            reservation = Reservation.objects.get(id=id)
        except Reservation.DoesNotExist:
            response = Response({"error": "Reservation not found"}, status=status.HTTP_404_NOT_FOUND)
            utils.log_traffic(request, response)
            return response

        serializer = ReservationSerializer(reservation)
        response = Response(serializer.data)
        utils.log_traffic(request, response)

        return response


@api_view(['POST'])
def create_reservation(request: Request) -> Response:
    flight_id = request.data.get('flight')
    user_email = request.data.get('passenger_email')

    try:
        flight = Flight.objects.get(id=flight_id)
    except Flight.DoesNotExist:
        response = Response({"error": "Flight not found"}, status=status.HTTP_404_NOT_FOUND)
        utils.log_traffic(request, response)
        return response

    if flight.reservations.count() >= flight.airplane.capacity:
        response = Response({"error": "Flight is fully booked"}, status=status.HTTP_400_BAD_REQUEST)
        utils.log_traffic(request, response)
        return response

    reservation_code = hashlib.sha256(f"{flight_id}-{user_email}-{uuid.uuid4().hex}".encode()).hexdigest()[:10]
    request.data['reservation_code'] = reservation_code

    user_name = request.data.get('passenger_name', 'Passenger')

    serializer = ReservationSerializer(data=request.data)
    if serializer.is_valid():
        try:
            reservation = serializer.save()
            response = Response(serializer.data, status=status.HTTP_201_CREATED)
            utils.log_traffic(request, response)
            utils.send_reservation_email(flight, user_email, reservation_code, user_name)
            return response
        except Exception as e:
            response = Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            utils.log_traffic(request, response)
            return response

    response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    utils.log_traffic(request, response)
    return response


class ReservationUpdateView(APIView):
    def patch(self, request: Request, id: int) -> Response:
        try:
            reservation = Reservation.objects.get(id=id)
        except Reservation.DoesNotExist:
            response = Response({"error": "Reservation not found"}, status=status.HTTP_404_NOT_FOUND)
            utils.log_traffic(request, response)
            return response

        serializer = ReservationSerializer(reservation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = Response(serializer.data)
            utils.log_traffic(request, response)
            return response

        response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        utils.log_traffic(request, response)
        return response

