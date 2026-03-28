import boto3
import os
from pathlib import Path
from src.logger import logger 
from botocore.exceptions import ClientError

# Use Environment Variables for flexibility
BUCKET = os.getenv("AWS_STORAGE_BUCKET_NAME")
REGION = os.getenv("AWS_REGION")

s3_client = boto3.client("s3", region_name=REGION)

def upload_file(local_path: Path, s3_key: str):
    if not local_path.exists():
        logger.error(f"File not found: {local_path}")
        return False
    
    try:
        logger.info(f"Uploading {local_path} to s3://{BUCKET}/{s3_key}...")
        s3_client.upload_file(str(local_path), BUCKET, s3_key)
        logger.info("Upload Successful.")
        return True
    except ClientError as e:
        logger.error(f"Credential or Permission Error: {e}")
    except Exception as e:
        logger.error(f"Unknown error during upload: {e}")
    return False

# Usage
if __name__ == "__main__":
    upload_file(Path("artifacts/model.pkl"), "models/latest_model.pkl")