from .base_table_model import TableModel

class NutritionistModel(TableModel):
    """
    NutritionistModel represents a nutritionist entity in the system.

    Attributes:
        userId (str): The unique identifier for the user.
        email (str): The email address of the nutritionist.
        password (str): The password for the nutritionist's account.
        isNutri (bool): A flag indicating if the user is a nutritionist.
        profilePicPath (str): The file path to the profile picture of the nutritionist.
    """
    userId: str
    email: str
    password: str
    isNutri: bool
    profilePicPath: str
