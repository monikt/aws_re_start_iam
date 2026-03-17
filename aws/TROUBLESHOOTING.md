# AWS CLI - Guía de Troubleshooting y Problemas Comunes

Soluciones para los problemas más frecuentes con AWS CLI.

---

## 📋 Tabla de Problemas

- [AWS CLI no está instalado](#aws-cli-no-está-instalado)
- [Error: "Unable to locate credentials"](#error-unable-to-locate-credentials)
- [Error: "InvalidUserID.Malformed"](#error-invaliduseridmalformed)
- [Error: "NoSuchBucket"](#error-nosuchbucket)
- [Error: "AccessDenied"](#error-accessdenied)
- [Error: "InvalidParameterValue"](#error-invalidparametervalue)
- [Credenciales expiradas](#credenciales-expiradas)
- [Región incorrecta](#región-incorrecta)
- [Comandos muy lentos](#comandos-muy-lentos)

---

## ❌ AWS CLI no está instalado

### Síntoma:
```
bash: aws: command not found
```

### Solución:

1. **Verificar si está instalado:**
   ```bash
   which aws
   ```

2. **Instalar AWS CLI v2:**
   ```bash
   # En Linux/Mac usando el script incluido
   cd /workspaces/aws_re_start_iam/aws
   sudo ./install
   ```

3. **O instalarlo sin sudo:**
   ```bash
   cd /workspaces/aws_re_start_iam/aws
   ./install -i ~/.local/aws-cli -b ~/.local/bin
   export PATH=~/.local/bin:$PATH
   ```

4. **Verificar instalación:**
   ```bash
   aws --version
   ```

---

## ❌ Error: "Unable to locate credentials"

### Síntoma:
```
Unable to locate credentials. You can configure credentials by running "aws configure".
```

### Causas:
- Las credenciales no están configuradas
- El archivo `~/.aws/credentials` no existe
- Las credenciales están mal formateadas

### Solución:

**Paso 1: Ejecutar aws configure**
```bash
aws configure
```

**Paso 2: Verificar que se guardaron**
```bash
cat ~/.aws/credentials
```

Debería verse así:
```
[default]
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

**Paso 3: Si aún no funciona**
```bash
# Verificar permisos del archivo
ls -la ~/.aws/credentials

# Debería tener permisos 600
chmod 600 ~/.aws/credentials
```

**Paso 4: Probar conexión**
```bash
aws sts get-caller-identity
```

---

## ❌ Error: "InvalidUserID.Malformed"

### Síntoma:
```
An error occurred (InvalidUserID.Malformed) when calling the ListUserPolicies operation:
The user with name usuario_inexistente cannot be found.
```

### Causas:
- El nombre de usuario está mal escrito
- El usuario no existe
- Permissions insuficientes

### Solución:

**Paso 1: Verificar nombre exacto**
```bash
aws iam list-users --query 'Users[].UserName' --output text
```

**Paso 2: Buscar usuario específico**
```bash
aws iam list-users --query 'Users[?contains(UserName, `parte_del_nombre`)]' --output table
```

**Paso 3: Usar nombre correcto**
```bash
# Correcto: sin espacios, con guiones si es necesario
aws iam get-user --user-name nombre-correcto
```

---

## ❌ Error: "NoSuchBucket"

### Síntoma:
```
An error occurred (NoSuchBucket) when calling the HeadBucket operation: 
The specified bucket does not exist
```

### Causas:
- El nombre del bucket está mal
- El bucket no existe en tu cuenta
- El bucket está en otra región
- No tienes permisos

### Solución:

**Paso 1: Listar buckets existentes**
```bash
aws s3 ls
```

**Paso 2: Verificar nombre exacto (sensible a mayúsculas)**
```bash
# Los nombres de buckets son en minúsculas
aws s3 ls s3://mi-bucket-correcto
```

**Paso 3: Verificar región del bucket**
```bash
# Ver región del bucket
aws s3api get-bucket-location --bucket mi-bucket
```

**Paso 4: Si el bucket está en otra región**
```bash
# Especificar región
aws s3api head-bucket --bucket mi-bucket --region us-west-2
```

---

## ❌ Error: "AccessDenied"

### Síntoma:
```
An error occurred (AccessDenied) when calling the ListUsers operation: 
User: arn:aws:iam::123456789012:user/usuario is not authorized to perform: 
iam:ListUsers on resource: *
```

### Causas:
- Tu usuario no tiene permisos para esa operación
- Falta una política IAM
- MFA requerida

### Solución:

**Paso 1: Verificar permisos**
```bash
# Ver políticas de tu usuario
aws iam list-attached-user-policies --user-name tu-usuario

# Ver políticas inline
aws iam list-user-policies --user-name tu-usuario
```

**Paso 2: Get-user para ver identidad actual**
```bash
aws sts get-caller-identity
```

**Paso 3: Si es MFA requerida**
```bash
# Usar con --serial-number y --token-code
aws sts get-session-token --serial-number arn:aws:iam::123456789012:mfa/usuario --token-code 123456
```

**Paso 4: Contactar al administrador**
```
Solicitar que agreguen la política:
- Para IAM: AmazonIAMFullAccess o IAMReadOnlyAccess
- Para S3: AmazonS3FullAccess o AmazonS3ReadOnlyAccess
```

---

## ❌ Error: "InvalidParameterValue"

### Síntoma:
```
An error occurred (InvalidParameterValue) when calling the ListUsers operation: 
Invalid value 'invalid-table' for output format. Valid output formats are: json, text, table, yaml
```

### Causas:
- Formato de salida incorrecto
- Parámetro mal escrito
- Región no válida

### Solución:

**Paso 1: Formatos válidos**
```bash
# Válidos:
aws iam list-users --output json    # JSON (por defecto)
aws iam list-users --output table   # Tabla ASCII
aws iam list-users --output text    # Texto plano
aws iam list-users --output yaml    # YAML

# Incorrecto:
aws iam list-users --output tabla   # ❌ tabla no existe
```

**Paso 2: Verificar región válida**
```bash
# Válidas:
us-east-1, us-west-2, eu-west-1, ap-southeast-1, etc.

# Configurar región
aws configure set region us-east-1
```

---

## ❌ Credenciales expiradas

### Síntoma:
```
The date value did not match the format 'YYYY-MM-DDTHH:MM:SSZ'
Error: The current date is before the start date of the temporary session
```

### Causas:
- Reloj del sistema desincronizado
- Token de sesión temporal expirado
- Credenciales muy antiguas

### Solución:

**Paso 1: Sincronizar reloj del sistema**
```bash
# Ver fecha actual
date

# En Linux: sincronizar con servidor NTP
sudo timedatectl set-ntp true

# En Mac
sudo ntpdate -s time.nist.gov
```

**Paso 2: Regenerar credenciales**
```bash
aws configure
```

**Paso 3: Si usas sesión temporal, renovarla**
```bash
# Obtener nuevas credenciales temporales
aws sts get-session-token
```

---

## ❌ Región incorrecta

### Síntoma:
```
No resources found in us-east-2 region (aunque sabes que están en us-west-1)
```

### Solución:

**Paso 1: Ver región configurada**
```bash
aws configure list | grep region
```

**Paso 2: Cambiar región**
```bash
# Opción 1: Cambiar globalmente
aws configure set region us-west-1

# Opción 2: Especificar para un comando
aws s3 ls --region us-west-1

# Opción 3: Usar variable de entorno
export AWS_DEFAULT_REGION=us-west-1
aws s3 ls
```

**Paso 3: Ver configuración actual**
```bash
cat ~/.aws/config
```

---

## ❌ Comandos muy lentos

### Síntoma:
```
# Tarda más de 10 segundos en responder
aws iam list-users
```

### Causas:
- Conexión lenta a internet
- Servidor AWS con latencia
- Demasiados resultados
- Región incorrecta

### Solución:

**Paso 1: Medir velocidad**
```bash
time aws iam list-users
```

**Paso 2: Usar región más cercana**
```bash
aws configure set region us-east-1  # Intenta diferentes regiones
```

**Paso 3: Limitar resultados**
```bash
# En lugar de listar todo, usar filtros
aws iam list-users --max-items 10
```

**Paso 4: Usar query para obtener solo lo necesario**
```bash
# En lugar de:
aws iam list-users  # Todos los detalles

# Usar:
aws iam list-users --query 'Users[].UserName' --output text  # Solo nombres
```

**Paso 5: Verificar conexión**
```bash
# Probar latencia
ping aws.amazon.com

# Ver velocidad de DNS
time nslookup iam.amazonaws.com
```

---

## 🔧 Debugging - Cómo obtener más info

### Activar debug mode
```bash
# Modo verbose
aws iam list-users --debug

# Guarda en archivo
aws iam list-users --debug 2>&1 | tee debug.log
```

### Ver cabeceras HTTP
```bash
aws iam list-users --debug 2>&1 | grep -E "Request|Response|Making request"
```

### Validar sintaxis sin ejecutar
```bash
# Validar que el comando está bien formado
aws iam list-users --dry-run
```

---

## 📝 Checklist de Troubleshooting

- [ ] ¿`aws --version` funciona?
- [ ] ¿`aws configure list` muestra credenciales?
- [ ] ¿`aws sts get-caller-identity` devuelve información?
- [ ] ¿Está correctamente el nombre de usuario/bucket/rol?
- [ ] ¿La región es correcta?
- [ ] ¿El formato de salida es válido?
- [ ] ¿Tengo permisos IAM para esto?
- [ ] ¿El reloj del sistema está sincronizado?
- [ ] ¿Hay variables de entorno conflictivas?

---

## 🆘 Si nada funciona:

1. **Resetear configuración:**
   ```bash
   rm ~/.aws/credentials
   rm ~/.aws/config
   aws configure
   ```

2. **Reinstalar AWS CLI:**
   ```bash
   sudo ./install --update
   ```

3. **Ver logs:**
   ```bash
   aws iam list-users --debug 2>&1 | head -50
   ```

4. **Contactar a AWS Support:**
   - Ir a https://console.aws.amazon.com
   - Click en "Support" > "Create case"

---

**Última actualización:** Marzo 2026