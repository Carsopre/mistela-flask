from functools import wraps

from flask import current_app, request
from flask_login import config, current_user


def admin_required(func):
    """
    Redefinition of the native `login_required` so that enforces the user to be an admin.

    Args:
        func (Callable): Function to be evaluted.

    Returns:
        Any: Will return unauthorized when the user is not logged in or has admin rights.
    """

    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in config.EXEMPT_METHODS or current_app.config.get(
            "LOGIN_DISABLED"
        ):
            pass
        elif not current_user.is_authenticated or not current_user.admin:
            return current_app.login_manager.unauthorized()

        # flask 1.x compatibility
        # current_app.ensure_sync is only available in Flask >= 2.0
        if callable(getattr(current_app, "ensure_sync", None)):
            return current_app.ensure_sync(func)(*args, **kwargs)
        return func(*args, **kwargs)

    return decorated_view
