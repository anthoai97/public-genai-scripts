import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def list_pending_deletion_keys():
    try:
        # Initialize the AWS KMS client
        kms_client = boto3.client('kms')

        # List all KMS keys
        paginator = kms_client.get_paginator('list_keys')
        pending_deletion_keys = []

        for page in paginator.paginate():
            for key in page['Keys']:
                key_id = key['KeyId']

                # Get the key metadata
                key_metadata = kms_client.describe_key(KeyId=key_id)['KeyMetadata']

                # Check if the key is pending deletion
                if key_metadata['KeyState'] == 'PendingDeletion':
                    pending_deletion_keys.append({
                        'KeyId': key_id,
                        'KeyArn': key_metadata['Arn'],
                        'DeletionDate': key_metadata['DeletionDate'].strftime('%Y-%m-%d %H:%M:%S')
                    })

        if pending_deletion_keys:
            print("Keys pending deletion:")
            for key in pending_deletion_keys:
                print(f"KeyId: {key['KeyId']}, KeyArn: {key['KeyArn']}, DeletionDate: {key['DeletionDate']}")
        else:
            print("No keys are pending deletion.")

    except NoCredentialsError:
        print("AWS credentials not found. Please configure your credentials.")
    except PartialCredentialsError:
        print("Incomplete AWS credentials configuration.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    list_pending_deletion_keys()
