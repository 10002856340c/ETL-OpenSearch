import requests
import json
from os import path
import aws_cdk as core
import os
from importlib.resources import path
from aws_cdk import (
    aws_events as events,
    aws_lambda as lambda_,
    aws_ec2 as ec2,
    aws_iam as iam_,
    aws_events_targets as targets,
    App, Duration, Stack
)


class OpenSearchEtlStack(Stack):
    def __init__(self, app: App, id: str, stage: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        shared_values = self.get_variables(self, stage)

        Ubits_layers = lambda_.LayerVersion.from_layer_version_arn(self, shared_values['layer_name_db'],
                                                                   layer_version_arn=shared_values['layer_arn_db'])
        lambda_role = iam_.Role.from_role_arn(self, shared_values['lambda_role_name'],
                                              role_arn=shared_values['rol_lambda_id'])
        vpc = ec2.Vpc.from_lookup(
            self, shared_values['vpc_name'], vpc_id=shared_values['vpc_id'])
        subnetid1 = ec2.Subnet.from_subnet_id(
            self, shared_values['subnet1'], shared_values['subnet1_id'])
        subnetid2 = ec2.Subnet.from_subnet_id(
            self, shared_values['subnet2'], shared_values['subnet2_id'])
        subnets = ec2.SubnetSelection(subnets=[subnetid1, subnetid2])

        ubitsTestBalancer_sg = ec2.SecurityGroup.from_security_group_id(
            self, shared_values['sg_name'], shared_values['sg_id'], mutable=False)

        lambdaFn = lambda_.Function(
            self, "OpenSearchEtlStack",
            environment=shared_values,
            code=lambda_.Code.from_asset("./files/"),
            handler="function.apiMain",
            vpc=vpc,
            vpc_subnets=subnets,
            security_groups=[ubitsTestBalancer_sg],
            role=lambda_role,
            timeout=Duration.seconds(300),
            runtime=lambda_.Runtime.PYTHON_3_8,
            layers=[Ubits_layers],
            memory_size=512
        )

        rule = events.Rule(
            self, "Rule",
            schedule=events.Schedule.cron(
                minute='0',
                hour='6-18/12',
                month='*',
                week_day='MON-FRI',
                year='*'),
        )

        rule.add_target(targets.LambdaFunction(lambdaFn))

    @staticmethod
    def get_variables(self, stage):
        shared_values = self.node.try_get_context('shared_values')
        return shared_values[stage]


env_environment = os.getenv("CDK_ENVIRONMENT")
env_stack_name = os.getenv("CDK_STACK_NAME")

app = App()

OpenSearchEtlStack(app, env_stack_name,
    env=core.Environment(account= os.environ['CDK_DEFAULT_ACCOUNT'], region= os.environ['CDK_DEFAULT_REGION']),
    stage=env_environment)

app.synth()
