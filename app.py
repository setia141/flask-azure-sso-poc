import uuid
from flask import Flask, render_template, redirect, url_for, session, request, flash
from config import Config
from auth_service import AuthService
from decorators import login_required, group_required

app = Flask(__name__)
app.config.from_object(Config)

# Validate configuration on startup
try:
    Config.validate()
except ValueError as e:
    print(f"Configuration Error: {e}")
    print("Please set up your .env file based on .env.example")


@app.route('/')
def index():
    """Home page."""
    user = session.get('user')
    return render_template('index.html', user=user)


@app.route('/login')
def login():
    """Initiate login flow."""
    # Generate a state token to prevent CSRF
    session['state'] = str(uuid.uuid4())
    
    # Build authorization URL
    auth_url = AuthService._build_auth_url(
        scopes=Config.SCOPE,
        state=session['state']
    )
    
    return redirect(auth_url)


@app.route('/getAToken')
def authorized():
    """Handle the redirect from Azure AD after authentication."""
    # Verify state to prevent CSRF
    if request.args.get('state') != session.get('state'):
        flash('Invalid state parameter. Please try logging in again.', 'danger')
        return redirect(url_for('index'))
    
    # Check for errors in the response
    if 'error' in request.args:
        error_description = request.args.get('error_description', 'Unknown error')
        flash(f'Authentication error: {error_description}', 'danger')
        return redirect(url_for('index'))
    
    # Exchange authorization code for token
    code = request.args.get('code')
    if code:
        result = AuthService.get_token_from_code(code)
        
        if 'error' in result:
            flash(f"Authentication failed: {result.get('error_description')}", 'danger')
            return redirect(url_for('index'))
        
        # Get user information
        try:
            user_info = AuthService.get_user_info(result['access_token'])
            session['user'] = {
                'name': user_info.get('displayName'),
                'email': user_info.get('mail') or user_info.get('userPrincipalName'),
                'id': user_info.get('id')
            }
            
            # Check group membership
            is_authorized, message = AuthService.is_user_authorized(result['access_token'])
            session['authorized'] = is_authorized
            
            if is_authorized:
                flash(f"Welcome, {session['user']['name']}!", 'success')
                return redirect(url_for('dashboard'))
            else:
                flash(f'Access Denied: {message}', 'danger')
                return redirect(url_for('unauthorized'))
                
        except Exception as e:
            flash(f'Error fetching user information: {str(e)}', 'danger')
            return redirect(url_for('index'))
    
    flash('No authorization code received', 'danger')
    return redirect(url_for('index'))


@app.route('/dashboard')
@group_required
def dashboard():
    """Protected dashboard - requires group membership."""
    user = session.get('user')
    return render_template('dashboard.html', user=user)


@app.route('/profile')
@login_required
def profile():
    """User profile page - requires login only."""
    user = session.get('user')
    authorized = session.get('authorized', False)
    return render_template('profile.html', user=user, authorized=authorized)


@app.route('/unauthorized')
@login_required
def unauthorized():
    """Unauthorized access page."""
    user = session.get('user')
    return render_template('unauthorized.html', user=user)


@app.route('/logout')
def logout():
    """Logout and clear session."""
    logout_url = AuthService.logout()
    return redirect(logout_url)


@app.route('/health')
def health():
    """Health check endpoint."""
    return {'status': 'healthy', 'service': 'Flask Azure SSO'}, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=Config.DEBUG)
