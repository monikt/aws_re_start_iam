# DESAFÍO 1: AWS S3 Backup Automatizado

Solución completa de backup automatizado a AWS S3 con notificaciones por email en Python.

## 🎯 Requisitos del Desafío

✅ **Crear script Python que:**
- Tome los archivos de `/workspaces/aws_re_start_iam/desafio_1/files`
- Genere backup automático 1 vez por día
- Cree el bucket donde se almacenará el backup
- Por cada ejecución cree la carpeta del día con los archivos
- Notifique vía email el éxito o fallo del proceso

## 📦 Solución Implementada

Se proporcionan los siguientes archivos:

### Archivos Principales

| Archivo | Descripción |
|---------|-------------|
| `backup_s3.py` | **Script principal** - Realiza el backup a S3 |
| `scheduler.py` | Automatización diaria - Usa APScheduler |
| `config.py` | Configuración centralizada (credenciales, email, etc.) |
| `email_notifier.py` | Módulo de notificaciones por email (SMTP/SES) |
| `diagnostico.py` | Verificación de configuración antes de ejecutar |

### Archivos de Configuración

| Archivo | Descripción |
|---------|-------------|
| `.env.example` | Template de variables de entorno |
| `requirements.txt` | Dependencias Python a instalar |
| `IMPLEMENTACION.md` | Guía completa de instalación y uso |

### Directorios

| Directorio | Descripción |
|-----------|-------------|
| `files/` | Archivos a respaldar (entrada) |
| `logs/` | Archivos de log (creado automáticamente) |

---

## 🚀 Inicio Rápido

### 1️⃣ Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 2️⃣ Configurar Credenciales

Copiar template y editar:

```bash
cp .env.example .env
```

Editar `.env` con:
- AWS Access Key ID
- AWS Secret Access Key
- AWS Region
- Email (SMTP o AWS SES)

### 3️⃣ Ejecutar Diagnóstico

```bash
python3 diagnostico.py
```

Verifica que todo está correctamente configurado.

### 4️⃣ Ejecutar Backup Manual

```bash
python3 backup_s3.py
```

Realiza un backup inmediatamente.

### 5️⃣ Automatizar Diariamente

```bash
python3 scheduler.py
```

Se ejecutará diariamente a la hora especificada en `.env` (por defecto 02:00).

---

## 📋 Características Implementadas

✨ **Cumple todos los requisitos del desafío:**

1. ✅ **Toma archivos de la ruta local**
   - Lee todos los archivos de `/workspaces/aws_re_start_iam/desafio_1/files`
   - Maneja múltiples formatos de archivo

2. ✅ **Genera backup automático diariamente**
   - Usa APScheduler para programación
   - Configurable a cualquier hora del día
   - Puede ejecutarse vía cron, systemd o directamente

3. ✅ **Crea bucket en S3**
   - Verifica si existe, si no lo crea
   - Soporta cualquier región de AWS
   - Maneja errores de nombre duplicado

4. ✅ **Crea carpeta del día**
   - Estructura: `s3://bucket/backups/YYYY-MM-DD/`
   - Un backup por día automáticamente
   - Historial organizado por fechas

5. ✅ **Notifica por email**
   - Envía email al finalizar (exitoso o fallido)
   - Soporta SMTP (Gmail, Outlook, etc.)
   - Soporta AWS SES
   - Email HTML formateado
   - Incluye detalles: timestamp, archivos, errores

---

## 🔍 Architeuctura de la Solución

```
┌─────────────────────────────────────┐
│    SCHEDULER / EJECUCIÓN MANUAL     │
│        (scheduler.py / cron)        │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│      BACKUP S3 (backup_s3.py)       │
├─────────────────────────────────────┤
│  • Leer archivos locales            │
│  • Conectar a AWS S3                │
│  • Crear bucket si no existe        │
│  • Subir archivos con fecha         │
│  • Registrar en logs                │
└──────────────┬──────────────────────┘
               │
       ┌───────┴────────┐
       ▼                ▼
    AWS S3         EMAIL NOTIFIER
   (Bucket)        (email_notifier.py)
   s3://           • SMTP
   bucket/         • AWS SES
   backups/        • HTML formateado
   YYYY-MM-DD/
```

---

## 📊 Estructura de Datos en S3

Después de ejecutar, verás:

