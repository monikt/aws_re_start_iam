# Script de Inventario AWS

## Descripción

Script en Python que escanea tu cuenta AWS y genera un inventario completo de recursos activos. Utiliza la librería `boto3` para consultar los servicios de AWS y clasifica los recursos por tipo y estado.

## Servicios Soportados

- **EC2**: Instancias (running, stopped, other)
- **S3**: Buckets
- **RDS**: Instancias de base de datos (available, stopped, other)
- **Lambda**: Funciones serverless

## Requisitos Previos

### 1. Credenciales AWS Configuradas

Debes tener credenciales AWS válidas configuradas. Elige una de las siguientes opciones:

**Opción A: Usando AWS CLI**
```bash
aws configure
```
Te pedirá:
- AWS Access Key ID
- AWS Secret Access Key
- Default region
- Default output format

**Opción B: Variables de Entorno**
```bash
export AWS_ACCESS_KEY_ID="tu_access_key"
export AWS_SECRET_ACCESS_KEY="tu_secret_key"
export AWS_DEFAULT_REGION="us-east-1"
```

**Opción C: Archivo de Credenciales**
Crea `~/.aws/credentials`:
```
[default]
aws_access_key_id = tu_access_key
aws_secret_access_key = tu_secret_key
```

### 2. Python 3.7+

Verifica tu versión de Python:
```bash
python --version
```

## Instalación

### Paso 1: Navega a la carpeta del proyecto
```bash
cd desafio_2
```

### Paso 2: Instala las dependencias
```bash
pip install -r requirements.txt
```

O instala directamente boto3:
```bash
pip install boto3>=1.28.0
```

## Uso

### Ejecutar el script

```bash
python inventario_aws.py
```

### Salida esperada

El script generará:
1. **En consola**: Un resumen con el conteo de recursos por tipo y estado
2. **En archivo**: Un JSON con timestamp (`inventario_aws_YYYYMMDD_HHMMSS.json`) con detalles completos

Ejemplo de salida en consola:
```
Iniciando escaneo de recursos AWS...

Resumen de inventario:

EC2:
  Running: 2 recursos
  Stopped: 1 recursos
  Other: 0 recursos

S3:
  Active: 3 recursos

RDS:
  Available: 1 recursos
  Stopped: 0 recursos
  Other: 0 recursos

Lambda:
  Active: 5 recursos

Inventario guardado en inventario_aws_20260318_123456.json
```

## Estructura del JSON generado

```json
{
  "inventory": {
    "EC2": [...],
    "S3": [...],
    "RDS": [...],
    "Lambda": [...],
    "Timestamp": "2026-03-18T12:34:56.789123"
  },
  "classified": {
    "EC2": {
      "running": [...],
      "stopped": [...],
      "other": [...]
    },
    ...
  }
}
```

## Permisos IAM Requeridos

Para que el script funcione correctamente, tu usuario o rol de AWS debe tener permisos para:

- `ec2:DescribeInstances`
- `s3:ListAllMyBuckets`
- `s3:GetBucketLocation`
- `rds:DescribeDBInstances`
- `lambda:ListFunctions`

### Política IAM mínima (Opcional)

Si necesitas crear una política IAM restrictiva:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "s3:ListAllMyBuckets",
        "s3:GetBucketLocation",
        "rds:DescribeDBInstances",
        "lambda:ListFunctions"
      ],
      "Resource": "*"
    }
  ]
}
```

## Solución de Problemas

### Error: `NoCredentialsError`
**Causa**: No hay credenciales AWS configuradas  
**Solución**: Ejecuta `aws configure` o establece las variables de entorno

### Error: `UnauthorizedOperation`
**Causa**: El usuario no tiene permisos para listar recursos  
**Solución**: Verifica que tu usuario tenga los permisos IAM necesarios

### Error: `An error occurred: Network error`
**Causa**: Problemas de conectividad con AWS  
**Solución**: Verifica tu conexión a internet y la región configurada

## Personalización

Para escanear múltiples regiones, puedes modificar las funciones `get_*()` para iterar sobre regiones adicionales.

## Archivos Incluidos

- `inventario_aws.py`: Script principal
- `requirements.txt`: Dependencias de Python
- `README.md`: Este archivo

## Soporte

Para problemas o mejoras, consulta la documentación oficial de boto3: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
