import json
#import requests
import boto3
from botocore.vendored import requests
SUCCESS = "SUCCESS"
FAILED = "FAILED"

def send(event, responseStatus, responseData, context = None, noEcho=False, PhysicalResourceId = None):
    responseUrl = event['ResponseURL']

    print(responseUrl)

    responseBody = {}
    responseBody['Status'] = responseStatus
    responseBody['Reason'] = 'See the details in CloudWatch Log Stream: '
    print("******************************************************************")
    print(responseBody['Reason'])
    responseBody['PhysicalResourceId'] = context.log_stream_name
    print("******************************************************************")
    print(responseBody['PhysicalResourceId'])
    responseBody['StackId'] = event['StackId']
    responseBody['RequestId'] = event['RequestId']
    responseBody['LogicalResourceId'] = event['LogicalResourceId']
    responseBody['NoEcho'] = noEcho
    responseBody['Data'] = responseData

    json_responseBody = json.dumps(responseBody)
    print("#############################################################")
    print(json_responseBody)

    headers = {
        'content-type' : '',
        'content-length' : str(len(json_responseBody))
    }
    try:
        response = requests.put(responseUrl,
                                data=json_responseBody,
                                headers=headers)
        print("Status code: " + response.reason)
    except Exception as e:
        print("send(..) failed executing requests.put(..): " + str(e))

def lambda_handler(event, context):
	try: 
		ssm = boto3.client('ssm')
		print(event)
		print(context)
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
		responseValue = event['ResourceProperties']['ServiceToken']
		responseData = {}
		responseData['Data'] = responseValue
		send(event, SUCCESS, responseData, context)
	except Exception as e:
	    print("send(..) failed executing requests.put(..): " + str(e))
