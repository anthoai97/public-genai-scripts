import boto3
import pandas as pd

def load_kms_data(csv_file_path):
    """
    Load KMS key data from a CSV file.
    """
    return pd.read_csv(csv_file_path)

def list_s3_buckets_with_kms():
    """
    List all S3 buckets and retrieve the KMS keys used by them.
    """
    s3_client = boto3.client('s3')
    buckets = s3_client.list_buckets()
    bucket_kms_mapping = []

    for bucket in buckets.get('Buckets', []):
        bucket_name = bucket['Name']
        try:
            encryption = s3_client.get_bucket_encryption(Bucket=bucket_name)
            rules = encryption.get('ServerSideEncryptionConfiguration', {}).get('Rules', [])
            for rule in rules:
                if rule['ApplyServerSideEncryptionByDefault']['SSEAlgorithm'] == 'aws:kms':
                    kms_key_id = rule['ApplyServerSideEncryptionByDefault']['KMSMasterKeyID']
                    bucket_kms_mapping.append({"ResourceType": "S3", "ResourceName": bucket_name, "KMSKeyId": kms_key_id})
        except s3_client.exceptions.ClientError as e:
            print(f"Error accessing encryption settings for bucket {bucket_name}: {e}")
    
    return pd.DataFrame(bucket_kms_mapping)

def list_rds_instances_with_kms():
    """
    List all RDS instances and retrieve the KMS keys used by them.
    """
    rds_client = boto3.client('rds')
    instances = rds_client.describe_db_instances()
    rds_kms_mapping = []

    for instance in instances.get('DBInstances', []):
        kms_key_id = instance.get('KmsKeyId')
        if kms_key_id:
            rds_kms_mapping.append({"ResourceType": "RDS", "ResourceName": instance['DBInstanceIdentifier'], "KMSKeyId": kms_key_id})
    
    return pd.DataFrame(rds_kms_mapping)

def save_to_csv(dataframe, file_path):
    """
    Save a DataFrame to a CSV file.
    """
    dataframe.to_csv(file_path, index=False)
    print(f"Data saved to: {file_path}")
