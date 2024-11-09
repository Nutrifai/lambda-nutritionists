from repositories.base_table_repository import TableRepository
from Entities.Tables.appointment_table import AppointmentTable
import uuid

class AppointmentService:
    def __init__(self):
        # self.repository = NutritionistRepository()
        self.repository = TableRepository(table=AppointmentTable())

    def get_appointments(self):
        appointments = self.repository.get_all()

        return appointments

    def post_appointments(self, body):
        new_appointment = self.repository.create_item(body={**body, "appointmentId": str(uuid.uuid4())})

        return new_appointment

    def put_appointments(self, body, nutriId, appointmentId):
        update_appointment = self.repository.update_item(new_values=body, pk=nutriId, sk=appointmentId)

        return update_appointment