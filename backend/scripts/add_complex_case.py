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

def run():
    print("🚀 Adding COMPLEX Case...")
    
    dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )
    
    cases_table = dynamodb.Table(settings.DYNAMODB_TABLE_CASES)
    evidence_table = dynamodb.Table(settings.DYNAMODB_TABLE_EVIDENCE)
    
    # COMPLEX CASE DEFINITION
    case_id = str(uuid.uuid4())
    case_number = f"CR-ORG-2025-{random.randint(1000, 9999)}"
    
    description = "Operation 'Red Ledger': Multi-national money laundering syndicate using crypto-currency to funnel proceeds from illegal arms trade. The syndicate operates through a network of shell companies in Panama and Singapore."
    
    evidence_items = [
        {
            "filename": "forensic_hdd_report.pdf",
            "type": "document",
            "summary": "Forensic analysis of the seized server HDD (Serial: WD-X99) reveals 10,000+ encrypted chat logs. Decryption of 'Partition A' uncovered communications between 'Kingpin' and 'Supplier_Alpha' regarding shipment of 'Hardware_X' to Port 4. Keys found in local wallet.dat.",
            "entities": [
                {"name": "Kingpin", "type": "Person"},
                {"name": "Supplier_Alpha", "type": "Person"},
                {"name": "HDD WD-X99", "type": "Evidence"},
                {"name": "Port 4", "type": "Location"}
            ],
            "links": [
                {"source": "HDD WD-X99", "target": "Kingpin", "value": "Contains chats of"},
                {"source": "Kingpin", "target": "Supplier_Alpha", "value": "Discussed shipment"},
                {"source": "Supplier_Alpha", "target": "Port 4", "value": "Shipping to"}
            ]
        },
        {
            "filename": "intercepted_call_audio.mp3",
            "type": "audio",
            "summary": "Audio intercept #4451 dated 15-Dec-2025. Voice verification confirms speakers as 'Alias: Viper' and 'Banker_Steve'. Viper instructs Steve to 'clean' 500 BTC through 'ShellCorp_Global' accounts in Singapore by Friday.",
            "entities": [
                {"name": "Viper", "type": "Person"},
                {"name": "Banker_Steve", "type": "Person"},
                {"name": "ShellCorp_Global", "type": "Organization"},
                {"name": "Singapore", "type": "Location"}
            ],
            "links": [
                {"source": "Viper", "target": "Banker_Steve", "value": "Instructed"},
                {"source": "Banker_Steve", "target": "ShellCorp_Global", "value": "Manages accounts for"},
                {"source": "ShellCorp_Global", "target": "Singapore", "value": "Registered in"}
            ]
        },
        {
            "filename": "surveillance_meeting_photo.jpg",
            "type": "image",
            "summary": "Surveillance image taken at 'Café Noir', Paris. Identifies 'Kingpin' meeting with 'Politician_X'. Exchange of a black briefcase (Evidence #99) observed at 14:00 hours.",
            "entities": [
                {"name": "Kingpin", "type": "Person"},
                {"name": "Politician_X", "type": "Person"},
                {"name": "Café Noir", "type": "Location"},
                {"name": "Black Briefcase", "type": "Evidence"}
            ],
            "links": [
                {"source": "Kingpin", "target": "Politician_X", "value": "Met with"},
                {"source": "Kingpin", "target": "Black Briefcase", "value": "Handed over"},
                {"source": "Café Noir", "target": "Kingpin", "value": "Sighted at"}
            ]
        },
        {
            "filename": "crypto_ledger.csv",
            "type": "document",
            "summary": "CSV export of the 'Cold Wallet' ledger. Traces flow of 5000 BTC from 'DarkMarket_Wallet' -> 'Mixer_Service' -> 'ShellCorp_Global'. Final exit node IP traced to 'Server_Beta' in Switzerland.",
            "entities": [
                {"name": "DarkMarket_Wallet", "type": "Account"},
                {"name": "ShellCorp_Global", "type": "Organization"},
                {"name": "Server_Beta", "type": "Device"},
                {"name": "Switzerland", "type": "Location"}
            ],
            "links": [
                {"source": "DarkMarket_Wallet", "target": "ShellCorp_Global", "value": "Transferred funds to"},
                {"source": "ShellCorp_Global", "target": "Server_Beta", "value": "Controlled by"},
                {"source": "Server_Beta", "target": "Switzerland", "value": "Located in"}
            ]
        },
        {
            "filename": "confession_video.mp4",
            "type": "video",
            "summary": "Video confession of 'Mule_John'. Mentions he was recruited by 'Viper' to transport cash to 'The warehouse'. Confirms 'The warehouse' is used to store illegal arms.",
            "entities": [
                {"name": "Mule_John", "type": "Person"},
                {"name": "Viper", "type": "Person"},
                {"name": "The Warehouse", "type": "Location"}
            ],
            "links": [
                {"source": "Mule_John", "target": "Viper", "value": "Recruited by"},
                {"source": "Mule_John", "target": "The Warehouse", "value": "Transported cash to"}
            ]
        },
        {
            "filename": "gps_tracker_log.json",
            "type": "document",
            "summary": "GPS logs from the suspect vehicle (Reg: XX-99-YY). Shows repeated trips between 'The Warehouse' and 'Port 4' between 01:00 AM and 04:00 AM for the past month.",
            "entities": [
                {"name": "Vehicle XX-99-YY", "type": "Vehicle"},
                {"name": "The Warehouse", "type": "Location"},
                {"name": "Port 4", "type": "Location"}
            ],
            "links": [
                {"source": "Vehicle XX-99-YY", "target": "The Warehouse", "value": "Visited frequently"},
                {"source": "Vehicle XX-99-YY", "target": "Port 4", "value": "Visited frequently"},
                {"source": "The Warehouse", "target": "Port 4", "value": "Connected via transport route"}
            ]
        },
        {
            "filename": "bank_statement.pdf",
            "type": "document",
            "summary": "Official bank statement of 'ShellCorp_Global' showing receipt of $5M USD from 'Offshore_Holdings' and immediate wire transfer to 'Arms_Dealer_Inc'.",
            "entities": [
                {"name": "ShellCorp_Global", "type": "Organization"},
                {"name": "Offshore_Holdings", "type": "Organization"},
                {"name": "Arms_Dealer_Inc", "type": "Organization"}
            ],
            "links": [
                {"source": "Offshore_Holdings", "target": "ShellCorp_Global", "value": "Sent $5M"},
                {"source": "ShellCorp_Global", "target": "Arms_Dealer_Inc", "value": "Wired $5M"}
            ]
        }
    ]

    evidence_list_wrapped = []
    
    for ev in evidence_items:
        evidence_id = str(uuid.uuid4())
        uploaded_at_str = datetime.now().isoformat()
        
        # Determine Graph
        kg = {
            "nodes": [], 
            "links": ev.get("links", [])
        }
        for ent in ev.get("entities", []):
            kg["nodes"].append({"id": ent["name"], "group": ent["type"]})

        # Match legacy keys if needed, but 'links' structure matches previously seen
        
        # Metadata
        ev_meta = {
            "evidence_id": evidence_id,
            "case_id": case_id,
            "filename": ev["filename"],
            "content_type": "video/mp4" if ev["type"] == "video" else "application/pdf" if ev["type"] == "document" else "image/jpeg",
            "uploader": "Senior Detective",
            "uploader_role": "Forensics",
            "tx_hash": f"0x{uuid.uuid4().hex}", 
            "url": f"https://s3.amazonaws.com/bucket/{evidence_id}/{ev['filename']}",
            "uploaded_at": uploaded_at_str,
            "ai_summary": ev["summary"],
            "knowledge_graph": kg
        }
        
        # Wrapper
        ev_wrapper = {
            "id": evidence_id,
            "name": ev["filename"],
            "type": ev["type"],
            "uploadedAt": uploaded_at_str,
            "metadata": ev_meta
        }
        
        evidence_list_wrapped.append(ev_wrapper)
        evidence_table.put_item(Item=ev_meta)

    # Insert Case
    case_item = {
        "id": case_id,
        "caseNumber": case_number,
        "district": "International Crime Unit",
        "unit": "Organized Crime Wing",
        "lawSections": ["PMLA Act", "Arms Act", "IPC 120B (Conspiracy)"],
        "dateOfOffence": (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d"),
        "dateOfReport": (datetime.now() - timedelta(days=85)).strftime("%Y-%m-%d"),
        "sceneOfCrime": "Multiple Locations (Global)",
        "latitude": "46.2044", # Geneva approx
        "longitude": "6.1432",
        "description": description,
        "accused": [
            {"name": "The Kingpin", "status": "Wanted", "gender": "Male", "age": "55"},
            {"name": "Viper", "status": "Arrested", "gender": "Male", "age": "32"}
        ],
        "status": "Charge Sheet Filed",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat(),
        "evidence": evidence_list_wrapped,
        "publicAlertEnabled": True,
        "publicAlertMessage": "Red Corner Notice issued for 'The Kingpin'.",
        "contrabandType": "Illegal Arms & Crypto",
        "contrabandQuantity": "$50M Value"
    }

    print(f"Adding Complex Case: {case_number}")
    cases_table.put_item(Item=case_item)
    print("✅ Complex Case Added!")

if __name__ == "__main__":
    run()
