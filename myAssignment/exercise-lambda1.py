import json
#import requests
import boto3
#import cfnresponse

def lambda_handler(event, context):
    ssm = boto3.client('ssm')
    parameter = ssm.get_parameter(Name='/myssm/dev/Username', WithDecryption=True)
    print(parameter['Parameter']['Value'])
    string = parameter['Parameter']['Value']
    encoded_string = string.encode("utf-8")
    bucket_name = "mybucket-lambda-dev"
    file_name = "data.txt"
    lambda_path = "/tmp/" + file_name
    s3_path = "/data/" + file_name
    s3 = boto3.resource("s3")
    s3.Bucket(bucket_name).put_object(Key=s3_path, Body=encoded_string)
    responseValue = int(event['ResourceProperties']['Input']) * 5
    responseData = {}
    responseData['Data'] = responseValue
    cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData, CustomResourcePhysicalID)