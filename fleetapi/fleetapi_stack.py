#!/usr/bin/env python
import json
from aws_cdk import (core, aws_lambda as _lambda, aws_apigateway as apigw,
                     aws_dynamodb as ddb)


class FleetapiStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        table = ddb.Table(self,
                                'Fleet',
                                read_capacity=5,
                                write_capacity=5,
                                partition_key={
                                    'name': 'category',
                                    'type': ddb.AttributeType.STRING
                                })

        fleet_lambda = _lambda.Function(
            self,
            'FleetHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='fleetapi.lambda_handler',
            environment={
                'FLEET_TABLE_NAME': table.table_name,
            }
        )

        # give permissions to lambda for dynamodb table
        table.grant_read_write_data(fleet_lambda)

        api = apigw.LambdaRestApi(
            self,
            'FleetApi',
            handler=fleet_lambda,
            proxy=False,
            parameters={"Content-Type": "application/json"},
        )
        request_model = api.add_model("RequestModel",
                                      content_type="application/json",
                                      model_name="FleetSchema",
                                      schema={
                                          "schema":
                                          apigw.JsonSchemaVersion.DRAFT4,
                                          "title": "FleetAPI",
                                          "type": apigw.JsonSchemaType.OBJECT,
                                          "properties": {
                                              "category": {
                                                  "type": apigw.JsonSchemaType.STRING,
                                                  "enum": ["cars", "trucks"]
                                              }
                                          },
                                          "required": ["category"]
                                      })
        error_response_model = api.add_model(
            "ErroResponseModel",
            content_type="application/json",
            model_name="ErrorResponseModel",
            schema={
                "schema": apigw.JsonSchemaVersion.DRAFT4,
                "title": "errorResponse",
                "type": apigw.JsonSchemaType.OBJECT,
                "properties": {
                    "state": {
                        "type": apigw.JsonSchemaType.STRING
                    },
                    "message": {
                        "type": apigw.JsonSchemaType.STRING
                    }
                }
            })
        resource = api.root.add_resource("fleet")
        resource.add_method("POST",
                            request_models={
                                "application/json": request_model,
                            },
                            request_parameters={
                                "method.request.header.Content-Type": True,
                            },
                            request_validator_options={
                                "request_validator_name": "fleetapi",
                                "validate_request_body": True,
                                "validate_request_parameters": True,
                            })  # POST /fleet
