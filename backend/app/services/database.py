import boto3
from app.core.config import settings
import uuid
from datetime import datetime

class DatabaseService:
    def __init__(self):
        self.dynamodb = None
        if settings.AWS_ACCESS_KEY_ID:
            self.dynamodb = boto3.resource(
                'dynamodb',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
            self.cases_table = self.dynamodb.Table(settings.DYNAMODB_TABLE_CASES)
            self.evidence_table = self.dynamodb.Table(settings.DYNAMODB_TABLE_EVIDENCE)
        
        # In-memory fallback
        self.mock_cases = {}
        self.mock_evidence = {}

    def create_case(self, case_data: dict):
        if self.dynamodb:
            self.cases_table.put_item(Item=case_data)
        else:
            self.mock_cases[case_data['id']] = case_data
        return case_data

    def get_case(self, case_id: str):
        if self.dynamodb:
            response = self.cases_table.get_item(Key={'id': case_id})
            return response.get('Item')
        else:
            return self.mock_cases.get(case_id)
            
    def list_cases(self):
        if self.dynamodb:
            response = self.cases_table.scan()
            return response.get('Items', [])
        else:
            return list(self.mock_cases.values())

    def store_evidence_metadata(self, evidence_data: dict):
        if self.dynamodb:
            self.evidence_table.put_item(Item=evidence_data)
        else:
            self.mock_evidence[evidence_data['evidence_id']] = evidence_data
        return evidence_data

    def get_evidence_metadata(self, case_id: str, evidence_id: str):
         if self.dynamodb:
            try:
                response = self.evidence_table.get_item(Key={'case_id': case_id, 'evidence_id': evidence_id})
                return response.get('Item')
            except Exception as e:
                print(f"Error fetching evidence: {e}")
                return None
         else:
             return self.mock_evidence.get(evidence_id)

    def list_case_evidence(self, case_id: str):
        if self.dynamodb:
            try:
                from boto3.dynamodb.conditions import Key
                response = self.evidence_table.query(
                    KeyConditionExpression=Key('case_id').eq(case_id)
                )
                return response.get('Items', [])
            except Exception as e:
                print(f"Error querying evidence: {e}")
                return []
        else:
            # Filter mock evidence by case_id (assuming mock structure has case_id)
            return [e for e in self.mock_evidence.values() if e.get('case_id') == case_id]

    def add_evidence_to_case(self, case_id: str, evidence_data: dict):
        if self.dynamodb:
            try:
                # Append to list if supported, or just ensure it's queryable via secondary index
                # For this specific data model where Case has 'evidence' list:
                from botocore.exceptions import ClientError
                
                # Check if evidence list exists, if not create, then append
                # This is a bit complex in DynamoDB efficiently without risk of overwriting
                # simpler approach: get, append, put
                case = self.cases_table.get_item(Key={'id': case_id}).get('Item')
                if case:
                    if 'evidence' not in case:
                        case['evidence'] = []
                    # Avoid duplicates
                    if not any(e['evidence_id'] == evidence_data['evidence_id'] for e in case['evidence']):
                        case['evidence'].append(evidence_data)
                        self.cases_table.put_item(Item=case)
            except Exception as e:
                print(f"Error adding evidence to case: {e}")
        else:
            case = self.mock_cases.get(case_id)
            if case:
                if 'evidence' not in case:
                    case['evidence'] = []
                case['evidence'].append(evidence_data)

    def update_evidence_in_case(self, case_id: str, evidence_id: str, updates: dict):
        # Update inside the nested list in Case object
        if self.dynamodb:
            try:
                case = self.cases_table.get_item(Key={'id': case_id}).get('Item')
                if case and 'evidence' in case:
                    for i, ev in enumerate(case['evidence']):
                        if ev['evidence_id'] == evidence_id:
                            # Update fields
                            case['evidence'][i].update(updates)
                            # Also update the standalone evidence table entry if needed
                            # self.store_evidence_metadata(case['evidence'][i]) 
                            break
                    self.cases_table.put_item(Item=case)
            except Exception as e:
                print(f"Error updating evidence in case: {e}")
        else:
            case = self.mock_cases.get(case_id)
            if case and 'evidence' in case:
                 for i, ev in enumerate(case['evidence']):
                        if ev['evidence_id'] == evidence_id:
                            case['evidence'][i].update(updates)
                            break


db = DatabaseService()
