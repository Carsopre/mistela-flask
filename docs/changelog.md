## v0.6.0 (2022-11-17)

### Feat

- **guest_invitations.html**: Guest can now manage their own invitations

## v0.5.0 (2022-11-16)

### Feat

- **admin_invitation_edit_bulk**: It is now possible to do a bulk edit from the admin menu
- **admin_invitations_summary.html**: Added summary for invitations
- **admin_views/invitations**: Added templates for create, read, delete invitations
- **admin_required**: Added method admin_required to replace and enforce a better decorator
- **admin/guests**: We can now do full CRUD operations on Guests (users without admin rights)
- **admin/guests**: We can now display an admin menu for listing all registered guests and their invitations
- **admin_view_guests.py**: Created new admin view guests file and class
- **admin_events**: Added better admin page for events via tabs
- **auth.py**: Users can now do a first login with a OTP
- **flask_admin**: Added flask admin layer to better handle the models CRUD panel

## v0.4.0 (2022-11-13)

### Feat

- **mistelaflask/__init__.py**: SECRET_KEY and DATABASE_URI are now read from the environment variables

### Fix

- **pyproject.toml**: Forgot a closing statement

## v0.3.0 (2022-11-13)

### Feat

- **main.py;guest_responses.html**: We now allow the user to update their responses to invitations
- **guest_responses.html**: Added page for a guest to manage their invitations
- **admin/responses**: Added endpoint for admin responses
- **admin.py;admin_guests.html**: Added logic to add guests and display them in order
- **admin_events;admin_guests**: Added logic to create events and guests
- **models.py**: Added new tables

### Fix

- Fixed logic for adding guests from admin menu

## v0.2.0 (2022-10-23)

### Feat

- **Protecting pages**: Added constraints to limit available information for not logged users
- **auth.py**: Added logic to logging in and user_loader
- **auth.py**: Added login post method
- **login;signup**: Added auth to both login and setup. Adapted templates
- **auth:signup**: Added signup logic
- Fixed initialization of database'

### Fix

- Small fix in auth

## v0.1.0 (2022-10-20)

### Feat

- Initial commit
