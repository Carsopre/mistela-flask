from flask import Blueprint, render_template

from mistelaflask.views.admin_view_base import admin_required
from mistelaflask.views.admin_view_events import AdminViewEvents
from mistelaflask.views.admin_view_guests import AdminViewGuests
from mistelaflask.views.admin_view_invitations import AdminViewInvitations

admin = Blueprint("admin", __name__, url_prefix="/admin/")


@admin.route("")
@admin_required
def index():
    return render_template("admin/admin_index.html")


event_view = AdminViewEvents.register(admin)
guest_view = AdminViewGuests.register(admin)
invitation_view = AdminViewInvitations.register(admin)
