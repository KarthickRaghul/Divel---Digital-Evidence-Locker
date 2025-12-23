import sys
import os
import boto3
import uuid
import json
import random
from datetime import datetime, timedelta

# Add backend directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.core.config import settings

# --- SEED DATA ---
SEED_CASE_JSON = """
{
  "dateOfOffence": "2025-12-10",
  "evidence": [
    {
      "name": "email_logs_encrypted.log",
      "uploadedAt": "2025-12-22 00:15:08.151178",
      "metadata": {
        "filename": "email_logs_encrypted.log",
        "content_type": "text/plain",
        "ai_summary": "Forensic analysis of the recovered email logs indicates a coordinated phishing campaign targeting bank employees. The emails originated from an external server (IP 192.168.4.22) and contained malicious attachments disguised as 'Audit_Reports_Q4.pdf'. Key actors identified include 'ZeroCool' (sender alias) and 'J. Smith' (internal recipient).",
        "uploaded_at": "2025-12-22 00:15:08.151164",
        "uploader": "Admin",
        "case_id": "a9111010-65f6-4adf-af3c-af94e244e9a7",
        "uploader_role": "Forensics",
        "tx_hash": "0x7f4c3a1b",
        "evidence_id": "a070677e-823f-4071-a1d7-9ed02da84d3d",
        "knowledge_graph": {
          "links": [
            { "value": "Sent", "source": "ZeroCool", "target": "Phishing Email" },
            { "value": "Received by", "source": "Phishing Email", "target": "J. Smith" },
            { "value": "Operates from", "source": "ZeroCool", "target": "192.168.4.22" },
            { "value": "Targeted", "source": "Phishing Email", "target": "City Bank Server" }
          ],
          "nodes": [
            { "id": "ZeroCool", "group": "Person" },
            { "id": "J. Smith", "group": "Person" },
            { "id": "Phishing Email", "group": "Evidence" },
            { "id": "192.168.4.22", "group": "Location" },
            { "id": "City Bank Server", "group": "Location" }
          ]
        },
        "url": "http://mock-s3/email_logs.log"
      },
      "id": "a070677e-823f-4071-a1d7-9ed02da84d3d",
      "type": "document"
    },
    {
      "name": "atm_cctv_clip.mp4",
      "uploadedAt": "2025-12-22 00:15:08.151182",
      "metadata": {
        "filename": "atm_cctv_clip.mp4",
        "content_type": "video/mp4",
        "ai_summary": "Video surveillance from the ATM at 5th Avenue shows a suspect, male, approx 180cm, wearing a dark hoodie, installing a skimming device at 23:42 on Dec 12th. The suspect was seen entering a 'White Van' (License: DL-4C-1234) shortly after.",
        "uploaded_at": "2025-12-22 00:15:08.151181",
        "uploader": "Admin",
        "case_id": "a9111010-65f6-4adf-af3c-af94e244e9a7",
        "uploader_role": "Forensics",
        "tx_hash": "0x9a2b8c7d",
        "evidence_id": "68508b13-88e4-4cc3-af93-feb0e73a7a87",
        "knowledge_graph": {
          "links": [
            { "value": "Visited", "source": "Suspect A", "target": "ATM 5th Ave" },
            { "value": "Installed", "source": "Suspect A", "target": "Skimmer Device" },
            { "value": "Entered", "source": "Suspect A", "target": "White Van" },
            { "value": "Has License", "source": "White Van", "target": "DL-4C-1234" }
          ],
          "nodes": [
            { "id": "Suspect A", "group": "Person" },
            { "id": "ATM 5th Ave", "group": "Location" },
            { "id": "Skimmer Device", "group": "Evidence" },
            { "id": "White Van", "group": "Evidence" },
            { "id": "DL-4C-1234", "group": "Evidence" }
          ]
        },
        "url": "http://mock-s3/cctv.mp4"
      },
      "id": "68508b13-88e4-4cc3-af93-feb0e73a7a87",
      "type": "video"
    }
  ],
  "unit": "Financial Crimes",
  "customFields": [],
  "lawSections": [ "IT Act 66C", "IT Act 66D", "IPC 420" ],
  "contrabandType": "Digital Data",
  "status": "Under Investigation",
  "caseNumber": "CR-CYBER-2025-001",
  "createdAt": "2025-12-22 00:15:08.151186",
  "sceneOfCrime": "City Bank ATM Network",
  "accused": [
    {
      "fatherName": "Unknown",
      "address": "Unknown (Traced to 192.168.4.22)",
      "gender": "Male",
      "name": "Unknown Suspect (ZeroCool)",
      "mobile": "Unknown",
      "age": "25-30",
      "status": "Absconding"
    }
  ],
  "publicAlertEnabled": true,
  "district": "Cyber Cell HQ",
  "publicAlertMessage": "Citizens are advised to check ATM slots for skimmers.",
  "contrabandQuantity": "50GB",
  "publicAlertMobile": "100",
  "updatedAt": "2025-12-22 00:15:08.151187",
  "longitude": "77.2090",
  "vehicleDetails": "White Van (DL-4C-1234)",
  "dateOfReport": "2025-12-12",
  "id": "a9111010-65f6-4adf-af3c-af94e244e9a7",
  "latitude": "28.6139"
}
"""

