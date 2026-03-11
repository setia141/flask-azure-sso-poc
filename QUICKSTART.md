# Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Step 1: Azure Setup (3 minutes)

1. **Go to Azure Portal** → App registrations → New registration
   - Name: `Flask SSO App`
   - Redirect URI: `http://localhost:5000/getAToken` (Web)
   
2. **Copy from Overview page:**
   - Application (client) ID
   - Directory (tenant) ID
   
3. **Create Secret:**
   - Certificates & secrets → New client secret → Copy value immediately
   
4. **Set Permissions:**
   - API permissions → Add permission → Microsoft Graph → Delegated
   - Add: `User.Read` and `GroupMember.Read.All`
   - Grant admin consent
   
5. **Create Group:**
   - Azure AD → Groups → New group (Security)
   - Add yourself as member
   - Copy Object ID

### Step 2: Local Setup (2 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy environment file
cp .env.example .env

# 3. Edit .env with your values
# Add the IDs you copied from Azure

# 4. Run the app
python app.py
```

### Step 3: Test (30 seconds)

1. Open http://localhost:5000
2. Click "Login with Microsoft"
3. Sign in with your account
4. You should see the dashboard!

## ✅ Checklist

- [ ] Created Azure App Registration
- [ ] Copied Client ID, Secret, Tenant ID
- [ ] Set API permissions and granted consent
- [ ] Created Azure AD group and got Object ID
- [ ] Updated .env file with all values
- [ ] Ran `pip install -r requirements.txt`
- [ ] Started app with `python app.py`
- [ ] Logged in successfully

## 🔧 Common Issues

**"Configuration Error"**
→ Check all values in `.env` are filled in

**"Not Authorized"**
→ Make sure you're in the Azure AD group

**"Authentication failed"**
→ Verify Client Secret is correct (they expire!)

**"Redirect URI mismatch"**
→ Must be exactly `http://localhost:5000/getAToken`

## 📚 Next Steps

- Read the full README.md for production deployment
- Customize templates in `templates/` folder
- Add more protected routes using decorators
- Configure for your domain when deploying

Need help? Check the README.md for detailed troubleshooting!
