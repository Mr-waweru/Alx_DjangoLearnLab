Library Project

# Permissions Setup

## Custom Permissions
- **can_view**: Allows viewing of instances.
- **can_create**: Allows creation of new instances.
- **can_edit**: Allows editing of instances.
- **can_delete**: Allows deletion of instances.

## User Groups
- **Editors**: Can create and edit instances.
- **Viewers**: Can only view instances.
- **Admins**: Can view, create, edit, and delete instances.

## Enforcing Permissions
Permissions are enforced in views using Django’s `@permission_required` decorator. Ensure that the correct permission is checked before allowing access to any restricted action.

# Security Settings

- **DEBUG**: Set to `False` in production to avoid exposing sensitive information.
- **CSRF_COOKIE_SECURE**: Ensures CSRF tokens are only sent over HTTPS.
- **CSP**: Implemented Content Security Policy to restrict the sources of content on the site.

## CSRF Protection

All forms include `{% csrf_token %}` to prevent CSRF attacks.

## Data Access

Used Django ORM to avoid SQL injection and validated user inputs through Django forms.

## HTTPS and Security Settings

- **SECURE_SSL_REDIRECT**: Redirects all HTTP traffic to HTTPS.
- **SECURE_HSTS_SECONDS**: Enforces HSTS for one year.
- **SESSION_COOKIE_SECURE**: Ensures session cookies are only sent over HTTPS.
- **X_FRAME_OPTIONS**: Protects against clickjacking by preventing the site from being framed.