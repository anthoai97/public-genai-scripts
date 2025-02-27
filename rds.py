import boto3
import json
import datetime

def json_serializer(obj):
    """Convert datetime objects to string format for JSON serialization."""
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

def get_rds_instance_details(instance_id):
    client = boto3.client('rds')
    ec2_client = boto3.client('ec2')
    
    # Get instance details
    response = client.describe_db_instances(DBInstanceIdentifier=instance_id)
    instance_details = response['DBInstances'][0]
    
    # Get parameter group details
    parameter_group_name = instance_details['DBParameterGroups'][0]['DBParameterGroupName']
    param_response = client.describe_db_parameters(DBParameterGroupName=parameter_group_name)
    parameters = param_response['Parameters']
    
    # Get security groups
    security_groups = instance_details.get('VpcSecurityGroups', [])
    security_group_details = []
    
    for sg in security_groups:
        sg_id = sg['VpcSecurityGroupId']
        sg_response = ec2_client.describe_security_groups(GroupIds=[sg_id])
        security_group_details.append(sg_response['SecurityGroups'][0])
    
    # Get option groups
    option_group_name = instance_details['OptionGroupMemberships'][0]['OptionGroupName']
    option_response = client.describe_option_groups(OptionGroupName=option_group_name)
    option_groups = option_response['OptionGroupsList']
    
    # Aggregate all settings
    rds_settings = {
        'DBInstance': instance_details,
        'DBParameters': parameters,
        'SecurityGroups': security_group_details,
        'OptionGroups': option_groups
    }
    
    return rds_settings

def export_rds_settings(instance_id, output_file='rds_settings.json'):
    settings = get_rds_instance_details(instance_id)
    
    with open(output_file, 'w') as f:
        json.dump(settings, f, indent=4, default=json_serializer)
    
    print(f"RDS settings exported to {output_file}")

# Example usage
if __name__ == "__main__":
    rds_instance_id = "your-rds-instance-id"  # Replace with your RDS instance ID
    export_rds_settings(rds_instance_id)
