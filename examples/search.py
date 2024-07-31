#!/usr/bin/env python3
import argparse
import os

from jmapc import Client, EmailQueryFilterCondition, MailboxQueryFilterCondition, Ref
from jmapc.methods import EmailQuery, MailboxGet, MailboxGetResponse, MailboxQuery

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--host", "-H", default="email.example.com")
	parser.add_argument("--username", "-u", default="me@example.com")
	parser.add_argument("--password", "-p", default="keep-it-secret")
	parser.add_argument("search", help="The terms to search for.")
	args = parser.parse_args()


	# Create and configure client
	#client = Client.create_with_api_token(
		#host=os.environ["JMAP_HOST"], api_token=os.environ["JMAP_API_TOKEN"]
	#)
	client = Client.create_with_password(
		host=args.host,
		user=args.username,
		password=args.password,
	)

	methods = [
		EmailQuery(filter=EmailQueryFilterCondition(text=args.search)),
	]

	# Call JMAP API with the prepared request
	results = client.request(methods)

	if not results:
		print("No results")
		return

	print(f"Found {len(results)} results")
	# Retrieve the InvocationResponse for the second method. The InvocationResponse
	# contains the client-provided method ID, and the result data model.
	method_1_result = results[0]

	# Retrieve the result data model from the InvocationResponse instance
	method_1_result_data = method_1_result.response

	# Retrieve the Email data from the result data model
	print(method_1_result_data)

if __name__ == "__main__":
	main()
