import boto3

def tag_rds_parameter_group(parameter_group_name, tags):
    """
    Adds or updates tags on the given RDS DB parameter group.

    :param parameter_group_name: Name of the DB parameter group
    :param tags: Dictionary of tag key-value pairs
    """
    client = boto3.client('rds')

    # Convert dict to AWS tag format
    tag_list = [{'Key': k, 'Value': v} for k, v in tags.items()]

    try:
        # Get the ARN of the parameter group
        response = client.describe_db_parameter_groups(DBParameterGroupName=parameter_group_name)
        arn = response['DBParameterGroups'][0]['DBParameterGroupArn']
        
        # Add tags
        client.add_tags_to_resource(ResourceName=arn, Tags=tag_list)
        print(f"Tags added to RDS parameter group '{parameter_group_name}'.")
    except client.exceptions.DBParameterGroupNotFoundFault:
        print(f"Parameter group '{parameter_group_name}' not found.")
    except Exception as e:
        print(f"Error tagging parameter group: {e}")

# Example usage
if __name__ == "__main__":
    tag_rds_parameter_group(
        parameter_group_name="my-custom-param-group",
        tags={
            "Environment": "dev",
            "Owner": "alice"
        }
    )
