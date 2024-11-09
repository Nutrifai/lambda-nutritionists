from repositories.base_table_repository import TableRepository
from Entities.Tables.user_table import UserTable
from boto3.dynamodb.conditions import Attr
from services.appointment_service import AppointmentService


class NutritionistService:
    def __init__(self):
        # self.repository = NutritionistRepository()
        self.repository = TableRepository(table=UserTable())
        self.appointment_service = AppointmentService()

    def get_nutritionists(self, params = {}):

        fields_to_exclude = ["password"]

        nutris = self.repository.get_all(
            filters=Attr("is_nutri").eq(True)
        )

        for nutri in nutris:
            for key in fields_to_exclude:
                nutri.pop(key)
        
        if params.get("withAppointment", "false").lower() == "true":
            # setar as consultas do nutricionista

            # recuperar as consultas
            appointments = self.appointment_service.get_appointments()

            # para cada nutricionista, buscamos se o id do nutricionista é igual ao da consulta
            for nutri in nutris:
                nutri["appointments"] = [
                    appointment 
                    for appointment in appointments
                    if appointment["nutriId"] == nutri["userId"]
                ]


        return nutris

    # def book_time_slot(self, nutritionist_id, time_slot):
    #     updated_availability = self.repository.update_availability(nutritionist_id, time_slot)
    #     return {
    #         "message": "Booking confirmed. The selected time has been updated.",
    #         "updatedAvailability": updated_availability
    #     }

    # def add_nutritionist(self, nutritionist_id, name, available_times, profile_pic):
    #     self.repository.add_nutritionist(nutritionist_id, name, available_times, profile_pic)
    #     return {
    #         "message": "New nutritionist added successfully.",
    #         "nutriId": nutritionist_id,
    #         "name": name,
    #         "availableTimes": available_times,
    #         "profilePic": profile_pic
    #     }
