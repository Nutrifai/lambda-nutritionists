from dataclasses import dataclass
from Entities.Tables.base_table import Table
from env.ddb_client import get_ddb_client
from boto3.dynamodb.conditions import Key

@dataclass
class TableRepository:
    """
    Repository class for interacting with a DynamoDB table.
    
    This class provides methods to perform CRUD operations on a DynamoDB table.
    """
    table: Table
    
    def __post_init__(self):
        """
        Post-initialization to set up the DynamoDB table instance.
        
        This method initializes the DynamoDB table instance using the provided table configuration.
        """
        self.__dynamo_table_instance = get_ddb_client().Table(self.table.name)

    @property
    def __dynamo_table(self):
        """
        Get the DynamoDB table instance.
        
        Returns:
            boto3.resources.factory.dynamodb.Table: The DynamoDB table instance.
        """
        return self.__dynamo_table_instance

    def get_all(self, filters = None):
        """
        Retrieve all items from the DynamoDB table with optional filters.
        
        Args:
            filters (boto3.dynamodb.conditions.ConditionBase, optional): The filter expression to apply.
        
        Returns:
            list: A list of items retrieved from the table.
        """
        params = {}

        if filters:
            params["FilterExpression"] = filters

        scan_response = self.__dynamo_table.scan(**params)

        return scan_response["Items"]
    
    def get_by_pk(self, pk, sk=""):
        """
        Retrieve an item from the DynamoDB table by its partition key and optional sort key.
        
        Args:
            pk (str): The partition key of the item to retrieve.
            sk (str, optional): The sort key of the item to retrieve.
        
        Returns:
            dict: The item retrieved from the table.
        """
        filters = Key(self.table.partition_key).eq(pk)

        if sk and self.table.sort_key:
            filters = filters & Key(self.table.sort_key).eq(sk)


        query = self.__dynamo_table.query(
            KeyConditionExpression=filters
        )

        return query["Items"]

    def create_item(self, body):
        """
        Create a new item in the DynamoDB table.
        
        Args:
            body (dict): The data for the new item.
        
        Returns:
            dict: The created item retrieved from the table.
        """
        item = self.table.model(**body).model_dump()
        
        self.__dynamo_table.put_item(Item=item)

        pk = item[self.table.partition_key]
        sk = "" if not self.table.sort_key else item[self.table.sort_key]

        return self.get_by_pk(pk, sk)
    

    def delete_item(self, pk, sk=""):
        """
        Delete an item from the DynamoDB table by its partition key and optional sort key.
        
        Args:
            pk (str): The partition key of the item to delete.
            sk (str, optional): The sort key of the item to delete.
        
        Raises:
            Exception: If the table has a sort key and it is not provided.
        
        Returns:
            dict: The response from the delete operation.
        """
        if self.table.sort_key and not sk:
            raise Exception(f"Should use Partition Key and Sort Key for table {self.table.name}")
        
        key = {self.table.partition_key: pk}
        
        if sk and self.table.sort_key:
            key[self.table.sort_key] = sk
        
        delete_response = self.__dynamo_table.delete_item(Key=key)
        
        return {
            "operationStatus": delete_response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        }
    
    def update_item(self, pk, sk="", new_values = {}):
        """
        Update an item in the DynamoDB table by its partition key and optional sort key.
        
        Args:
            pk (str): The partition key of the item to update.
            sk (str, optional): The sort key of the item to update.
            new_values (dict): The new values for the item.
        
        Raises:
            Exception: If the table has a sort key and it is not provided.
            ValueError: If the partition key or sort key in the new values differ from the provided keys.
            Exception: If the item with the provided keys is not found.
        
        Returns:
            dict: The updated item retrieved from the table.
        """
        if self.table.sort_key and not sk:
            raise Exception(f"Should use Partition Key and Sort Key for table {self.table.name}")
        
        if (
            self.table.partition_key in new_values and pk != str(new_values.get(self.table.partition_key, ""))
            or self.table.sort_key in new_values and sk != str(new_values.get(self.table.sort_key, ""))
        ):

            raise ValueError(
                f"the value of partition_key '{self.table.partition_key}'"
                f"{' or sort_key ' + self.table.sort_key if self.table.sort_key else ''} "
                f"in the body is different from partition_key '{pk}'"
                f"{' or sort_key ' + sk if self.table.sort_key else ''} "
                "present in request path"
            )


        current_value = self.get_by_pk(pk, sk)

        if not current_value:
            raise Exception(f"Item with pk: {pk} and sk: {sk} not found")

        updated_item = self.table.model(
            **{
                **current_value[0],
                **new_values
            }
        )

        self.__dynamo_table.put_item(Item=updated_item.model_dump())

        return self.get_by_pk(pk, sk)