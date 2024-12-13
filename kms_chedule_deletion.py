import boto3
import pandas as pd
import sys
import logging

"""
This script reads an Excel file containing KMS Key IDs and schedules deletion for those keys using AWS KMS.

Description:
- The script processes an Excel file with a mandatory column 'KMSKeyID'.
- It uses the AWS Boto3 library to interact with the AWS KMS service.
- It schedules the deletion of the specified KMS keys and logs the results to a file named 'execution.log'.

Usage:
1. Ensure you have Python installed along with the required libraries (boto3, pandas, openpyxl).
2. Prepare an Excel file with a column named 'KMSKeyID' containing the KMS Key IDs to be deleted.
3. Run the script using the following command:

   python script_name.py <excel_file_path> <sheet_name>

   - <excel_file_path>: Path to the Excel file (e.g., data.xlsx).
   - <sheet_name>: Name of the sheet in the Excel file containing the data.

Logs:
- All execution details are saved in 'execution.log', including successes and failures.

Dependencies:
- boto3
- pandas
- openpyxl (for reading .xlsx files)
"""

def set_kms_key_from_excel(excel_file_path, sheet_name):
    # Configure logging
    logging.basicConfig(
        filename='execution.log', 
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Initialize counters for statistics
    total_keys = 0
    successful_deletions = 0
    failed_deletions = 0

    try:
        # Read the Excel file
        df = pd.read_excel(excel_file_path, sheet_name=sheet_name)

        # Ensure the required column is present
        if 'KMSKeyID' not in df.columns:
            raise ValueError("The Excel file must contain a 'KMSKeyID' column.")

        # Initialize AWS client for KMS
        client = boto3.client('kms')

        for index, row in df.iterrows():
            kms_key_id = row['KMSKeyID']
            total_keys += 1

            try:
                # API call to schedule KMS key deletion
                response = client.schedule_key_deletion(
                    KeyId=kms_key_id,
                    PendingWindowInDays=30  # 30 Days
                )

                message = f"Successfully scheduled key deletion for KMSKey {kms_key_id}: {response}"
                print(message)
                logging.info(message)
                successful_deletions += 1
            except Exception as e:
                error_message = f"Failed to schedule key deletion for KMSKey {kms_key_id}: {e}"
                print(error_message)
                logging.error(error_message)
                failed_deletions += 1

        # Log the statistics at the end of execution
        stats_message = f"Total Keys Processed: {total_keys}, Successful Deletions: {successful_deletions}, Failed Deletions: {failed_deletions}"
        print(stats_message)
        logging.info(stats_message)

    except FileNotFoundError:
        error_message = f"The file {excel_file_path} does not exist."
        print(error_message)
        logging.error(error_message)
    except Exception as e:
        error_message = f"An error occurred: {e}"
        print(error_message)
        logging.error(error_message)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <excel_file_path> <sheet_name>")
        sys.exit(1)

    excel_file_path = sys.argv[1]
    sheet_name = sys.argv[2]

    set_kms_key_from_excel(excel_file_path, sheet_name)
