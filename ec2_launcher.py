import boto3

def get_ec2_client(aws_access_key_id, aws_secret_access_key, region):
    return boto3.client(
        'ec2',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region
    )

def create_key_pair(aws_access_key_id, aws_secret_access_key, region, key_name):
    ec2_client = get_ec2_client(aws_access_key_id, aws_secret_access_key, region)
    response = ec2_client.create_key_pair(KeyName=key_name)
    return response['KeyMaterial']

def get_iam_client(aws_access_key_id, aws_secret_access_key, region):
    return boto3.client(
        'iam',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region
    )

def get_recent_ubuntu_amis(aws_access_key_id, aws_secret_access_key, region, count=3):
    ec2_client = get_ec2_client(aws_access_key_id, aws_secret_access_key, region)
    response = ec2_client.describe_images(
        Owners=['099720109477'],
        Filters=[
            {'Name': 'name', 'Values': ['ubuntu/images/hvm-ssd/ubuntu-22.04-amd64-server-*']},
            {'Name': 'state', 'Values': ['available']}
        ]
    )
    images = sorted(response['Images'], key=lambda x: x['CreationDate'], reverse=True)
    return [{"ImageId": img["ImageId"], "Name": img["Name"]} for img in images[:count]]

def get_recent_amazon_linux_amis(aws_access_key_id, aws_secret_access_key, region, count=3):
    ec2_client = get_ec2_client(aws_access_key_id, aws_secret_access_key, region)
    response = ec2_client.describe_images(
        Owners=['137112412989'],
        Filters=[
            {'Name': 'name', 'Values': ['amzn2-ami-hvm-*-x86_64-gp2']},
            {'Name': 'state', 'Values': ['available']}
        ]
    )
    images = sorted(response['Images'], key=lambda x: x['CreationDate'], reverse=True)
    return [{"ImageId": img["ImageId"], "Name": img["Name"]} for img in images[:count]]

def get_recent_rhel_amis(aws_access_key_id, aws_secret_access_key, region, count=3):
    ec2_client = get_ec2_client(aws_access_key_id, aws_secret_access_key, region)
    response = ec2_client.describe_images(
        Owners=['309956199498'],
        Filters=[
            {'Name': 'name', 'Values': ['RHEL-8.*x86_64*']},
            {'Name': 'state', 'Values': ['available']}
        ]
    )
    images = sorted(response['Images'], key=lambda x: x['CreationDate'], reverse=True)
    return [{"ImageId": img["ImageId"], "Name": img["Name"]} for img in images[:count]]

def get_recent_windows_amis(aws_access_key_id, aws_secret_access_key, region, count=3):
    ec2_client = get_ec2_client(aws_access_key_id, aws_secret_access_key, region)
    response = ec2_client.describe_images(
        Owners=['801119661308'],
        Filters=[
            {'Name': 'name', 'Values': ['Windows_Server-2022-English-Full-Base-*']},
            {'Name': 'state', 'Values': ['available']}
        ]
    )
    images = sorted(response['Images'], key=lambda x: x['CreationDate'], reverse=True)
    return [{"ImageId": img["ImageId"], "Name": img["Name"]} for img in images[:count]]

def get_recent_macos_amis(aws_access_key_id, aws_secret_access_key, region, count=3):
    ec2_client = get_ec2_client(aws_access_key_id, aws_secret_access_key, region)
    response = ec2_client.describe_images(
        Owners=['679593333241'],
        Filters=[
            {'Name': 'name', 'Values': ['amzn-ec2-macos-*-x86_64']},
            {'Name': 'state', 'Values': ['available']}
        ]
    )
    images = sorted(response['Images'], key=lambda x: x['CreationDate'], reverse=True)
    return [{"ImageId": img["ImageId"], "Name": img["Name"]} for img in images[:count]]

