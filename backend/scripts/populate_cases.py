import sys
import os
import boto3
import uuid
from datetime import datetime, timedelta
import random

# Add backend directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.core.config import settings

def generate_knowledge_graph(case_type, entities):
    """Generates a mock knowledge graph based on case type and entities."""
    nodes = []
    links = []
    
    # Add core entities as nodes
    for entity in entities:
        nodes.append({"id": entity["name"], "group": entity["type"]})
    
    # Generate some logical links
    if case_type == "Cyber":
        links.append({"source": entities[0]["name"], "target": entities[1]["name"], "value": "hacked"})
        links.append({"source": entities[0]["name"], "target": entities[2]["name"], "value": "accessed_from"})
    elif case_type == "Financial":
        links.append({"source": entities[0]["name"], "target": entities[1]["name"], "value": "authorized_transfer"})
        links.append({"source": entities[1]["name"], "target": entities[2]["name"], "value": "deposited_to"})
    elif case_type == "Narcotics":
         links.append({"source": entities[0]["name"], "target": entities[1]["name"], "value": "smuggled"})
         links.append({"source": entities[1]["name"], "target": entities[2]["name"], "value": "concealed_in"})
    elif case_type == "Terrorism":
         links.append({"source": entities[0]["name"], "target": entities[1]["name"], "value": "orchestrated"})
         links.append({"source": entities[0]["name"], "target": entities[2]["name"], "value": "supplied_material"})
    
    return {"nodes": nodes, "links": links}

def populate_cases_with_evidence():
    print("Populating test cases with RICH evidence data...")
    
    try:
        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        
        cases_table = dynamodb.Table(settings.DYNAMODB_TABLE_CASES)
        evidence_table = dynamodb.Table(settings.DYNAMODB_TABLE_EVIDENCE)
        
        # Define test cases with embedded evidence generation params
        cases_data = [
            {
                "meta": {"type": "Cyber", "suffix": "CYBER"},
                "district": "Metropolis Central",
                "unit": "Cyber Crime Cell",
                "lawSections": ["Sec 66C IT Act", "Sec 420 IPC"],
                "sceneOfCrime": "123 Tech Park, Server Room B",
                "description": "Unauthorized access to corporate servers and data theft.",
                "accused": [{"name": "John Doe", "status": "Arrested"}],
                "status": "Under Investigation",
                "evidence_files": [
                    {
                        "filename": "server_logs_dump.log",
                        "summary": "Server logs indicating multiple unauthorized login attempts from IP 192.168.1.105 followed by bulk data export command 'expdb' at 03:00 AM.",
                        "graph_entities": [
                            {"name": "John Doe", "type": "Person"}, 
                            {"name": "Server Alpha", "type": "Device"},
                            {"name": "IP 192.168.1.105", "type": "Location"}
                        ]
                    },
                    {
                        "filename": "seized_laptop_disk_image.img",
                        "summary": "Forensic image of the suspect's laptop showing deleted chat logs with 'Handler_X' discussing the sale of proprietary data.",
                        "graph_entities": [
                            {"name": "John Doe", "type": "Person"},
                            {"name": "Handler_X", "type": "Person"},
                            {"name": "DarkWeb Forum", "type": "Location"}
                        ]
                    }
                ]
            },
            {
                "meta": {"type": "Financial", "suffix": "FIN"},
                "district": "North District",
                "unit": "Financial Fraud Wing",
                "lawSections": ["Sec 406 IPC", "Sec 409 IPC"],
                "sceneOfCrime": "Banking Complex, Downtown",
                "description": "Embezzlement of funds amounting to 5 Crores from public sector bank accounts.",
                "accused": [{"name": "Jane Smith", "status": "Absconding"}],
                "status": "Charge Sheet Filed",
                "evidence_files": [
                    {
                        "filename": "transaction_ledger.xlsx",
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
                "accused": [{"name": "Unknown Person 1", "status": "Detained"}],
                "status": "Under Investigation",
                "evidence_files": [
                    {
                        "filename": "cctv_dockyard_feed.mp4",
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
                # 1. Prepare Case Object
                case_id = str(uuid.uuid4())
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
                    "evidence": [], # Will fill this
                    "publicAlertEnabled": random.choice([True, False])
                }
                
                print(f"Processing Case: {case_item['caseNumber']}")

                # 2. Process Evidence for this case
                for ev_def in case_def.get("evidence_files", []):
                    evidence_id = str(uuid.uuid4())
                    
                    # Generate Mock Meta
                    ev_meta = {
                        "evidence_id": evidence_id,
                        "case_id": case_id,
                        "filename": ev_def["filename"],
                        "content_type": "application/pdf" if ev_def["filename"].endswith("pdf") else "image/jpeg",
                        "uploader": "System Seeder",
                        "uploader_role": "Forensics",
                        "tx_hash": f"0x{uuid.uuid4().hex}", # Mock TX Hash
                        "url": f"https://s3.amazonaws.com/bucket/{evidence_id}/{ev_def['filename']}", # Mock URL
                        "uploaded_at": datetime.now().isoformat(),
                        "ai_summary": ev_def["summary"],
                        "knowledge_graph": generate_knowledge_graph(case_def['meta']['type'], ev_def['graph_entities'])
                    }
                    
                    # Add to Case's specific evidence list
                    case_item["evidence"].append(ev_meta)
                    
                    # Insert into independent Evidence Table
                    evidence_table.put_item(Item=ev_meta)
                    print(f"  -> Added Evidence: {ev_def['filename']}")

                # 3. Insert Case
                batch.put_item(Item=case_item)

        print(f"✅ Successfully added {len(cases_data)} rich test cases.")

    except Exception as e:
        print(f"❌ Failed to populate cases: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    populate_cases_with_evidence()
