

from datetime import datetime
import os
import zipfile
import schedule
import time
import math
import paramiko

B_DIR_NAME = "world_p"
DIR_M = "server"
HOST = "fusemeowstorawindows.net"
USER = "fusemeowstorageu"
PASS = "S7/ZrFsT1k0upJsyRhNUhVLlZ/2MK"
remote_path = '/backups'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def calculate_chunks(file_size):
    if file_size <= 1024:
        chunk_size = file_size
    elif file_size <= 1024*1024:
        chunk_size = 1024
    else:
        chunk_size = 1024*1024
        
    num_chunks = int(math.ceil(file_size / float(chunk_size)))
    chunks = [chunk_size] * num_chunks
    chunks[-1] = file_size - chunk_size * (num_chunks - 1)
    return chunks

def upload_file(local_path, remote_file_path):
    try:
        ssh.connect(HOST, username=USER, password=PASS)
        sftp = ssh.open_sftp()

        file_size = os.stat(local_path).st_size
        chunks = calculate_chunks(file_size)

        with open(local_path, 'rb') as f:
            offset = 0
            sftp_file = sftp.open(remote_file_path, mode='wb')
            for chunk in chunks:
                f.seek(offset)
                data = f.read(chunk)
                sftp_file.write(data)
                offset += chunk
            sftp_file.close()

    except Exception as e:
        print(f"Error uploading file: {str(e)}")
    finally:
        time_now = datetime.utcnow()
        datef = time_now.strftime("%Y-%m-%d_%H-%M-%S_UTC")
        print(f"Backup uploaded: {datef}")
        sftp.close()
        ssh.close()

def main():
    time_now = datetime.utcnow()
    datef = time_now.strftime("%Y-%m-%d_%H-%M-%S_UTC")
    BACKUP_NAME = f"backup_{datef}.zip"
    
    try:
        os.makedirs(B_DIR_NAME, exist_ok=True)
        
        with zipfile.ZipFile(os.path.join(B_DIR_NAME, BACKUP_NAME), "w", compression=zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(DIR_M):
                for file in files:
                    zipf.write(os.path.join(root, file))
        print(f"Backup created: {BACKUP_NAME}")
        
        remote_file_path = os.path.join(remote_path, BACKUP_NAME)
        local_path = os.path.abspath(os.path.join(B_DIR_NAME, BACKUP_NAME))
        upload_file(local_path, remote_file_path)

    except Exception as e:
        print(f"Error creating or uploading backup: {e}")

if __name__ == '__main__':
    schedule.every(10).minutes.do(main)
    
    while True:
        schedule.run_pending()
        time.sleep(1)





"""
from datetime import datetime
import os
import zipfile
import schedule
import time

B_DIR_NAME = "world_backup"
DIR_M = "world"

def main():
    time_now = datetime.utcnow()
    datef = time_now.strftime("%Y-%m-%d_%H-%M-%S_UTC")
    BACKUP_NAME = f"backup_{datef}.zip"
    
    try:
        os.makedirs(B_DIR_NAME, exist_ok=True)
        
        with zipfile.ZipFile(os.path.join(B_DIR_NAME, BACKUP_NAME), "w", compression=zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(DIR_M):
                for file in files:
                    zipf.write(os.path.join(root, file))
        print(f"Backup created: {BACKUP_NAME}")

    except Exception as e:
        print(f"Error creating backup: {e}")

if __name__ == '__main__':
    schedule.every(1).minutes.do(main)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
        
        
        """
        
        
        
