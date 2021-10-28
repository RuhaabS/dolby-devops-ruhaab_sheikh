# Dolby DevOps Take-Home Assignment

## Abstract

There are two files included in this repository: *CF_Dolby.yml* and *Dolby<span>.py*. 

The *CF_Dolby.yml* file contains the CloudFormation script and is ready to be uploaded with no configuration changes. The script creates the relevant IAM roles and policies to provide relevant permissions for the table.

The *Dolby<span>.py* file contains the script which will conduct the updating of the table and only requires a region input in which the table is currently created (currently set to ap-southeast-2). 

There are 4 different functions included in the *Dolby<span>.py* script:

1. **update_records**: This is the main update function which will set the tables test field to 1 iif it doesn't exist.
2. **table_check**: This is a check function which will conduct a breif check to see if all the entries have been updated (requires a region input).
3. **init_records**: This is a function which populates the table with random data excluding the test variable and was used to initialise the table with records for personal testing and debugging puposes
4. **init_test_records**: This is a function which populates the table with random data including a test variable and was used to add records to the table for personal testing and debugging puposes

## How the update task was performed

To perform this task, we require the boto3 python library which is used to communicate with AWS services and perform tasks you would generally be able to do through the console. Also, make sure the AWS cli is configured with your *AWSAccessKeyId* and *AWSSecretAccessKey*.

After everything is setup, we can start creating the update function. The purpose of this function would be to scan the database and identify any entries that may not have the 'test' attributes value set. For these specifc entries, the value, will be set to '1'. 

To accomplish this, first a connection needs to be established with the the DynamoDB table (make sure the region in the connection statement, is the matches the region the table exists in).

Following this, begin a scan of the table with a 'FilterExpression' with the condition to only pass those entries which do not have the 'test' attribute. Save these entries in an array variable by using a loop in conjunction with the scan.

In a second loop following the scan, iterate over the array and perform an 'update_item' function on each entry of the array to set the 'test' attribute to '1'.

Add the update loop within a 'try' and 'except' condition for better error handling.

The follwing links can be used to aid in the process:

1. Get AWS root keys: https://docs.aws.amazon.com/powershell/latest/userguide/pstools-appendix-sign-up.html
2. AWS Python DynamoDB CRUD documentation: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.03.html
3. AWS Python DynamoDB Scan documentation: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.04.html

## Table Check

In order to check if all entries were successfully updated, I implemented a check function. This does another sanity check to make sure all entries have been updated. Another way to make sure is to manually run a query from the DynamoDB Console on AWS with the Attribute name set to 'test' and condition set to 'Not exists'. 

## Concerns 

When trying to update large datasets of up to 5 million entries, we need to make sure sufficient read and write capacity units are assigned. This can be solved faily easily by changing the value set in the CloudFormation Template (line 21 & 22 of submitted template).

## Things I would do differently

Scan functions can be fairly slow and take time to sequentially read each individual entry. To combat this I would add a Global Secondary Index to allow me to run a query function instead.

