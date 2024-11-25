from .base_table import Table
from ..Models.appointment_model import AppointmentModel, TableModel

class AppointmentTable(Table):
    """
    Represents the Appointment table in the database.
    
    Attributes:
        partition_key (str): The partition key for the table, default is "nutriId".
        sort_key (str): The sort key for the table, default is "appointmentId".
        name (str): The name of the table, default is "Appointment".
        model (TableModel): The model associated with the table, default is AppointmentModel.
    """
    partition_key: str = "nutriId"
    sort_key: str = "appointmentId"
    name: str = "Appointment"
    model: TableModel = AppointmentModel