# AWS S3 Backup Automatizado - Guía de Implementación

Solución completa en Python para realizar backups automáticos diarios a AWS S3 con notificaciones por email.

## 📋 Tabla de Contenidos

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [Automatización](#automatización)
- [Monitoreo](#monitoreo)
- [Troubleshooting](#troubleshooting)

---

## ✨ Características

✅ **Backup Automatizado Diario**
- Se ejecuta automáticamente a una hora especificada
- Crea carpetas por fecha (YYYY-MM-DD)
- Sube archivos con estructura clara

✅ **Gestión de Buckets S3**
- Crea automáticamente el bucket si no existe
- Verifica conflictos de nombres
- Compatible con cualquier región de AWS

✅ **Notificaciones por Email**
- Confirmación de ejecución exitosa o fallida
- HTML formateado con detalles del backup
- Soporte para SMTP (Gmail, Outlook, etc.) o AWS SES

✅ **Logging Completo**
- Registro detallado de cada operación
- Almacenado en archivo `logs/backup.log`
- Salida en consola en tiempo real

✅ **Manejo de Errores Robusto**
- Captura y reporta excepciones
- Continúa incluso si algunos archivos fallan
- Notificación de errores por email

---

## 📋 Requisitos

### Software
- Python 3.8 o superior
- pip (gestor de paquetes Python)
- Git (opcional)

### Credenciales AWS
- Access Key ID
- Secret Access Key
- Región de AWS

### Credenciales de Email
- SMTP: Email y contraseña de usuario SMTP
- AWS SES: Cuenta configurada en AWS

---

## 🚀 Instalación

### Paso 1: Clonar o descargar el repositorio

```bash
cd /workspaces/aws_re_start_iam/desafio_1
```

### Paso 2: Crear entorno virtual (recomendado)

```bash
python3 -m venv venv
```

Activar entorno virtual:

**En Linux/Mac:**
```bash
source venv/bin/activate
```

**En Windows:**
```bash
venv\Scripts\activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

Verificar instalación:
```bash
pip list
```

Deberías ver:
```
boto3
botocore
APScheduler
python-dotenv
```

---

## ⚙️ Configuración

### Paso 1: Copiar archivo de configuración

```bash
cp .env.example .env
```

### Paso 2: Configurar AWS Credentials

**Opción A: Variables de Entorno (Recomendado)**

```bash
export AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
export AWS_SECRET_ACCESS_KEY="wJalrXUtn..."
export AWS_REGION="us-east-1"
export S3_BUCKET_NAME="mi-backup-bucket-automatizado"
```

O en archivo `.env`:
```
AWS_ACCESS_KEY_ID=tu-access-key-id
AWS_SECRET_ACCESS_KEY=tu-secret-access-key
AWS_REGION=us-east-1
S3_BUCKET_NAME=mi-backup-bucket-automatizado
```

**Opción B: Editar config.py directamente**

```python
# config.py
AWS_ACCESS_KEY_ID = 'tu-access-key-id'
AWS_SECRET_ACCESS_KEY = 'tu-secret-access-key'
```

### Paso 3: Configurar Notificaciones por Email

#### Para Gmail (RECOMENDADO)

1. Ir a https://myaccount.google.com/apppasswords
2. Seleccionar:
   - App: Mail
   - Device: Windows Computer (o tu dispositivo)
3. Copiar la "App Password" generada
4. En `.env`:

```env
EMAIL_PROVIDER=smtp
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=tu-email@gmail.com
SMTP_PASSWORD=xxxx-xxxx-xxxx-xxxx
FROM_EMAIL=tu-email@gmail.com
TO_EMAILS=destinatario@ejemplo.com
SEND_EMAILS=True
```

#### Para Outlook/Hotmail

```env
SMTP_HOST=smtp.outlook.com
SMTP_PORT=587
SMTP_USERNAME=tu-email@outlook.com
SMTP_PASSWORD=tu-contraseña
```

#### Para AWS SES

```env
EMAIL_PROVIDER=ses
SES_REGION=us-east-1
FROM_EMAIL=tu-email@ejemplo.com
TO_EMAILS=destinatario@ejemplo.com
```

⚠️ **Nota:** En AWS SES, debes verificar las direcciones de email primero.

### Paso 4: Configurar Hora y Zona Horaria

```env
BACKUP_TIME=02:00
TIMEZONE=America/Bogota
```

Timezones comunes:
- `UTC` - Hora UTC
- `America/New_York` - Hora Este
- `America/Mexico_City` - Hora Central
- `America/Los_Angeles` - Hora del Pacífico
- `America/Bogota` - Hora Bogotá
- `Europe/London` - Hora Londres
- `Europe/Paris` - Hora París
- `Asia/Tokyo` - Hora Tokio

### Paso 5: Verificar Configuración

```bash
python3 -c "from config import *; print('✓ Configuración cargada exitosamente')"
```

---

## 📖 Uso

### Ejecutar Backup Manual

```bash
python3 backup_s3.py
```

**Salida esperada:**
```
2024-03-18 10:30:45,123 - root - INFO - ============================================================
2024-03-18 10:30:45,124 - root - INFO - INICIANDO PROCESO DE BACKUP
2024-03-18 10:30:45,125 - root - INFO - ============================================================
2024-03-18 10:30:45,500 - root - INFO - Conexión a AWS S3 establecida exitosamente
2024-03-18 10:30:46,000 - root - INFO - Bucket creado exitosamente: mi-backup-bucket-automatizado
2024-03-18 10:30:46,100 - root - INFO - Se encontraron 20 archivo(s) para subir
2024-03-18 10:30:47,500 - root - INFO - ✓ Archivo subido: backup1.txt
2024-03-18 10:30:48,000 - root - INFO - ✓ Archivo subido: backup2.txt
...
2024-03-18 10:31:00,000 - root - INFO - Backup completado exitosamente. 20 archivo(s) subido(s)
2024-03-18 10:31:00,500 - root - INFO - BACKUP FINALIZADO
```

### Verificar en AWS Console

```bash
aws s3 ls
aws s3 ls s3://mi-backup-bucket-automatizado
aws s3 ls s3://mi-backup-bucket-automatizado/backups/2024-03-18 --recursive
```

---

## ⏰ Automatización

### Opción 1: Usando APScheduler (Recomendado)

Ejecutar scheduler en segundo plano:

```bash
python3 scheduler.py
```

Se ejecutará continuamente, realizando backup a la hora especificada.

**Salida:**
```
╔════════════════════════════════════════════╗
║    AWS S3 BACKUP SCHEDULER - EJECUTANDO    ║
╠════════════════════════════════════════════╣
║  • Backup programado a las: 02:00          │
║  • Timezone: America/Bogota               │
║  • Estado: ACTIVO ✓                        │
║                                            │
║  Para detener, presiona CTRL+C             │
╚════════════════════════════════════════════╝
```

Ejecutar backup inmediatamente en modo prueba:
```bash
python3 scheduler.py run-now
```

### Opción 2: Usando CRON (Linux/Mac)

Para ejecutar diariamente a las 2 AM:

```bash
crontab -e
```

Agregar línea:
```
0 2 * * * cd /workspaces/aws_re_start_iam/desafio_1 && /usr/bin/python3 backup_s3.py >> logs/backup.log 2>&1
```

Ver tareas cron:
```bash
crontab -l
```

### Opción 3: Usando systemd (Linux)

Crear archivo `/etc/systemd/system/aws-backup.service`:

```ini
[Unit]
Description=AWS S3 Backup Service
After=network.target

[Service]
Type=simple
User=tu-usuario
WorkingDirectory=/workspaces/aws_re_start_iam/desafio_1
ExecStart=/usr/bin/python3 scheduler.py
Restart=on-failure
RestartSec=60
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

Habilitar y iniciar:
```bash
sudo systemctl enable aws-backup.service
sudo systemctl start aws-backup.service
```

Verificar estado:
```bash
sudo systemctl status aws-backup.service
```

---

## 📊 Monitoreo

### Ver Logs

```bash
# Últimas 50 líneas
tail -50 logs/backup.log

# Ver en tiempo real (con tail -f)
tail -f logs/backup.log

# Buscar errores
grep ERROR logs/backup.log

# Ver resumen del día
grep "$(date +%Y-%m-%d)" logs/backup.log
```

### Verificar Emails Recibidos

Revisar bandeja de entrada para confirmar:
- ✅ Emails de backup exitoso
- ⚠️ Emails de errores

### Verificar en AWS Console

```bash
# Listar buckets
aws s3 ls

# Ver contenido del backup
aws s3 ls s3://mi-backup-bucket-automatizado/backups/ --recursive

# Contar archivos subidos
aws s3 ls s3://mi-backup-bucket-automatizado/backups/2024-03-18 --recursive | wc -l
```

---

## 🔍 Troubleshooting

### Problema: "Unable to locate credentials"

**Solución:**
```bash
# Verificar credenciales
aws configure list

# O establecer variables de entorno
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
```

### Problema: "Email connection refused"

**Solución:**
```bash
# Para Gmail: Verificar que usaste App Password
# No la contraseña de tu cuenta

# Para otros: Verificar credenciales SMTP
env | grep SMTP
```

### Problema: "NoSuchBucket"

**Solución:**
```bash
# El bucket no existe o está mal escrito
aws s3 ls

# Verificar nombre exacto
echo $S3_BUCKET_NAME
```

### Problema: "AccessDenied"

**Solución:**
```bash
# Verificar permisos IAM
aws iam get-user

# La política debe incluir:
# s3:GetObject
# s3:PutObject
# s3:ListBucket
# s3:CreateBucket
```

### Problema: Scheduler no se ejecuta

**Solución:**
```bash
# Ejecutar manualmente para testing
python3 backup_s3.py

# Verificar logs
tail -50 logs/backup.log

# Modo debug
DEBUG=True python3 scheduler.py
```

---

## 📝 Estructura de Archivos

```
desafio_1/
├── backup_s3.py          # Script principal de backup
├── scheduler.py          # Automatización de backups
├── config.py             # Configuración centralizada
├── email_notifier.py     # Módulo de notificaciones
├── requirements.txt      # Dependencias Python
├── .env.example          # Variables de entorno (template)
├── IMPLEMENTACION.md     # Esta guía
├── logs/                 # Directorio de logs
│   └── backup.log       # Archivo de log
├── files/                # Archivos a respaldar
│   ├── backup1.txt
│   ├── backup2.txt
│   └── ...
└── venv/                 # Entorno virtual (opcional)
```

---

## 🔐 Seguridad

### Mejores Prácticas

1. **Nunca commitear variables sensibles:**
   ```bash
   echo ".env" >> .gitignore
   echo "*.log" >> .gitignore
   ```

2. **Usar IAM User específico:**
   - No usar credenciales root
   - Crear usuario con permisos mínimos (S3, SES)

3. **Rotar credenciales regularmente:**
   - Cambiar Access Keys cada 90 días
   - Cambiar App Passwords cada 6 meses

4. **Usar MFA:**
   - Habilitar 2FA en cuenta AWS
   - Considerar MFA con AWS SES

5. **Encripción:**
   - S3: Habilitar Server-Side Encryption
   - SMTP: Usar TLS/SSL

### Política IAM Mínima Recomendada

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:CreateBucket",
                "s3:GetBucketLocation",
                "s3:ListBucket",
                "s3:PutObject",
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::mi-backup-bucket*",
                "arn:aws:s3:::mi-backup-bucket*/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "ses:SendEmail",
                "ses:SendRawEmail"
            ],
            "Resource": "*"
        }
    ]
}
```

---

## 📞 Soporte

### Recursos Útiles

- [AWS CLI Documentation](https://docs.aws.amazon.com/cli/)
- [Boto3 Documentation](https://boto3.amazonaws.com/)
- [APScheduler Documentation](https://apscheduler.readthedocs.io/)
- [Python Email SMTP](https://docs.python.org/3/library/smtplib.html)

### Comandos Útiles

```bash
# Ver archivos creados
find . -type f -name "*.py"

# Contar archivos a respaldar
ls -1 files/ | wc -l

# Ver historial de cambios
git log --oneline

# Debug: Ver variables de entorno
env | grep -E "AWS_|SMTP_|EMAIL_"
```

---

**Última actualización:** Marzo 2026
**Versión:** 1.0.0
