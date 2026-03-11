from functools import wraps
from flask import session, redirect, url_for, flash
from auth_service import AuthService


def login_required(f):
    """Decorator to require user to be logged in."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user'):
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def group_required(f):
    """Decorator to require user to be member of authorized group."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user'):
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        
        # Check if user is authorized (group membership already validated during login)
        if not session.get('authorized'):
            flash('You do not have permission to access this resource.', 'danger')
            return redirect(url_for('unauthorized'))
        
        return f(*args, **kwargs)
    return decorated_function
