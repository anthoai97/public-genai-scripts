import boto3
import time
import pandas as pd
from botocore.exceptions import ClientError

# Global list to store analysis results
analysis_results = []

# Policies to ignore
IGNORED_POLICIES = ["Example1", "Example2"]

def analyze_kms_usage(role_name):
    iam = boto3.client('iam')
    try:
        # Fetch inline policies
        inline_policies = iam.list_role_policies(RoleName=role_name)['PolicyNames']
        
        # Fetch attached managed policies
        attached_policies = iam.list_attached_role_policies(RoleName=role_name)['AttachedPolicies']
        
        # Analyze inline policies
        for policy_name in inline_policies:
            if policy_name in IGNORED_POLICIES:
                continue
            policy = iam.get_role_policy(RoleName=role_name, PolicyName=policy_name)
            statements = policy['PolicyDocument']['Statement']
            extract_kms_resources(statements, policy_name, role_name)
        
        # Analyze managed policies
        for policy in attached_policies:
            if policy['PolicyName'] in IGNORED_POLICIES:
                continue
            policy_arn = policy['PolicyArn']
            policy_version = iam.get_policy(PolicyArn=policy_arn)['Policy']['DefaultVersionId']
            policy_document = iam.get_policy_version(
                PolicyArn=policy_arn,
                VersionId=policy_version
            )['PolicyVersion']['Document']
            statements = policy_document['Statement']
            extract_kms_resources(statements, policy['PolicyName'], role_name)
    except ClientError as e:
        print(f"Error for role {role_name}: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def extract_kms_resources(statements, policy_name, role_name):
    if not isinstance(statements, list):
        statements = [statements]
    
    for statement in statements:
        actions = statement.get('Action', [])
        resources = statement.get('Resource', [])
        if isinstance(actions, str):
            actions = [actions]
        
        # Check for KMS actions and collect resources
        kms_actions = [action for action in actions if action.lower().startswith('kms:')]
        if kms_actions:
            if isinstance(resources, str):
                resources = [resources]
            for resource in resources:
                # Append the policy name along with the role name and KMS resource ARN
                analysis_results.append({
                    "RoleName": role_name,
                    "PolicyName": policy_name,
                    "KMSResourceARN": resource
                })

def list_all_roles(limit=200):
    iam = boto3.client('iam')
    paginator = iam.get_paginator('list_roles')
    roles = []
    for page in paginator.paginate():
        for role in page['Roles']:
            roles.append(role['RoleName'])
            if len(roles) >= limit:  # Stop once we have `limit` roles
                return roles
    return roles

def main():
    # Process first 200 roles
    roles = list_all_roles(limit=200)
    for role_name in roles:
        print(f"Analyzing role: {role_name}")
        try:
            analyze_kms_usage(role_name)
        except Exception as e:
            print(f"Error processing role {role_name}: {e}")
        # Throttle requests to avoid rate limits
        time.sleep(0.1)  # Adjust based on API limits

    # Save results to CSV
    output_csv = "role_kms_resources_with_policy.csv"
    save_to_csv(output_csv)

def save_to_csv(file_name):
    if analysis_results:
        df = pd.DataFrame(analysis_results)
        df.drop_duplicates(inplace=True)  # Remove duplicate entries
        df.to_csv(file_name, index=False)
        print(f"Analysis results saved to {file_name}")
    else:
        print("No results to save.")

if __name__ == "__main__":
    main()
