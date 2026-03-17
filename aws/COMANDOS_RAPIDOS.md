# AWS CLI - Referencia Rápida de Comandos

Una lista de comandos útiles para uso frecuente.

---

## 🔧 Configuración

```bash
# Configurar credenciales (primera vez)
aws configure

# Ver configuración actual
aws configure list

# Cambiar región
aws configure set region us-west-2

# Ver perfiles disponibles
aws configure list-profiles

# Usar un perfil específico
aws s3 ls --profile produccion
```

---

## 🆔 Verificación de Identidad

```bash
# Ver tu identidad actual
aws sts get-caller-identity

# Ver detalles de tu usuario
aws iam get-user

# Ver tu cuenta de AWS
aws sts get-caller-identity --query Account --output text
```

---

## 🪣 Comandos S3 (Buckets)

```bash
# LISTAR
aws s3 ls                                    # Listar todos los buckets
aws s3 ls --output table                    # Con formato tabla
aws s3api list-buckets                      # Ver detalles JSON

# CONTAR
aws s3 ls | wc -l                          # Contar buckets

# OBJETOS DENTRO DE UN BUCKET
aws s3 ls s3://mi-bucket                   # Listar objetos
aws s3 ls s3://mi-bucket --recursive       # Listar recursivamente
aws s3 ls s3://mi-bucket/carpeta/          # Filtrar por carpeta

# INFORMACIÓN
aws s3api head-bucket --bucket mi-bucket   # Verificar si existe
aws s3api get-bucket-versioning --bucket mi-bucket
aws s3api get-bucket-acl --bucket mi-bucket
```

---

## 👥 Comandos IAM - Usuarios

```bash
# LISTAR
aws iam list-users                         # Listar todos
aws iam list-users --output table         # Formato tabla
aws iam list-users --query 'Users[].UserName' --output text

# DETALLES ESPECÍFICOS DE UN USUARIO
aws iam get-user --user-name usuario       # Detalles de usuario
aws iam list-groups-for-user --user-name usuario
aws iam list-user-policies --user-name usuario
aws iam list-attached-user-policies --user-name usuario
aws iam list-access-keys --user-name usuario

# CONTAR
aws iam list-users --query 'length(Users)' --output text

# FILTRAR
aws iam list-users --query 'Users[?PasswordLastUsed!=null]' --output table  # Usuarios activos
aws iam list-users --query 'Users[?PasswordLastUsed==null]' --output table  # Usuarios inactivos
```

---

## 🔐 Comandos IAM - Roles

```bash
# LISTAR
aws iam list-roles                         # Listar todos
aws iam list-roles --output table         # Formato tabla
aws iam list-roles --query 'Roles[].RoleName' --output text

# DETALLES DE UN ROL
aws iam get-role --role-name nombre-rol
aws iam get-role --role-name AWSServiceRoleForAmazonSSM 
aws iam list-role-policies --role-name nombre-rol
aws iam list-attached-role-policies --role-name nombre-rol

# CONTAR
aws iam list-roles --query 'length(Roles)' --output text
```

---

## 📊 Comandos IAM - Grupos

```bash
# LISTAR
aws iam list-groups                        # Listar todos
aws iam list-groups --output table        # Formato tabla
aws iam list-groups --query 'Groups[].GroupName' --output text

# MIEMBROS DE UN GRUPO
aws iam get-group --group-name nombre-grupo

# POLÍTICAS DE UN GRUPO
aws iam list-group-policies --group-name nombre-grupo
aws iam list-attached-group-policies --group-name nombre-grupo
```

---

## 🔑 Comandos IAM - Claves de Acceso

```bash
# LISTAR CLAVES DE ACCESO DE UN USUARIO
aws iam list-access-keys --user-name usuario

# OBTENER INFORMACIÓN DE UNA CLAVE ESPECÍFICA
aws iam get-access-key-last-used --access-key-id TU_ACCESS_KEY_ID

# VER FECHA ÚLTIMA ROTACIÓN
aws iam list-access-keys --user-name usuario --query 'AccessKeyMetadata[].{AccessKeyId:AccessKeyId, CreateDate:CreateDate}'
```

---

## 📋 Comandos IAM - Políticas

