"""
Django settings for hrmm project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
# import zoneinfo
from pathlib import Path
import os
from datetime import timedelta

# CORS_ORIGIN_ALLOW_ALL = True
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-jdpf2v1-4x!m&v)f!x%2z0u22)^si=i4h7t21vivl^^2%3#w0%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '192.168.1.18',
    '127.0.0.1',
    '192.168.1.17',
    # ".vercel.app",
    'hrmbe.onrender.com',
    'www.hrmbe.onrender.com',
]


# Application definition
    
INSTALLED_APPS = [
    # "daphne",
    "admin_interface",
    "colorfield",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'base.apps.BaseConfig',
    'department.apps.DepartmentConfig',
    'leave.apps.LeaveConfig',
    'leave_type.apps.LeaveTypeConfig',
    # 'organization.apps.OrganizationConfig',
    'project.apps.ProjectConfig',
    'task.apps.TaskConfig',
    'rest_framework',
    'djoser',
    'rest_framework_swagger',
    'timesheet.apps.TimeSheetConfig',
    'job.apps.JobConfig',
    'salary.apps.SalaryConfig',
    "rest_framework.authtoken",
    'corsheaders',
    # "import_export",
    'drf_spectacular',
    "role.apps.RoleConfig",
    
]
X_FRAME_OPTIONS = "SAMEORIGIN"              
SILENCED_SYSTEM_CHECKS = ["security.W019"]  
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'coreheaders.middleware.CorsMiddleware'
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'base.middleware.CustomAdminMiddleware',
]
CSRF_TRUSTED_ORIGINS=[    ' https://hrmbe.onrender.com',
    'https://www.hrmbe.onrender.com',
    ] 

ROOT_URLCONF = 'hrmm.urls'
ASGI_APPLICATION = "hrmm.asgi.application"
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
# CSRF_COOKIE_SECURE = True  # Nếu sử dụng HTTPS
WSGI_APPLICATION = 'hrmm.wsgi.application'
CORS_ALLOWED_ORIGINS=[
    "http://localhost:5173",
    "https://hrmbe.onrender.com",
]
SECURITY_PASSWORD_SALT="abcd"
BACKEND_URL = "http://192.168.1.17:8765"
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
}}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Bangkok'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'staticfiles')]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL='base.UserAccount'

EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_HOST_USER='test12202023test@gmail.com'
EMAIL_HOST_PASSWORD='prymsxigzsntalpj'
EMAIL_USE_TLS=True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# #gửi email xác thực bằng djoser
# DJOSER={
#     'LOGIN_FIELD':'email',
#     'USER_CREATE_PASSOWRD_RETYPE':True,
#     'USERNAME_CHANGED_EMAIL_CONFIRMATION':True,
#     'PASSWORD_CHANGED_EMAIL_CONFIRMATION':True,
#     'SEND_CONFIRMATION_EMAIL':True,
#     'SET_USERNAME_RETYPE':True,
#     'SET_PASSWORD_RETYPE':True,
#     'PASSWORD_RESET_CONFIRM_URL':'/password/reset/{uid}/{token}',
#     'USERNAME_RESET_CONFIRM_URL':'/email/reset/{uid}/{token}',
#     'ACTIVATION_URL':'/activate/{uid}/{token}',
#     'SEND_ACTIVATION_EMAIL':True,
#     'SERIALIZERS':{
#         'user_create':'base.serializers.UserRegisterSerializer',
#         'user':'base.serializers.UserRegisterSerializer',
#         'user_delete':'djoser.serializers.UserDeleteSerializer',
#     }
# }
REST_FRAMEWORK = {
    # 'DEFAULT_SCHEMA_CLASS':'rest_framework.schemas.coreapi.AutoSchema' ,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication', # xác thực người dùng 
        # "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        'rest_framework.authentication.BasicAuthentication',
   ),
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'base.permissions.IsAdminOrReadOnly',
    #     'base.permissions.IsOwnerOrReadonly',
    # ],

    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    # "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticatedOrReadOnly"),
    # 'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    # 'DEFAULT_PERMISSION_CLASSES': ( 'rest_framework.permissions.IsAdminUser', ),

}

SPECTACULAR_SETTING={
    "TITLE":"Django DRF Ecommerce",
    
}
SIMPLE_JWT = {
#    'AUTH_HEADER_TYPES': ('JWT',),
    "USER_ID_FIELD": "UserID",
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}
