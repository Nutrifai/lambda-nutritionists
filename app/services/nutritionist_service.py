from repositories.base_table_repository import TableRepository
from Entities.Tables.user_table import UserTable
from boto3.dynamodb.conditions import Attr
from services.appointment_service import AppointmentService


class NutritionistService:
    """
    Service class for handling nutritionist-related operations.
    
    This class provides methods to interact with the nutritionist repository and appointment service.
    """
    def __init__(self):
        """
        Initialize the NutritionistService instance.
        
        This constructor sets up the repository for interacting with the user table and initializes the appointment service.
        """
        self.repository = TableRepository(table=UserTable())
        self.appointment_service = AppointmentService()

    def get_nutritionists(self, params = {}):
        """
        Retrieve all nutritionists with optional appointments.
        
        Args:
            params (dict, optional): The query parameters to filter nutritionists and include appointments.
        
        Returns:
            list: A list of all nutritionists with their available time slots if specified.
        """
        fields_to_exclude = ["password"]

        nutris = self.repository.get_all(
            filters=Attr("isNutri").eq(True)
        )

        for nutri in nutris:
            for key in fields_to_exclude:
                nutri.pop(key)

        # Set the appointments for the nutritionist
        if params.get("withAppointment", "false").lower() == "true":

            # Retrieve the appointments
            appointments = self.appointment_service.get_appointments(query_params={"onlyAvailable": "true"})

            # For each nutritionist, check if the nutritionist ID matches the appointment's nutritionist ID
            for nutri in nutris:
                nutri["appointments"] = [
                    appointment 
                    for appointment in appointments
                    if appointment["nutriId"] == nutri["userId"]
                ]

        return nutris