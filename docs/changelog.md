## v0.14.3 (2022-12-11)

### Fix

- **admin_view_main_events.py**: Fix updating location from a main event

## v0.14.2 (2022-12-11)

### Fix

- **admin/events**: Now we can manage an event time (Start / duration)

## v0.14.1 (2022-12-11)

### Fix

- **admin_view_guests.py**: Fix removing user

## v0.14.0 (2022-12-11)

## v0.7.0 (2022-11-20)

### Feat

- **GuestViewEvents**: Added view for events (timeline)
- **guest_invitations**: Guests handle their invitation as 'one' instead of per event
- **guest_invitations.html**: Guest can now manage their own invitations
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

### Fix

- **auth.py**: Fix mismatch between user and username

## v0.4.0 (2022-11-13)

### Feat

- **mistelaflask/__init__.py**: SECRET_KEY and DATABASE_URI are now read from the environment variables

### Fix

- **pyproject.toml**: Forgot a closing statement

## v0.13.0 (2022-12-11)

### Feat

- **scripts**: We now have available scripts to process images while sandboxing

## v0.12.0 (2022-11-28)

### Feat

- **static**: We now provide the static files through flask environment variables

## v0.11.0 (2022-11-28)

### Feat

- **flask-mail**: Added support to send mails when a user has sent their RSVP

### Fix

- **auth.py**: Fixed logging in
- **auth.py**: Small bug fix when no password still present

## v0.10.0 (2022-11-21)

### Feat

- **guest/events**: Added location information to the event tab

### Fix

- **guest_view_events.py**: Fixed error when no main events present
- **guest_views**: Fixed error when no main events available

## v0.9.0 (2022-11-21)

### Feat

- **locations**: Added  html templates for locations admin view
- **AdminViewLocations**: Created view for admin locations
- **MainEvent**: It is now possible to encapsulate all events under a main one and display it in the index page
- **models**: It is possible to add a new main event with a concrete location for the index view

## v0.8.1 (2022-11-21)

### Fix

- **wsgi.py**: Removed self from local method
- **wsgi.py**: We can now install the development environment when provided

## v0.8.0 (2022-11-21)

### Feat

- **guest_events.html**: Added detailed timeline

## v0.7.0 (2022-11-20)

### Feat

- **GuestViewEvents**: Added view for events (timeline)
- **guest_invitations**: Guests handle their invitation as 'one' instead of per event
- **guest_invitations.html**: Guest can now manage their own invitations

### Fix

- **auth.py**: Fix mismatch between user and username

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