def generate_knowledge_graph(case_type, entities):
    nodes = []
    links = []
    for entity in entities:
        nodes.append({"id": entity["name"], "group": entity["type"]})
    
    if case_type == "Cyber":
        if len(entities) > 1: links.append({"source": entities[0]["name"], "target": entities[1]["name"], "value": "hacked"})
        if len(entities) > 2: links.append({"source": entities[0]["name"], "target": entities[2]["name"], "value": "accessed_from"})
    elif case_type == "Financial":
        if len(entities) > 1: links.append({"source": entities[0]["name"], "target": entities[1]["name"], "value": "authorized_transfer"})
        if len(entities) > 2: links.append({"source": entities[1]["name"], "target": entities[2]["name"], "value": "deposited_to"})
    elif case_type == "Narcotics":
         if len(entities) > 1: links.append({"source": entities[0]["name"], "target": entities[1]["name"], "value": "smuggled"})
         if len(entities) > 2: links.append({"source": entities[1]["name"], "target": entities[2]["name"], "value": "concealed_in"})
    elif case_type == "Terrorism":
         if len(entities) > 1: links.append({"source": entities[0]["name"], "target": entities[1]["name"], "value": "orchestrated"})
         if len(entities) > 2: links.append({"source": entities[0]["name"], "target": entities[2]["name"], "value": "supplied_material"})
    
    return {"nodes": nodes, "links": links}

