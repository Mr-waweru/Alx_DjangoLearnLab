"""
Django settings for LibraryProject project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-f(o&ur4$5^ady8i&56zuufvdm6(olr+2zm_-^i1#%iznwgx%u('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'bookshelf',
    'relationship_app',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'LibraryProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'LibraryProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


""""Additional Security Modification"""
# Specifies a custom user model (CustomUser) as the authentication model, 
# allowing you to extend the default user model with additional fields and functionalities.
AUTH_USER_MODEL = [
    "bookshelf.CustomUser",
]

# Enables the Cross-Site Scripting (XSS) filter in modern browsers, which helps detect and prevent cross-site scripting attacks.
# When set to True, it tells the browser to block pages that appear to contain XSS vulnerabilities, adding an extra layer of defense.
SECURE_BROWSER_XSS_FILTER = True

# Prevents the website from being displayed in an iframe by any site, mitigating the risk of "clickjacking" attacks.
X_FRAME_OPTIONS = "DENY"

# This tells browsers not to try to guess the content type and forces them to adhere strictly to the declared Content-Type, helping prevent certain types of injection attacks
# Protects against content type sniffing vulnerabilities by setting the X-Content-Type-Options header to nosniff
SECURE_CONTENT_TYPE_NOSNIFF = True

# Ensures CSRF cookie is only sent over HTTPS connections, preventing the CSRF token from being intercepted on unencrypted HTTP connections.
CSRF_COOKIE_SECURE = True

# Ensures that the session cookie (used to keep users logged in) is only sent over HTTPS.
SESSION_COOKIE_SECURE = True


"""Configure Django for HTTPS Support"""
# any request made to an HTTP URL will be automatically redirected to HTTPS
SECURE_SSL_REDIRECT = True

# Instructs the browser to enforce HTTPS on your site for a year. 
# HSTS prevents downgrade attacks by ensuring users can't accidentally access an unsecured HTTP version.
SECURE_HSTS_SECONDS = 31536000

# Extends HSTS protection to all subdomains of your site.
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Indicates your site’s readiness to be included in browsers' "preload lists" for HSTS.
# browsers will always enforce HTTPS on your site and subdomains, even on the very first visit.
SECURE_HSTS_PRELOAD = True


"""Cookie Settings to Configure"""
# keeps session information protected by ensuring it’s only transmitted over encrypted connections.
SESSION_COOKIE_SECURE = True

# Ensures the CSRF cookie is only sent over HTTPS. 
CSRF_COOKIE_SECURE = True


"""Secure Headers Implementation"""
# Prevents the site from being embedded in an iframe, 
# which helps mitigate clickjacking attacks.
X_FRAME_OPTIONS = "DENY"


# Instructs the browser to stick to the declared Content-Type.
# Prevents browsers from "sniffing" the content type, which helps protect against MIME-type confusion attacks.
SECURE_CONTENT_TYPE_NOSNIFF = True

# This setting tells the browser to block pages that appear to contain XSS vulnerabilities.
SECURE_BROWSER_XSS_FILTER = True

# Used to ensure that Django correctly recognizes requests as HTTPS when your application is 
# deployed behind a reverse proxy (such as Nginx or a load balancer) that handles SSL termination.
# How It Works: The SECURE_PROXY_SSL_HEADER tuple instructs Django to check for the presence of HTTP_X_FORWARDED_PROTO and 
# verify that its value is https. 
# If both conditions are met, Django treats the request as secure (i.e., over HTTPS),
SECURE_PROXY_SSL_HEADER = (
    'HTTP_X_FORWARDED_PROTO',
    'https',
)
