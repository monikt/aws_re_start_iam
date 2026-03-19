#!/usr/bin/env python3
"""
Script para generar un inventario de recursos AWS activos.
Utiliza boto3 para escanear servicios comunes y clasifica los recursos por tipo y estado.
Requiere credenciales AWS configuradas (aws configure o variables de entorno).
"""

import boto3
import json
import sys
from datetime import datetime


def get_ec2_instances():
    """
    Obtiene instancias EC2 activas.
    Clasifica por estado: running, stopped, etc.
    """
    try:
        ec2 = boto3.client('ec2')
        response = ec2.describe_instances()
        instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instances.append({
                    'InstanceId': instance['InstanceId'],
                    'State': instance['State']['Name'],
                    'InstanceType': instance['InstanceType'],
                    'Region': ec2.meta.region_name,
                    'LaunchTime': instance['LaunchTime'].isoformat() if 'LaunchTime' in instance else None
                })
        return instances
    except Exception as e:
        print(f"Error obteniendo instancias EC2: {e}")
        return []


def get_s3_buckets():
    """
    Obtiene buckets S3.
    Todos los buckets listados se consideran activos.
    """
    try:
        s3 = boto3.client('s3')
        response = s3.list_buckets()
        buckets = []
        for bucket in response['Buckets']:
            buckets.append({
                'Name': bucket['Name'],
                'CreationDate': bucket['CreationDate'].isoformat(),
                'Region': s3.get_bucket_location(Bucket=bucket['Name'])['LocationConstraint'] or 'us-east-1'
            })
        return buckets
    except Exception as e:
        print(f"Error obteniendo buckets S3: {e}")
        return []


def get_rds_instances():
    """
    Obtiene instancias RDS.
    Clasifica por estado: available, stopped, etc.
    """
    try:
        rds = boto3.client('rds')
        response = rds.describe_db_instances()
        instances = []
        for db in response['DBInstances']:
            instances.append({
                'DBInstanceIdentifier': db['DBInstanceIdentifier'],
                'DBInstanceStatus': db['DBInstanceStatus'],
                'DBInstanceClass': db['DBInstanceClass'],
                'Engine': db['Engine'],
                'Region': rds.meta.region_name
            })
        return instances
    except Exception as e:
        print(f"Error obteniendo instancias RDS: {e}")
        return []


def get_lambda_functions():
    """
    Obtiene funciones Lambda.
    Todas se consideran activas si existen.
    """
    try:
        lambda_client = boto3.client('lambda')
        response = lambda_client.list_functions()
        functions = []
        for func in response['Functions']:
            functions.append({
                'FunctionName': func['FunctionName'],
                'Runtime': func['Runtime'],
                'LastModified': func['LastModified'],
                'Region': lambda_client.meta.region_name
            })
        return functions
    except Exception as e:
        print(f"Error obteniendo funciones Lambda: {e}")
        return []


def classify_resources(inventory):
    """
    Clasifica los recursos por tipo y estado.
    Retorna un diccionario clasificado.
    """
    classified = {
        'EC2': {'running': [], 'stopped': [], 'other': []},
        'S3': {'active': []},
        'RDS': {'available': [], 'stopped': [], 'other': []},
        'Lambda': {'active': []}
    }

    for instance in inventory.get('EC2', []):
        state = instance['State']
        if state == 'running':
            classified['EC2']['running'].append(instance)
        elif state == 'stopped':
            classified['EC2']['stopped'].append(instance)
        else:
            classified['EC2']['other'].append(instance)

    for bucket in inventory.get('S3', []):
        classified['S3']['active'].append(bucket)

    for db in inventory.get('RDS', []):
        status = db['DBInstanceStatus']
        if status == 'available':
            classified['RDS']['available'].append(db)
        elif status == 'stopped':
            classified['RDS']['stopped'].append(db)
        else:
            classified['RDS']['other'].append(db)

    for func in inventory.get('Lambda', []):
        classified['Lambda']['active'].append(func)

    return classified


def main():
    """
    Función principal: recopila inventario, clasifica y guarda en JSON.
    """
    print("Iniciando escaneo de recursos AWS...")

    inventory = {
        'EC2': get_ec2_instances(),
        'S3': get_s3_buckets(),
        'RDS': get_rds_instances(),
        'Lambda': get_lambda_functions(),
        'Timestamp': datetime.utcnow().isoformat()
    }

    classified = classify_resources(inventory)

    # Imprimir resumen en consola
    print("\nResumen de inventario:")
    for service, states in classified.items():
        print(f"\n{service}:")
        for state, resources in states.items():
            print(f"  {state.capitalize()}: {len(resources)} recursos")

    # Guardar en archivo JSON
    filename = f"inventario_aws_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump({'inventory': inventory, 'classified': classified}, f, indent=4)

    print(f"\nInventario guardado en {filename}")


if __name__ == '__main__':
    main()