"""
Módulo para enviar notificaciones por email
Soporta SMTP y AWS SES
"""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

try:
    from config import EMAIL_CONFIG
except ImportError:
    EMAIL_CONFIG = {'enabled': False}

logger = logging.getLogger(__name__)


def format_email_body(backup_result):
    """Formatea el cuerpo del email con los resultados del backup"""
    
    status = "✅ EXITOSO" if backup_result['success'] else "❌ FALLIDO"
    
    html_body = f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .container {{ max-width: 600px; margin: 0 auto; }}
                .header {{ background-color: #2c3e50; color: white; padding: 20px; border-radius: 5px 5px 0 0; }}
                .content {{ background-color: #ecf0f1; padding: 20px; }}
                .footer {{ background-color: #34495e; color: white; padding: 10px; text-align: center; border-radius: 0 0 5px 5px; }}
                .status {{ font-size: 24px; font-weight: bold; margin: 10px 0; }}
                .success {{ color: #27ae60; }}
                .error {{ color: #e74c3c; }}
                .info-box {{ background-color: white; padding: 15px; margin: 10px 0; border-left: 4px solid #3498db; }}
                .info-label {{ font-weight: bold; color: #2c3e50; }}
                table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
                th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #bdc3c7; }}
                th {{ background-color: #3498db; color: white; }}
                .error-item {{ background-color: #fadbd8; padding: 10px; margin: 5px 0; border-left: 3px solid #e74c3c; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📦 Reporte de Backup Automatizado a AWS S3</h1>
                </div>
                
                <div class="content">
                    <div class="status {'success' if backup_result['success'] else 'error'}">
                        {status}
                    </div>
                    
                    <div class="info-box">
                        <p><span class="info-label">Mensaje:</span> {backup_result['message']}</p>
                    </div>
                    
                    <table>
                        <tr>
                            <th>Información</th>
                            <th>Detalle</th>
                        </tr>
                        <tr>
                            <td>Timestamp</td>
                            <td>{backup_result['timestamp']}</td>
                        </tr>
                        <tr>
                            <td>Bucket S3</td>
                            <td><strong>s3://{backup_result['bucket']}</strong></td>
                        </tr>
                        <tr>
                            <td>Archivos Subidos</td>
                            <td><strong>{backup_result['files_uploaded']}</strong></td>
                        </tr>
                        <tr>
                            <td>Errores</td>
                            <td><strong>{len(backup_result['errors'])}</strong></td>
                        </tr>
                    </table>
                    
                    {''.join([f'<div class="error-item"><strong>Error:</strong> {error}</div>' for error in backup_result['errors']]) if backup_result['errors'] else ''}
                    
                </div>
                
                <div class="footer">
                    <p>Este es un mensaje automático del sistema de backup. No responder.</p>
                    <p>Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
                </div>
            </div>
        </body>
    </html>
    """
    
    return html_body


def send_via_smtp(subject, html_body):
    """Envía email utilizando SMTP"""
    try:
        config = EMAIL_CONFIG['smtp']
        
        # Crear mensaje
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = EMAIL_CONFIG['from_email']
        msg['To'] = ', '.join(EMAIL_CONFIG['to_emails'])
        
        # Agregar contenido HTML
        msg.attach(MIMEText(html_body, 'html'))
        
        # Conectar y enviar
        server = smtplib.SMTP(config['host'], config['port'])
        
        if config['use_tls']:
            server.starttls()
        
        server.login(config['username'], config['password'])
        server.send_message(msg)
        server.quit()
        
        logger.info(f"Email enviado exitosamente a {EMAIL_CONFIG['to_emails']}")
        return True
        
    except Exception as e:
        logger.error(f"Error al enviar email por SMTP: {e}")
        return False


def send_via_ses(subject, html_body):
    """Envía email utilizando AWS SES"""
    try:
        import boto3
        from botocore.exceptions import ClientError
        
        # Crear cliente SES
        ses_client = boto3.client(
            'ses',
            region_name=EMAIL_CONFIG['ses']['region']
        )
        
        # Enviar email
        response = ses_client.send_email(
            Source=EMAIL_CONFIG['from_email'],
            Destination={
                'ToAddresses': EMAIL_CONFIG['to_emails']
            },
            Message={
                'Subject': {
                    'Data': subject,
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Html': {
                        'Data': html_body,
                        'Charset': 'UTF-8'
                    }
                }
            }
        )
        
        logger.info(f"Email enviado exitosamente por SES. MessageId: {response['MessageId']}")
        return True
        
    except ClientError as e:
        logger.error(f"Error al enviar email por SES: {e}")
        return False
    except ImportError:
        logger.error("boto3 no está instalado. Instala con: pip install boto3")
        return False


def send_notification(backup_result):
    """
    Envía notificación por email del resultado del backup
    
    Args:
        backup_result (dict): Diccionario con resultado del backup
    """
    
    if not EMAIL_CONFIG.get('enabled', False):
        logger.info("Notificaciones por email deshabilitadas")
        return
    
    try:
        # Crear asunto del email
        status = "EXITOSO" if backup_result['success'] else "FALLIDO"
        subject = f"[AWS Backup] Proceso de backup {status} - {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        
        # Formatear cuerpo del email
        html_body = format_email_body(backup_result)
        
        # Determinar proveedor de email
        provider = EMAIL_CONFIG.get('provider', 'smtp').lower()
        
        if provider == 'ses':
            logger.info("Enviando notificación por AWS SES...")
            send_via_ses(subject, html_body)
        else:
            logger.info("Enviando notificación por SMTP...")
            send_via_smtp(subject, html_body)
    
    except Exception as e:
        logger.error(f"Error enviando notificación por email: {e}")


# Para testing
if __name__ == "__main__":
    # Ejemplo de uso
    test_result = {
        'success': True,
        'timestamp': datetime.now().isoformat(),
        'bucket': 'mi-backup-bucket',
        'files_uploaded': 20,
        'errors': [],
        'message': 'Backup completado exitosamente'
    }
    
    send_notification(test_result)
