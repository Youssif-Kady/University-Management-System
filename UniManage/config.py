"""
UniManage – Configuration Module
AWS Integration Points:
  - DB_HOST        → Amazon RDS MySQL endpoint
  - S3_BUCKET      → Amazon S3 bucket for profile picture uploads
  - AWS_REGION     → AWS region (e.g. us-east-1)
"""
import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "unimanage-dev-secret-2024")
    DEBUG = False

    # Database (MySQL / Amazon RDS)
    DB_HOST     = os.getenv("DB_HOST",     "localhost")
    DB_PORT     = int(os.getenv("DB_PORT", "3306"))
    DB_NAME     = os.getenv("DB_NAME",     "unimanage")
    DB_USER     = os.getenv("DB_USER",     "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USER','root')}:{os.getenv('DB_PASSWORD','')}"
        f"@{os.getenv('DB_HOST','localhost')}:{os.getenv('DB_PORT','3306')}/{os.getenv('DB_NAME','unimanage')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Amazon S3
    S3_BUCKET         = os.getenv("S3_BUCKET",             "unimanage-profiles")
    S3_REGION         = os.getenv("AWS_REGION",            "us-east-1")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID",     "")
    AWS_SECRET_KEY    = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    S3_BASE_URL       = f"https://{os.getenv('S3_BUCKET','unimanage-profiles')}.s3.{os.getenv('AWS_REGION','us-east-1')}.amazonaws.com/"

    # Local uploads fallback
    UPLOAD_FOLDER      = os.path.join(os.path.dirname(__file__), "static", "images", "uploads")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB
    STUDENTS_PER_PAGE  = 10

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config_map = {
    "development": DevelopmentConfig,
    "production":  ProductionConfig,
    "default":     DevelopmentConfig,
}

