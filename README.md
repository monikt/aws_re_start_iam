# AWS Re:Start - IAM Repository

Repositorio completo para aprender y practicar con AWS CLI, IAM y gestión de identidades.

## 📚 Documentación Disponible

Este repositorio contiene guías completas en español para trabajar con AWS CLI:

### 1. **[AWS CLI - Guía Completa](aws/AWS_CLI_GUIA.md)** 📖
   - ✅ Instalación de AWS CLI
   - ✅ Configuración con `aws configure`
   - ✅ Verificar conexión a AWS
   - ✅ Operaciones con Buckets S3 (listar, filtrar, contar)
   - ✅ Operaciones con Roles IAM (listar, detalles, políticas)
   - ✅ Operaciones con Usuarios IAM (listar, grupos, claves)
   - ✅ Scripts útiles combinados
   - ✅ Consejos de seguridad

### 2. **[Referencia Rápida de Comandos](aws/COMANDOS_RAPIDOS.md)** ⚡
   - ✅ Comandos más usados
   - ✅ Cheat sheet
   - ✅ Combinaciones útiles
   - ✅ Exportar datos
   - ✅ Filtros avanzados

### 3. **[Guía de Troubleshooting](aws/TROUBLESHOOTING.md)** 🔧
   - ✅ Problemas comunes y soluciones
   - ✅ Errores de credenciales
   - ✅ Debugging tips
   - ✅ Checklist de troubleshooting

---

## 🚀 Inicio Rápido

### Paso 1: Instalar AWS CLI
```bash
cd aws
sudo ./install
aws --version
```

### Paso 2: Configurar credenciales
```bash
aws configure
# Responde con:
# - Access Key ID
# - Secret Access Key  
# - Región (ejemplo: us-east-1)
# - Formato (json)
```

### Paso 3: Verificar conexión
```bash
aws sts get-caller-identity
```

### Paso 4: Comenzar a explorar
```bash
aws s3 ls              # Ver buckets
aws iam list-users     # Ver usuarios
aws iam list-roles     # Ver roles
```

---

## 📋 Comandos Básicos

```bash
# Verificar quién eres
aws sts get-caller-identity

# Listar todos los buckets S3
aws s3 ls

# Listar todos los usuarios IAM
aws iam list-users

# Listar todos los roles IAM
aws iam list-roles

# Ver configuración actual
aws configure list
```

---

## 📂 Estructura del Repositorio

```
aws_re_start_iam/
├── README.md                      # Este archivo
├── aws/
│   ├── README.md                  # Instrucciones de instalación
│   ├── AWS_CLI_GUIA.md           # Guía completa (COMIENZA AQUÍ)
│   ├── COMANDOS_RAPIDOS.md       # Referencia rápida
│   ├── TROUBLESHOOTING.md        # Solución de problemas
│   ├── install                    # Script de instalación
│   ├── dist/                      # Distribución de AWS CLI v2
│   └── THIRD_PARTY_LICENSES      # Licencias de terceros
└── awscliv2.zip                  # Archivo comprimido de AWS CLI
```

---

## 🔐 Seguridad

⚠️ **IMPORTANTE:**
- **Nunca compartas** tus credenciales de AWS
- **Nunca hagas commit** del archivo `~/.aws/credentials` en Git
- **Usa perfiles** para diferentes entornos
- **Rota tus claves** regularmente (cada 90 días)
- **Habilita MFA** en tu cuenta

### Proteger credenciales
```bash
# Agregar a .gitignore
echo "~/.aws/credentials" >> ~/.gitignore
echo "~/.aws/config" >> ~/.gitignore
```

---

## 📖 Documentación de Referencia

- [AWS CLI Official Docs](https://docs.aws.amazon.com/cli/)
- [AWS IAM Guide](https://docs.aws.amazon.com/iam/)
- [AWS S3 Guide](https://docs.aws.amazon.com/s3/)

---

## 🤝 Contribuir

Se aceptan contribuciones. Para reportar problemas o sugerir mejoras, abre un issue.

---

## 📝 Licencia

Este repositorio incluye AWS CLI v2 con sus propias licencias. Ver [THIRD_PARTY_LICENSES](aws/THIRD_PARTY_LICENSES).

---

**Última actualización:** Marzo 2026
