# Flask Azure SSO - Organization Level Authentication

A complete Flask application demonstrating Single Sign-On (SSO) with Azure Active Directory and group-based authorization.

## Features

- ✅ Azure AD SSO authentication
- ✅ Group-based authorization (organization-level access control)
- ✅ Microsoft Graph API integration
- ✅ Secure session management
- ✅ Protected routes with decorators
- ✅ User profile management
- ✅ Clean, modern UI

## Prerequisites

- Python 3.8+
- Azure AD tenant
- Azure AD App Registration
- Azure AD Security Group

## Azure AD Setup

### 1. Create App Registration

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** → **App registrations**
3. Click **New registration**
4. Fill in:
   - **Name**: Flask SSO App
   - **Supported account types**: Single tenant
   - **Redirect URI**: 
     - Type: Web
     - URI: `http://localhost:5000/getAToken`
5. Click **Register**

### 2. Get Client ID and Tenant ID

From the app's **Overview** page, copy:
- **Application (client) ID** → `AZURE_CLIENT_ID`
- **Directory (tenant) ID** → `AZURE_TENANT_ID`

### 3. Create Client Secret

1. Go to **Certificates & secrets**
2. Click **New client secret**
3. Add description and expiry
4. Click **Add**
5. **Copy the secret value immediately** → `AZURE_CLIENT_SECRET`
   - ⚠️ You won't be able to see it again!

### 4. Configure API Permissions

1. Go to **API permissions**
2. Click **Add a permission**
3. Select **Microsoft Graph**
4. Choose **Delegated permissions**
5. Add:
   - `User.Read`
   - `GroupMember.Read.All`
6. Click **Add permissions**
7. Click **Grant admin consent for [Your Organization]**

### 5. Create Azure AD Group

1. Navigate to **Azure Active Directory** → **Groups**
2. Click **New group**
3. Fill in:
   - **Group type**: Security
   - **Group name**: Flask App Users
   - **Members**: Add authorized users
4. Click **Create**
5. Open the group and copy **Object ID** → `AZURE_ALLOWED_GROUP_ID`

### 6. Update Redirect URI for Production

When deploying to production:
1. Go to **Authentication**
2. Add production redirect URI: `https://yourdomain.com/getAToken`
3. Click **Save**

## Installation

### 1. Clone or Download

```bash
cd flask-azure-sso
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Edit `.env` and add your Azure values:

```dotenv
# Flask Configuration
FLASK_SECRET_KEY=your-random-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=True

# Azure AD App Registration
AZURE_CLIENT_ID=your-client-id-from-azure
AZURE_CLIENT_SECRET=your-client-secret-from-azure
AZURE_TENANT_ID=your-tenant-id-from-azure

# Azure AD Group Authorization
AZURE_ALLOWED_GROUP_ID=your-group-object-id-from-azure

# Redirect URI
REDIRECT_URI=http://localhost:5000/getAToken
```

**To generate a secure secret key:**

```python
python -c "import secrets; print(secrets.token_hex(32))"
```

## Running the Application

### Development

```bash
python app.py
```

Visit: http://localhost:5000

### Production

For production deployment, use a WSGI server like Gunicorn:

```bash
pip install gunicorn

gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Project Structure

```
flask-azure-sso/
├── app.py                 # Main Flask application
├── config.py              # Configuration management
├── auth_service.py        # Azure AD authentication service
├── decorators.py          # Authentication decorators
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── dashboard.html    # Protected dashboard
│   ├── profile.html      # User profile
│   └── unauthorized.html # Access denied page
└── README.md             # This file
```

## Usage

### Routes

- `/` - Home page
- `/login` - Initiate SSO login
- `/getAToken` - OAuth callback (configured in Azure)
- `/dashboard` - Protected dashboard (requires group membership)
- `/profile` - User profile (requires login)
- `/unauthorized` - Access denied page
- `/logout` - Logout and clear session
- `/health` - Health check endpoint

### Authentication Flow

1. User clicks "Login with Microsoft"
2. Redirected to Azure AD login page
3. User authenticates with Microsoft credentials
4. Azure AD redirects back with authorization code
5. App exchanges code for access token
6. App fetches user info and group memberships
7. App validates group membership
8. User granted/denied access based on group membership

### Decorators

**@login_required**
```python
@app.route('/profile')
@login_required
def profile():
    # Requires user to be logged in
    return render_template('profile.html')
```

**@group_required**
```python
@app.route('/dashboard')
@group_required
def dashboard():
    # Requires user to be logged in AND member of authorized group
    return render_template('dashboard.html')
```

## Security Considerations

1. **Environment Variables**: Never commit `.env` file to version control
2. **Client Secret**: Store securely, rotate regularly
3. **HTTPS**: Always use HTTPS in production
4. **Session Security**: Configure secure session cookies in production
5. **CSRF Protection**: State parameter prevents CSRF attacks
6. **Group Validation**: Verify group membership on every protected request

## Production Deployment

### Environment Variables for Production

```dotenv
FLASK_SECRET_KEY=<strong-random-key>
FLASK_ENV=production
FLASK_DEBUG=False
REDIRECT_URI=https://yourdomain.com/getAToken
```

### Security Enhancements

1. Enable HTTPS
2. Set secure cookie flags:
```python
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax'
)
```

3. Use environment-specific configs
4. Implement rate limiting
5. Add logging and monitoring

## Troubleshooting

### "Configuration Error: Missing required environment variables"
- Ensure all required variables in `.env` are set
- Check `.env` file is in the project root

### "Invalid state parameter"
- Clear browser cookies and session
- Try login again

### "User is not a member of the authorized group"
- Verify user is added to the Azure AD group
- Check `AZURE_ALLOWED_GROUP_ID` is correct
- Ensure admin consent was granted for GroupMember.Read.All

### "Authentication failed"
- Verify client ID and secret are correct
- Check redirect URI matches Azure configuration exactly
- Ensure tenant ID is correct

## API Reference

### AuthService Methods

- `get_token_from_cache()` - Retrieve cached token
- `get_token_from_code(code)` - Exchange auth code for token
- `get_user_info(token)` - Fetch user profile from Graph API
- `get_user_groups(token)` - Fetch user's group memberships
- `is_user_authorized(token)` - Validate group membership
- `logout()` - Clear session and get logout URL

## License

MIT License - feel free to use this for your projects!

## Support

For issues or questions:
1. Check Azure AD configuration
2. Review application logs
3. Verify environment variables
4. Check Microsoft Graph API permissions

## References

- [Microsoft Authentication Library (MSAL) for Python](https://github.com/AzureAD/microsoft-authentication-library-for-python)
- [Microsoft Graph API Documentation](https://docs.microsoft.com/en-us/graph/)
- [Azure AD App Registration Guide](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app)
