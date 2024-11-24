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
    Initialize the NutritionistService instance if it hasn't been initialized yet.
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
    Handle the request to retrieve all nutritionists with their availability.
    Returns:
        A list of all nutritionists with their available time slots.
    """
    
    return __nutritionist_service.get_nutritionists(params=resolver.current_event.query_string_parameters)

@router.get("/appointments")
def get_appointment():
    return __appointment_service.get_appointments()

@router.post("/nutritionists/<nutriId>/appointments")
def post_appointment(nutriId):
    return __appointment_service.post_appointments(body=resolver.current_event.body, nutriId=nutriId)

@router.put("/nutritionists/<nutriId>/appointments/<appointmentId>")
def put_appointment(nutriId, appointmentId):
    return __appointment_service.put_appointments(body=resolver.current_event.body, nutriId=nutriId, appointmentId=appointmentId)

@router.put("/nutritionists/<nutriId>/appointments/<appointmentId>/book")
def put_appointment_book(nutriId, appointmentId):
    user_info = router.context.get("user")
    return __appointment_service.put_appointments(body={'patientId': user_info.userId}, nutriId=nutriId, appointmentId=appointmentId)


# Initialize APIGatewayHttpResolver with CORS
resolver = APIGatewayHttpResolver(cors=cors_config)
resolver.include_router(router=router, prefix="")

def lambda_handler(event, context=None):
    """
    AWS Lambda handler function.
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
