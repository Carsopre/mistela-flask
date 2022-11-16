from flask import Blueprint, render_template

from mistelaflask.utils import admin_required
from mistelaflask.views.admin_views.admin_view_events import AdminViewEvents
from mistelaflask.views.admin_views.admin_view_guests import AdminViewGuests
from mistelaflask.views.admin_views.admin_view_invitations import AdminViewInvitations

admin_view = Blueprint("admin", __name__, url_prefix="/admin/")


@admin_view.route("")
@admin_required
def index():
    return render_template("admin/admin_index.html")


event_view = AdminViewEvents.register(admin_view)
guest_view = AdminViewGuests.register(admin_view)
invitation_view = AdminViewInvitations.register(admin_view)
