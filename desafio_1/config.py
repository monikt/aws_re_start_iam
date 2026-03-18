"""
Configuración para el script de backup de S3
Modifica los valores según tu entorno
"""

import os
from pathlib import Path

# =====================================================
# CONFIGURACIÓN DE AWS
# =====================================================

# Credenciales AWS (obtenidas de aws configure)
# Alternativamente, usa variables de entorno:
# AWS_ACCESS_KEY_ID y AWS_SECRET_ACCESS_KEY

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', 'tu-access-key-id')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', 'tu-secret-access-key')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')

# Nombre del bucket S3 (debe ser único globalmente)
# Formato: nombre-unico-backup-TIMESTAMP
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'mi-backup-bucket-automated')

# =====================================================
# CONFIGURACIÓN DE DIRECTORIOS
# =====================================================

# Ruta de los archivos locales a respaldar
LOCAL_FILES_PATH = os.getenv(
    'LOCAL_FILES_PATH',
    '/workspaces/aws_re_start_iam/desafio_1/files'
)

# Ruta del archivo de log
LOG_FILE = os.path.join(
    os.path.dirname(__file__),
    'logs',
    'backup.log'
)

# Crear directorio de logs si no existe
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# =====================================================
# CONFIGURACIÓN DE EMAIL
# =====================================================

EMAIL_CONFIG = {
    # Especifica el proveedor: 'smtp' o 'ses' (AWS SES)
    'provider': os.getenv('EMAIL_PROVIDER', 'smtp'),
    
    # Para SMTP (Gmail, Outlook, etc.)
    'smtp': {
        'host': os.getenv('SMTP_HOST', 'smtp.gmail.com'),
        'port': int(os.getenv('SMTP_PORT', '587')),
        'username': os.getenv('SMTP_USERNAME', 'tu-email@gmail.com'),
        'password': os.getenv('SMTP_PASSWORD', 'tu-contraseña-app'),
        'use_tls': os.getenv('SMTP_USE_TLS', 'True') == 'True',
    },
    
    # Para AWS SES (Simple Email Service)
    'ses': {
        'region': os.getenv('SES_REGION', 'us-east-1'),
    },
    
    # Remitente y destinatarios
    'from_email': os.getenv('FROM_EMAIL', 'tu-email@ejemplo.com'),
    'to_emails': os.getenv(
        'TO_EMAILS',
        'destinatario@ejemplo.com'
    ).split(','),  # Separa múltiples emails con comas
    
    # Habilitar notificaciones
    'enabled': os.getenv('SEND_EMAILS', 'True') == 'True',
}

# =====================================================
# CONFIGURACIÓN DE AUTOMATIZACIÓN
# =====================================================

# Hora del día en que se ejecutará el backup (formato 24h: HH:MM)
BACKUP_TIME = os.getenv('BACKUP_TIME', '02:00')  # 2 AM

# Timezone (ej: 'UTC', 'America/New_York', 'America/Bogota')
TIMEZONE = os.getenv('TIMEZONE', 'UTC')

# =====================================================
# CONFIGURACIÓN DE SEGURIDAD
# =====================================================

# Habilitar validación SSL para SMTP
VERIFY_SSL = os.getenv('VERIFY_SSL', 'True') == 'True'

# Retención de backups (días)
# 0 = sin límite
BACKUP_RETENTION_DAYS = int(os.getenv('BACKUP_RETENTION_DAYS', '30'))

# =====================================================
# INFORMACIÓN PARA DEBUG
# =====================================================

DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Mostrar configuración cargada
if DEBUG:
    print(f"""
    === CONFIGURACIÓN CARGADA ===
    AWS_REGION: {AWS_REGION}
    S3_BUCKET_NAME: {S3_BUCKET_NAME}
    LOCAL_FILES_PATH: {LOCAL_FILES_PATH}
    LOG_FILE: {LOG_FILE}
    EMAIL_PROVIDER: {EMAIL_CONFIG['provider']}
    BACKUP_TIME: {BACKUP_TIME}
    TIMEZONE: {TIMEZONE}
    DEBUG: {DEBUG}
    """)
