from .base_table_model import TableModel

class AppointmentModel(TableModel):
    nutriId: str
    appointmentId: str
    appointmentDate: str
    patientId: str = ''
