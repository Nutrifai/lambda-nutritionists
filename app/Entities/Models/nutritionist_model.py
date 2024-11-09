from .base_table_model import TableModel

class NutritionistModel(TableModel):
    userId: str
    email: str
    password: str
    is_nutri: bool
    profile_pic_path: str
