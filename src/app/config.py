import os
from pathlib import Path

# Caminho base do projeto (subindo um nível de src/app/)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / 'data'
DATA_DIR.mkdir(exist_ok=True)

class BaseConfig:
    """Configuração base para todas as configurações"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Caminho do banco de dados SQLite
    DATABASE_PATH = DATA_DIR / 'tere_verde.db'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'

class DevelopmentConfig(BaseConfig):
    """Configuração para desenvolvimento"""
    DEBUG = True

class ProductionConfig(BaseConfig):
    """Configuração para produção"""
    DEBUG = False
    # Em produção, SECRET_KEY deve ser definida via variável de ambiente
    SECRET_KEY = os.environ.get('SECRET_KEY') or None

# Dicionário para escolher a configuração pelo nome
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}

