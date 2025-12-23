import sys
import os
import boto3
import json
from decimal import Decimal

# Helper to handle Decimal serialization
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

# Add backend directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.core.config import settings

def inspect_evidence(case_number=None):
    print(f"Inspecting evidence for Case Number: {case_number}")
    
    try:
        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        
        cases_table = dynamodb.Table(settings.DYNAMODB_TABLE_CASES)
        
        # 1. Find the case by CaseNumber
        scan_response = cases_table.scan(
            FilterExpression=boto3.dynamodb.conditions.Attr('caseNumber').eq(case_number)
        )
        
        items = scan_response['Items']
        if not items:
            print(f"❌ Case {case_number} not found.")
            return

        case = items[0]
        print(f"✅ Found Case ID: {case['id']}")
        
        evidence_list = case.get('evidence', [])
        print(f"Evidence Count: {len(evidence_list)}")
        
        for idx, ev in enumerate(evidence_list):
            print(f"\n--- Evidence #{idx+1} ---")
            
            # Check for Wrapped Structure
            meta = ev.get('metadata', {})
            # If metadata is empty, maybe it's the old flat structure?
            if not meta:
                meta = ev # Fallback
            
            evidence_id = meta.get('evidence_id') or ev.get('id')
            filename = meta.get('filename') or ev.get('name')
            ai_summary = meta.get('ai_summary')
            
            print(f"ID: {evidence_id}")
            print(f"Filename: {filename}")
            print(f"AI Summary: {ai_summary[:50]}..." if ai_summary else "AI Summary: MISSING")
            
            kg = meta.get('knowledge_graph')
            if kg:
                nodes = kg.get('nodes', [])
                links = kg.get('links', [])
                print(f"Knowledge Graph: {len(nodes)} Nodes, {len(links)} Links")
                if nodes:
                    print(f"Sample Node: {nodes[0]}")
            else:
                print("Knowledge Graph: MISSING")

    except Exception as e:
        print(f"❌ Failed to inspect cases: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        inspect_evidence(sys.argv[1])
    else:
        print("Please provide a Case Number as argument.")
