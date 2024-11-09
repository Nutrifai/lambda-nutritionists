from .base_table import Table
from ..Models.nutritionist_model import NutritionistModel, TableModel

class UserTable(Table):
    partition_key: str = "userId"
    name: str = "User"
    model: TableModel = NutritionistModel