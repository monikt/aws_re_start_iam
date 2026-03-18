# DESAFÍO 1: Guía de Resolución Rápida

Soluciones rápidas para problemas comunes en la solución de backup S3.

---

## ⚡ Resolución Rápida

### Problema: "ModuleNotFoundError: No module named 'boto3'"

```bash
# Solución: Instalar dependencias
pip install -r requirements.txt

# O instalar boto3 directamente
pip install boto3 apscheduler python-dotenv
```

---

### Problema: "Unable to locate credentials"

```bash
# Verificar que las credenciales estén configuradas
echo $AWS_ACCESS_KEY_ID
echo $AWS_SECRET_ACCESS_KEY

# O editar config.py con tus credenciales
# O crear archivo .env con:
AWS_ACCESS_KEY_ID=tu-access-key-id
AWS_SECRET_ACCESS_KEY=tu-secret-access-key
```

---

### Problema: Archivo .env no se carga

```bash
# Asegúrate de haberlo renombrado correctamente
ls -la .env

# Crear desde el template si no existe
cp .env.example .env
```

---

### Problema: "Email connection refused"

```bash
# Para Gmail: Verificar que generaste App Password
# 1. https://myaccount.google.com/apppasswords
# 2. Selecciona Mail y Windows Computer
# 3. Copia la contraseña generada (16 caracteres)
# 4. En .env:
SMTP_PASSWORD=xxxx-xxxx-xxxx-xxxx

# NO es tu contraseña regular de Gmail
# NO uses contraseña de 2FA
```

---

### Problema: S3 bucket ya existe

```bash
# Es normal. El script verifica si existe y lo usa si ya está creado.
# Si quieres crear uno nuevo, usa un nombre diferente en .env:
S3_BUCKET_NAME=mi-backup-nuevo-nombre
```

---

### Problema: "NoSuchBucket" o "AccessDenied"

```bash
# Verificacion:
1. Verificar nombre de bucket (sensible a mayúsculas)
2. Ver buckets existentes: aws s3 ls
3. Verificar región: aws s3api get-bucket-location --bucket nombre

# O crear uno nuevo:
S3_BUCKET_NAME=nombre-unico-nuevo
```

---

### Problema: Scheduler no se ejecuta

```bash
# Ejecutar en modo verbose para debug
DEBUG=True python3 scheduler.py

# Ver logs en tiempo real
tail -f logs/backup.log

# O ejecutar backup manual para testear
python3 backup_s3.py
```

---

### Problema: "Permission denied" al crear logs

```bash
# Crear directorio de logs manualmente
mkdir -p logs

# O ejecutar con permisos suficientes
sudo python3 backup_s3.py
```

---

### Problema: Archivos no se suben a S3

```bash
# Verificar que hay archivos en la carpeta
ls -la files/

# Si está vacía, crear archivos de prueba:
for i in {1..5}; do echo "Contenido $i" > files/backup$i.txt; done

# Luego ejecutar backup
python3 backup_s3.py
```

---

### Problema: "Bucket name contains invalid characters"

```bash
# Los nombres de bucket solo pueden contener:
# - Letras minúsculas (a-z)
# - Números (0-9)
# - Guiones (-) - pero no al inicio ni final
# - Puntos (.) - pero no consecutivos

# ✅ Válidos:
# - my-backup-bucket
# - backup.bucket.2024
# - my-bucket-123

# ❌ Inválidos:
# - MyBackupBucket (mayúsculas)
# - my_backup (guiones bajos)
# - -my-bucket (comienza con guión)
```

---

### Problema: Email no llega

```bash
# 1. Verificar que SEND_EMAILS=True en .env
# 2. Verificar folder Spam/Junk
# 3. Revisar logs para errores:
tail -f logs/backup.log | grep -i email

# 4. Testear email manualmente:
python3 email_notifier.py
```

---

### Problema: "local_files_path does not exist"

```bash
# Verificar ruta correcta
echo $LOCAL_FILES_PATH

# Asegúrate que la ruta existe:
ls -la /workspaces/aws_re_start_iam/desafio_1/files

# O crear los directorios:
mkdir -p /workspaces/aws_re_start_iam/desafio_1/files
```

---

### Problema: Los archivos se suben pero no aparecen en S3

