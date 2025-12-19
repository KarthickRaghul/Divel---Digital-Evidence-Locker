# Divel---Digital-Evidence-Lockerx
**Blockchain & GenAI–Powered Digital Evidence Management and Intelligence Platform**

Divel is a secure, cloud-native digital evidence intelligence platform designed for **law enforcement, forensic labs, and judicial systems**.  
It ensures **tamper-proof evidence handling**, **verifiable integrity**, and **AI-assisted understanding of digital evidence** using modern cloud, blockchain, and generative AI technologies.

---

## 🚨 Problem Statement

Digital evidence such as CCTV footage, images, audio recordings, documents, and mobile data is critical in modern investigations. However, existing systems suffer from:

- ❌ Evidence tampering and manipulation  
- ❌ No reliable integrity verification  
- ❌ Poor access control and audit trails  
- ❌ Delays due to fragmented systems  
- ❌ Courts unable to independently verify authenticity  

---

## 💡 Solution Overview

Divel provides a **unified, tamper-resistant digital evidence locker** that:

- Secures evidence using **cryptographic hashing**
- Stores integrity proofs on **blockchain**
- Uses **Generative AI** to analyze and summarize evidence
- Maintains **strict role-based access control (RBAC)**
- Provides **end-to-end auditability**

---

## 🏗️ System Architecture (High Level)

1. **Evidence Upload**
   - Files uploaded via secure API
   - SHA-256 hash generated at ingestion

2. **Cloud Storage**
   - Evidence stored in AWS S3
   - Metadata stored in database

3. **Blockchain Layer**
   - Hash + metadata recorded on blockchain
   - Immutable integrity verification

4. **AI Intelligence Layer**
   - Multimodal GenAI analyzes documents, images, audio, and video
   - Generates summaries, key insights, and timelines

5. **Access & Audit**
   - Role-based access (Police, Forensics, Judge)
   - Full access logs and chain-of-custody tracking

---

## 🔑 Key Features

### 🛡️ Evidence Integrity & Security
- SHA-256 hashing
- Blockchain-based immutability
- Tamper detection on re-upload or access

### 🤖 AI-Powered Intelligence
- Multimodal Generative AI (text, image, audio, video)
- Automatic evidence summarization
- Context extraction for judges and investigators

### 🔐 Role-Based Access Control (RBAC)
- **Polaris (Police)** – Upload & manage evidence  
- **Forensics** – Analyze and verify evidence  
- **Judiciary** – View summaries & verify authenticity  

### 📜 Audit & Chain of Custody
- Timestamped logs for every action
- Immutable access history
- Court-ready verification reports

### ☁️ Cloud-Native & Scalable
- Serverless APIs (AWS Lambda)
- Secure object storage (AWS S3)
- Cost-efficient and scalable design

---

## 🧠 Technology Stack

### Frontend
- React.js
- Tailwind CSS
- Axios / WebSockets

### Backend
- AWS Lambda / EC2
- API Gateway
- Python (FastAPI / Flask)
- Node.js (optional services)

### Cloud & Storage
- AWS S3
- AWS IAM
- AWS CloudWatch

### Blockchain
- Ethereum / Hyperledger (configurable)
- Smart contracts for hash storage

### AI & ML
- Multimodal Generative AI
- NLP for document analysis
- Audio & video metadata extraction

---

## 📡 API Sample

### Upload Evidence
```http
POST /upload
