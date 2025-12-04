import argparse
from datetime import datetime, timedelta, date

from . import db
from . import create_app
from .models import AdminUser, Park, Trail, Event, AvailabilityPeriod


def init_db(app):
	"""Cria as tabelas no banco de dados."""
	with app.app_context():
		db.create_all()
		print("Banco de dados inicializado (tabelas criadas).")


def seed_db(app):
	"""Insere dados mínimos de exemplo."""
	with app.app_context():
		# Garantir que tabelas existam
		db.create_all()

		# 1) AdminUser de teste
		admin_email = 'admin@teste.com'
		admin = AdminUser.query.filter_by(email=admin_email).first()
		if not admin:
			admin = AdminUser(name='Administrador', email=admin_email)
			admin.set_password('admin123')
			db.session.add(admin)

		# 2) Parques
		parks_data = [
			{
				'name': 'Parque Nacional da Serra dos Órgãos',
				'description': 'Famoso pelos seus picos e trilhas como a Travessia Petrópolis-Teresópolis.',
				'type': 'Nacional',
				'location': 'Teresópolis / Petrópolis / Guapimirim'
			},
			{
				'name': 'Parque Estadual dos Três Picos',
				'description': 'Maior parque estadual do RJ, destaque para o Pico Maior.',
				'type': 'Estadual',
				'location': 'Teresópolis / Nova Friburgo / Cachoeiras de Macacu'
			},
			{
				'name': 'Parque Natural Municipal Montanhas de Teresópolis',
				'description': 'Unidade municipal com belas paisagens e biodiversidade.',
				'type': 'Municipal',
				'location': 'Teresópolis'
			},
		]

		name_to_park = {}
		for pdata in parks_data:
			park = Park.query.filter_by(name=pdata['name']).first()
			if not park:
				park = Park(
					name=pdata['name'],
					description=pdata['description'],
					type=pdata['type'],
					location=pdata['location']
				)
				db.session.add(park)
				# flush para ter o id
				db.session.flush()
			name_to_park[pdata['name']] = park

		# 3) Trilhas (algumas por parque)
		trails_seed = [
			# Serra dos Órgãos
			{
				'park': 'Parque Nacional da Serra dos Órgãos',
				'name': 'Trilha da Pedra do Sino',
				'difficulty': 'difícil',
				'duration_estimated': '6-8h',
				'description': 'Uma das trilhas mais famosas, com vista incrível no cume.',
				'is_open': True,
			},
			{
				'park': 'Parque Nacional da Serra dos Órgãos',
				'name': 'Trilha Suspensa',
				'difficulty': 'fácil',
				'duration_estimated': '1-2h',
				'description': 'Trilha adaptada, excelente para iniciantes e famílias.',
				'is_open': True,
			},
			# Três Picos
			{
				'park': 'Parque Estadual dos Três Picos',
				'name': 'Acesso ao Pico Maior (base)',
				'difficulty': 'moderada',
				'duration_estimated': '3-4h',
				'description': 'Acesso até a base, com belas vistas e campos de altitude.',
				'is_open': True,
			},
			# Montanhas de Teresópolis
			{
				'park': 'Parque Natural Municipal Montanhas de Teresópolis',
				'name': 'Trilha da Vargem Grande',
				'difficulty': 'moderada',
				'duration_estimated': '2-3h',
				'description': 'Vegetação exuberante e riachos no caminho.',
				'is_open': True,
			},
		]

		for t in trails_seed:
			park = name_to_park.get(t['park'])
			if not park:
				continue
			exists = Trail.query.filter_by(park_id=park.id, name=t['name']).first()
			if not exists:
				db.session.add(Trail(
					park_id=park.id,
					name=t['name'],
					difficulty=t['difficulty'],
					duration_estimated=t['duration_estimated'],
					description=t['description'],
					is_open=t['is_open']
				))

		# 4) Eventos (alguns futuros)
		now = datetime.utcnow()
		events_seed = [
			{
				'park': 'Parque Nacional da Serra dos Órgãos',
				'title': 'Caminhada ao nascer do sol',
				'description': 'Atividade guiada para apreciar o nascer do sol na Pedra do Sino.',
				'start': now + timedelta(days=7, hours=6),
				'end': now + timedelta(days=7, hours=12),
				'is_active': True,
			},
			{
				'park': 'Parque Estadual dos Três Picos',
				'title': 'Mutirão de limpeza',
				'description': 'Ação voluntária de limpeza de trilhas.',
				'start': now + timedelta(days=14, hours=9),
				'end': now + timedelta(days=14, hours=13),
				'is_active': True,
			},
		]

		for e in events_seed:
			park = name_to_park.get(e['park'])
			if not park:
				continue
			exists = Event.query.filter_by(park_id=park.id, title=e['title']).first()
			if not exists:
				db.session.add(Event(
					park_id=park.id,
					title=e['title'],
					description=e['description'],
					start_datetime=e['start'],
					end_datetime=e['end'],
					is_active=e['is_active']
				))

		# 5) Períodos de disponibilidade
		periods_seed = [
			{
				'park': 'Parque Nacional da Serra dos Órgãos',
				'season_name': 'Alta Temporada Verão',
				'open_time': '08:00',
				'close_time': '17:00',
				'start_date': date(date.today().year, 12, 1),
				'end_date': date(date.today().year + 1, 3, 15),
			},
			{
				'park': 'Parque Estadual dos Três Picos',
				'season_name': 'Baixa Temporada',
				'open_time': '08:00',
				'close_time': '16:00',
				'start_date': date(date.today().year, 4, 1),
				'end_date': date(date.today().year, 11, 30),
			},
		]

		for p in periods_seed:
			park = name_to_park.get(p['park'])
			if not park:
				continue
			exists = AvailabilityPeriod.query.filter_by(park_id=park.id, season_name=p['season_name']).first()
			if not exists:
				db.session.add(AvailabilityPeriod(
					park_id=park.id,
					season_name=p['season_name'],
					open_time=p['open_time'],
					close_time=p['close_time'],
					start_date=p['start_date'],
					end_date=p['end_date'],
				))

		# Commit final
		db.session.commit()
		print("Banco populado com dados de exemplo.")


def main():
	parser = argparse.ArgumentParser(description='CLI do Terê Verde Online')
	parser.add_argument('command', choices=['init-db', 'seed'], help='Comando a executar')
	parser.add_argument('--config', default='development', help='Nome da configuração (development|production)')
	args = parser.parse_args()

	app = create_app(args.config)

	if args.command == 'init-db':
		init_db(app)
	elif args.command == 'seed':
		seed_db(app)


if __name__ == "__main__":
	main()


