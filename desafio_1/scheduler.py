#!/usr/bin/env python3
"""
Scheduler para ejecutar backups automáticos diariamente
Utiliza APScheduler para programar la ejecución
"""

import logging
import signal
import sys
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

try:
    from config import BACKUP_TIME, TIMEZONE, DEBUG
    from backup_s3 import perform_backup
    from email_notifier import send_notification
except ImportError as e:
    print(f"Error al importar módulos: {e}")
    sys.exit(1)


# Configurar logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Instancia global del scheduler
scheduler = None


def backup_job():
    """Función que ejecuta el backup"""
    logger.info("=" * 60)
    logger.info("⏰ EJECUTANDO BACKUP PROGRAMADO")
    logger.info("=" * 60)
    
    try:
        result = perform_backup()
        send_notification(result)
    except Exception as e:
        logger.error(f"Error en backup_job: {e}")
        # Enviar notificación de error
        error_result = {
            'success': False,
            'timestamp': datetime.now().isoformat(),
            'bucket': 'N/A',
            'files_uploaded': 0,
            'errors': [str(e)],
            'message': f'Error crítico en el backup programado: {str(e)}'
        }
        send_notification(error_result)


def start_scheduler():
    """Inicia el scheduler de backups"""
    global scheduler
    
    try:
        logger.info("Iniciando scheduler de backups automáticos...")
        
        # Crear scheduler
        scheduler = BackgroundScheduler(timezone=TIMEZONE)
        
        # Parsear hora del backup (HH:MM)
        hour, minute = BACKUP_TIME.split(':')
        
        logger.info(f"Backup programado para las {BACKUP_TIME} ({TIMEZONE})")
        
        # Programar job diario
        scheduler.add_job(
            backup_job,
            trigger=CronTrigger(hour=int(hour), minute=int(minute), timezone=TIMEZONE),
            id='daily_backup',
            name='Daily S3 Backup',
            replace_existing=True,
            max_instances=1  # Evitar ejecuciones simultáneas
        )
        
        # Iniciar scheduler
        scheduler.start()
        
        logger.info("✓ Scheduler iniciado correctamente")
        logger.info(f"Próxima ejecución: {scheduler.get_job('daily_backup').next_run_time}")
        
        print("""
╔════════════════════════════════════════════╗
║    AWS S3 BACKUP SCHEDULER - EJECUTANDO    ║
╠════════════════════════════════════════════╣
║  • Backup programado a las: """ + BACKUP_TIME + f"""     │
║  • Timezone: {TIMEZONE:<28}│
║  • Estado: ACTIVO ✓                        │
║                                            │
║  Para detener, presiona CTRL+C             │
╚════════════════════════════════════════════╝
        """)
        
        # Mantener el script ejecutándose
        try:
            while True:
                pass
        except KeyboardInterrupt:
            logger.info("\nDeteniendo scheduler...")
            stop_scheduler()
            sys.exit(0)
    
    except Exception as e:
        logger.error(f"Error al iniciar scheduler: {e}")
        sys.exit(1)


def stop_scheduler():
    """Detiene el scheduler"""
    global scheduler
    
    if scheduler and scheduler.running:
        logger.info("Deteniendo scheduler...")
        scheduler.shutdown()
        logger.info("✓ Scheduler detenido")


def signal_handler(sig, frame):
    """Manejador para señales (CTRL+C)"""
    logger.info("Señal recibida, deteniendo scheduler...")
    stop_scheduler()
    sys.exit(0)


def run_now():
    """Ejecuta el backup inmediatamente (para testing)"""
    logger.info("Ejecutando backup manualmente...")
    backup_job()


def show_schedule():
    """Muestra el próximo backup programado"""
    global scheduler
    
    if scheduler:
        job = scheduler.get_job('daily_backup')
        if job:
            logger.info(f"Próxima ejecución: {job.next_run_time}")
        else:
            logger.warning("No hay job programado")
    else:
        logger.warning("Scheduler no está ejecutándose")


if __name__ == "__main__":
    # Registrar manejador para CTRL+C
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Procesar argumentos
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'run-now':
            logger.info("Backup manual solicitado")
            run_now()
        elif command == 'check':
            logger.info("Verificando schedule...")
            show_schedule()
        else:
            logger.error(f"Comando desconocido: {command}")
            logger.info("Comandos disponibles: run-now, check")
    else:
        # Iniciar scheduler normalmente
        start_scheduler()
