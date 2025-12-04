from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from .config import config_by_name

# Inicializar extensões fora da factory para poder importar em outros módulos
db = SQLAlchemy()
csrf = CSRFProtect()

def create_app(config_name='development'):
	"""
	Factory function para criar a aplicação Flask.
	
	Args:
		config_name: Nome da configuração a ser usada ('development' ou 'production')
	
	Returns:
		Instância configurada da aplicação Flask
	"""
	app = Flask(__name__, 
	            template_folder='templates',
	            static_folder='static')
	
	# Carregar configuração
	config_class = config_by_name.get(config_name, config_by_name['development'])
	app.config.from_object(config_class)
	
	# Inicializar SQLAlchemy
	db.init_app(app)
	
	# Inicializar CSRF Protection
	csrf.init_app(app)
	
	# Adicionar helper de contexto para token CSRF
	@app.context_processor
	def inject_csrf_token():
		from flask_wtf.csrf import generate_csrf
		return dict(csrf_token=generate_csrf)
	
	# Importar modelos para garantir que sejam registrados
	from . import models  # noqa: F401
	
	# Registrar blueprints
	from .routes_public import bp as public_bp
	from .routes_admin import bp as admin_bp
	
	app.register_blueprint(public_bp)
	# admin_bp já possui url_prefix='/admin'
	app.register_blueprint(admin_bp)
	
	return app

