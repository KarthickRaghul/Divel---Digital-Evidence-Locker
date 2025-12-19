import boto3
import os
import sys
import uuid
import datetime

# Add backend to path to import config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.config import settings

def check_aws():
    print(f"Checking AWS Connection to Region: {settings.AWS_REGION}")
    
    # 1. Check DynamoDB (Read/Write)
    print("\n--- Checking DynamoDB ---")
    try:
        ddb = boto3.resource(
            'dynamodb',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        table = ddb.Table(settings.DYNAMODB_TABLE_CASES)
        
        # Write Test
        try:
            test_id = str(uuid.uuid4())
            table.put_item(Item={'id': test_id, 'check': 'write_test'})
            print(f"[OK] DynamoDB Write (PutItem) successful.")
            table.delete_item(Key={'id': test_id})
        except Exception as e:
            print(f"[FAIL] DynamoDB Write failed: {e}")
            
    except Exception as e:
        print(f"[FAIL] DynamoDB Connection failed: {e}")

    # 2. Check S3 (Write) - CRITICAL
    print("\n--- Checking S3 Permissions (CRITICAL) ---")
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        bucket_name = settings.S3_BUCKET_NAME
        print(f"Target Bucket: {bucket_name}")
        
        try:
            s3.put_object(Bucket=bucket_name, Key="test_access.txt", Body=b"check")
            print(f"[OK] S3 Upload (PutObject) successful!")
            s3.delete_object(Bucket=bucket_name, Key="test_access.txt")
        except Exception as e:
            print(f"[FAIL] S3 Upload failed (Access Denied?): {e}")
            
    except Exception as e:
        print(f"[FAIL] S3 Connection failed: {e}")

    # 3. Check Lambda (Can we list/invoke?)
    print("\n--- Checking Lambda Permissions ---")
    try:
        lam = boto3.client(
            'lambda',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        try:
            funcs = lam.list_functions(MaxItems=5)
            print("[OK] ListFunctions successful. Found:")
            for f in funcs.get('Functions', []):
                print(f" - {f['FunctionName']}")
        except Exception as e:
             print(f"[FAIL] Lambda ListFunctions failed: {e}")
             
    except Exception as e:
        print(f"[FAIL] Lambda Client Init failed: {e}")

if __name__ == "__main__":
    check_aws()
