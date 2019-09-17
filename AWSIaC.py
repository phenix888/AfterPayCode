import logging
import boto3
from operator import itemgetter

"""Exercise create_ec2_instance()"""
client = boto3.client('ec2')

filters = [ {
    'Name': 'name',
    'Values': ['amzn-ami-hvm-*']
},{
    'Name': 'description',
    'Values': ['Amazon Linux AMI*']
},{
    'Name': 'architecture',
    'Values': ['x86_64']
},{
    'Name': 'owner-alias',
    'Values': ['amazon']
},{
    'Name': 'state',
    'Values': ['available']
},{
    'Name': 'root-device-type',
    'Values': ['ebs']
},{
    'Name': 'virtualization-type',
    'Values': ['hvm']
},{
    'Name': 'hypervisor',
    'Values': ['xen']
},{
    'Name': 'image-type',
    'Values': ['machine']
} ]

# Use above filters 
response = client.describe_images(
  Filters=filters,
  Owners=[
      'amazon'
  ]
)

# Sort on Creation date Desc
image_details = sorted(response['Images'],key=itemgetter('CreationDate'),reverse=True)
ami_id = image_details[0]['ImageId']
logging.basicConfig(format='%(asctime)s %(message)s')

logging.warning('Script will use Amazon AMI ID :  %s for bulding base customized AMI', ami_id)


#ec2 = boto3.client('ec2')
#response = ec2.create_key_pair(KeyName='AfterPayKey2')
logging.warning('Generating a SSH-key file AfterPayKey.pem whcih can be used to loggin to server ')

#f= open("AfterPayKey2.pem","w+")
#f.write(str(response))
#f.close()

logging.warning('Creating a customised AMI ...')

ec2_client = boto3.client('ec2')
response = ec2_client.run_instances(ImageId=ami_id,
                                            InstanceType='t2.micro',
                                            KeyName='AfterPayKey',
                                            MinCount=1,
                                            MaxCount=1)
 
