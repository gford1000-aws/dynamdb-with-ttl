import boto3
import random
import time
import uuid

def get_times(offset_backwards_in_days, ttl_interval_in_days):
	start_time = time.time() - random.random() * offset_backwards_in_days * 86400
	end_time = start_time + ttl_interval_in_days * 86400
	return (start_time, end_time)

def create_items(region, table_name, num_items, offset_backwards_in_days, ttl_interval_in_days):
	client = boto3.client('dynamodb', region_name=region)

	for r in range(0, num_items):
		(create_time, delete_time) = get_times(offset_backwards_in_days, ttl_interval_in_days)
		client.put_item(
			TableName=table_name,
			Item={
				"MyKey" : { "S" : str(uuid.uuid4()) },
				"MyRange" : { "S" : str(r) },
				"MyTTL" : { "N" : str(delete_time) },
				"Creation" : { "N" : str(create_time) }
			})


if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("-r", "--region", type=str, help="AWS Region in which the table is located")
	parser.add_argument("-t", "--table_name", type=str, help="Name of the DynamoDB table", required=True)
	parser.add_argument("-n", "--num_items", type=int, help="Number of items to add into the table", default=100)
	parser.add_argument("-o", "--offset", type=int, help="Number of days in which items could be created", default=10)
	parser.add_argument("-l", "--lifetime", type=int, help="Number of days that an item can live", default=5)
	args = parser.parse_args()

	create_items(args.region, args.table_name, args.num_items, args.offset, args.lifetime)

