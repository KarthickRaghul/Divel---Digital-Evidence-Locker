import sys
import os
import boto3
import json
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app.core.config import settings

def dump_case(case_number):
    dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )
    table = dynamodb.Table(settings.DYNAMODB_TABLE_CASES)
    response = table.scan(
        FilterExpression=boto3.dynamodb.conditions.Attr('caseNumber').eq(case_number)
    )
    items = response['Items']
    if items:
        print(json.dumps(items[0], cls=DecimalEncoder, indent=2))
    else:
        print("Case not found")

if __name__ == "__main__":
    dump_case("CR-CYBER-2025-001")
