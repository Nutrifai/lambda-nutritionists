from tables.dynamodb_table import get_dynamodb_table

class NutritionistRepository:
    def __init__(self):
        self.table = get_dynamodb_table()

    def get_all_nutritionists(self):
        response = self.table.scan()
        return response.get('Items', [])

    def get_nutritionist_availability(self, nutritionist_id):
        response = self.table.get_item(Key={'nutriId': nutritionist_id})
        return response.get('Item', {})

    def update_availability(self, nutritionist_id, time_slot):
        nutritionist = self.get_nutritionist_availability(nutritionist_id)
        available_times = nutritionist.get('availableTimes', [])

        if time_slot in available_times:
            available_times.remove(time_slot)
            self.table.update_item(
                Key={'nutriId': nutritionist_id},
                UpdateExpression="SET availableTimes = :times",
                ExpressionAttributeValues={':times': available_times}
            )
        return available_times

    def add_nutritionist(self, nutritionist_id, name, available_times):
        self.table.put_item(
            Item={
                'nutriId': nutritionist_id,
                'name': name,
                'availableTimes': available_times
            }
        )
