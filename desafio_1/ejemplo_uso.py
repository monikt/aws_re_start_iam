#!/usr/bin/env python3
"""
Script de Ejemplo - Ejecutar Backup
Muestra cómo usar la solución de backup
"""

import sys
from pathlib import Path

# Agregamos el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

def show_menu():
    """Muestra el menú principal"""
    print("""
╔════════════════════════════════════════════╗
║   HERRAMIENTA DE BACKUP A AWS S3          ║
╠════════════════════════════════════════════╣
║  1. Ejecutar backup MANUAL                 │
║  2. Iniciar SCHEDULER (automático)         │
║  3. Verificar CONFIGURACIÓN                │
║  4. Ejecutar backup MANUAL (scheduler)     │
║  5. Ver LOGS                               │
║  6. Salir                                  │
╚════════════════════════════════════════════╝
    """)


def option_1_manual_backup():
    """Opción 1: Backup manual"""
    print("\n" + "="*60)
    print("EJECUTANDO BACKUP MANUAL")
    print("="*60 + "\n")
    
    try:
        from backup_s3 import perform_backup
        from email_notifier import send_notification
        
        result = perform_backup()
        
        print("\n" + "="*60)
        print("ENVIANDO NOTIFICACIÓN")
        print("="*60)
        
        send_notification(result)
        
        print("\n✅ Backup completado")
        
    except ImportError as e:
        print(f"❌ Error: {e}")
        print("Asegúrate de instalar las dependencias: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error: {e}")


def option_2_scheduler():
    """Opción 2: Iniciar scheduler"""
    print("\n" + "="*60)
    print("INICIANDO SCHEDULER")
    print("="*60 + "\n")
    
    try:
        import scheduler
        scheduler.start_scheduler()
    except ImportError as e:
        print(f"❌ Error: {e}")
        print("Asegúrate de instalar las dependencias: pip install -r requirements.txt")


def option_3_diagnostico():
    """Opción 3: Verificar configuración"""
    print("\n" + "="*60)
    print("VERIFICANDO CONFIGURACIÓN")
    print("="*60 + "\n")
    
    try:
        import diagnostico
        diagnostico.main()
    except ImportError as e:
        print(f"❌ Error: {e}")


def option_4_scheduler_run_now():
    """Opción 4: Backup mediante scheduler (para testing)"""
    print("\n" + "="*60)
    print("EJECUTANDO BACKUP VÍA SCHEDULER")
    print("="*60 + "\n")
    
    try:
        from backup_s3 import perform_backup
        from email_notifier import send_notification
        
        print("Ejecutando backup...")
        result = perform_backup()
        
        print("\nEnviando notificación...")
        send_notification(result)
        
        print("\n✅ Backup completado via scheduler")
        
    except ImportError as e:
        print(f"❌ Error: {e}")
        print("Asegúrate de instalar las dependencias: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error: {e}")


def option_5_logs():
    """Opción 5: Ver logs"""
    print("\n" + "="*60)
    print("MOSTRANDO LOGS")
    print("="*60 + "\n")
    
    import subprocess
    
    log_file = Path(__file__).parent / "logs" / "backup.log"
    
    if log_file.exists():
        print(f"Últimas 50 líneas de {log_file}:\n")
        subprocess.run(['tail', '-50', str(log_file)])
    else:
        print(f"❌ Archivo de log no encontrado: {log_file}")
        print("(Se crea después del primer backup)")


def main():
    """Función principal"""
    while True:
        show_menu()
        choice = input("Selecciona una opción (1-6): ").strip()
        
        if choice == '1':
            option_1_manual_backup()
        elif choice == '2':
            option_2_scheduler()
        elif choice == '3':
            option_3_diagnostico()
        elif choice == '4':
            option_4_scheduler_run_now()
        elif choice == '5':
            option_5_logs()
        elif choice == '6':
            print("\n👋 ¡Hasta pronto!")
            sys.exit(0)
        else:
            print("\n❌ Opción no válida. Intenta de nuevo.\n")
        
        input("\nPresiona ENTER para continuar...")
        print("\n" * 2)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Programa cancelado por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