```bash
# LISTAR TODAS LAS POLÍTICAS
aws iam list-policies

# LISTAR POLÍTICAS ADMINISTRADAS
aws iam list-policies --scope AWS   # Políticas de AWS
aws iam list-policies --scope Local # Políticas propias

# OBTENER VERSIÓN DE UNA POLÍTICA
aws iam get-policy-version --policy-arn arn:aws:iam::123456789012:policy/nombre --version-id v1
```

---

## 🎯 Combinaciones Útiles

```bash
# Listar todos los usuarios y sus ARNs
aws iam list-users --query 'Users[].{Nombre:UserName, ARN:Arn}' --output table

# Listar todos los roles y sus ARNs
aws iam list-roles --query 'Roles[].{Nombre:RoleName, ARN:Arn}' --output table

# Listar buckets y contar
aws s3 ls && echo "" && aws s3 ls | wc -l

# Contar usuarios, roles y buckets
echo "Usuarios: $(aws iam list-users --query 'length(Users)' --output text)"; echo "Roles: $(aws iam list-roles --query 'length(Roles)' --output text)"; echo "Buckets: $(aws s3 ls | wc -l)"

# Exportar usuarios a CSV
aws iam list-users --query 'Users[].{UserName:UserName, ARN:Arn, Creado:CreateDate}' --output text > usuarios.csv

# Buscar usuario por nombre
aws iam list-users --query 'Users[?contains(UserName, `juan`)]' --output table

# Listar buckets por región
aws s3api list-buckets --query 'Buckets[].Name' | xargs -I {} aws s3api get-bucket-location --bucket {} --query 'LocationConstraint'
```

---

## 💾 Exportar Datos

```bash
# Exportar usuarios a JSON
aws iam list-users > usuarios.json

# Exportar roles a JSON
aws iam list-roles > roles.json

# Exportar buckets a texto
aws s3 ls > buckets.txt

# Exportar usuarios a tabla formateada (ASCII)
aws iam list-users --output table > usuarios_tabla.txt
```

---

## 🔍 Filtros JQ (Versión avanzada)

Si tienes `jq` instalado, puedes hacer filtros más potentes:

```bash
# Instalar jq (si no lo tienes)
sudo apt-get install jq

# Usuarios creados en el último mes
aws iam list-users | jq '.Users[] | select(.CreateDate > "'$(date -d '1 month ago' -Iseconds)'") | .UserName'

# Roles que contienen "admin"
aws iam list-roles | jq '.Roles[] | select(.RoleName | contains("admin")) | .RoleName'

# Usuarios sin contraseña configurada
aws iam list-users | jq -r '.Users[] | select(.PasswordLastUsed == null) | .UserName'
```

---

## ⏱️ Monitoreo y Auditoría

```bash
# Ver CloudTrail (últimos eventos)
aws cloudtrail lookup-events --max-results 10

# Ver acciones de un usuario específico
aws cloudtrail lookup-events --lookup-attributes AttributeKey=Username,AttributeValue=username

# Ver eventos de la última hora
aws cloudtrail lookup-events --start-time $(date -u -d '-1 hour' +%s)
```

---

## ⚙️ Configuración Avanzada

```bash
# Usar MFA
aws s3 ls --serial-number arn:aws:iam::123456789012:mfa/usuario --token-code 123456

# Assumir un rol en otra cuenta
aws sts assume-role --role-arn arn:aws:iam::OTRA_CUENTA:role/RoleName --role-session-name sesion-nombre

# Listar todas las configuraciones disponibles
env | grep AWS
```

---

## 📌 Cheat Sheet (Lo Más Usado)

```bash
# Top 10 de comandos más usados

1. aws configure                          # Configurar credenciales
2. aws s3 ls                             # Listar buckets
3. aws iam list-users                    # Listar usuarios
4. aws iam list-roles                    # Listar roles
5. aws sts get-caller-identity           # Ver quién eres
6. aws s3 ls s3://bucket-name            # Listar objetos
7. aws iam list-users --output table     # Ver usuarios formateado
8. aws configure list                    # Ver configuración
9. aws s3 cp archivo s3://bucket         # Subir archivo
10. aws ec2 describe-instances           # Listar instancias EC2
```

---

**Última actualización:** Marzo 2026