import json
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, CORSConfig
from aws_lambda_powertools.event_handler.api_gateway import Router
from services.nutritionist_service import NutritionistService
from utils.response_utils import create_response

# CORS configuration settings for handling CORS securely
cors_config = CORSConfig(allow_credentials=True)

# Initialize the router for handling API Gateway events
router = Router()

# Global variable to hold the NutritionistService instance
__nutritionist_service: NutritionistService = None

def __setup_services():
    """
    Initialize the NutritionistService instance if it hasn't been initialized yet.
    """
    global __nutritionist_service

    if __nutritionist_service:
        return

    __nutritionist_service = NutritionistService()


@router.get("/nutritionists/list")
def get_nutritionists():
    """
    Handle the request to retrieve all nutritionists with their availability.
    Returns:
        A list of all nutritionists with their available time slots.
    """
    return create_response(200, __nutritionist_service.get_nutritionists())


@router.post("/nutritionists/book")
def book_time_slot():
    """
    Handle the request to book a time slot for a specific nutritionist.
    Expects a JSON body with 'nutriId' and 'timeSlot' fields.
    Returns:
        A confirmation message and updated availability.
    """
    body = resolver.current_event.json_body
    nutritionist_id = body.get("nutriId")
    time_slot = body.get("timeSlot")

    if not nutritionist_id or not time_slot:
        return create_response(400, {"error": "nutriId and timeSlot are required"})

    result = __nutritionist_service.book_time_slot(nutritionist_id, time_slot)
    return create_response(200, result)


@router.post("/nutritionists/create")
def add_nutritionist():
    """
    Handle the request to add a new nutritionist.
    Expects a JSON body with 'nutriId', 'name', and 'availableTimes' fields.
    Returns:
        A success message with the added nutritionist details.
    """
    body = resolver.current_event.json_body
    nutritionist_id = body.get("nutriId")
    name = body.get("name")
    available_times = body.get("availableTimes", [])
    profile_pic = body.get("profilePic") # base64 encoded image

    if not nutritionist_id or not name or not profile_pic:
        return create_response(400, {"error": "nutriId, name and profilePic are required"})

    result = __nutritionist_service.add_nutritionist(nutritionist_id, name, available_times, profile_pic)
    return create_response(201, result)


# Initialize APIGatewayRestResolver with CORS
resolver = APIGatewayRestResolver(cors=cors_config)
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

    # Parse stringified JSON body if present
    if "body" in event and isinstance(event["body"], str):
        event["body"] = json.loads(event["body"])

    response = resolver.resolve(event, context)

    # Ensure response body is JSON-encoded
    if "body" in response and not isinstance(response["body"], str):
        response["body"] = json.dumps(response["body"], ensure_ascii=False)

    return response
