#!/usr/bin/env python3
"""
Script de Backup Automatizado a AWS S3
Realiza backup diario de archivos locales a S3 y notifica por email
"""

import os
import sys
import boto3
import logging
from datetime import datetime
from pathlib import Path
from botocore.exceptions import ClientError
import traceback

# Importar configuración
try:
    from config import (
        AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY,
        AWS_REGION,
        S3_BUCKET_NAME,
        LOCAL_FILES_PATH,
        EMAIL_CONFIG,
        LOG_FILE
    )
    from email_notifier import send_notification
except ImportError as e:
    print(f"Error al importar configuración: {e}")
    sys.exit(1)


# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class S3BackupManager:
    """Gestor de backups a S3"""
    
    def __init__(self):
        """Inicializa el cliente de S3"""
        try:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                region_name=AWS_REGION
            )
            logger.info("Conexión a AWS S3 establecida exitosamente")
        except Exception as e:
            logger.error(f"Error al conectar a AWS S3: {e}")
            raise
    
    def bucket_exists(self, bucket_name):
        """Verifica si el bucket existe"""
        try:
            self.s3_client.head_bucket(Bucket=bucket_name)
            logger.info(f"Bucket '{bucket_name}' existe")
            return True
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                logger.warning(f"Bucket '{bucket_name}' no existe")
                return False
            else:
                logger.error(f"Error al verificar bucket: {e}")
                raise
    
    def create_bucket(self, bucket_name):
        """Crea un nuevo bucket en S3"""
        try:
            if self.bucket_exists(bucket_name):
                logger.info(f"Bucket ya existe: {bucket_name}")
                return True
            
            if AWS_REGION == 'us-east-1':
                self.s3_client.create_bucket(Bucket=bucket_name)
            else:
                self.s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': AWS_REGION}
                )
            
            logger.info(f"Bucket creado exitosamente: {bucket_name}")
            return True
        except ClientError as e:
            logger.error(f"Error al crear bucket: {e}")
            raise
    
    def upload_files(self, local_path, bucket_name, s3_prefix):
        """
        Sube archivos a S3 en la carpeta del día
        
        Args:
            local_path: Ruta local de los archivos
            bucket_name: Nombre del bucket S3
            s3_prefix: Prefijo/carpeta en S3 (ej: 2024-03-18)
        
        Returns:
            tuple: (cantidad_archivos, lista_errores)
        """
        try:
            local_path = Path(local_path)
            
            if not local_path.exists():
                raise FileNotFoundError(f"Ruta local no existe: {local_path}")
            
            files_uploaded = 0
            errors = []
            
            # Listar archivos en la ruta local
            files = list(local_path.glob('*'))
            
            if not files:
                logger.warning(f"No hay archivos en {local_path}")
                return files_uploaded, errors
            
            logger.info(f"Se encontraron {len(files)} archivo(s) para subir")
            
            for file_path in files:
                if file_path.is_file():
                    try:
                        # Crear nombre en S3: carpeta_dia/nombre_archivo
                        s3_key = f"{s3_prefix}/{file_path.name}"
                        
                        logger.info(f"Subiendo: {file_path.name} -> s3://{bucket_name}/{s3_key}")
                        
                        self.s3_client.upload_file(
                            str(file_path),
                            bucket_name,
                            s3_key
                        )
                        
                        files_uploaded += 1
                        logger.info(f"✓ Archivo subido: {file_path.name}")
                        
                    except Exception as e:
                        error_msg = f"Error al subir {file_path.name}: {str(e)}"
                        logger.error(error_msg)
                        errors.append(error_msg)
            
            return files_uploaded, errors
            
        except Exception as e:
            logger.error(f"Error en upload_files: {e}")
            raise
    
    def get_bucket_info(self, bucket_name):
        """Obtiene información del bucket"""
        try:
            response = self.s3_client.head_bucket(Bucket=bucket_name)
            logger.info(f"Información del bucket: {response}")
            return response
        except Exception as e:
            logger.error(f"Error al obtener información del bucket: {e}")
            raise


def perform_backup():
    """
    Ejecuta el proceso de backup
    
    Returns:
        dict: Resultado del backup con información de éxito/error
    """
    backup_result = {
        'success': False,
        'timestamp': datetime.now().isoformat(),
        'bucket': S3_BUCKET_NAME,
        'files_uploaded': 0,
        'errors': [],
        'message': ''
    }
    
    try:
        logger.info("=" * 60)
        logger.info("INICIANDO PROCESO DE BACKUP")
        logger.info("=" * 60)
        
        # Inicializar manager
        manager = S3BackupManager()
        
        # Crear bucket si no existe
        logger.info("Verificando/creando bucket en S3...")
        manager.create_bucket(S3_BUCKET_NAME)
        
        # Generar nombre de carpeta: YYYY-MM-DD
        backup_date = datetime.now().strftime('%Y-%m-%d')
        s3_prefix = f"backups/{backup_date}"
        
        logger.info(f"Carpeta de backup será: s3://{S3_BUCKET_NAME}/{s3_prefix}")
        
        # Subir archivos
        logger.info(f"Subiendo archivos desde: {LOCAL_FILES_PATH}")
        files_uploaded, errors = manager.upload_files(
            LOCAL_FILES_PATH,
            S3_BUCKET_NAME,
            s3_prefix
        )
        
        backup_result['files_uploaded'] = files_uploaded
        backup_result['errors'] = errors
        
        if errors:
            backup_result['success'] = False
            backup_result['message'] = f"Backup completado con errores. {files_uploaded} archivo(s) subido(s), {len(errors)} error(es)"
            logger.warning(backup_result['message'])
        else:
            backup_result['success'] = True
            backup_result['message'] = f"Backup completado exitosamente. {files_uploaded} archivo(s) subido(s)"
            logger.info(backup_result['message'])
        
        logger.info("=" * 60)
        logger.info("BACKUP FINALIZADO")
        logger.info("=" * 60)
        
        return backup_result
        
    except Exception as e:
        backup_result['success'] = False
        backup_result['errors'] = [str(e)]
        backup_result['message'] = f"Error durante el backup: {str(e)}"
        logger.error(f"Error crítico: {e}")
        logger.error(traceback.format_exc())
        return backup_result


def main():
    """Función principal"""
    try:
        # Ejecutar backup
        result = perform_backup()
        
        # Enviar notificación por email
        logger.info("Enviando notificación por email...")
        send_notification(result)
        
        # Retornar código de salida apropiado
        sys.exit(0 if result['success'] else 1)
        
    except Exception as e:
        logger.error(f"Error no controlado en main: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
