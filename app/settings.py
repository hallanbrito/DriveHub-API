import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Helper nativo para carregar arquivo .env sem dependências obrigatórias
def _load_env_file(env_file_path: Path) -> None:
    if not env_file_path.is_file():
        return
    with open(env_file_path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            key, val = stripped.split("=", 1)
            os.environ.setdefault(key.strip(), val.strip().strip("'\""))

_load_env_file(BASE_DIR / ".env")

# Segregação de Ambientes
DJANGO_ENV = os.environ.get("DJANGO_ENV", "development").lower()
IS_PRODUCTION = DJANGO_ENV == "production"

if IS_PRODUCTION:
    # Produção estrita: nenhuma chave ou host default permissivo
    SECRET_KEY = os.environ["SECRET_KEY"]
    DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1", "yes")
    hosts = os.environ.get("ALLOWED_HOSTS", "")
    ALLOWED_HOSTS = [h.strip() for h in hosts.split(",") if h.strip()]
    if not ALLOWED_HOSTS:
        raise ValueError("ALLOWED_HOSTS deve ser definido explicitamente em produção.")

    cors_allowed = os.environ.get("CORS_ALLOWED_ORIGINS", "")
    CORS_ALLOWED_ORIGINS = [o.strip() for o in cors_allowed.split(",") if o.strip()]
    CORS_ALLOW_ALL_ORIGINS = False
else:
    # Desenvolvimento / Testes locais: defaults seguros e prontos para uso
    SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-drivehub-local-dev-key")
    DEBUG = os.environ.get("DEBUG", "True").lower() in ("true", "1", "yes")
    hosts_str = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1,0.0.0.0,testserver")
    ALLOWED_HOSTS = [h.strip() for h in hosts_str.split(",") if h.strip()]

    cors_origins_env = os.environ.get("CORS_ALLOWED_ORIGINS")
    if cors_origins_env:
        CORS_ALLOWED_ORIGINS = [o.strip() for o in cors_origins_env.split(",") if o.strip()]
        CORS_ALLOW_ALL_ORIGINS = False
    else:
        # Default local: apenas origens locais do frontend (Vite porta 5173 e 3000)
        CORS_ALLOWED_ORIGINS = [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ]
        CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOW_CREDENTIALS = True

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "drf_spectacular",
    "apps.vehicles.apps.VehiclesConfig",
    "apps.sales.apps.SalesConfig",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "app.urls"

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [],
    "APP_DIRS": True,
    "OPTIONS": {
        "context_processors": [
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
        ],
    },
}]

WSGI_APPLICATION = "app.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
}

SPECTACULAR_SETTINGS = {
    "TITLE": "DriveHub API",
    "DESCRIPTION": "API REST para governança e gestão de concessionárias com Clean Architecture e DDD",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
