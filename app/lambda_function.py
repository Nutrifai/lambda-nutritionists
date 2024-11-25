import json
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver, CORSConfig
from aws_lambda_powertools.event_handler.api_gateway import Router
from services.nutritionist_service import NutritionistService
from services.appointment_service import AppointmentService
from utils.get_user_info import get_user_info

# CORS configuration settings for handling CORS securely
cors_config = CORSConfig(allow_credentials=True)

# Initialize the router for handling API Gateway events
router = Router()

# Global variable to hold the NutritionistService instance
__nutritionist_service: NutritionistService = None
__appointment_service: AppointmentService = None

def __setup_services():
    """
    Initialize the NutritionistService and AppointmentService instances if they haven't been initialized yet.
    
    This function checks if the global __nutritionist_service and __appointment_service variables are None.
    If they are, it initializes the respective service instances and assigns them to the global variables.
    """
    global __nutritionist_service
    global __appointment_service

    if __nutritionist_service:
        return

    __nutritionist_service = NutritionistService()
    __appointment_service = AppointmentService()


@router.get("/nutritionists")
def get_nutritionists():
    """
    Handle GET requests to retrieve all nutritionists with their availability.
    
    This function calls the get_nutritionists method of the NutritionistService instance
    and passes the query string parameters from the current event.
    
    Returns:
        list: A list of all nutritionists with their available time slots.
    """
    return __nutritionist_service.get_nutritionists(params=resolver.current_event.query_string_parameters)

@router.get("/appointments")
def get_appointment():
    """
    Handle GET requests to retrieve all appointments.
    
    This function calls the get_appointments method of the AppointmentService instance.
    
    Returns:
        list: A list of all appointments.
    """
    return __appointment_service.get_appointments()

@router.post("/nutritionists/<nutriId>/appointments")
def post_appointment(nutriId):
    """
    Handle POST requests to create a new appointment for a specific nutritionist.
    
    Args:
        nutriId (str): The ID of the nutritionist.
    
    Returns:
        dict: The details of the created appointment.
    """
    return __appointment_service.post_appointments(body=resolver.current_event.body, nutriId=nutriId)

@router.put("/nutritionists/<nutriId>/appointments/<appointmentId>")
def put_appointment(nutriId, appointmentId):
    """
    Handle PUT requests to update an appointment for a specific nutritionist.
    
    Args:
        nutriId (str): The ID of the nutritionist.
        appointmentId (str): The ID of the appointment.
    
    Returns:
        dict: The details of the updated appointment.
    """
    return __appointment_service.put_appointments(body=resolver.current_event.body, nutriId=nutriId, appointmentId=appointmentId)

@router.put("/nutritionists/<nutriId>/appointments/<appointmentId>/book")
def put_appointment_book(nutriId, appointmentId):
    """
    Handle PUT requests to book an appointment for a specific nutritionist.
    
    Args:
        nutriId (str): The ID of the nutritionist.
        appointmentId (str): The ID of the appointment.
    
    Returns:
        dict: The details of the booked appointment.
    """
    user_info = router.context.get("user")
    return __appointment_service.put_appointments(body={'patientId': user_info.userId}, nutriId=nutriId, appointmentId=appointmentId)

# Initialize APIGatewayHttpResolver with CORS
resolver = APIGatewayHttpResolver(cors=cors_config)
resolver.include_router(router=router, prefix="")

def lambda_handler(event, context=None):
    """
    AWS Lambda handler function.
    
    This function sets up the services, appends user information to the context,
    parses the request body if it is a string, and resolves the event using the resolver.
    
    Args:
        event (dict): The event dictionary containing request data.
        context (object, optional): The context object containing runtime information.
    
    Returns:
        dict: The response dictionary to be returned to API Gateway.
    """
    __setup_services()

    resolver.append_context(user=get_user_info(event))

    # Parse stringified JSON body if present
    if "body" in event and type(event["body"]) is str:
        event["body"] = json.loads(event["body"])

    return resolver.resolve(event, context)
