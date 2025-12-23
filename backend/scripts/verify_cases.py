import sys
import os
import boto3
import json

# Add backend directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.core.config import settings

def verify_cases():
    print("Verifying cases in DynamoDB...")
    
    try:
        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        
        table = dynamodb.Table(settings.DYNAMODB_TABLE_CASES)
        
        response = table.scan()
        items = response['Items']
        print(f"Total cases found: {len(items)}")
        
        for item in items:
            print(f"- {item.get('caseNumber', 'N/A')}: {item.get('district', 'N/A')} ({item.get('unit', 'N/A')})")

    except Exception as e:
        print(f"❌ Failed to verify cases: {e}")

if __name__ == "__main__":
    verify_cases()
