#!/usr/bin/env python3
"""
Script de Diagnóstico de Configuración
Verifica que todo está correctamente configurado antes de ejecutar backups
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Verifica la versión de Python"""
    print("\n" + "="*60)
    print("1️⃣  VERIFICANDO VERSIÓN DE PYTHON")
    print("="*60)
    
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} (Se requiere 3.8+)")
        return False


def check_dependencies():
    """Verifica que todas las dependencias estén instaladas"""
    print("\n" + "="*60)
    print("2️⃣  VERIFICANDO DEPENDENCIAS")
    print("="*60)
    
    required_packages = ['boto3', 'apscheduler', 'dotenv']
    all_installed = True
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NO INSTALADO")
            all_installed = False
    
    if not all_installed:
        print("\n💡 Instala dependencias con: pip install -r requirements.txt")
    
    return all_installed


def check_aws_config():
    """Verifica configuración de AWS"""
    print("\n" + "="*60)
    print("3️⃣  VERIFICANDO CONFIGURACIÓN DE AWS")
    print("="*60)
    
    try:
        from config import (
            AWS_ACCESS_KEY_ID, 
            AWS_SECRET_ACCESS_KEY, 
            AWS_REGION,
            S3_BUCKET_NAME
        )
        
        # Verificar que no son valores por defecto
        if AWS_ACCESS_KEY_ID == 'ASIAWIBDWS3ZCDE5ENGV':
            print("❌ AWS_ACCESS_KEY_ID no configurado (valor por defecto)")
            return False
        
        if AWS_SECRET_ACCESS_KEY == 'HQNJCDpupAYvNG/oev3oDBccpcgmor0YFKblKlRK':
            print("❌ AWS_SECRET_ACCESS_KEY no configurado (valor por defecto)")
            return False
        
        print(f"✅ AWS_ACCESS_KEY_ID: {AWS_ACCESS_KEY_ID[:10]}...{AWS_ACCESS_KEY_ID[-5:]}")
        print(f"✅ AWS_SECRET_ACCESS_KEY: ****** (configurado)")
        print(f"✅ AWS_REGION: {AWS_REGION}")
        print(f"✅ S3_BUCKET_NAME: {S3_BUCKET_NAME}")
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def check_local_files():
    """Verifica que existen los archivos locales"""
    print("\n" + "="*60)
    print("4️⃣  VERIFICANDO ARCHIVOS LOCALES")
    print("="*60)
    
    try:
        from config import LOCAL_FILES_PATH
        
        path = Path(LOCAL_FILES_PATH)
        
        if not path.exists():
            print(f"❌ Ruta no existe: {LOCAL_FILES_PATH}")
            return False
        
        files = list(path.glob('*'))
        
        if not files:
            print(f"⚠️  Directorio vacío: {LOCAL_FILES_PATH}")
            print(f"    Se respaldarán cero archivos")
            return True
        
        print(f"✅ Ruta existe: {LOCAL_FILES_PATH}")
        print(f"✅ Archivos encontrados: {len(files)}")
        
        # Mostrar primeros 5 archivos
        for file in files[:5]:
            if file.is_file():
                size_kb = file.stat().st_size / 1024
                print(f"   • {file.name} ({size_kb:.1f} KB)")
        
        if len(files) > 5:
            print(f"   ... y {len(files) - 5} más")
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def check_email_config():
    """Verifica configuración de email"""
    print("\n" + "="*60)
    print("5️⃣  VERIFICANDO CONFIGURACIÓN DE EMAIL")
    print("="*60)
    
    try:
        from config import EMAIL_CONFIG
        
        if not EMAIL_CONFIG.get('enabled', False):
            print("⚠️  Notificaciones por email deshabilitadas")
            return True
        
        provider = EMAIL_CONFIG.get('provider', 'smtp').lower()
        print(f"✅ Provider: {provider}")
        
        from_email = EMAIL_CONFIG.get('from_email')
        to_emails = EMAIL_CONFIG.get('to_emails')
        
        if from_email == 'tu-email@ejemplo.com':
            print("❌ FROM_EMAIL no configurado (valor por defecto)")
            return False
        
        print(f"✅ FROM_EMAIL: {from_email}")
        print(f"✅ TO_EMAILS: {', '.join(to_emails)}")
        
        if provider == 'smtp':
            smtp_config = EMAIL_CONFIG.get('smtp', {})
            print(f"✅ SMTP_HOST: {smtp_config.get('host')}")
            print(f"✅ SMTP_PORT: {smtp_config.get('port')}")
            print(f"✅ SMTP_USERNAME: {smtp_config.get('username')}")
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def check_aws_connectivity():
    """Verifica conectividad con AWS"""
    print("\n" + "="*60)
    print("6️⃣  VERIFICANDO CONECTIVIDAD CON AWS S3")
    print("="*60)
    
    try:
        import boto3
        from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
        
        print("Intentando conectar a AWS S3...")
        
        print("✅ Creando cliente de S3...", AWS_ACCESS_KEY_ID + '...' + AWS_ACCESS_KEY_ID)
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )
        
        # Intentar listar buckets
        response = s3_client.list_buckets()
        
        num_buckets = len(response.get('Buckets', []))
        print(f"✅ Conexión exitosa a AWS S3")
        print(f"✅ Buckets encontrados: {num_buckets}")
        
        # Mostrar primeros 5 buckets
        for bucket in response.get('Buckets', [])[:5]:
            print(f"   • {bucket['Name']}")
        
        return True
    
    except Exception as e:
        print(f"❌ Error de conectividad: {e}")
        return False


