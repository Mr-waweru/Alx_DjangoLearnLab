# Authentication System Documentation

## Features
1. **Registration**: Allows users to create an account.
2. **Login**: Authenticates users to access their profile.
3. **Logout**: Safely logs users out of their account.
4. **Profile Management**: Enables users to view and manage their profile.

## How to Test
- Navigate to `/register` to create an account.
- Test `/login` and `/logout` for authentication.
- Ensure `/profile` only works for authenticated users.

## Security Measures
- CSRF protection enabled on all forms.
- Passwords securely hashed with Django’s built-in algorithms.


# Blog Application with CRUD Operations

## Features
- **List Posts**: Displays all blog posts with titles and publication dates.
- **View Post Details**: Shows the full content of a selected post.
- **Create Posts**: Authenticated users can create new posts.
- **Edit Posts**: Authors can edit their own posts.
- **Delete Posts**: Authors can delete their own posts.

## URLs
- `/`: View all posts.
- `/post/<id>/`: View a specific post.
- `/post/new/`: Create a new post.
- `/post/<id>/edit/`: Edit a post.
- `/post/<id>/delete/`: Delete a post.

## Permissions
- Only authenticated users can create, update, or delete posts.
- Authors can only modify or delete their own posts.
- List and detail views are public.

## Setup
1. Migrate the database: `python manage.py migrate`
2. Run the server: `python manage.py runserver`
3. Access the app at `http://127.0.0.1:8000/`.

