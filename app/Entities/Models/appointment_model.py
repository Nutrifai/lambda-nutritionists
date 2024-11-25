from .base_table_model import TableModel

class AppointmentModel(TableModel):
    """
    AppointmentModel represents the data structure for an appointment in the NutrifAI application.

    Attributes:
        nutriId (str): The ID of the nutritionist.
        appointmentId (str): The ID of the appointment.
        appointmentDate (str): The date of the appointment.
        patientId (str): The ID of the patient. Defaults to an empty string.
    """
    nutriId: str
    appointmentId: str
    appointmentDate: str
    patientId: str = ''