def run_test_backup():
    """Inicia un backup de prueba"""
    print("\n" + "="*60)
    print("7️⃣  EJECUTAR BACKUP DE PRUEBA")
    print("="*60)
    
    try:
        print("\n🚀 ¿Deseas ejecutar un backup de prueba ahora? (s/n): ", end="")
        response = input().strip().lower()
        
        if response == 's':
            print("\nIniciando backup...")
            import backup_s3
            result = backup_s3.perform_backup()
            
            print(f"\nResultado: {'✅ EXITOSO' if result['success'] else '❌ FALLIDO'}")
            print(f"Archivos subidos: {result['files_uploaded']}")
            print(f"Errores: {len(result['errors'])}")
            
            if result['errors']:
                print("\nErrores encontrados:")
                for error in result['errors']:
                    print(f"  • {error}")
            
            return result['success']
        else:
            print("Backup de prueba omitido")
            return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def show_summary(checks):
    """Muestra resumen de verificaciones"""
    print("\n" + "="*60)
    print("📊 RESUMEN DE DIAGNÓSTICO")
    print("="*60)
    
    total = len(checks)
    passed = sum(c[1] for c in checks)
    failed = total - passed
    
    for check_name, passed_check in checks:
        status = "✅" if passed_check else "❌"
        print(f"{status} {check_name}")
    
    print(f"\nTotal: {passed}/{total} verificaciones pasaron")
    
    if passed == total:
        print("\n✅ ¡Toda la configuración está correcta! Listo para ejecutar backups.")
        return True
    else:
        print(f"\n⚠️  {failed} verificación(es) fallaron. Revisa los errores arriba.")
        return False


def main():
    """Ejecuta todas las verificaciones"""
    
    print("""
╔════════════════════════════════════════════╗
║   DIAGNÓSTICO DE CONFIGURACIÓN AWS        ║
║          SOLUCIÓN DE BACKUP S3            ║
╚════════════════════════════════════════════╝
    """)
    
    checks = []
    
    # Ejecutar verificaciones
    checks.append(("Python 3.8+", check_python_version()))
    checks.append(("Dependencias instaladas", check_dependencies()))
    checks.append(("Configuración AWS", check_aws_config()))
    checks.append(("Archivos locales", check_local_files()))
    checks.append(("Configuración Email", check_email_config()))
    checks.append(("Conectividad AWS S3", check_aws_connectivity()))
    
    # Mostrar resumen
    success = show_summary(checks)
    
    # Ofrecer backup de prueba si todo OK
    if success:
        run_test_backup()
    
    print("\n" + "="*60)
    print("Diagnóstico completado")
    print("="*60 + "\n")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Diagnóstico cancelado por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)
