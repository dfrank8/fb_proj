from boto3 import resource
from boto.dynamodb2.fields import HashKey, RangeKey
from boto.dynamodb2.table import Table
from boto3.dynamodb.conditions import Key, Attr
import os 
import datetime


os.environ["AWS_ACCESS_KEY_ID"] = "AKIAI7SV5VXL45RP2D4A"
os.environ["AWS_SECRET_ACCESS_KEY"] = "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"
os.environ["AWS_REGION"] = "us-west-1"

class Dynamo_Wrapper:
    """Class for interaction with Dynamo"""

    def __init__(self, table_name, primary_key, sort_key = None):
        self.dynamodb_resource = resource('dynamodb', 'us-west-1')
        self.primary_key = primary_key
        self.sort_key = sort_key
        self.table = self.dynamodb_resource.Table(table_name)

    def addItem(self,item):
        item['time'] = str(datetime.datetime.now().isoformat())
        self.table.put_item(Item=item)

    def query(self, key):
        response = self.table.query(
            KeyConditionExpression=Key(self.primary_key).eq(key))
        return response

    def updateDBIntValue(self, primKey, updateCol, newVal, sortKey = None):
        if(sortKey != None):
            self.table.update_item(
                        Key={
                            self.sort_key: sortKey,
                            self.primary_key: primKey
                        },
                        UpdateExpression='SET ' + updateCol + ' = :val1',
                        ExpressionAttributeValues={
                            ':val1': (newVal)
                        }
                    )
        else:
            self.table.update_item(
                    Key={
                        self.primary_key: primKey
                    },
                    UpdateExpression='SET ' + updateCol + ' = :val1',
                    ExpressionAttributeValues={
                        ':val1': (newVal)
                    }
                )
    
    def update_post_list(self, primKey, post_id = None):
        """
        Updates a draft list by appending. 
        """  
        if(post_id == None):
            return False
        else:
            result = self.table.update_item(
                Key={
                        self.primary_key: primKey
                    },
                    UpdateExpression="SET drafts = list_append(drafts, :i)",
                    ExpressionAttributeValues={
                        ':i': [post_id],
                        },
                    ReturnValues="UPDATED_NEW"
                )

    def delete_draft(self, primKey, post_index):
        """
        Deletes a draft by index. 
        """
        result = self.table.update_item(
            Key={
                    self.primary_key: primKey
                },
                UpdateExpression="REMOVE drafts["+str(post_index)+"]",
                ReturnValues="ALL_NEW"
            )
        return result












    	
