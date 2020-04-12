#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import boto3
import os


# environment vars
FLEET_TABLE = os.getenv('FLEET_TABLE_NAME')
# boto3 config
dynamodb_resource = boto3.resource('dynamodb')
fleet_table = dynamodb_resource.Table(FLEET_TABLE)

def lambda_handler(event, context):
    print('request: {}'.format(json.dumps(event)))
    body = json.loads(event["body"])
    category = body["category"]
    print(f'category is : {category}')
    table_response = fleet_table.get_item(
        Key={'category': category}
    )
    item = table_response.get('Item')
    print(f'table response {item}')
    id = str(item.get('id'))
    item['id']= id
    # data = {
    #     "cars": [{
    #         "id": 0,
    #         "status": "en_route"
    #     }, {
    #         "id": 1,
    #         "status": "on_standby"
    #     }],
    #     "trucks": [{
    #         "id": 0,
    #         "status": "on_standby"
    #     }, {
    #         "id": 1,
    #         "status": "en_route"
    #     }]
    # }


    return {'statusCode': 200, 'body': json.dumps(item)}