def run():
    print("🚀 Starting Cleanup and Repopulation...")
    
    dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )
    
    cases_table = dynamodb.Table(settings.DYNAMODB_TABLE_CASES)
    evidence_table = dynamodb.Table(settings.DYNAMODB_TABLE_EVIDENCE)
    
    # 1. Cleanup
    print("🧹 Clearing existing data...")
    for table in [cases_table, evidence_table]:
        scan = table.scan()
        with table.batch_writer() as batch:
            for each in scan.get('Items', []):
                key_dict = {k['AttributeName']: each[k['AttributeName']] for k in table.key_schema}
                batch.delete_item(Key=key_dict)
    
    # 2. Restore Proper Case
    print("♻️ Restoring CR-CYBER-2025-001...")
    seed_case = json.loads(SEED_CASE_JSON)
    cases_table.put_item(Item=seed_case)
    
    # Restore evidence metadata to evidence table as well
    for ev in seed_case['evidence']:
        meta = ev['metadata']
        # Ensure Types are compatible
        evidence_table.put_item(Item=meta)

    # 3. Create New Rich Cases
    print("✨ Creating New Rich Cases...")
    cases_data = [
        {
            "meta": {"type": "Financial", "suffix": "FIN"},
            "district": "North District",
            "unit": "Financial Fraud Wing",
            "lawSections": ["Sec 406 IPC", "Sec 409 IPC"],
            "sceneOfCrime": "Banking Complex, Downtown",
            "description": "Embezzlement of funds amounting to 5 Crores from public sector bank accounts.",
            "accused": [{"name": "Jane Smith", "status": "Absconding", "gender": "Female", "age": "45"}],
            "status": "Charge Sheet Filed",
            "evidence_files": [
                {
                    "filename": "transaction_ledger.xlsx",
                    "type": "document",
                    "summary": "Bank ledger showing 50 unauthorized transfers of INR 10 Lakhs each to dummy accounts linked to 'Shell Corp via SWIFT network'.",
                    "graph_entities": [
                        {"name": "Jane Smith", "type": "Person"},
                        {"name": "Dummy Account 1", "type": "Evidence"},
                        {"name": "Shell Corp", "type": "Organization"}
                    ]
                }
            ]
        },
        {
            "meta": {"type": "Narcotics", "suffix": "NDPS"},
            "district": "Port City",
            "unit": "Narcotics Control Bureau",
            "lawSections": ["NDPS Act Section 21"],
            "sceneOfCrime": "Dockyard Container Terminal 4",
            "description": "Seizure of high-grade heroin concealed in machinery parts.",
            "accused": [{"name": "Unknown Person 1", "status": "Detained", "gender": "Male", "age": "Unknown"}],
            "status": "Under Investigation",
            "evidence_files": [
                {
                    "filename": "cctv_dockyard_feed.mp4",
                    "type": "video",
                    "summary": "Video footage showing two individuals loading package 'Box-77' into a delivery van at midnight. Face recognition inconclusive due to low light.",
                    "graph_entities": [
                        {"name": "Suspect A", "type": "Person"},
                        {"name": "Box-77", "type": "Evidence"},
                        {"name": "Delivery Van", "type": "Vehicle"}
                    ]
                }
            ]
        },
        {
            "meta": {"type": "Terrorism", "suffix": "ATS"},
            "district": "South Zone",
            "unit": "Anti-Terrorism Squad",
            "lawSections": ["UAPA Section 15"],
            "sceneOfCrime": "Abandoned Warehouse, Industrial Area",
            "description": "Recovery of bomb-making materials and blueprints.",
            "accused": [],
            "status": "Open",
             "evidence_files": [
                {
                    "filename": "blueprint_schematic.pdf",
                    "type": "document",
                    "summary": "Detailed schematic found on site depicting a timer circuit connected to a chemical dispersal device. Handwriting matches known suspect 'Vector'.",
                    "graph_entities": [
                        {"name": "Vector", "type": "Person"},
                        {"name": "Timer Circuit", "type": "Evidence"},
                        {"name": "Chemical Device", "type": "Evidence"}
                    ]
                }
            ]
        }
    ]

    with cases_table.batch_writer() as batch:
        for case_def in cases_data:
            case_id = str(uuid.uuid4())
            
            # Construct Evidence List with WRAPPER
            evidence_list_wrapped = []
            
            for ev_def in case_def.get("evidence_files", []):
                evidence_id = str(uuid.uuid4())
                uploaded_at_str = datetime.now().isoformat()
                
                # Metadata (Inner)
                ev_meta = {
                    "evidence_id": evidence_id,
                    "case_id": case_id,
                    "filename": ev_def["filename"],
                    "content_type": "video/mp4" if ev_def["type"] == "video" else "application/pdf",
                    "uploader": "System Seeder",
                    "uploader_role": "Forensics",
                    "tx_hash": f"0x{uuid.uuid4().hex}", 
                    "url": f"https://s3.amazonaws.com/bucket/{evidence_id}/{ev_def['filename']}",
                    "uploaded_at": uploaded_at_str,
                    "ai_summary": ev_def["summary"],
                    "knowledge_graph": generate_knowledge_graph(case_def['meta']['type'], ev_def['graph_entities'])
                }
                
                # Wrapper (Outer) - This matches the 'Proper' structure
                ev_wrapper = {
                    "id": evidence_id,
                    "name": ev_def["filename"],
                    "type": ev_def["type"],
                    "uploadedAt": uploaded_at_str,
                    "metadata": ev_meta
                }
                
                evidence_list_wrapped.append(ev_wrapper)
                
                # Insert independent metadata record
                evidence_table.put_item(Item=ev_meta)
            
            # Case Item
            case_item = {
                "id": case_id,
                "caseNumber": f"CR-{case_def['meta']['suffix']}-2025-{random.randint(1000, 9999)}",
                "district": case_def["district"],
                "unit": case_def["unit"],
                "lawSections": case_def["lawSections"],
                "dateOfOffence": (datetime.now() - timedelta(days=random.randint(1, 60))).strftime("%Y-%m-%d"),
                "dateOfReport": (datetime.now()).strftime("%Y-%m-%d"),
                "sceneOfCrime": case_def["sceneOfCrime"],
                "latitude": str(random.uniform(12.0, 28.0)),
                "longitude": str(random.uniform(74.0, 80.0)),
                "description": case_def["description"],
                "accused": case_def["accused"],
                "status": case_def["status"],
                "createdAt": datetime.now().isoformat(),
                "updatedAt": datetime.now().isoformat(),
                "evidence": evidence_list_wrapped,  # USING WRAPPED LIST
                "publicAlertEnabled": True,
                "publicAlertMessage": f"Alert regarding {case_def['description'][:50]}..."
            }
            
            print(f"Adding Case: {case_item['caseNumber']}")
            batch.put_item(Item=case_item)

    print("✅ Cleanup and Repopulation Complete!")

if __name__ == "__main__":
    run()
