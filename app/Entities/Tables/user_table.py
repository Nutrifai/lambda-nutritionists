from .base_table import Table
from ..Models.nutritionist_model import NutritionistModel, TableModel

class UserTable(Table):
    """
    Represents the User table in the database.
    
    Attributes:
        partition_key (str): The partition key for the table, default is "userId".
        name (str): The name of the table, default is "User".
        model (TableModel): The model associated with the table, default is NutritionistModel.
    """
    partition_key: str = "userId"
    name: str = "User"
    model: TableModel = NutritionistModel