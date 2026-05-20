# ScaleFit Login System - Setup Guide

## Overview
Professional login page with username, 10-digit mobile number, and password authentication for the ScaleFit fitness management application.

## Features

✅ **Dual Authentication Method**
- Login with username OR 10-digit mobile number
- Enhanced security with password validation

✅ **Professional UI**
- Modern, responsive design
- Smooth animations and transitions
- Gradient backgrounds and glassmorphic elements
- Mobile-friendly interface

✅ **Advanced Validation**
- Real-time mobile number format validation (10 digits)
- Real-time username validation
- Form submission validation
- User-friendly error messages

✅ **User Experience**
- Password visibility toggle
- Remember me option
- Auto-dismissing alerts
- Keyboard shortcuts support
- Loading states on submission

✅ **Security Features**
- CSRF protection
- Secure password handling
- Session management
- Database validation

---

## Installation & Setup

### 1. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

This will create the `UserProfile` table with the mobile number field.

### 2. Create a Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 3. Collect Static Files (Optional, for production)

```bash
python manage.py collectstatic
```

### 4. Run Development Server

```bash
python manage.py runserver
```

Access the application at: `http://127.0.0.1:8000/`

---

## Usage

### Login Page
- **URL**: `http://localhost:8000/fitness/login/` or `http://localhost:8000/`
- **Credentials Required**:
  - Username OR 10-digit mobile number
  - Password

### Dashboard (After Login)
- **URL**: `http://localhost:8000/fitness/dashboard/`
- View user information and fitness features

### Logout
- **URL**: `http://localhost:8000/fitness/logout/`
- Click the "Logout" button on the dashboard

### Admin Panel
- **URL**: `http://localhost:8000/admin/`
- Manage users, user profiles, and authentication

---

## Creating User Profiles

### Via Admin Panel
1. Go to `http://localhost:8000/admin/`
2. Navigate to "User Profiles"
3. Click "Add User Profile"
4. Select a User and enter the 10-digit mobile number
5. Click "Save"

### Via Django Shell

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from fitness.models import UserProfile

# Create a new user (optional, if not already exists)
user = User.objects.create_user(
    username='john_doe',
    email='john@example.com',
    password='SecurePassword123',
    first_name='John',
    last_name='Doe'
)

# Create user profile with mobile number
profile = UserProfile.objects.create(
    user=user,
    mobile_number='9876543210'
)

print(f"Profile created: {profile}")
```

### Via Python Script

Create a file named `create_users.py` in your project root:

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ScaleFit.settings')
django.setup()

from django.contrib.auth.models import User
from fitness.models import UserProfile

# User data
users_data = [
    {
        'username': 'user1',
        'email': 'user1@example.com',
        'first_name': 'User',
        'last_name': 'One',
        'password': 'User@123',
        'mobile': '9876543210'
    },
    {
        'username': 'user2',
        'email': 'user2@example.com',
        'first_name': 'User',
        'last_name': 'Two',
        'password': 'User@456',
        'mobile': '9876543211'
    }
]

for user_data in users_data:
    user, created = User.objects.get_or_create(
        username=user_data['username'],
        defaults={
            'email': user_data['email'],
            'first_name': user_data['first_name'],
            'last_name': user_data['last_name'],
        }
    )
    
    if created:
        user.set_password(user_data['password'])
        user.save()
    
    profile, profile_created = UserProfile.objects.get_or_create(
        user=user,
        defaults={'mobile_number': user_data['mobile']}
    )
    
    status = "Created" if created else "Already exists"
    print(f"{status}: {user.username} - {user.email} - {profile.mobile_number}")

print("\nUsers setup completed!")
```

Run the script:
```bash
python create_users.py
```

---

## File Structure

```
fitness/
├── migrations/
│   ├── __init__.py
│   └── 0001_initial.py
├── templates/
│   └── fitness/
│       ├── login.html          # Login form page
│       └── dashboard.html      # Dashboard after login
├── static/
│   ├── css/
│   │   └── login.css          # Professional login styling
│   └── js/
│       └── login.js           # Interactive JS features
├── admin.py                   # Admin configuration
├── models.py                  # UserProfile model
├── views.py                   # Authentication views
├── urls.py                    # App-specific URLs
├── apps.py
├── tests.py
└── __init__.py

ScaleFit/
├── settings.py                # Updated with templates, static dirs
├── urls.py                    # Updated with fitness URLs
├── asgi.py
└── wsgi.py
```

---

## API Endpoints

| Method | URL | Purpose |
|--------|-----|---------|
| GET | `/fitness/login/` | Display login page |
| POST | `/fitness/login/` | Process login |
| GET | `/fitness/dashboard/` | Show dashboard (restricted) |
| GET | `/fitness/logout/` | Logout user |

---

## Mobile Number Validation

- **Format**: Exactly 10 digits
- **Pattern**: `0-9` only
- **Examples**: 
  - ✅ Valid: `9876543210`, `8123456789`
  - ❌ Invalid: `987654321`, `98765432101`, `9876a43210`

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Enter` | Submit login form |
| `Ctrl + Shift + D` | Toggle "Remember me" checkbox |

---

## Troubleshooting

### Issue: Module Import Error
**Solution**: Run migrations
```bash
python manage.py migrate
```

### Issue: Static files not loading
**Solution**: Collect static files and ensure DEBUG=True in development
```bash
python manage.py collectstatic --noinput
```

### Issue: CSRF Token Error
**Solution**: Ensure you're accessing the login page directly (not embedded in iframe)

### Issue: Mobile Number Validation Failed
**Solution**: Ensure exactly 10 digits are entered with no special characters

---

## Customization

### Change Primary Color
Edit `/fitness/static/css/login.css`:
```css
--primary-color: #FF6B35;      /* Change this hex code */
--primary-dark: #E55100;       /* And this */
```

### Change Dashboard Landing Page
Edit `/fitness/views.py` in `login_view()`:
```python
return redirect('dashboard')  # Change 'dashboard' to your view name
```

### Add Forgot Password Feature
Create a new view in `views.py`:
```python
@require_http_methods(["GET", "POST"])
def forgot_password(request):
    # Your implementation here
    pass
```

---

## Security Best Practices

1. ✅ Always use HTTPS in production
2. ✅ Keep Django updated
3. ✅ Use strong passwords
4. ✅ Enable CSRF protection (already enabled)
5. ✅ Store sensitive data securely
6. ✅ Regularly backup your database

---

## Testing the Login

### Test Credentials
Use the admin superuser created earlier:
- **Username**: (your superuser username)
- **Password**: (your superuser password)

Then add a mobile number in Admin Panel:
- Go to `/admin/fitness/userprofile/`
- Click "Add User Profile"
- Select the superuser
- Enter a 10-digit mobile number

### Test Scenarios
1. **Valid Username + Password**: ✅ Login succeeds
2. **Valid Mobile + Password**: ✅ Login succeeds
3. **Invalid Credentials**: ❌ Error message shown
4. **Empty Fields**: ❌ Validation error shown
5. **Invalid Mobile Format**: ❌ Format validation error shown

---

## Support & Documentation

For more information:
- Django Documentation: https://docs.djangoproject.com/
- Django Authentication: https://docs.djangoproject.com/en/stable/topics/auth/
- Font Awesome Icons: https://fontawesome.com/

---

## License

Internal Project - ScaleFit

---

## Version History

- **v1.0.0** - Initial release with login page and dashboard
  - Username/Mobile authentication
  - 10-digit mobile validation
  - Professional UI
  - Dashboard page
  - User profile management

---

**Last Updated**: May 7, 2026
