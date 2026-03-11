import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration."""
    
    # Flask
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Azure AD
    CLIENT_ID = os.getenv('AZURE_CLIENT_ID')
    CLIENT_SECRET = os.getenv('AZURE_CLIENT_SECRET')
    TENANT_ID = os.getenv('AZURE_TENANT_ID')
    AUTHORITY = f"https://login.microsoftonline.com/{os.getenv('AZURE_TENANT_ID')}"
    
    # Group Authorization
    ALLOWED_GROUP_ID = os.getenv('AZURE_ALLOWED_GROUP_ID')
    
    # Redirect URI
    REDIRECT_URI = os.getenv('REDIRECT_URI', 'http://localhost:5000/getAToken')
    
    # Microsoft Graph
    GRAPH_ENDPOINT = os.getenv('GRAPH_ENDPOINT', 'https://graph.microsoft.com/v1.0')
    
    # Scopes
    SCOPE = [
        "User.Read",
        "GroupMember.Read.All"
    ]
    
    # Session configuration
    SESSION_TYPE = "filesystem"
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    @staticmethod
    def validate():
        """Validate required configuration variables."""
        required_vars = [
            'CLIENT_ID',
            'CLIENT_SECRET', 
            'TENANT_ID',
            'ALLOWED_GROUP_ID'
        ]
        
        missing = []
        for var in required_vars:
            if not os.getenv(f'AZURE_{var}') and var != 'CLIENT_SECRET':
                missing.append(f'AZURE_{var}')
            elif var == 'CLIENT_SECRET' and not os.getenv('AZURE_CLIENT_SECRET'):
                missing.append('AZURE_CLIENT_SECRET')
        
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        
        return True
