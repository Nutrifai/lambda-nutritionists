from .base_table_model import TableModel

class NutritionistModel(TableModel):
    userId: str
    email: str
    password: str
    isNutri: bool
    profilePicPath: str
