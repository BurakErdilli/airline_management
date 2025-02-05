

This project is a REST API built using Django and Django REST Framework to manage flights, reservations, and airplanes. It includes features such as flight searches, reservations, and email notifications.

## Table of Contents

1. [Environment Setup](#environment-setup)
2. [Models](#models)
3. [Serializers](#serializers)
4. [Views](#views)
5. [URL Endpoints](#url-endpoints)
6. [Utilities](#utilities)
7. [Logging](#logging)
8. [Environment Variables](#environment-variables)

## Environment Setup

Set up a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows use .venv\Scripts\activate 
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Set up environment variables in a `.env` file:
```env
DJANGO_ENV=production
SENDGRID_API_KEY="your_sendgrid_api_key"
DEFAULT_FROM_EMAIL="your_email@gmail.com"
```

Run migrations:
```bash
python manage.py migrate
```

Run the development server:
```bash
python manage.py runserver
```


## Models & Serializers

### **Airplane**

The `Airplane` model represents an airplane used for flights.

- **Fields**:
    
    - `tail_number`: `CharField` (max length: 10, unique) — Unique identifier for the airplane.
    - `model`: `CharField` (max length: 50) — The model of the airplane.
    - `capacity`: `PositiveIntegerField` — The maximum number of passengers the airplane can accommodate.
    - `production_year`: `PositiveIntegerField` — The year the airplane was produced.
    - `status`: `BooleanField` (default: `True`) — Indicates whether the airplane is active (`True`) or inactive (`False`).
- **Methods**:
    
    - `__str__()`: Returns a string representation of the airplane in the format: `{model} ({tail_number})`.
- **Serializer**:
    
    - **Fields**:
        - `id`: The unique identifier for the airplane (read-only).
        - `tail_number`: The airplane's unique identifier (e.g., tail number).
        - `model`: The model of the airplane.
        - `capacity`: The maximum number of passengers the airplane can accommodate.
        - `production_year`: The year the airplane was produced.
        - `status`: Indicates whether the airplane is active (`True`) or inactive (`False`).
    - **Meta**:
        - `model`: The `Airplane` model.
        - `fields`: Includes all the fields to be serialized.
        - `read_only_fields`: The `id` field is read-only.

### **Flight**

The `Flight` model represents a flight between two locations, assigned to an airplane.

- **Fields**:
    
    - `flight_number`: `CharField` (max length: 10, unique) — A unique identifier for the flight.
    - `departure`: `CharField` (max length: 100) — The departure location.
    - `destination`: `CharField` (max length: 100) — The destination location.
    - `departure_time`: `DateTimeField` — The date and time of the flight's departure.
    - `arrival_time`: `DateTimeField` — The date and time of the flight's arrival.
    - `airplane`: `ForeignKey` to `Airplane` — The airplane used for the flight, with a cascading delete on the airplane.
- **Methods**:
    
    - `__str__()`: Returns a string representation of the flight in the format: `{flight_number}: {departure} -> {destination}`.
- **Serializer**:
    
    - **Fields**:
        - `id`: The unique identifier for the flight (read-only).
        - `flight_number`: The flight's unique identifier.
        - `departure`: The departure location of the flight.
        - `destination`: The destination location of the flight.
        - `departure_time`: The date and time of the flight’s departure.
        - `arrival_time`: The date and time of the flight’s arrival.
        - `airplane`: The ID of the associated airplane (`PrimaryKeyRelatedField`).
    - **Meta**:
        - `model`: The `Flight` model.
        - `fields`: Includes all the fields to be serialized.
        - `read_only_fields`: The `id` field is read-only.

### **Reservation**

The `Reservation` model represents a passenger’s booking for a specific flight.

- **Fields**:
    
    - `passenger_name`: `CharField` (max length: 100) — The name of the passenger.
    - `passenger_email`: `EmailField` — The email address of the passenger.
    - `reservation_code`: `CharField` (max length: 10, unique, editable=False) — A unique code generated for the reservation.
    - `flight`: `ForeignKey` to `Flight` — The flight for which the reservation is made, with a cascading delete on the flight.
    - `status`: `BooleanField` (default: `True`) — Indicates whether the reservation is active (`True`) or canceled (`False`).
    - `created_at`: `DateTimeField` (auto_now_add=True) — The timestamp of when the reservation was created.
- **Methods**:
    
    - `save()`: This method is overridden to automatically generate a unique reservation code before saving. It creates a code using the `flight.id`, `passenger_email`, and a random UUID, and then hashes it to ensure it’s unique.
- **Serializer**:
    
    - **Fields**:
        - `id`: The unique identifier for the reservation (read-only).
        - `passenger_name`: The name of the passenger.
        - `passenger_email`: The email address of the passenger.
        - `reservation_code`: The unique reservation code (read-only).
        - `flight`: The ID of the associated flight (`PrimaryKeyRelatedField`).
        - `status`: Indicates whether the reservation is active (`True`) or canceled (`False`).
        - `created_at`: The timestamp when the reservation was created (read-only).
    - **Meta**:
        - `model`: The `Reservation` model.
        - `fields`: Includes all the fields to be serialized.
        - `read_only_fields`: The `id`, `reservation_code`, and `created_at` fields are read-only.
## Views

### **Airplane API Views**

- **`create_airplane` (POST)**:
    
    - Ensures the `tail_number` is unique. If it already exists, returns a 400 error.
- **`AirplaneUpdateView` (PATCH)**:
    
    - Verifies if the airplane exists. If not, returns a 404 error.
- **`AirplaneDeleteView` (DELETE)**:
    
    - Verifies if the airplane exists. If not, returns a 404 error.

### **Flight API Views**

- **`create_flight` (POST)**:
    
    - Ensures the `flight_number` is unique. If it already exists, returns a 400 error.
- **`FlightUpdateView` (PATCH)**:
    
    - Verifies if the flight exists. If not, returns a 404 error.
- **`FlightDeleteView` (DELETE)**:
    
    - Verifies if the flight exists. If not, returns a 404 error.

### **Reservation API Views**

- **`create_reservation` (POST)**:
    
    - Ensures the `flight_id` exists. If the flight does not exist, returns a 404 error.
    - Verifies flight availability: if the flight is fully booked, returns a 400 error.
- **`ReservationUpdateView` (PATCH)**:
    
    - Verifies if the reservation exists. If not, returns a 404 error.

## URL Endpoints

| Endpoint                      | HTTP Method | Description                                     |
| ----------------------------- | ----------- | ----------------------------------------------- |
| `/airplanes/`                 | GET         | Get a list of all airplanes                     |
| `/airplanes/{id}/`            | GET         | Get details of a specific airplane              |
| `/airplanes/{id}/flights/`    | GET         | Get all flights assigned to a specific airplane |
| `/airplanes/`                 | POST        | Create a new airplane                           |
| `/airplanes/{id}/`            | PATCH       | Update an airplane's details                    |
| `/airplanes/{id}/`            | DELETE      | Delete a specific airplane                      |
| `/flights/`                   | GET         | Get a list of flights with optional filters     |
| `/flights/{id}/`              | GET         | Get details of a specific flight                |
| `/flights/{id}/reservations/` | GET         | Get all reservations for a specific flight      |
| `/flights/`                   | POST        | Create a new flight                             |
| `/flights/{id}/`              | PATCH       | Update a flight's details                       |
| `/flights/{id}/`              | DELETE      | Delete a specific flight                        |
| `/reservations/`              | GET         | Get a list of all reservations                  |
| `/reservations/{id}/`         | GET         | Get details of a specific reservation           |
| `/reservations/`              | POST        | Create a new reservation                        |
| `/reservations/{id}/`         | PATCH       | Update a reservation's details                  |

## Utilities

### **`log_traffic` (Logging Function)**:

- Logs essential details of API requests:
    - **Method**: HTTP method (GET, POST, etc.)
    - **URL**: Full URL of the request
    - **Status Code**: HTTP status code of the response
    - **IP Address**: Client IP address
    - **Timestamp**: Date and time of the request

### **`send_reservation_email` (Email Helper)**:

- Sends an email to the user upon successful reservation.
    - **Subject**: "Reservation Confirmation"
    - **Message**: Includes flight details (flight number, departure/destination, times) and the reservation code.
    - **Recipient**: Sends to the `user_email` provided during reservation.
    - **Sender**: Uses `settings.DEFAULT_FROM_EMAIL` as the sender address.## Logging

The project has logging enabled for two categories:

- **traffic.log**: Logs all API request and response traffic.

## **Environment Variables (Configured in `settings.py`)**


### **Email Configuration (SendGrid SMTP Setup)**

- **`SENDGRID_API_KEY`**: API key for SendGrid to enable email sending.
- **`DEFAULT_FROM_EMAIL`**: The sender email address for outgoing emails.
- **`EMAIL_BACKEND`**: Uses SMTP for production and console backend for local testing.
- **`EMAIL_HOST`**: SendGrid's SMTP host (`smtp.sendgrid.net`).
- **`EMAIL_PORT`**: Uses port **587** for TLS encryption.
- **`EMAIL_USE_TLS`**: Enables **TLS** for secure email transmission.
- **`EMAIL_HOST_USER`**: Always set to `"apikey"` when using SendGrid.
- **`EMAIL_HOST_PASSWORD`**: Uses the `SENDGRID_API_KEY` from environment variables.

## Notes


