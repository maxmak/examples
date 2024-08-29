import boto3
import json

# authenticate with AWS
session = boto3.Session(
    aws_access_key_id='xxx',
    aws_secret_access_key='xxx',
    region_name='us-east-1'
)


# Initialize the SQS client
sqs = session.client('sqs')

# Your SQS queue URL
queue_url = 'https://sqs.us-east-1.amazonaws.com/<account id>/<sqs queue name>'

def process_message(message_body):
    """
    Function to process the message.
    For this example, we'll just print the message.
    You can add your custom processing logic here.
    """
    print(f"Processing message: {message_body}")
    # Add your processing logic here

def main():
    try:
        # Receive a message from the SQS queue
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,  # Retrieve only one message
            VisibilityTimeout=30,  # Hide the message for 30 seconds
            WaitTimeSeconds=10  # Long polling (optional)
        )
        
        messages = response.get('Messages', [])
        
        if not messages:
            print("No messages to process.")
            return
        
        # Process the received message
        for message in messages:
            message_body = message['Body']
            receipt_handle = message['ReceiptHandle']
            message_id = message['MessageId']

            # Process the message (customize this function)
            print(message_id)
            process_message(message_body)

            # Delete the message from the queue after processing
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )
            print("Message deleted successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
