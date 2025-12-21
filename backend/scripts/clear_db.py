import sys
import os
import boto3

# Add backend directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.core.config import settings

def clear_table(table_name):
    print(f"Clearing table: {table_name}...")
    try:
        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        
        table = dynamodb.Table(table_name)
        
        # Scan and delete is inefficient for large tables but fine for dev/test
        scan = table.scan()
        with table.batch_writer() as batch:
            for each in scan['Items']:
                # DynamoDB delete requires the Primary Key. 
                # We need to know the key structure.
                # Based on previous code, 'id' seems to be the PK for cases.
                # For evidence, it might be composite.
                # Let's inspect the key schema from the table description.
                
                key_dict = {}
                for key_schema in table.key_schema:
                    key_name = key_schema['AttributeName']
                    key_dict[key_name] = each[key_name]
                
                batch.delete_item(Key=key_dict)
                
        print(f"✅ Cleared {scan['Count']} items from {table_name}")
        
    except Exception as e:
        print(f"❌ Failed to clear {table_name}: {e}")

if __name__ == "__main__":
    confirm = input("Are you sure you want to delete ALL data? (y/n): ")
    if confirm.lower() == 'y':
        clear_table(settings.DYNAMODB_TABLE_CASES)
        clear_table(settings.DYNAMODB_TABLE_EVIDENCE)
        print("Done.")
    else:
        print("Operation cancelled.")
