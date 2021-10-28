from pprint import pprint
import boto3
import time
import uuid
from botocore.exceptions import ClientError
from decimal import Decimal
from boto3.dynamodb.conditions import Attr, Key

def update_records(region):

    # Setting up connection with Dynamodb
    dynamodb = boto3.resource('dynamodb', region_name=region)

    # Selcting Table
    table = dynamodb.Table('stuff')
    # Filter to only get entries which do not have 'test' attribute
    scan_filter = {
        'FilterExpression': Attr("test").not_exists()
    }

    # Initialising start and stop flags
    stop = False
    start = None

    # Loop to save all table fields in array
    while not stop:
        response = table.scan(**scan_filter) # Scan table
        items = response.get('Items', []) # Save entry in 'items' array
        start = response.get('LastEvaluatedKey', None) # Looking for last entry
        stop = start is None # Setting flag as per 'start' flag
    
    # Iterate over 'items' array
    for x in items:

        # Attempt Update
        try:
            print("Updatating id: ", x['id']) # Prints id information of entry beign udated
            table.update_item(
                Key={
                        'id': x['id'],
                        'created': x['created']
                    },
                UpdateExpression="set test=:t", # Updates 'test' attribute to 'testVal' variable for entry
                ExpressionAttributeValues={':t': Decimal(1)}, # Sets test variable for update
                ReturnValues="UPDATED_NEW" # Return variable for confirmation
            )
        # Update failed (condition not met)
        except ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException": # Checks error code for condition check failure
                print("Passed id: ", x['id']) # Prints id for which condition check failed
            else:
                print(e.response['Error']['Code']) # Prints the error response
                raise  # Raise the exception

    return "**************** DONE ****************"

def table_check(region):

    # Setting up connection with Dynamodb
    dynamodb = boto3.resource('dynamodb', region_name=region)

    # Selcting Table
    table = dynamodb.Table('stuff')
    # Filter to only get entries which do not have 'test' attribute
    scan_filter = {
        'FilterExpression': Attr("test").not_exists()
    }

    # Initialising start and stop flags
    stop = False
    start = None

    while not stop:
        response = table.scan(**scan_filter) # Scan table
        items = response.get('Items', []) # Save entry in 'items' array
        start = response.get('LastEvaluatedKey', None) # Looking for last entry
        stop = start is None # Setting flag as per 'start' flag
    
    if (len(items) == 0):
        return "All entries updated"
    else:
        return len(items), "entries not updated"

def init_records(guid, timestamp):

    # Setting up connection with Dynamodb
    dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-2")

    # Selecting Table
    table = dynamodb.Table('stuff')
    
    # Putting items in table (id:guid & created:timestamp)
    response = table.put_item(
       Item={
            'id': guid,
            'created': timestamp,
        }
    )
    
    # Return confirmation response
    return response

def init_test_records(guid, timestamp):

    # Setting up connection with Dynamodb
    dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-2")

    # Selecting Table
    table = dynamodb.Table('stuff')
    
    # Putting items in table (id:guid, created:timestamp & test:2 - set to 2 for testing)
    response = table.put_item(
       Item={
            'id': guid,
            'created': timestamp,
            'test': 2
        }
    )
    
    # Return confirmation response
    return response


if __name__ == '__main__':

    ########## Update function ##########

    print(update_records("ap-southeast-2")) # Calling update_records function (requires region input)

    ########## Table check function ##########

    # print(table_check("ap-southeast-2")) # Requires region input

    ########## Testing Table Creation ##########

    ### Initialising test data ###
    ## Initialise records
    # for x in range(5000):
        
    #     # GUID and Timestamp in string
    #     guid = str(uuid.uuid4())
    #     timestamp = str(int(time.time()))

    #     resp = init_records(guid, timestamp) # Calling init_records function

    #     pprint(resp, sort_dicts=False) # Printing confirmation response

    ## initiialise test values
    # for x in range(50):

    #     # GUID and Timestamp in string
    #     guid = str(uuid.uuid4())
    #     timestamp = str(int(time.time()))

    #     resp = init_test_records(guid, timestamp) # Calling init_test_records function

    #     pprint(resp, sort_dicts=False) # Printing confirmation response

    
