import pytest

from src.app import create_app, db
from src.app.models import AdminUser, Park


@pytest.fixture()
def app():
	app = create_app('development')
	# Configuração específica para testes
	app.config.update(
		TESTING=True,
		SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',
		WTF_CSRF_ENABLED=False,
	)
	with app.app_context():
		# Criar tabelas
		db.create_all()
		# Seed mínimo para rotas públicas (opcional, mas útil)
		if Park.query.count() == 0:
			p = Park(name='Parque Teste', description='Descrição de teste', type='Municipal', location='Teresópolis')
			db.session.add(p)
			db.session.commit()
		yield app
		# Teardown
		db.session.remove()
		db.drop_all()


@pytest.fixture()
def client(app):
	return app.test_client()


def test_app_creation(app):
	assert app is not None
	assert app.config['TESTING'] is True


def test_index_route_ok(client):
	resp = client.get('/')
	assert resp.status_code == 200


def test_parks_route_ok(client):
	resp = client.get('/parks')
	assert resp.status_code == 200


def test_admin_login_flow(client, app):
	# Criar admin
	with app.app_context():
		admin = AdminUser(name='Admin Teste', email='admin@test.local')
		admin.set_password('secret123')
		db.session.add(admin)
		db.session.commit()
	# Executar login
	resp = client.post('/admin/login', data={
		'email': 'admin@test.local',
		'password': 'secret123'
	}, follow_redirects=False)
	# Deve redirecionar para o dashboard
	assert resp.status_code in (302, 303)
	assert '/admin' in resp.headers.get('Location', '')


