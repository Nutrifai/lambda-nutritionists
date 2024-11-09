from .base_table import Table
from ..Models.appointment_model import AppointmentModel, TableModel

class AppointmentTable(Table):
    partition_key: str = "nutriId"
    sort_key: str = "appointmentId"
    name: str = "Appointment"
    model: TableModel = AppointmentModel