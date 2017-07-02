# DynamoDB with Time to Live (TTL)

Currently AWS Cloudformation (July 2017) does not provide the capability to declare the Time to Live (TTL) attribute on the items
of a DynamoDB table.

This Cloudformation script allows this to be applied, using Lambda and a CloudWatch Scheduled Event.

The script creates the following:

![alt text](https://github.com/gford1000-aws/dynamdb-with-ttl/blob/master/DynamoDB%20table%20assignment%20of%20TTL.png "Script per designer")

The CloudWatch Event triggers a Lambda, whose only tasks are to asynchronously start another Lambda that will perform the TTL assignment, and then
to disable the Event that triggered it (i.e. guaranteeing a "run once" model).  

The two-step approach then allows the second Lambda to run within a private VPC if this is required, updating the DynamoDB table via a VPC Endpoint.  This is useful 
when the solution has no direct access to call internet services (i.e. AWS services).

Lambda is used to avoid needing to provision an EC2 Instance to perform the TTL assignment - it is both faster and cheaper.

Notes:

1. The ENI used by Lambda within a VPC may remain active, causing the stack to wait during deletion.  To resolve, switch to the EC2 Dashboard and manually Detach the ENI (easily identified in the dashboard).  Once the ENI is detached, delete it.  CloudFormation will then detect the dependency has been removed and continue its deletion of the stack.
2. The RANGE key (`RangeKeyAttributeName`) is optional.  If not specified, then the `RangeKeyAttributeType` parameter is ignored.
3. Streaming is optional.  To switch off, select NONE - otherwise any other selection will enable streaming.  This is useful so that deleted items can be captured from the stream (e.g. perhaps to archive in S3).
4. If UpdateViaVPC is set to `true`, then `VPC`, `VPCRouteTable`, `VPCSubnetList`, and `DDBEndpointPrefixList` must be correctly specified (i.e. point to existing resources).  Otherwise these parameters are ignored.
5. If a VPC is used, then the script creates a VPC Endpoint.  The Endpoint policy limits access to the new DynamoDB table, but allows all actions on the table, so that other processes can use the same Endpoint.  For this reason the Endpoint is returned as an output.


## Arguments

| Argument                      | Description                                                                     |
| ----------------------------- |:-------------------------------------------------------------------------------:|
| DDBEndpointPrefixList         | The VPC Endpoint to the DynamoDB service for the region                         |
| HashKeyAttributeName          | The name of the attribute which is the HASH key for the table                   |
| HashKeyAttributeType          | The type of the HASH key attribute                                              |
| ProvisionedReadCapacityUnits  | The read IOPS of the table                                                      |
| ProvisionedWriteCapacityUnits | The write IOPS of the table                                                     |
| RangeKeyAttributeName         | The name of the attribute which is the RANGE key for the table (if defined)     |
| RangeKeyAttributeType         | The type of the RANGE key attribute                                             |
| TTLAttributeName              | The name of the attribute used for TTL.  This should be a Number type           |
| VPCRouteTable                 | The route table within the VPC that provides the route to the DDB for Lambda    |
| VPCSubnetList                 | The subnets within the VPC thate the Lambda should be associated with via ENI   |


## Outputs

| Output         | Description                                      |
| ---------------|:------------------------------------------------:|
| TableName      | The table name of the DynamoDB table             |
| TableStreamArn | The Arn of the table stream, if enabled          |
| VPCEndpoint    | The VPC Endpoint pointing to the DynamoDB table  |

## Licence

This project is released under the MIT license. See [LICENSE](LICENSE) for details.
