from __future__ import annotations

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from flask_mail import Mail, Message

from mistelaflask import db, models
from mistelaflask.views.guest_views.guest_view_protocol import GuestViewProtocol


class GuestViewInvitations(GuestViewProtocol):
    view_name: str = "invitations"
    _mail: Mail = None

    def _render_guest_view_template(self, template_name: str, **context):
        return render_template(f"guest/" + template_name, **context)

    @classmethod
    def register(cls, guest_blueprint: Blueprint) -> GuestViewInvitations:
        _view = cls()
        guest_blueprint.add_url_rule(
            "/invitations/", "invitations_list", _view._list_view, methods=["GET"]
        )
        guest_blueprint.add_url_rule(
            "/invitations/",
            "invitations_bulk_update",
            _view._bulk_update_view,
            methods=["POST", "PUT"],
        )
        return _view

    @login_required
    def _list_view(self):
        # current_user
        user_invitations = models.UserEventInvitation.query.filter_by(
            guest_id=current_user.id
        )
        if not user_invitations:
            return self._render_guest_view_template(
                "guest_invitations.html",
                invitation=models.UserEventInvitation(guest=current_user),
            )
        _all_values = [
            (ui.response, ui.n_adults, ui.n_children, ui.n_babies, ui.remarks)
            for ui in user_invitations
        ]
        if not _all_values:
            flash(
                f"An error occured while loading your invitation. Please contact us if the problem persists.",
                category="danger",
            )
            return redirect(url_for("main.index"))
        _list_values = list(zip(*_all_values))
        _assisting = all(_list_values[0])
        if not _assisting:
            _assisting = False if all(ui is False for ui in _list_values[0]) else None
        _adults = max(_list_values[1])
        _children = max(_list_values[2])
        _babies = max(_list_values[3])
        _remarks = "\n".join(
            [_remark if _remark else "" for _remark in _list_values[4]]
        )

        return self._render_guest_view_template(
            "guest_invitations.html",
            invitation=models.UserEventInvitation(
                guest=current_user,
                response=_assisting,
                n_adults=_adults,
                n_children=_children,
                n_babies=_babies,
                remarks=_remarks,
            ),
        )

    @login_required
    def _bulk_update_view(self):
        _response = request.form.get("response", None)
        if _response:
            _response = _response.lower() == "true"
        else:
            flash(
                f"Please provide a valid answer for the main question `Will you be assisting to our event?`",
                category="danger",
            )
            return redirect(url_for("main.invitations_list"))
        _n_adults = min(
            int(request.form.get(f"n_adults")),
            current_user.max_adults,
        )
        _n_children = int(request.form.get(f"n_children"))
        _n_babies = int(request.form.get(f"n_babies"))
        _remarks = request.form.get(f"remarks", "").strip()
        if _remarks:
            _remarks = _remarks.splitlines()
        _email = request.form.get("email", "")
        for _idx, _inv in enumerate(
            models.UserEventInvitation.query.filter_by(guest_id=current_user.id)
        ):
            _inv.response = _response
            _inv.n_adults = _n_adults
            _inv.n_children = _n_children
            _inv.n_babies = _n_babies
            if _remarks and len(_remarks) > _idx:
                _inv.remarks = _remarks[_idx]
            else:
                _inv.remarks = ""
            db.session.add(_inv)
            db.session.commit()
        with current_app.app_context():
            _admin_mail = current_app.config.get("MAIL_USERNAME")
            msg = Message(
                subject=f"RSVP from {current_user.name}",
                sender=_admin_mail,
                recipients=[
                    _admin_mail,
                ],  # replace with your email for testing
                body="""
                Response: {}
                Adults: {}
                Children: {}
                Babies: {}
                Remarks: {}
                Email: {}
                """.format(
                    _response, _n_adults, _n_children, _n_babies, _remarks, _email
                ),
            )
            _mail = Mail(current_app)
            _mail.send(msg)
        return redirect(url_for("main.invitations_list"))

    @login_required
    def _bulk_detail_update_view(self):
        # Currently disabled from templates.
        for _inv in models.UserEventInvitation.query.filter_by(guest=current_user.id):
            _response = request.form.get("response", None)
            if _response:
                _response = _response.lower() == "true"
            else:
                _response = None
            _inv.response = _response
            _inv.n_adults = min(
                int(request.form.get(f"{_inv.id}_n_adults", _inv.n_adults)),
                _inv.guest.max_adults,
            )
            _inv.n_children = int(
                request.form.get(f"{_inv.id}_n_children", _inv.n_children)
            )
            _inv.n_babies = int(request.form.get(f"{_inv.id}_n_babies", _inv.n_babies))
            _inv.remarks = request.form.get(f"{_inv.id}_remarks", _inv.remarks)
            db.session.add(_inv)
            db.session.commit()
        return redirect(url_for("main.invitations_list"))