```
s3://mi-backup-bucket-automatizado/
└── backups/
    ├── 2024-03-18/
    │   ├── backup1.txt
    │   ├── backup2.txt
    │   └── ... (todos los archivos del día)
    ├── 2024-03-19/
    │   ├── backup1.txt
    │   ├── backup2.txt
    │   └── ...
    └── 2024-03-20/
        └── ...
```

---

## 📈 Ejemplo de Ejecución

```bash
$ python3 backup_s3.py

2024-03-18 10:30:45 - root - INFO - ============================================================
2024-03-18 10:30:45 - root - INFO - INICIANDO PROCESO DE BACKUP
2024-03-18 10:30:45 - root - INFO - ============================================================
2024-03-18 10:30:45 - root - INFO - Conexión a AWS S3 establecida exitosamente
2024-03-18 10:30:46 - root - INFO - Bucket creado exitosamente: mi-backup-bucket-automatizado
2024-03-18 10:30:46 - root - INFO - Carpeta de backup será: s3://mi-backup-bucket-automatizado/backups/2024-03-18
2024-03-18 10:30:47 - root - INFO - Se encontraron 20 archivo(s) para subir
2024-03-18 10:30:47 - root - INFO - Subiendo: backup1.txt -> s3://mi-backup-bucket-automatizado/backups/2024-03-18/backup1.txt
2024-03-18 10:30:48 - root - INFO - ✓ Archivo subido: backup1.txt
...
2024-03-18 10:31:00 - root - INFO - ✓ Archivo subido: backup20.txt
2024-03-18 10:31:00 - root - INFO - Backup completado exitosamente. 20 archivo(s) subido(s)
2024-03-18 10:31:00 - root - INFO - ============================================================
2024-03-18 10:31:00 - root - INFO - BACKUP FINALIZADO
2024-03-18 10:31:00 - root - INFO - ============================================================
2024-03-18 10:31:01 - root - INFO - Enviando notificación por email...
2024-03-18 10:31:02 - root - INFO - Email enviado exitosamente a ['destinatario@ejemplo.com']
```

---

## 📧 Ejemplo de Email Recibido

**Asunto:** `[AWS Backup] Proceso de backup EXITOSO - 18/03/2024 10:30`

**Contenido HTML:**

```
📦 Reporte de Backup Automatizado a AWS S3

✅ EXITOSO

Mensaje: Backup completado exitosamente. 20 archivo(s) subido(s)

Información                    Detalle
─────────────────────────────────────────
Timestamp                      2024-03-18T10:31:00.000000
Bucket S3                      s3://mi-backup-bucket-automatizado
Archivos Subidos              20
Errores                        0
```

---

## 🛠️ Comandos Útiles

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar diagnóstico de configuración
python3 diagnostico.py

# Hacer backup manual
python3 backup_s3.py

# Iniciar scheduler automático
python3 scheduler.py

# Ejecutar backup mediante scheduler (para testing)
python3 scheduler.py run-now

# Ver logs
tail -50 logs/backup.log

# Verificar en AWS
aws s3 ls s3://mi-backup-bucket-automatizado/
aws s3 ls s3://mi-backup-bucket-automatizado/backups/2024-03-18 --recursive

# Contar archivos
aws s3 ls s3://mi-backup-bucket-automatizado/backups/2024-03-18 --recursive | wc -l
```

---

## 📞 Documentación

Para más detalles, ver:

- **[IMPLEMENTACION.md](IMPLEMENTACION.md)** - Guía completa de instalación
- **[config.py](config.py)** - Variables de configuración
- **[backup_s3.py](backup_s3.py)** - Código del backup
- **[email_notifier.py](email_notifier.py)** - Módulo de email
- **[diagnostico.py](diagnostico.py)** - Verificación de configuración

---

## ✅ Checklist de Implementación

- [x] Script Python para backup a S3
- [x] Toma archivos de la ruta especificada
- [x] Crea bucket automáticamente
- [x] Crea carpeta por día (YYYY-MM-DD)
- [x] Automatización diaria (APScheduler)
- [x] Notificaciones por email
- [x] Manejo de errores robusto
- [x] Logging detallado
- [x] Configuración flexible
- [x] Diagnóstico/validación

---

**Desafío completado** ✅

**Última actualización:** Marzo 2026
