# Guía Completa: AWS CLI - Conexión y Operaciones Básicas

Esta guía te mostrará cómo conectarte a AWS utilizando la terminal y realizar las operaciones más comunes con la AWS CLI.

---

## Tabla de Contenidos

1. [Instalación de AWS CLI](#instalación-de-aws-cli)
2. [Configuración Inicial (aws configure)](#configuración-inicial-aws-configure)
3. [Verificar la Conexión](#verificar-la-conexión)
4. [Operaciones con Buckets S3](#operaciones-con-buckets-s3)
5. [Operaciones con Roles IAM](#operaciones-con-roles-iam)
6. [Operaciones con Usuarios IAM](#operaciones-con-usuarios-iam)
7. [Consejos de Seguridad](#consejos-de-seguridad)

---

## Instalación de AWS CLI

### En Linux/Mac

#### Opción 1: Usando el script de instalación incluido
```bash
cd /workspaces/aws_re_start_iam/aws
sudo ./install
```

Verifica la instalación:
```bash
aws --version
```

#### Opción 2: Instalación sin permisos de sudo
```bash
cd /workspaces/aws_re_start_iam/aws
./install -i ~/.local/aws-cli -b ~/.local/bin
```

Luego actualiza tu PATH:
```bash
export PATH=~/.local/bin:$PATH
```

#### Opción 3: Usando pip (si tienes Python instalado)
```bash
pip install awscli
```

### Verificar instalación
```bash
aws --version
```

Deberías ver algo como:
```
aws-cli/2.x.x Python/3.x.x Linux/5.x.x exe/x86_64 dist/ubuntu
```

---

## Configuración Inicial (aws configure)

La configuración inicial se realiza una sola vez con el comando `aws configure`.

### Paso 1: Ejecutar el comando
```bash
aws configure
```

### Paso 2: Proporcionar las credenciales

El comando te pedirá la siguiente información:

```
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: us-east-1
Default output format [None]: json
```

**Explicación de cada campo:**

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **AWS Access Key ID** | Tu ID de clave de acceso (como usuario) | AKIAIOSFODNN7EXAMPLE |
| **AWS Secret Access Key** | Tu clave secreta de acceso (CONFIDENCIAL) | wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY |
| **Default region name** | Región AWS por defecto | us-east-1, eu-west-1, ap-southeast-1 |
| **Default output format** | Formato de salida | json, table, text, yaml |

### Obtener tus Credenciales

Para obtener tus credenciales AWS:

1. **Accede a AWS Console:**
   - Ve a https://console.aws.amazon.com
   - Inicia sesión con tu cuenta

2. **Navega a IAM:**
   - En el panel de búsqueda, escribe "IAM"
   - Haz clic en "Identity and Access Management"

3. **Crea una clave de acceso:**
   - En el menú izquierdo, selecciona "Users"
   - Haz clic en tu usuario
   - Selecciona la pestaña "Security credentials"
   - Haz clic en "Create access key"
   - Selecciona "Command Line Interface (CLI)"
   - Guarda las credenciales en un lugar seguro

### Archivos de Configuración

Después de ejecutar `aws configure`, se crean dos archivos:

- **`~/.aws/credentials`** - Almacena tus Access Key ID y Secret Access Key
- **`~/.aws/config`** - Almacena tu región y formato de salida por defecto

Ver contenido de configuración:
```bash
cat ~/.aws/config
cat ~/.aws/credentials
```

---

## Verificar la Conexión

### Comando básico para probar la conexión
```bash
aws sts get-caller-identity
```

Respuesta exitosa:
```json
{
    "UserId": "AIDACKCEVSQ6C2EXAMPLE",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/tu-usuario"
}
```

### Verificar versión
```bash
aws --version
```

### Listar tu identidad y cuenta
```bash
aws iam get-user
```

---

## Operaciones con Buckets S3

### 1. Listar todos los buckets
```bash
aws s3 ls
```

**Salida esperada:**
```
2024-01-15 10:30:45 mi-primer-bucket
2024-02-20 14:22:11 mi-segundo-bucket
2024-03-10 09:15:33 imagenes-backup
```

### 2. Listar buckets con formato tabla (más legible)
```bash
aws s3 ls --output table
```

### 3. Listar con información detallada (creación, región, etc.)
```bash
aws s3api list-buckets
```

**Salida JSON:**
```json
{
    "Buckets": [
        {
            "Name": "mi-primer-bucket",
            "CreationDate": "2024-01-15T10:30:45+00:00"
        },
        {
            "Name": "mi-segundo-bucket",
            "CreationDate": "2024-02-20T14:22:11+00:00"
        }
    ],
    "Owner": {
        "DisplayName": "tu-usuario",
        "ID": "canoniocal-id-aqui"
    }
}
```

### 4. Contar el número de buckets
```bash
aws s3 ls | wc -l
```

### 5. Listar objetos dentro de un bucket específico
```bash
aws s3 ls s3://mi-primer-bucket
```

### 6. Listar objetos de forma recursiva
```bash
aws s3 ls s3://mi-primer-bucket --recursive
```

### 7. Filtrar por prefijo (carpeta virtual)
```bash
aws s3 ls s3://mi-primer-bucket/carpeta/
```

### 8. Obtener información de un bucket específico
```bash
aws s3api head-bucket --bucket mi-primer-bucket
```

Si el bucket existe, no devuelve nada (HTTP 200). Si no existe, devuelve un error.

---

## Operaciones con Roles IAM

### 1. Listar todos los roles
```bash
aws iam list-roles
```

**Salida JSON:**
```json
{
    "Roles": [
        {
            "Path": "/",
            "RoleName": "Mi-Rol-EC2",
            "RoleId": "AIDACKCEVSQ6C2EXAMPLE",
            "Arn": "arn:aws:iam::123456789012:role/Mi-Rol-EC2",
            "CreateDate": "2024-01-15T10:30:45+00:00",
            "AssumeRolePolicyDocument": "..."
        }
    ]
}
```

### 2. Listar roles con formato tabla
```bash
aws iam list-roles --output table
```

### 3. Listar solo los nombres de los roles
```bash
aws iam list-roles --query 'Roles[].RoleName' --output text
```

**Salida:**
```
Mi-Rol-EC2 Mi-Rol-Lambda Mi-Rol-Produccion
```

### 4. Listar roles uno por línea
```bash
aws iam list-roles --query 'Roles[].RoleName' --output text | tr ' ' '\n'
```

**Salida:**
```
Mi-Rol-EC2
Mi-Rol-Lambda
Mi-Rol-Produccion
```

### 5. Obtener detalles de un rol específico
```bash
aws iam get-role --role-name Mi-Rol-EC2
```

### 6. Listar políticas asociadas a un rol
```bash
aws iam list-role-policies --role-name Mi-Rol-EC2
```

### 7. Listar políticas administradas de un rol
```bash
aws iam list-attached-role-policies --role-name Mi-Rol-EC2
```

### 8. Obtener política inline de un rol
```bash
aws iam get-role-policy --role-name Mi-Rol-EC2 --policy-name nombre-politica
```

### 9. Contar total de roles
```bash
aws iam list-roles --query 'length(Roles)' --output text
```

### 10. Listar roles modificados en el último mes
```bash
aws iam list-roles --query 'Roles[?CreateDate>=`2024-02-17`]' --output table
```

---

## Operaciones con Usuarios IAM

### 1. Listar todos los usuarios
```bash
aws iam list-users
```

**Salida JSON:**
```json
{
    "Users": [
        {
            "Path": "/",
            "UserName": "juan-desarrollador",
            "UserId": "AIDACKCEVSQ6C2EXAMPLE",
            "Arn": "arn:aws:iam::123456789012:user/juan-desarrollador",
            "CreateDate": "2024-01-15T10:30:45+00:00",
            "PasswordLastUsed": "2024-03-10T14:22:11+00:00"
        }
    ]
}
```

### 2. Listar usuarios con formato tabla
```bash
aws iam list-users --output table
```

### 3. Listar solo nombres de usuarios
```bash
aws iam list-users --query 'Users[].UserName' --output text
```

**Salida:**
```
juan-desarrollador maria-admin pedro-devops
```

### 4. Listar usuarios uno por línea
```bash
aws iam list-users --query 'Users[].UserName' --output text | tr ' ' '\n'
```

**Salida:**
```
juan-desarrollador
maria-admin
pedro-devops
```

### 5. Obtener detalles de un usuario específico
```bash
aws iam get-user --user-name juan-desarrollador
```

### 6. Listar grupos de un usuario
```bash
aws iam list-groups-for-user --user-name juan-desarrollador
```

### 7. Listar políticas inline de un usuario
```bash
aws iam list-user-policies --user-name juan-desarrollador
```

### 8. Listar políticas administradas de un usuario
```bash
aws iam list-attached-user-policies --user-name juan-desarrollador
```

### 9. Listar claves de acceso de un usuario
```bash
aws iam list-access-keys --user-name juan-desarrollador
```

### 10. Listar credenciales de consola (contraseña)
```bash
aws iam get-login-profile --user-name juan-desarrollador
```

### 11. Contar total de usuarios
```bash
aws iam list-users --query 'length(Users)' --output text
```

### 12. Listar usuarios activos (que han usado contraseña)
```bash
aws iam list-users --query 'Users[?PasswordLastUsed!=null]' --output table
```

### 13. Listar usuarios inactivos (sin historial de login)
```bash
aws iam list-users --query 'Users[?PasswordLastUsed==null]' --output table
```

---

## Comandos Combinados Útiles

### Crear un script para resumen de IAM
```bash
#!/bin/bash

echo "========== RESUMEN IAM =========="
echo ""
echo "Total de Usuarios:"
aws iam list-users --query 'length(Users)' --output text
echo ""
echo "Total de Roles:"
aws iam list-roles --query 'length(Roles)' --output text
echo ""
echo "Total de Buckets:"
aws s3 ls | wc -l
echo ""
echo "Tu Identidad Actual:"
aws sts get-caller-identity --output table
```

Guarda como `iam-summary.sh` y ejecuta:
```bash
chmod +x iam-summary.sh
./iam-summary.sh
```

### Exportar usuarios a un archivo CSV
```bash
aws iam list-users --query 'Users[].{UserName:UserName, Arn:Arn, CreatedDate:CreateDate}' --output text > usuarios.csv
```

### Exportar roles a un archivo JSON
```bash
aws iam list-roles > roles.json
```

---

## Consejos de Seguridad

### ⚠️ IMPORTANTE: Protege tus Credenciales

1. **Never share your credentials** - Nunca compartas tu Access Key o Secret Access Key
2. **Never commit credentials** - No subas `~/.aws/credentials` a Git
3. **Use IAM Users** - Crea usuarios específicos para cada aplicación o persona
4. **Rotate keys regularly** - Rota tus claves de acceso regularmente
5. **Use MFA** - Habilita la autenticación multifactor

### Agregar .aws a .gitignore
```bash
echo "~/.aws/credentials" >> ~/.gitignore
echo "~/.aws/config" >> ~/.gitignore
```

### Usar Perfiles de Configuración
Puedes tener múltiples configuraciones (para diferentes cuentas):

**En `~/.aws/config`:**
```
[default]
region = us-east-1
output = json

[profile produccion]
region = eu-west-1
output = json
```

**Usar un perfil específico:**
```bash
aws s3 ls --profile produccion
aws iam list-users --profile produccion
```

### Listar perfiles disponibles
```bash
aws configure list-profiles
```

---

## Resolución de Problemas

### Error: "Unable to locate credentials"
**Solución:** Ejecuta `aws configure` nuevamente y verifica que tus credenciales sean correctas.

### Error: "InvalidUserID.Malformed"
**Solución:** Verifica el nombre de usuario sea correcto. Usa:
```bash
aws iam list-users --query 'Users[].UserName'
```

### Error: "NoSuchBucket"
**Solución:** El bucket no existe en tu cuenta o región. Verifica el nombre con:
```bash
aws s3 ls
```

### Error: "AccessDenied"
**Solución:** Tu usuario no tiene permisos para esa operación. Contacta al administrador de la cuenta AWS.

### Cambiar región por defecto
```bash
aws configure set region us-west-2
```

### Ver configuración actual
```bash
aws configure list
```

---

## Recursos Adicionales

- [AWS CLI Official Documentation](https://docs.aws.amazon.com/cli/)
- [AWS CLI Reference](https://docs.aws.amazon.com/cli/latest/reference/)
- [AWS IAM Documentation](https://docs.aws.amazon.com/iam/)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)

---

**Última actualización:** Marzo 2026
