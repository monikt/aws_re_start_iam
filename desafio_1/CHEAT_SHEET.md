# DESAFÍO 1: Cheat Sheet - Referencia Rápida

Guía visual y comandos rápidos para la solución de backup S3.

---

## 📦 INSTALACIÓN (30 segundos)

```bash
cd /workspaces/aws_re_start_iam/desafio_1

# Instalar dependencias
pip install -r requirements.txt

# Crear configuración
cp .env.example .env

# Editar .env con tus credenciales de AWS y email
nano .env  # O tu editor preferido
```

---

## ⚙️ CONFIGURACIÓN DE .env

```env
# AWS
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=wJal...
AWS_REGION=us-east-1
S3_BUCKET_NAME=mi-backup-bucket

# Email
SMTP_USERNAME=tu-email@gmail.com
SMTP_PASSWORD=xxxx-xxxx-xxxx-xxxx  # App password de Google
FROM_EMAIL=tu-email@gmail.com
TO_EMAILS=destinatario@ejemplo.com

# Automatización
BACKUP_TIME=02:00
TIMEZONE=America/Bogota
```

---

## ✅ VERIFICACIÓN RÁPIDA

```bash
# Diagnóstico completo (RECOMENDADO PRIMERO)
python3 diagnostico.py

# Verificar AWS conectividad
aws s3 ls

# Verificar Python
python3 --version

# Verificar dependencias
pip list | grep boto3
```

---

## 🚀 EJECUCIÓN

### Ejecutar Backup Manual (Prueba)
```bash
python3 backup_s3.py
```

**Salida esperada:** ✅ Archivos subidos

### Iniciar Backup Automático (Diario)
```bash
python3 scheduler.py
```

**Salida esperada:** Mensaje indicando próxima ejecución

### Menú Interactivo
```bash
python3 ejemplo_uso.py
```

---

## 📊 VERIFICAR RESULTADOS

### En AWS
```bash
# Ver buckets creados
aws s3 ls

# Ver archivos en bucket
aws s3 ls s3://mi-backup-bucket

# Ver archivos de hoy
aws s3 ls s3://mi-backup-bucket/backups/2024-03-18 --recursive

# Contar archivos
aws s3 ls s3://mi-backup-bucket/backups/2024-03-18 --recursive | wc -l
```

### En Email
- ✅ Revisa inbox
- 📧 Busca emails de "tu-email@ejemplo.com"
- 📧 Revisa Spam si no llega

### En Logs
```bash
tail -50 logs/backup.log
tail -f logs/backup.log      # Ver en tiempo real
grep ERROR logs/backup.log   # Ver errores

```

---

## 🎯 FLUJO DE EJECUCIÓN

```
┌──────────────────┐
│  Crear .env      │
│  Actualizar      │
│  credenciales    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  diagnostico.py  │ ← Verificar todo está bien
│  Ver si ✅       │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  backup_s3.py    │ ← Test manual
│  (una vez)       │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  scheduler.py    │ ← Automático diariamente
│  (siempre)       │
└──────────────────┘
```

---

## 🔧 SOLUCIONES RÁPIDAS

| Problema | Solución |
|----------|----------|
| `ModuleNotFoundError: boto3` | `pip install -r requirements.txt` |
| `Unable to locate credentials` | Editar `.env` con Access Key/Secret Key |
| `Email nicht llegue` | Verificar `SEND_EMAILS=True` en .env |
| `NoSuchBucket` | Cambiar `S3_BUCKET_NAME` a nombre único |
| `Permission denied` | `mkdir -p logs && chmod 755 logs` |
| `Scheduler no se ejecuta` | `python3 diagnostico.py` (debug) |

---

## 🎮 COMANDOS PRINCIPALES

```bash
# Instalación
pip install -r requirements.txt
cp .env.example .env

# Verificación
python3 diagnostico.py
aws iam get-user

# Ejecución
python3 backup_s3.py              # Manual
python3 scheduler.py              # Automático
python3 scheduler.py run-now      # via Scheduler
python3 ejemplo_uso.py            # Menú

# Información
tail -f logs/backup.log           # Ver logs
aws s3 ls                         # Ver buckets
aws s3 ls s3://bucket/backups/    # Ver archivos

# Limpiar
rm logs/backup.log
rm ~/.aws/credentials  # ⚠️ Peligroso
```

---

## 📁 ESTRUCTURA DE ARCHIVOS

