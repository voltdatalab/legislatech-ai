# utils/auth.py
import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from config import BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD

security = HTTPBasic()

def verify_basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    """Verifica as credenciais de autenticação básica."""
    correct_username = secrets.compare_digest(credentials.username, BASIC_AUTH_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, BASIC_AUTH_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Basic"},
        )