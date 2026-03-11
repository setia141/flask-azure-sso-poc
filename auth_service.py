import msal
import requests
from flask import session, url_for
from config import Config


class AuthService:
    """Service for handling Azure AD authentication."""
    
    @staticmethod
    def _build_msal_app(cache=None, authority=None):
        """Build MSAL confidential client application."""
        return msal.ConfidentialClientApplication(
            Config.CLIENT_ID,
            authority=authority or Config.AUTHORITY,
            client_credential=Config.CLIENT_SECRET,
            token_cache=cache
        )
    
    @staticmethod
    def _build_auth_url(authority=None, scopes=None, state=None):
        """Build authorization URL for login."""
        return AuthService._build_msal_app(authority=authority).get_authorization_request_url(
            scopes or Config.SCOPE,
            state=state or str(session.get('state')),
            redirect_uri=Config.REDIRECT_URI
        )
    
    @staticmethod
    def get_token_from_cache(scope=None):
        """Get token from cache if available."""
        cache = AuthService._load_cache()
        cca = AuthService._build_msal_app(cache=cache)
        accounts = cca.get_accounts()
        
        if accounts:
            result = cca.acquire_token_silent(
                scope or Config.SCOPE,
                account=accounts[0]
            )
            AuthService._save_cache(cache)
            return result
        
        return None
    
    @staticmethod
    def get_token_from_code(code, scope=None):
        """Exchange authorization code for access token."""
        cache = AuthService._load_cache()
        result = AuthService._build_msal_app(cache=cache).acquire_token_by_authorization_code(
            code,
            scopes=scope or Config.SCOPE,
            redirect_uri=Config.REDIRECT_URI
        )
        
        if "error" in result:
            return result
        
        AuthService._save_cache(cache)
        return result
    
    @staticmethod
    def _load_cache():
        """Load token cache from session."""
        cache = msal.SerializableTokenCache()
        if session.get("token_cache"):
            cache.deserialize(session["token_cache"])
        return cache
    
    @staticmethod
    def _save_cache(cache):
        """Save token cache to session."""
        if cache.has_state_changed:
            session["token_cache"] = cache.serialize()
    
    @staticmethod
    def call_graph_api(endpoint, token):
        """Call Microsoft Graph API."""
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(endpoint, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Graph API call failed: {response.status_code} - {response.text}")
    
    @staticmethod
    def get_user_info(token):
        """Get user information from Microsoft Graph."""
        endpoint = f"{Config.GRAPH_ENDPOINT}/me"
        return AuthService.call_graph_api(endpoint, token)
    
    @staticmethod
    def get_user_groups(token):
        """Get user's group memberships from Microsoft Graph."""
        endpoint = f"{Config.GRAPH_ENDPOINT}/me/memberOf"
        result = AuthService.call_graph_api(endpoint, token)
        return result.get('value', [])
    
    @staticmethod
    def is_user_authorized(token):
        """Check if user is member of the allowed group."""
        try:
            groups = AuthService.get_user_groups(token)
            
            # Check if user is in the allowed group
            for group in groups:
                if group.get('id') == Config.ALLOWED_GROUP_ID:
                    return True, "Access granted"
            
            return False, "User is not a member of the authorized group"
            
        except Exception as e:
            return False, f"Error checking group membership: {str(e)}"
    
    @staticmethod
    def logout():
        """Clear session and return logout URL."""
        session.clear()
        return (
            f"{Config.AUTHORITY}/oauth2/v2.0/logout"
            f"?post_logout_redirect_uri={url_for('index', _external=True)}"
        )
