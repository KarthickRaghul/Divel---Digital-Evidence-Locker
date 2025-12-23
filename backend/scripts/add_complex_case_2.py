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
    print("🚀 Adding Second COMPLEX Case (Corporate Espionage)...")
    
    dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )
    
    cases_table = dynamodb.Table(settings.DYNAMODB_TABLE_CASES)
    evidence_table = dynamodb.Table(settings.DYNAMODB_TABLE_EVIDENCE)
    
    # CASE DEFINITION: Corporate Espionage
    case_id = str(uuid.uuid4())
    case_number = f"CR-CORP-2025-{random.randint(1000, 9999)}"
    
    description = "Case 'Project Titan': Theft of proprietary autonomous vehicle algorithms from 'AutoDrive Inc'. The stolen IP was attempted to be sold to a foreign competitor 'RedStar Motors'. Involves insider threat and encrypted data exfiltration."
    
    evidence_items = [
        {
            "filename": "server_access_logs_dec12.log",
            "type": "document",
            "summary": "Server access logs showing user 'Dev_Mark' accessing restricted directory '/src/lidar_core/' at 03:00 AM on a Sunday. Data exfiltration of 50GB detected via port 443.",
            "entities": [
                {"name": "Dev_Mark", "type": "Person"},
                {"name": "/src/lidar_core/", "type": "File"},
                {"name": "AutoDrive Server", "type": "Device"}
            ],
            "links": [
                {"source": "Dev_Mark", "target": "AutoDrive Server", "value": "Accessed at 03:00 AM"},
                {"source": "Dev_Mark", "target": "/src/lidar_core/", "value": "Downloaded"},
                {"source": "AutoDrive Server", "target": "Port 443", "value": "Exfiltrated Data via"}
            ]
        },
        {
            "filename": "encrypted_email_thread.txt",
            "type": "document",
            "summary": "Decrypted email thread between 'Dev_Mark' and 'Handler_Victor'. Mark confirms 'Payload is ready' and demands payment of 500k USDT. Victor replies with wallet address.",
            "entities": [
                {"name": "Dev_Mark", "type": "Person"},
                {"name": "Handler_Victor", "type": "Person"},
                {"name": "500k USDT", "type": "Evidence"},
                {"name": "Crypto Wallet", "type": "Account"}
            ],
            "links": [
                {"source": "Dev_Mark", "target": "Handler_Victor", "value": "Emailed"},
                {"source": "Dev_Mark", "target": "500k USDT", "value": "Demanded"},
                {"source": "Handler_Victor", "target": "Crypto Wallet", "value": "Provided Address"}
            ]
        },
        {
            "filename": "cctv_office_lobby.mp4",
            "type": "video",
            "summary": "CCTV footage identifying 'Handler_Victor' entering the AutoDrive Inc lobby as a guest signed in by 'Dev_Mark' two days prior to the breach.",
            "entities": [
                {"name": "Handler_Victor", "type": "Person"},
                {"name": "Dev_Mark", "type": "Person"},
                {"name": "AutoDrive Lobby", "type": "Location"}
            ],
            "links": [
                {"source": "Handler_Victor", "target": "AutoDrive Lobby", "value": "Entered"},
                {"source": "Dev_Mark", "target": "Handler_Victor", "value": "Signed in as Guest"}
            ]
        },
        {
            "filename": "source_code_fragment.c",
            "type": "document",
            "summary": "Recovered source code fragment found on a USB drive in 'Dev_Mark's' car. Matches the proprietary LIDAR processing logic of AutoDrive Inc (98% similarity).",
            "entities": [
                {"name": "USB Drive", "type": "Evidence"},
                {"name": "Dev_Mark", "type": "Person"},
                {"name": "LIDAR Logic", "type": "Evidence"}
            ],
            "links": [
                {"source": "Dev_Mark", "target": "USB Drive", "value": "Possessed"},
                {"source": "USB Drive", "target": "LIDAR Logic", "value": "Contained Stolen Code"}
            ]
        },
        {
            "filename": "flight_manifest_hk.pdf",
            "type": "document",
            "summary": "Flight manifest showing 'Handler_Victor' flew to Hong Kong one day after the data breach. Seat 4A, Flight CX-881.",
            "entities": [
                {"name": "Handler_Victor", "type": "Person"},
                {"name": "Hong Kong", "type": "Location"},
                {"name": "Flight CX-881", "type": "Evidence"}
            ],
            "links": [
                {"source": "Handler_Victor", "target": "Hong Kong", "value": "Traveled to"},
                {"source": "Handler_Victor", "target": "Flight CX-881", "value": "Passenger on"}
            ]
        },
        {
            "filename": "meeting_recording_jan12.wav",
            "type": "audio",
            "summary": "Audio recording from a bugged meeting room. 'CEO_RedStar' is heard discussing 'Upcoming acquisition of new tech' with 'Handler_Victor'.",
            "entities": [
                {"name": "CEO_RedStar", "type": "Person"},
                {"name": "Handler_Victor", "type": "Person"},
                {"name": "RedStar Motors", "type": "Organization"}
            ],
            "links": [
                {"source": "Handler_Victor", "target": "CEO_RedStar", "value": "Met with"},
                {"source": "CEO_RedStar", "target": "RedStar Motors", "value": "Leads"}
            ]
        },
        {
            "filename": "steg_image_cat.png",
            "type": "image",
            "summary": "Steganographic analysis of a seemingly harmless cat image sent by Mark reveals hidden zip archive password 'TitanFall2025'.",
            "entities": [
                {"name": "Cat Image", "type": "Evidence"},
                {"name": "Dev_Mark", "type": "Person"},
                {"name": "Password", "type": "Evidence"}
            ],
            "links": [
                {"source": "Dev_Mark", "target": "Cat Image", "value": "Sent"},
                {"source": "Cat Image", "target": "Password", "value": "Concealed"}
            ]
        },
        {
            "filename": "forensic_timeline_report.pdf",
            "type": "document",
            "summary": "Consolidated forensic report establishing the timeline of the insider threat, data staging, encryption, exfiltration, and recipient hand-off.",
            "entities": [
                {"name": "Dev_Mark", "type": "Person"},
                {"name": "Data Breach Incident", "type": "Incident"},
                {"name": "AutoDrive Inc", "type": "Organization"}
            ],
            "links": [
                {"source": "Dev_Mark", "target": "Data Breach Incident", "value": "Perpetrated"},
                {"source": "Data Breach Incident", "target": "AutoDrive Inc", "value": "Victim"}
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

        # Metadata
        ev_meta = {
            "evidence_id": evidence_id,
            "case_id": case_id,
            "filename": ev["filename"],
            "content_type": "video/mp4" if ev["type"] == "video" else "audio/wav" if ev["type"] == "audio" else "application/pdf" if ev["type"] == "document" else "image/png",
            "uploader": "IP Protection Unit",
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
        "district": "Tech Park Zone",
        "unit": "Economic Offences Wing",
        "lawSections": ["IT Act Sec 66", "Corporate Espionage Act", "Breach of Contract"],
        "dateOfOffence": (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d"),
        "dateOfReport": (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"),
        "sceneOfCrime": "AutoDrive Inc HQ, Server Room",
        "latitude": "37.3861", # Silicon Valley approx
        "longitude": "-122.0839",
        "description": description,
        "accused": [
            {"name": "Mark 'Dev_Mark' Sullivan", "status": "Terminated", "gender": "Male", "age": "29"},
            {"name": "Victor 'Handler' Kovac", "status": "Wanted (Red Corner)", "gender": "Male", "age": "45"}
        ],
        "status": "Under Investigation",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat(),
        "evidence": evidence_list_wrapped,
        "publicAlertEnabled": False,
        "contrabandType": "Source Code & Algorithms",
        "contrabandQuantity": "50 GB"
    }

    print(f"Adding Second Complex Case: {case_number}")
    cases_table.put_item(Item=case_item)
    print("✅ Corporate Espionage Case Added!")

if __name__ == "__main__":
    run()
