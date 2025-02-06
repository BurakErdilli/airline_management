import logging
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings

# Set up logger
traffic_logger = logging.getLogger('traffic')

def log_traffic(request, response):

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    traffic_logger.info(
        f"[{timestamp}] Method: {request.method} | URL: {request.build_absolute_uri()} | Status: {response.status_code} | IP: {request.META.get('REMOTE_ADDR', 'Unknown IP')}"
    )


# Helper function to send email
def send_reservation_email(flight, user_email, reservation_code, user_name):
    subject = "Reservation Confirmation"
    message = f'''Dear {user_name},

Thank you for reserving your seat with us! We're excited to have you aboard. Below are the details of your reservation:

Flight Number: {flight.flight_number}
Departure Location: {flight.departure}
Destination: {flight.destination}
Departure Time: {flight.departure_time.strftime('%A, %B %d, %Y at %I:%M %p')}
Arrival Time: {flight.arrival_time.strftime('%A, %B %d, %Y at %I:%M %p')}

Your reservation code is: {reservation_code}

Please keep this code for future reference. If you need to make any changes or require further assistance, feel free to contact our support team.

We look forward to welcoming you on board and wish you a pleasant journey!

Best regards,
'''

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )