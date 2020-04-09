#!/usr/bin/env python3

from aws_cdk import core

from fleetapi.fleetapi_stack import FleetapiStack


app = core.App()
FleetapiStack(app, "fleetapi")

app.synth()