```bash
# Esperar a que se sincronicen (puede tomar segundos)
sleep 5

# Verificar con AWS CLI:
aws s3 ls s3://mi-backup-bucket-automatizado/

# Si aún no aparecen, revisar:
aws s3api list-objects-v2 --bucket mi-backup-bucket-automatizado --prefix backups/

# O con consola: https://s3.console.aws.amazon.com
```

---

### Problema: Scheduler requiere demasiada CPU

```bash
# Es normal en primer plano. Para usar background:
# Opción 1: Usar systemd (Linux)
sudo systemctl start aws-backup

# Opción 2: Usar screen (cualquier OS)
screen -S backup python3 scheduler.py

# Opción 3: Usar cron (Linux/Mac)
crontab -e
# Agregar: 0 2 * * * cd /workspaces/aws_re_start_iam/desafio_1 && python3 backup_s3.py
```

---

### Problema: Diagnostico.py falla

```bash
# Ejecutar diagnóstico en modo verbose
python3 -u diagnostico.py

# Ver errores completos
python3 diagnostico.py 2>&1 | head -50

# O ejecutar verificaciones individuales:
python3 -c "from config import AWS_REGION; print(AWS_REGION)"
python3 -c "import boto3; print('boto3 OK')"
```

---

## 🔍 Debug Avanzado

### Ver qué está pasando en AWS CLI

```bash
# Modo verbose
aws s3 ls --debug 2>&1 | head -50

# Ver credenciales cargadas
aws configure list

# Ver configuración actual
cat ~/.aws/config
cat ~/.aws/credentials
```

---

### Probar conectividad

```bash
# Ping a AWS
ping aws.amazon.com

# Test de S3
aws s3 ls

# Test específico
aws s3api head-bucket --bucket mi-backup-bucket-automatizado
```

---

### Ver logs del sistema

```bash
# Últimas líneas del log
tail -50 logs/backup.log

# Tail en vivo
tail -f logs/backup.log

# Buscar errores
grep ERROR logs/backup.log

# Contar ejecuciones
grep "INICIANDO PROCESO" logs/backup.log | wc -l
```

---

## 📋 Checklist de Verificación

Antes de contactar soporte, verifica:

- [ ] Las dependencias están instaladas: `pip list | grep boto3`
- [ ] Las credenciales están configuradas: `aws configure list`
- [ ] La conectividad funciona: `aws s3 ls`
- [ ] Los archivos existen: `ls files/`
- [ ] El archivo .env existe: `ls -la .env`
- [ ] El directorio logs existe: `mkdir -p logs`
- [ ] Puedes conectar a AWS: `python3 backup_s3.py`

---

## 🆘 Si nada funciona

1. **Reset completo:**
   ```bash
   # Eliminar archivos de configuración
   rm -f .env
   cp .env.example .env
   
   # Reinstalar dependencias
   pip install --upgrade -r requirements.txt
   ```

2. **Verificar Python:**
   ```bash
   python3 --version  # Debe ser 3.8+
   pip --version
   ```

3. **Ejecutar diagnóstico:**
   ```bash
   python3 diagnostico.py
   ```

4. **Ver logs completos:**
   ```bash
   tail -100 logs/backup.log
   ```

5. **Contactar soporte con:**
   - Salida de `diagnostico.py`
   - Últimas líneas de `logs/backup.log`
   - Tu comando exact que falló
   - Mensaje de error exacto

---

## 💡 Tips Útiles

**Para testing sin AWS:**
```bash
# Si no tienes credenciales reales, puedes:
# 1. Usar AWS Free Tier (primeros 12 meses)
# 2. Usar LocalStack (emulador local)
# 3. Ver logs en logs/backup.log sin credenciales

# LocalStack (opcional):
pip install localstack
localstack start
export AWS_ENDPOINT_URL=http://localhost:4566
```

**Para automatizar:**
```bash
# Cron (Linux/Mac):
crontab -e
0 2 * * * /usr/bin/python3 /ruta/backup_s3.py

# Systemd (Linux):
sudo systemctl enable aws-backup
sudo systemctl start aws-backup

# Task Scheduler (Windows):
python c:\ruta\backup_s3.py
```

**Para notificaciones:**
```bash
# Testear email
python3 email_notifier.py

# Ver si llegó a inbox/spam
# Buscar correo de: tu-email@ejemplo.com

# Si no llega:
tail -20 logs/backup.log | grep -i email
```

---

**Última actualización:** Marzo 2026
