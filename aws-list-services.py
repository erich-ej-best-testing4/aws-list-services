import boto3
import argparse

#########################################################################################
# aws-list-services.py                                                                  #
#                                                                                       #
#  Function......Lists the following                                                    #                
#       VPC,EC2,Loadbalancer,LambdaSecurityGroups,ECS,EKS,SNS,Dynamo,                   #
#       EMR,RDS,Redshift,ElasticIP                                                       #
#  Requires......https://aws.amazon.com/sdk-for-python/                                 #
#  Released......March 16, 2021                                                         #
#  Scripter......                                                                       #
#  Invoke........python3 aws-list-services.py                                           #
#                                                                                       #
#########################################################################################
#                                                                                       #
# Parameters -r and -v                                                                  #
# python3 aws-list-services.py -r us-east-1                                             #
# python3 aws-list-services.py -v non-verbose                                           #
# python3 aws-list-services.py -v non-verbose   -r us-east-1                            #
#                                                                                       #      
#########################################################################################

class myList:
    def GetRegions(self):
        RegionList = []
        region = boto3.client('ec2')
        Response = region.describe_regions()
        for RegionCount in range(len(Response['Regions'])):
            RegionList.append(Response['Regions'][RegionCount]['RegionName'])
        if selected_region is not None:
            RegionList = [selected_region]
        print("Number of Regions {}".format(len(RegionList)))
        print("Regions::")
        print(RegionList)
        print("**********************************")
        return RegionList

    def ListEc2Instance(self):
        # Fetch domain
        client = boto3.client('route53domains')
        response = client.list_domains()
        if len(response['Domains']) != 0:
            for each in response['Domains']:
                print(
                    "Route 53 --> DomainName : {}. AutoRenewEnabled? : {}. ExpiryDate : {}.".format(each['DomainName'],
                                                                                                    each['AutoRenew'],
                                                                                                    each['Expiry']))
        else:
            if NoResLog:
                print("No DNS Record found")
        print("**********************************")

        FetchRegionList = self.GetRegions()
        for Region in range(len(FetchRegionList)):
            print("Region : --> {}".format(FetchRegionList[Region]))
            # Find all VPC in a Region
            Ec2 = boto3.client('ec2', region_name=FetchRegionList[Region])
            vpcs = Ec2.describe_vpcs()
            for vpc in vpcs['Vpcs']:
                print("VPC --> VPCId : {}. CidrBlock : {}. DefaultVPC? : {}. ".format(vpc['VpcId'], vpc['CidrBlock'],
                                                                                      vpc['IsDefault']))

            # Fetch security groups used in Region
            GetSecurityGroup = Ec2.describe_security_groups()
            if len(GetSecurityGroup['SecurityGroups']) != 0:
                for SecurityGroupCount in range(len(GetSecurityGroup['SecurityGroups'])):
                    GroupId = GetSecurityGroup['SecurityGroups'][SecurityGroupCount]['GroupId']
                    VpcId = GetSecurityGroup['SecurityGroups'][SecurityGroupCount]['VpcId']
                    GroupName = GetSecurityGroup['SecurityGroups'][SecurityGroupCount]['GroupName']
                    print("Security --> Groupid : {}. VpcId : {}. GroupName : {}.".format(GroupId, VpcId, GroupName))
            else:
                if NoResLog:
                    print("No security group available for this region.")

            # fetch secretsmanager list
            sm = boto3.client('secretsmanager', region_name=FetchRegionList[Region])
            response = sm.list_secrets()
            if len(response['SecretList']) != 0:
                for each in response['SecretList']:
                    if "LastAccessedDate" in each:
                        print("SecretsManager --> Name : {}. LastChangedDate : {}. LastAccessedDate : {}.".format(
                            each['Name'], each['LastChangedDate'], each['LastAccessedDate']))
                    else:
                        print("SecretsManager --> Name : {}. LastChangedDate : {}.".format(
                            each['Name'], each['LastChangedDate']))
            else:
                if NoResLog:
                    print("No Secrets in Region.")

            # ec2 instances
            GetInstance = Ec2.describe_instances()
            if len(GetInstance['Reservations']) != 0:
                for InstanceCount in range(len(GetInstance['Reservations'])):
                    InstID = GetInstance['Reservations'][InstanceCount]['Instances'][0]['InstanceId']
                    InstType = GetInstance['Reservations'][InstanceCount]['Instances'][0]['InstanceType']
                    InstState = GetInstance['Reservations'][InstanceCount]['Instances'][0]['State']['Name']
                    print(
                        "EC2 Instance --> id : {}. InstanceType: {}. Status : {}.".format(InstID, InstType, InstState))
            else:
                if NoResLog:
                    print("No EC2 Instance(s) running in Region.")

            # Find all volumes used in Region:
            GetVolume = Ec2.describe_volumes()
            if len(GetVolume['Volumes']) != 0:
                for VolumeCount in range(len(GetVolume['Volumes'])):
                    GetVolumeID = GetVolume['Volumes'][VolumeCount]['VolumeId']
                    GetDiskState = GetVolume['Volumes'][VolumeCount]['State']
                    GetVolumeType = GetVolume['Volumes'][VolumeCount]['VolumeType']
                    GetVolumeSize = GetVolume['Volumes'][VolumeCount]['Size']
                    print("Disk --> Volumeid : {}. VolumeState: {}. VolumeType: {}. VolumeSize {}".format(GetVolumeID,
                                                                                                          GetDiskState, \
                                                                                                          GetVolumeType,
                                                                                                          GetVolumeSize))
            else:
                if NoResLog:
                    print("No Volumes found in Region.")

            # Find all ELBv2 loadbalancer running in Region.
            ELBLoad = boto3.client('elbv2', region_name=FetchRegionList[Region])
            ELBv2 = ELBLoad.describe_load_balancers()
            if len(ELBv2['LoadBalancers']) != 0:
                for ElbCount in range(len(ELBv2['LoadBalancers'])):
                    LBname = ELBv2['LoadBalancers'][ElbCount]['LoadBalancerName']
                    LBState = ELBv2['LoadBalancers'][ElbCount]['State']['Code']
                    LBType = ELBv2['LoadBalancers'][ElbCount]['Type']
                    print("Loadbalancer --> LBName : {}. LBState : {}. LBType : {}".format(LBname, LBState, LBType))
            else:
                if NoResLog:
                    print("No LoadBalancer found in Region.")

            # Find all Lambda functions running in Region.
            Lmbda = boto3.client('lambda', region_name=FetchRegionList[Region])
            LambdaLst = Lmbda.list_functions()
            if len(LambdaLst['Functions']) != 0:
                for FncCount in range(len(LambdaLst['Functions'])):
                    FncName = LambdaLst['Functions'][FncCount]['FunctionName']
                    FncMem = LambdaLst['Functions'][FncCount]['MemorySize']
                    FncCodeSize = LambdaLst['Functions'][FncCount]['CodeSize']
                    FncRuntime = LambdaLst['Functions'][FncCount]['Runtime']
                    print("Lambda Function --> Name : {}. Memory : {}. CodeSize : {}. Runtime : {}.".format(FncName, \
                                                                                                            FncMem,
                                                                                                            FncCodeSize,
                                                                                                            FncRuntime))
            else:
                if NoResLog:
                    print("No Lambda function available in Region.")

            # Fetch ecs
            ecs = boto3.client('ecs', region_name=FetchRegionList[Region])
            response = ecs.list_clusters(maxResults=100)
            if len(response['clusterArns']) != 0:
                desc = ecs.describe_clusters(
                    clusters=response['clusterArns'])
                [print("ECS --> ClusterName : {}. clusterArn : {}. clusterStatus : {}. registeredContainerInstancesCount : {}. runningTasksCount : {}. pendingTasksCount : {}. activeServicesCount : {}".
                    format(each['clusterName'], each['clusterArn'], each['status'], each['registeredContainerInstancesCount'], each['runningTasksCount'],
                           each['pendingTasksCount'], each['activeServicesCount'])) for each in desc['clusters']]
            else:
                if NoResLog:
                    print("No ECS Cluster(s) running in Region.")

            # Fetch eks
            eks = boto3.client('eks', region_name=FetchRegionList[Region])
            response = eks.list_clusters(maxResults=100)
            if len(response['clusters']) != 0:
                for each in response['clusters']:
                    eks_cluster_det = eks.describe_cluster(
                        name=each
                    )
                    print("EKS --> ClusterName : {}. ClusterStatus : {}. ClusterArn : {}.".format(
                        eks_cluster_det['cluster']['name'], eks_cluster_det['cluster']['status'],
                        eks_cluster_det['cluster']['arn']))
            else:
                if NoResLog:
                    print("No EKS Cluster(s) running in Region.")

            # fetch sns topics
            sns = boto3.client('sns',region_name=FetchRegionList[Region])
            response = sns.list_topics()
            if len(response['Topics'])!=0:
                for each in response['Topics']:
                    topic_det = sns.get_topic_attributes(
                        TopicArn=each['TopicArn']
                    )
                    print("SNS --> TopicDisplayName : {}. TopicArn : {}. SubscriptionsConfirmed : {}.".format(
                        topic_det['Attributes']['DisplayName'],topic_det['Attributes']['TopicArn'],topic_det['Attributes']['SubscriptionsConfirmed']))
            else:
                if NoResLog:
                    print("No SNS topics found in Region.")

            # fetch dynamodb tables
            ddy = boto3.client('dynamodb',region_name=FetchRegionList[Region])
            response = ddy.list_tables()
            if len(response['TableNames'])!=0:
                for each in response['TableNames']:
                    print("DynamoDB --> TableName : {} .".format(
                        each))
            else:
                if NoResLog:
                    print("No DynamoDB table found in Region.")

            # fetch sqs
            sqs = boto3.client('sqs', region_name=FetchRegionList[Region])
            response = sqs.list_queues()
            if "QueueUrls" in response:
                for each in response['QueueUrls']:
                    print("SQS --> QueueUrl : {} .".format(
                        each))
            else:
                if NoResLog:
                    print("No SQS queue found in Region.")

            # fetch running emr
            emr = boto3.client('emr', region_name=FetchRegionList[Region])
            response = emr.list_clusters(
                ClusterStates=['STARTING','BOOTSTRAPPING','RUNNING','WAITING','TERMINATING','TERMINATED','TERMINATED_WITH_ERRORS' ],
            )
            if len(response['Clusters']) != 0:
                for each in response['Clusters']:
                    print("EMR --> ClusterName : {}. ClusterID : {} . Status : {} . NormalizedInstanceHours : {}".
                          format(each['Name'],each['Id'], each['Status']['State'], each['NormalizedInstanceHours']))
            else:
                if NoResLog:
                    print("No EMR cluster found in Region.")

            # fetch rds
            rds = boto3.client('rds', region_name=FetchRegionList[Region])
            response = rds.describe_db_instances()
            if len(response['DBInstances']) != 0:
                for each in response['DBInstances']:
                    print(
                        "RDS --> DBName : {}. DBInstanceClass : {} . DBInstanceStatus : {} . DBInstanceIdentifier : {}".
                        format(each['DBName'], each['DBInstanceClass'], each['DBInstanceStatus'],
                               each['DBInstanceIdentifier']))
            else:
                if NoResLog:
                    print("No RDS cluster found in Region.")

            # fetch redshift clusters
            redshift = boto3.client('redshift', region_name=FetchRegionList[Region])
            response = redshift.describe_clusters()
            if len(response['Clusters']) != 0:
                for each in response['Clusters']:
                    print(
                        "RDS --> DBName : {}. NodeType : {} . ClusterStatus : {} . ClusterIdentifier : {}".
                            format(each['DBName'], each['NodeType'], each['ClusterStatus'],
                                   each['ClusterIdentifier']))
            else:
                if NoResLog:
                    print("No Redshift cluster found in Region.")

            # fetch elasticip
            response = Ec2.describe_addresses()
            if len(response['Addresses']) != 0:
                for each in response['Addresses']:
                    print("ElasicIP --> EIP : {}.".format(each['PublicIp']))
            else:
                if NoResLog:
                    print("No Elastic IP found in Region.")

            print("**********************************")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", dest="verbose", required=False, default="verbose")
    parser.add_argument("-r", "--region", dest="region", required=False, default=None)
    args = parser.parse_args()
    verbose = args.verbose
    selected_region = args.region
    NoResLog = True
    if verbose == 'non-verbose':
        NoResLog = False
    RunQuery = myList()
    RunQuery.ListEc2Instance()