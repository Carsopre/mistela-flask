from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required

from mistelaflask import models
from mistelaflask.views.admin_view_events import AdminViewEvents
from mistelaflask.views.admin_view_guests import AdminViewGuests
from mistelaflask.views.admin_view_invitations import AdminViewInvitations

admin = Blueprint("admin", __name__, url_prefix="/admin/")


@admin.route("")
@login_required
def index():
    if not current_user.admin:
        return redirect(url_for("main.index"))
    return render_template("admin/admin_index.html")


event_view = AdminViewEvents.register(admin)
guest_view = AdminViewGuests.register(admin)
invitation_view = AdminViewInvitations.register(admin)
