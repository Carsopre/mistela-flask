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
