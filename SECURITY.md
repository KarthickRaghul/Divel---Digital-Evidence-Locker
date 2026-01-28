# Security Considerations for DiVeL

This document outlines the security improvements made to the Digital Evidence Locker project and provides guidance on deploying it securely.

## Critical Security Fixes Applied

### 1. CORS Configuration (HIGH PRIORITY)
**Issue**: The backend was configured with a wildcard (`*`) CORS origin, allowing any website to make requests.

**Fixed**: Removed the wildcard and restricted CORS to specific allowed origins:
- `http://localhost:5173` (Vite dev server)
- `http://localhost:3000` (Alternative frontend port)

**Action Required for Production**:
```python
# In backend/main.py, add your production domain:
origins = [
    "https://your-production-domain.com",
    "http://localhost:5173",  # Keep for local dev
]
```

### 2. Secret Key Management (HIGH PRIORITY)
**Issue**: The JWT secret key was hardcoded in the source code with a weak default value.

**Fixed**: Added prominent warning comments and instructions.

**Action Required for Production**:
1. Generate a strong random secret key:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```
2. Add it to your `.env` file:
   ```
   SECRET_KEY=your-generated-secure-random-key-here
   ```
3. **NEVER** commit this key to version control.

### 3. Blockchain Private Key (CRITICAL)
**Issue**: A well-known Hardhat test account private key was hardcoded in the source code.

**Fixed**: Added security warnings and environment variable support.

**Action Required for Production**:
1. Generate a new Ethereum wallet:
   ```bash
   # Using web3.py or other tools
   python -c "from eth_account import Account; acc = Account.create(); print(f'Address: {acc.address}\nPrivate Key: {acc.key.hex()}')"
   ```
2. Add to `.env`:
   ```
   BLOCKCHAIN_PRIVATE_KEY=0xyour-secure-private-key
   BLOCKCHAIN_ACCOUNT_ADDRESS=0xyour-wallet-address
   ```
3. **Best Practice**: Use AWS KMS, Azure Key Vault, or similar key management service in production.

### 4. Authentication Bypass (HIGH PRIORITY)
**Issue**: The evidence upload endpoint used `get_mock_polaris_user()` which bypassed authentication.

**Fixed**: Changed to use proper `get_current_user()` authentication.

**Impact**: Evidence upload now requires valid JWT authentication.

### 5. Error Disclosure (MEDIUM)
**Issue**: Debug error messages were exposing internal details in authentication failures.

**Fixed**: Replaced detailed error messages with generic "Could not validate credentials" message.

### 6. Print Statements (MEDIUM)
**Issue**: Using `print()` for logging in production code.

**Fixed**: Replaced all `print()` statements with proper `logging` module calls.

## Additional Security Improvements

### File Upload Validation
- **Size Limit**: 100MB maximum file size
- **Type Validation**: Only allows specific evidence file types (PDF, images, video, audio, etc.)
- **Hash Verification**: All files are cryptographically hashed using SHA-256

### Frontend Security
- **Development Mode**: Vite server now binds to `localhost` only (not `::` which exposed to all IPv6)
- **Production Mode**: Server binding disabled for production builds

## Security Checklist for Production Deployment

- [ ] Generate and configure a strong `SECRET_KEY` in `.env`
- [ ] Generate and secure a proper blockchain private key (not the Hardhat test key)
- [ ] Update CORS origins to include only your production domain
- [ ] Remove or disable the mock authentication functions
- [ ] Enable HTTPS/TLS for all API endpoints
- [ ] Set up proper AWS IAM roles with least-privilege access
- [ ] Enable AWS CloudTrail for audit logging
- [ ] Configure rate limiting on API Gateway
- [ ] Set up monitoring and alerting for suspicious activities
- [ ] Regular security audits of uploaded evidence files
- [ ] Implement proper session management and token rotation
- [ ] Enable DynamoDB point-in-time recovery
- [ ] Set up S3 bucket versioning and access logging
- [ ] Review and harden all security group rules
- [ ] Implement IP whitelisting if applicable
- [ ] Set up Web Application Firewall (WAF)

## Dependencies Security

### Backend Dependencies
The project uses the following security-relevant packages:
- `fastapi`: Modern web framework with built-in security features
- `python-jose[cryptography]`: JWT token handling
- `passlib[bcrypt]`: Password hashing (currently unused but available)
- `boto3`: AWS SDK with IAM-based security

**Action**: Regularly update dependencies:
```bash
cd backend
pip install --upgrade -r requirements.txt
pip-audit  # Check for known vulnerabilities
```

### Frontend Dependencies
**Action**: Regularly update dependencies:
```bash
cd frontend
npm audit
npm audit fix
npm update
```

## Vulnerability Reporting

If you discover a security vulnerability in this project, please:
1. **Do NOT** open a public issue
2. Contact the maintainers privately
3. Provide detailed information about the vulnerability
4. Allow time for a fix before public disclosure

## Compliance Notes

This system handles sensitive digital evidence. Depending on your jurisdiction, you may need to comply with:
- **GDPR** (Europe): Data protection and privacy
- **HIPAA** (US Healthcare): If handling medical evidence
- **CCPA** (California): Consumer privacy rights
- **Local Law Enforcement Standards**: Chain of custody requirements

Consult with your legal team before deploying in production.

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [AWS Security Best Practices](https://aws.amazon.com/security/best-practices/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Web3 Security](https://consensys.github.io/smart-contract-best-practices/)