```
desafio_1/
├── backup_s3.py          ← PRINCIPAL
├── scheduler.py          ← AUTOMATIZACIÓN
├── config.py             ← CONFIGURACIÓN
│
├── files/                ← ENTRADA (archivos a respaldar)
├── logs/                 ← SALIDA (logs de ejecución)
│
├── .env                  ← CONFIGURACIÓN (PRIVADO)
├── .env.example          ← TEMPLATE
├── requirements.txt      ← DEPENDENCIAS
│
├── README.md             ← Guía rápida
├── IMPLEMENTACION.md     ← Guía completa (⭐ LEER)
├── RESOLUCION_RAPIDA.md  ← Troubleshooting
└── CHEAT_SHEET.md        ← Este archivo
```

---

## 📧 EJEMPLO DE EMAIL RECIBIDO

**Asunto:** `[AWS Backup] Proceso de backup EXITOSO - 18/03/2024 10:30`

```
📦 Reporte de Backup Automatizado a AWS S3
✅ EXITOSO
Mensaje: Backup completado exitosamente. 20 archivo(s) subido(s)

Información                  Detalle
─────────────────────────────────────────
Timestamp                    2024-03-18T10:31:00
Bucket S3                    s3://mi-backup-bucket
Archivos Subidos            20
Errores                     0
```

---

## ⏰ CRONOGRAMA DURANTE EL DÍA

```
02:00 AM      ← Backup automático se ejecuta
              → Archivos suben a S3
              → Email se envía

Durante el día ← Script en background esperando

02:00 AM +1   ← Nuevo backup (próximo día)
(siguiente día)
```

---

## 🔐 SEGURIDAD - NO HACER

```
❌ NO:
git add .env                 # Nunca commitear credenciales
git add logs/                # No subes logs a repos
                            
echo $AWS_SECRET_ACCESS_KEY # No muestres en terminal

cat ~/.aws/credentials      # No copies en Slack/Teams
```

```
✅ SÍ:
echo .env >> .gitignore
git add .gitignore

cp .env.example .env
# Editar solo localmente
```

---

## 🆘 ÚLTIMO RECURSO SI NADA FUNCIONA

```bash
# 1. Limpiar todo
rm -f .env
cp .env.example .env

# 2. Reinstalar
pip uninstall -y boto3 apscheduler
pip install -r requirements.txt

# 3. Verificar
python3 diagnostico.py 2>&1 | head -50

# 4. Debug
DEBUG=True python3 backup_s3.py

# 5. Contactar soporte con:
# - Salida de diagnostico.py
# - Últimas líneas de logs/backup.log
# - Exacto comando que ejecutaste
# - Exacto error que viste
```

---

## 🎓 APRENDER MÁS

```
📚 Archivos a leer:
1. README.md              ← Empieza aquí (5 min)
2. IMPLEMENTACION.md      ← Guía completa (20 min)
3. RESOLUCION_RAPIDA.md   ← Si algo falla (10 min)

💻 Código a entender:
1. backup_s3.py           ← Lógica principal
2. config.py              ← Variables de configuración
3. email_notifier.py      ← Envío de emails

🔗 Recursos externos:
- https://docs.aws.amazon.com/s3/
- https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
```

---

## ✨ EJEMPLO COMPLETO (5 MINUTOS)

```bash
# 1. Preparar (2 min)
cp .env.example .env
# Editar .env: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, etc.

# 2. Verificar (1 min)
python3 diagnostico.py

# 3. Probar (1 min)
python3 backup_s3.py

# 4. Automatizar (1 min)
python3 scheduler.py

# 5. Confirmar
# ✅ Ver logs: tail -f logs/backup.log
# ✅ Ver AWS: aws s3 ls s3://mi-backup-bucket
# ✅ Ver email: Revisar inbox
```

---

## 🚀 PRÓXIMOS PASOS

```
Fase 1: Instalación (Ahora)
  → pip install -r requirements.txt
  → cp .env.example .env
  ✅ Completado

Fase 2: Configuración (5 min)
  → Editar .env
  → Ejecutar diagnostico.py
  ✅ Cuando termines

Fase 3: Testing (5 min)
  → python3 backup_s3.py
  → Verificar en AWS y email
  ✅ Cuando termines

Fase 4: Automatización (1 min)
  → python3 scheduler.py
  ✅ LISTO PARA PRODUCCIÓN
```

---

**Última actualización:** Marzo 2026
**Versión:** 1.0.0
**Estado:** ✅ PRODUCCIÓN LISTA
