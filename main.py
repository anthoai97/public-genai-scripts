import kms_utils

# Paths
kms_csv_file = '/mnt/data/kms_keys_sample.csv'
output_csv_file = '/mnt/data/merged_resources_kms_data.csv'

# Load KMS key data
kms_keys_df = kms_utils.load_kms_data(kms_csv_file)

# Get S3 bucket KMS mappings
bucket_kms_df = kms_utils.list_s3_buckets_with_kms()

# Get RDS instance KMS mappings
rds_kms_df = kms_utils.list_rds_instances_with_kms()

# Combine S3 and RDS mappings
combined_kms_df = pd.concat([bucket_kms_df, rds_kms_df], ignore_index=True)

# Merge combined mappings with KMS key data
merged_data = combined_kms_df.merge(kms_keys_df, left_on='KMSKeyId', right_on='KeyId', how='left')

# Save the merged data to a CSV file
kms_utils.save_to_csv(merged_data, output_csv_file)
