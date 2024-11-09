import boto3
import os

def get_dynamodb_table():
    dynamodb = boto3.resource('dynamodb')
    table_name = 'Nutri'
    return dynamodb.Table(table_name)
