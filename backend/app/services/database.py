"""
Database service that abstracts local JSON storage and AWS DynamoDB.
Automatically detects if AWS credentials are available and falls back to local storage.
"""
import json
import os
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from app.core.config import settings

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        self.local_db_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
            "local_db.json"
        )
        self.use_aws = False
        self.dynamodb = None
        self.cases_table = None
        self.evidence_table = None
        
        # Try to initialize AWS DynamoDB if credentials are available
        if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
            try:
                import boto3
                self.dynamodb = boto3.resource(
                    'dynamodb',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_REGION
                )
                self.cases_table = self.dynamodb.Table(settings.DYNAMODB_TABLE_CASES)
                self.evidence_table = self.dynamodb.Table(settings.DYNAMODB_TABLE_EVIDENCE)
                self.use_aws = True
                logger.info("Using AWS DynamoDB for database operations")
            except Exception as e:
                logger.warning(f"Failed to initialize AWS DynamoDB: {e}. Using local database.")
                self.use_aws = False
        else:
            logger.info("Using local JSON database (AWS credentials not configured)")
        
        # Initialize local database if needed
        if not self.use_aws:
            self._init_local_db()
    
    def _init_local_db(self):
        """Initialize local JSON database if it doesn't exist."""
        if not os.path.exists(self.local_db_path):
            with open(self.local_db_path, 'w') as f:
                json.dump({"cases": {}, "evidence": {}}, f, indent=4)
            logger.info(f"Created new local database at {self.local_db_path}")
    
    def _read_local_db(self) -> Dict:
        """Read the local JSON database."""
        try:
            with open(self.local_db_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"cases": {}, "evidence": {}}
    
    def _write_local_db(self, data: Dict):
        """Write to the local JSON database."""
        with open(self.local_db_path, 'w') as f:
            json.dump(data, f, indent=4)
    
    def list_cases(self) -> List[Dict]:
        """List all cases."""
        if self.use_aws:
            try:
                response = self.cases_table.scan()
                return response.get('Items', [])
            except Exception as e:
                logger.error(f"Error listing cases from DynamoDB: {e}")
                return []
        else:
            db = self._read_local_db()
            return list(db.get("cases", {}).values())
    
    def get_case(self, case_id: str) -> Optional[Dict]:
        """Get a specific case by ID."""
        if self.use_aws:
            try:
                response = self.cases_table.get_item(Key={'id': case_id})
                return response.get('Item')
            except Exception as e:
                logger.error(f"Error getting case from DynamoDB: {e}")
                return None
        else:
            db = self._read_local_db()
            return db.get("cases", {}).get(case_id)
    
    def create_case(self, case_data: Dict) -> Dict:
        """Create a new case."""
        if self.use_aws:
            try:
                self.cases_table.put_item(Item=case_data)
                return case_data
            except Exception as e:
                logger.error(f"Error creating case in DynamoDB: {e}")
                raise
        else:
            db = self._read_local_db()
            case_id = case_data.get('id')
            db["cases"][case_id] = case_data
            self._write_local_db(db)
            return case_data
    
    def update_case(self, case_id: str, case_data: Dict) -> Dict:
        """Update an existing case."""
        if self.use_aws:
            try:
                self.cases_table.put_item(Item=case_data)
                return case_data
            except Exception as e:
                logger.error(f"Error updating case in DynamoDB: {e}")
                raise
        else:
            db = self._read_local_db()
            if case_id in db["cases"]:
                db["cases"][case_id].update(case_data)
                self._write_local_db(db)
                return db["cases"][case_id]
            return None
    
    def list_case_evidence(self, case_id: str) -> List[Dict]:
        """List all evidence for a specific case."""
        if self.use_aws:
            try:
                response = self.evidence_table.query(
                    IndexName='case_id-index',
                    KeyConditionExpression='case_id = :case_id',
                    ExpressionAttributeValues={':case_id': case_id}
                )
                return response.get('Items', [])
            except Exception as e:
                logger.error(f"Error listing evidence from DynamoDB: {e}")
                return []
        else:
            case = self.get_case(case_id)
            if case:
                return case.get("evidence", [])
            return []
    
    def get_evidence_metadata(self, evidence_id: str) -> Optional[Dict]:
        """Get metadata for a specific evidence item."""
        if self.use_aws:
            try:
                response = self.evidence_table.get_item(Key={'evidence_id': evidence_id})
                return response.get('Item')
            except Exception as e:
                logger.error(f"Error getting evidence from DynamoDB: {e}")
                return None
        else:
            db = self._read_local_db()
            return db.get("evidence", {}).get(evidence_id)
    
    def store_evidence_metadata(self, metadata: Dict):
        """Store evidence metadata."""
        if self.use_aws:
            try:
                self.evidence_table.put_item(Item=metadata)
            except Exception as e:
                logger.error(f"Error storing evidence in DynamoDB: {e}")
                raise
        else:
            db = self._read_local_db()
            evidence_id = metadata.get('evidence_id')
            db["evidence"][evidence_id] = metadata
            self._write_local_db(db)
    
    def add_evidence_to_case(self, case_id: str, evidence_metadata: Dict):
        """Add evidence metadata to a case's evidence list."""
        case = self.get_case(case_id)
        if case:
            if "evidence" not in case:
                case["evidence"] = []
            case["evidence"].append(evidence_metadata)
            case["updatedAt"] = str(datetime.now())
            self.update_case(case_id, case)
    
    def update_evidence_in_case(self, case_id: str, evidence_id: str, updated_metadata: Dict):
        """Update evidence metadata within a case."""
        case = self.get_case(case_id)
        if case and "evidence" in case:
            for i, ev in enumerate(case["evidence"]):
                if ev.get("evidence_id") == evidence_id:
                    case["evidence"][i].update(updated_metadata)
                    case["updatedAt"] = str(datetime.now())
                    self.update_case(case_id, case)
                    break

# Global database instance
db = DatabaseService()
