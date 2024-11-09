from repositories.nutritionist_repository import NutritionistRepository

class NutritionistService:
    def __init__(self):
        self.repository = NutritionistRepository()

    def get_nutritionists(self):
        return self.repository.get_all_nutritionists()

    def book_time_slot(self, nutritionist_id, time_slot):
        updated_availability = self.repository.update_availability(nutritionist_id, time_slot)
        return {
            "message": "Booking confirmed. The selected time has been updated.",
            "updatedAvailability": updated_availability
        }

    def add_nutritionist(self, nutritionist_id, name, available_times, profile_pic):
        self.repository.add_nutritionist(nutritionist_id, name, available_times, profile_pic)
        return {
            "message": "New nutritionist added successfully.",
            "nutriId": nutritionist_id,
            "name": name,
            "availableTimes": available_times,
            "profilePic": profile_pic
        }