def get_latest_ubuntu_ami(aws_access_key_id, aws_secret_access_key, region):
    ec2_client = get_ec2_client(aws_access_key_id, aws_secret_access_key, region)
    response = ec2_client.describe_images(
        Owners=['099720109477'],
        Filters=[
            {'Name': 'name', 'Values': ['ubuntu/images/hvm-ssd/ubuntu-22.04-amd64-server-*']},
            {'Name': 'state', 'Values': ['available']}
        ]
    )
    images = sorted(response['Images'], key=lambda x: x['CreationDate'], reverse=True)
    return images[0]['ImageId'] if images else None

def get_key_pairs(aws_access_key_id, aws_secret_access_key, region):
    ec2_client = get_ec2_client(aws_access_key_id, aws_secret_access_key, region)
    response = ec2_client.describe_key_pairs()
    return [kp['KeyName'] for kp in response['KeyPairs']]

def get_security_groups(aws_access_key_id, aws_secret_access_key, region):
    ec2_client = get_ec2_client(aws_access_key_id, aws_secret_access_key, region)
    response = ec2_client.describe_security_groups()
    return [{'GroupId': sg['GroupId'], 'GroupName': sg['GroupName']} for sg in response['SecurityGroups']]

def get_subnets(aws_access_key_id, aws_secret_access_key, region):
    ec2_client = get_ec2_client(aws_access_key_id, aws_secret_access_key, region)
    response = ec2_client.describe_subnets()
    return [{'SubnetId': sn['SubnetId'], 'CidrBlock': sn['CidrBlock']} for sn in response['Subnets']]

def get_iam_roles(aws_access_key_id, aws_secret_access_key, region):
    iam_client = get_iam_client(aws_access_key_id, aws_secret_access_key, region)
    paginator = iam_client.get_paginator('list_roles')
    roles = []
    for page in paginator.paginate():
        for role in page['Roles']:
            roles.append(role['RoleName'])
    return roles

def launch_instance(
    aws_access_key_id,
    aws_secret_access_key,
    region,
    instance_type,
    ami_id,
    key_name,
    security_group_ids=None,
    subnet_id=None,
    iam_instance_profile=None,
    user_data=None,
    volume_size=8,
    volume_type='gp2',
    tags=None
):
    ec2 = boto3.resource(
        'ec2',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region
    )
    try:
        instance_args = {
            'ImageId': ami_id,
            'MinCount': 1,
            'MaxCount': 1,
            'InstanceType': instance_type,
            'KeyName': key_name,
            'BlockDeviceMappings': [{
                'DeviceName': '/dev/xvda',
                'Ebs': {
                    'VolumeSize': volume_size,
                    'VolumeType': volume_type,
                    'DeleteOnTermination': True
                }
            }],
        }
        if security_group_ids:
            instance_args['SecurityGroupIds'] = security_group_ids
        if subnet_id:
            instance_args['SubnetId'] = subnet_id
        if iam_instance_profile:
            instance_args['IamInstanceProfile'] = {'Name': iam_instance_profile}
        if user_data:
            instance_args['UserData'] = user_data
        if tags:
            instance_args['TagSpecifications'] = [{
                'ResourceType': 'instance',
                'Tags': tags
            }]
        instance = ec2.create_instances(**instance_args)[0]
        instance.wait_until_running()
        instance.reload()
        return {
            'Instance ID': instance.id,
            'State': instance.state['Name'],
            'Type': instance.instance_type,
            'Public IP': instance.public_ip_address,
            'AMI': instance.image_id
        }
    except Exception as e:
        return {"Error": str(e)}

def stop_instance(aws_access_key_id, aws_secret_access_key, region, instance_id):
    ec2 = get_ec2_client(aws_access_key_id, aws_secret_access_key, region)
    ec2.stop_instances(InstanceIds=[instance_id])
    return True

def terminate_instance(aws_access_key_id, aws_secret_access_key, region, instance_id):
    ec2 = get_ec2_client(aws_access_key_id, aws_secret_access_key, region)
    ec2.terminate_instances(InstanceIds=[instance_id])
    return True
