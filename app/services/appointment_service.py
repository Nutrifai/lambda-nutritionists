from repositories.base_table_repository import TableRepository
from Entities.Tables.appointment_table import AppointmentTable
from boto3.dynamodb.conditions import Attr
import uuid

class AppointmentService:
    """
    Service class for handling appointment-related operations.
    
    This class provides methods to interact with the appointment repository.
    """
    def __init__(self):
        """
        Initialize the AppointmentService instance.
        
        This constructor sets up the repository for interacting with the appointment table.
        """
        self.repository = TableRepository(table=AppointmentTable())

    def get_appointments(self, query_params={}):
        """
        Retrieve all appointments with optional filters.
        
        Args:
            query_params (dict, optional): The query parameters to filter appointments.
        
        Returns:
            list: A list of all appointments.
        """
        params = {}

        if query_params.get("onlyAvailable", "false").lower() == "true":
            params["filters"] = Attr("patientId").eq("")
        
        appointments = self.repository.get_all(**params)

        return appointments

    def post_appointments(self, body, nutriId):
        """
        Create a new appointment for a specific nutritionist.
        
        Args:
            body (dict): The data for the new appointment.
            nutriId (str): The ID of the nutritionist.
        
        Returns:
            dict: The details of the created appointment.
        """
        new_appointment = self.repository.create_item(body={**body, "nutriId": nutriId, "appointmentId": str(uuid.uuid4())})

        return new_appointment

    def put_appointments(self, body, nutriId, appointmentId):
        """
        Update an appointment for a specific nutritionist.
        
        Args:
            body (dict): The new data for the appointment.
            nutriId (str): The ID of the nutritionist.
            appointmentId (str): The ID of the appointment.
        
        Returns:
            dict: The details of the updated appointment.
        """
        update_appointment = self.repository.update_item(new_values=body, pk=nutriId, sk=appointmentId)

        return update_appointment
