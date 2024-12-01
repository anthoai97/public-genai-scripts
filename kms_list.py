import boto3
import csv

def list_kms_keys():
    # Initialize the KMS client
    kms_client = boto3.client('kms')
    
    # Paginate through all keys
    paginator = kms_client.get_paginator('list_keys')
    page_iterator = paginator.paginate()
    
    keys = []
    for page in page_iterator:
        keys.extend(page['Keys'])
    
    # Fetch additional details about each key
    detailed_keys = []
    for key in keys:
        key_id = key['KeyId']
        try:
            key_metadata = kms_client.describe_key(KeyId=key_id)['KeyMetadata']
            detailed_keys.append(key_metadata)
        except Exception as e:
            print(f"Error describing key {key_id}: {e}")
    
    return detailed_keys

def list_s3_buckets_using_kms():
    # Initialize the S3 client
    s3_client = boto3.client('s3')
    
    # List all S3 buckets
    response = s3_client.list_buckets()
    buckets = response.get('Buckets', [])
    
    # Dictionary to store which buckets are using which KMS key
    bucket_kms_mapping = {}
    
    for bucket in buckets:
        bucket_name = bucket['Name']
        try:
            # Check if the bucket is using KMS encryption
            encryption = s3_client.get_bucket_encryption(Bucket=bucket_name)
            if 'ServerSideEncryptionConfiguration' in encryption:
                for rule in encryption['ServerSideEncryptionConfiguration']['Rules']:
                    if rule['ServerSideEncryptionByDefault']['SSEAlgorithm'] == 'aws:kms':
                        kms_key_id = rule['ServerSideEncryptionByDefault'].get('KMSMasterKeyID', None)
                        if kms_key_id:
                            if kms_key_id not in bucket_kms_mapping:
                                bucket_kms_mapping[kms_key_id] = []
                            bucket_kms_mapping[kms_key_id].append(bucket_name)
        except s3_client.exceptions.NoEncryptionConfigurationError:
            # No encryption configuration, skip this bucket
            continue
        except Exception as e:
            print(f"Error fetching encryption for bucket {bucket_name}: {e}")
    
    return bucket_kms_mapping

def export_keys_to_csv(keys, bucket_kms_mapping, filename="kms_keys.csv"):
    # Define CSV header
    csv_header = ["KeyId", "Arn", "Description", "KeyState", "CreationDate", "KeyUsage", "KeyManager", "UsedInBuckets"]
    
    # Write to CSV file
    with open(filename, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_header)
        writer.writeheader()
        
        for key in keys:
            key_id = key.get("KeyId", "")
            used_in_buckets = bucket_kms_mapping.get(key_id, [])
            writer.writerow({
                "KeyId": key.get("KeyId", ""),
                "Arn": key.get("Arn", ""),
                "Description": key.get("Description", ""),
                "KeyState": key.get("KeyState", ""),
                "CreationDate": key.get("CreationDate", "").strftime('%Y-%m-%d %H:%M:%S') if key.get("CreationDate") else "",
                "KeyUsage": key.get("KeyUsage", ""),
                "KeyManager": key.get("KeyManager", ""),
                "UsedInBuckets": ', '.join(used_in_buckets) if used_in_buckets else "None"
            })

if __name__ == "__main__":
    # List KMS keys
    keys = list_kms_keys()
    
    # List which buckets are using KMS encryption
    bucket_kms_mapping = list_s3_buckets_using_kms()
    
    # Export the key details with bucket usage info
    if keys:
        export_keys_to_csv(keys, bucket_kms_mapping)
        print(f"Exported {len(keys)} KMS keys with their associated S3 buckets to 'kms_keys.csv'")
    else:
        print("No KMS keys found.")
