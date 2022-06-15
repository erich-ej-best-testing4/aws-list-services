# aws-list-services

List out running aws services by region
“aws_list_services.py” is a program that will list by region the AWS services that are running or are configured.  The initial idea of this was to find “if a big bill will be sent” after the month finishes.

## Getting started
If you have AWS Command Line configured and working so there is not any security credential issues this should work.

Python 3 is required

## Usage
ensure that you are in the folder with this program
python3 aws-list-services.py

## Badges
<pre>
Parameters -r and -v                                                                  #
python3 aws-list-services.py -r us-east-1                                             #
python3 aws-list-services.py -v non-verbose                                           #
python3 aws-list-services.py -v non-verbose   -r us-east-1  
</pre>
## About the Programmer 
Let us be clear “not a programmer” and only dream and aspire to one day be a “hack”.  This program was an attempt to learn some Python and the Boto3 API and the result to find my AWS Bill.  Moreover, there is a handful of friends along with way from online places; moreover, the NYC Python Meetup, where they were so kind and giving that I am forever in their debt.  The NYC Python Meetups were an awesome learning experience.’
<br>

## Installation
There is many ways to run a python program and python is very versital.  One way to install is using the git command line. 
<br>
git clone https://gitlab.com/advocatediablo/aws-list-services.git
<br>

## Example output 
<pre>
python3 aws-list-services.py   -r us-east-1
No DNS Record found
**********************************
Number of Regions 1
Regions::
['us-east-1']
**********************************
Region : --> us-east-1
VPC --> VPCId : vpc-b43d52cf. CidrBlock : 172.31.0.0/16. DefaultVPC? : True. 
VPC --> VPCId : vpc-0a8d2d94057097c21. CidrBlock : 172.16.0.0/16. DefaultVPC? : False. 
VPC --> VPCId : vpc-062211fad5b8dbf48. CidrBlock : 192.168.0.0/16. DefaultVPC? : False. 
Security --> Groupid : sg-0876a738278564aba. VpcId : vpc-062211fad5b8dbf48. GroupName : default.
Security --> Groupid : sg-09dfeaaf707fdc95b. VpcId : vpc-b43d52cf. GroupName : launch-wizard-4.
Security --> Groupid : sg-0f5089d598648deba. VpcId : vpc-b43d52cf. GroupName : launch-wizard-2.
Security --> Groupid : sg-06f4c3c85b20ab192. VpcId : vpc-b43d52cf. GroupName : launch-wizard-3.
Security --> Groupid : sg-67c0322e. VpcId : vpc-b43d52cf. GroupName : default.
Security --> Groupid : sg-0fea3368d889f845e. VpcId : vpc-0a8d2d94057097c21. GroupName : default.
Security --> Groupid : sg-048c7d5920b69ad78. VpcId : vpc-b43d52cf. GroupName : launch-wizard-1.
SecretsManager --> Name : MySecrets. LastChangedDate : 2022-05-11 10:32:56.203000-04:00. LastAccessedDate : 2022-05-14 20:00:00-04:00.
EC2 Instance --> id : i-01758efa6ee12839e. InstanceType: t2.micro. Status : running.
Disk --> Volumeid : vol-01d740e45cbeb99fc. VolumeState: in-use. VolumeType: gp2. VolumeSize 8
No LoadBalancer found in Region.
Lambda Function --> Name : chef_node_cleanup. Memory : 320. CodeSize : 1042409. Runtime : python2.7.
Lambda Function --> Name : bastion. Memory : 128. CodeSize : 1889475. Runtime : nodejs8.10.
Lambda Function --> Name : chef_node_cleanup_terraform. Memory : 128. CodeSize : 1042393. Runtime : python2.7.
Lambda Function --> Name : myServerlessWebpage. Memory : 128. CodeSize : 297. Runtime : python3.6.
No ECS Cluster(s) running in Region.
No EKS Cluster(s) running in Region.
SNS --> TopicDisplayName : BillDetail. TopicArn : arn:aws:sns:us-east-1:346310308399:BillingAlert. SubscriptionsConfirmed : 0.
SNS --> TopicDisplayName : . TopicArn : arn:aws:sns:us-east-1:346310308399:emails. SubscriptionsConfirmed : 2.
No DynamoDB table found in Region.
No SQS queue found in Region.
No EMR cluster found in Region.
No RDS cluster found in Region.
No Redshift cluster found in Region.
No Elastic IP found in Region.
**********************************
</pre> 


## Support
No promises but I care about you being happy.  You can find me on linked in here and let me know any feedback or ask me questions.
<br>
https://www.linkedin.com/in/ejbest/