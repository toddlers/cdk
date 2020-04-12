#!/usr/bin/env python3

from aws_cdk import core

from fleetapi.fleetapi_stack import FleetapiStack


app = core.App()
env_USA = core.Environment(account="<ACCOUNT_ID>", region="us-east-1")
FleetapiStack(app, "fleetapi")

app.synth()
