from repositories.base_table_repository import TableRepository
from Entities.Tables.appointment_table import AppointmentTable
from boto3.dynamodb.conditions import Attr
import uuid

class AppointmentService:
    def __init__(self):
        # self.repository = NutritionistRepository()
        self.repository = TableRepository(table=AppointmentTable())

    def get_appointments(self, query_params={}):
        params = {}

        if query_params.get("onlyAvailable", "false").lower() == "true":
            params["filters"] = Attr("patientId").eq("")
        
        appointments = self.repository.get_all(**params)

        return appointments

    def post_appointments(self, body, nutriId):
        new_appointment = self.repository.create_item(body={**body, "nutriId": nutriId, "appointmentId": str(uuid.uuid4())})

        return new_appointment

    def put_appointments(self, body, nutriId, appointmentId):
        update_appointment = self.repository.update_item(new_values=body, pk=nutriId, sk=appointmentId)

        return update_appointment
