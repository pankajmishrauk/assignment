# assignment
## Task for Today
1.	I have created one ssm user, who can get/put ssm through AWS CLI command.
2.	I have created one user who can get/put/delete objects in bucket.
3.	I have created one private access bucket. Added lambda role and one IAM user I created in step two.
4.	I have created lambda role, which can get ssm, get/put on bucket and aws log access.
5.	I have created one lambda function, which writes ssm values in s3 bucket and if any update/deletion happen to stack it will write in logs.
6.	I have created one aws event also, so suppose if any user creates ssm key through AWS CLI it will call lambda function and lambda will write keys value in s3 bucket.
