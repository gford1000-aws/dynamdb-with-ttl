# Example of DynamoDB with Time to Live (TTL)

This AWS Cloudformation script illustrates how a DynamoDB with TTL enabled can stream the deletion events to a Lambda function,
which in turn can archive the item in S3.  This all occurs within a private VPC that has no access to the internet, instead using
VPC Endpoints for both S3 and DynamoDB.

The script leaves the standard scripts:

* [Run-once Lambda script](https://github.com/gford1000-aws/lambda-run-once)
* [TTL script for DynamoDB](https://github.com/gford1000-aws/dynamdb-with-ttl)
* [VPC creation script](https://github.com/gford1000-aws/vpc) 

The Prefix List for the S3 and DynamoDB service can be found using the CLI: `aws ec2 describe-prefix-lists`.

The script creates the following:

![alt text](https://github.com/gford1000-aws/dynamdb-with-ttl/blob/master/example/Example%20script%20resources.png "Script per designer")

Notes:

1. The ENI used by Lambda within a VPC may remain active, causing the stack to wait during deletion.  To resolve, switch to the EC2 Dashboard and manually Detach the ENI (easily identified in the dashboard).  Once the ENI is detached, delete it.  CloudFormation will then detect the dependency has been removed and continue its deletion of the stack.


## Arguments

| Argument                      | Description                                                                     |
| ----------------------------- |:-------------------------------------------------------------------------------:|
| DDBEndpointPrefixList         | The Prefix List to the DynamoDB service for the region                          |
| HashKeyAttributeName          | The name of the attribute which is the HASH key for the table                   |
| HashKeyAttributeType          | The type of the HASH key attribute                                              |
| ProvisionedReadCapacityUnits  | The read IOPS of the table                                                      |
| ProvisionedWriteCapacityUnits | The write IOPS of the table                                                     |
| RangeKeyAttributeName         | The name of the attribute which is the RANGE key for the table (if defined)     |
| RangeKeyAttributeType         | The type of the RANGE key attribute                                             |
| RunOnceTemplateURL            | The URL of the template that for single execution of Lambda functions           |
| S3EndpointPrefixList          | The Prefix List to the S3 service for the region                                |
| TTLAttributeName              | The name of the attribute used for TTL.  This should be a Number type           |
| TTLDynamoDBTemplateURL        | The S3 URL to the DynamoDB TTL template                                         |
| VPCTemplateURL                | The S3 URL to the VPC template                                                  |


## Outputs

| Output         | Description                                      |
| ---------------|:------------------------------------------------:|
| Bucket         | The bucket in which the items are archived       |
| TableName      | The table name of the DynamoDB table             |

## Licence

This project is released under the MIT license. See [LICENSE](LICENSE) for details.
