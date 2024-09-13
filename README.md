Role-based User Authentication and Dashboard System
Project Overview
This is a Python-based user authentication system with role-based access control, supporting four roles: Superadmin, Admin, Superuser, and User. The application includes JWT authentication and is deployed on an AWS EC2 Free Tier instance.

Roles and Permissions
Superadmin:

Full control over the system.
Can create and manage Admins, Superusers, and Users.
Can assign roles and view all users.
Admin:

Can create and manage Superusers and Users.
Can view Superusers and Users created by them.
Superuser:

Can manage specific company departments.
Cannot manage or view other users.
User:

Basic access with no management privileges.
Project Features
Role-based Authentication using JWT tokens.
Dashboard view with different levels of access based on user roles.
RESTful APIs for managing users and roles.
SQLite as a lightweight database.
Deployment on AWS EC2 Free Tier.
Tech Stack
Backend Framework: Django
Authentication: JWT (JSON Web Token)
Database: SQLite
Deployment: AWS EC2 Free Tier
Setup Instructions
Prerequisites
Python 3.12
AWS EC2 Free Tier instance
