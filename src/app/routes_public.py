from flask import Blueprint, render_template, request, abort
from datetime import datetime
from . import db
from .models import Park, Trail, Event, BiodiversityItem, AvailabilityPeriod

bp = Blueprint('public', __name__)


@bp.route('/')
def index():
	"""Página inicial com visão geral dos parques e principais atrações"""
	# Buscar todos os parques ordenados por nome
	parks = Park.query.order_by(Park.name).all()
	
	# Buscar trilhas abertas mais recentes (limitadas a 5)
	recent_trails = Trail.query.filter_by(is_open=True).order_by(Trail.id.desc()).limit(5).all()
	
	# Buscar próximos eventos ativos (limitados a 5)
	upcoming_events = Event.query.filter(
		Event.is_active == True,
		Event.start_datetime >= datetime.utcnow()
	).order_by(Event.start_datetime).limit(5).all()
	
	return render_template('index.html', 
					   parks=parks,
					   recent_trails=recent_trails,
					   upcoming_events=upcoming_events)


@bp.route('/parks')
def parks_list():
	"""Lista todos os parques com breve descrição"""
	parks = Park.query.order_by(Park.name).all()
	return render_template('parks.html', parks=parks)


@bp.route('/parks/<int:park_id>')
def park_detail(park_id):
	"""Detalhes do parque com trilhas, eventos, biodiversidade e disponibilidade"""
	park = Park.query.get_or_404(park_id)
	
	# Buscar trilhas do parque ordenadas por nome
	trails = Trail.query.filter_by(park_id=park_id).order_by(Trail.name).all()
	
	# Buscar eventos futuros ativos do parque
	upcoming_events = Event.query.filter(
		Event.park_id == park_id,
		Event.is_active == True,
		Event.start_datetime >= datetime.utcnow()
	).order_by(Event.start_datetime).all()
	
	# Buscar principais itens de biodiversidade (limitados a 10)
	biodiversity_items = BiodiversityItem.query.filter_by(
		park_id=park_id
	).order_by(BiodiversityItem.type, BiodiversityItem.name).limit(10).all()
	
	# Buscar período de disponibilidade atual (se houver)
	today = datetime.utcnow().date()
	current_availability = AvailabilityPeriod.query.filter(
		AvailabilityPeriod.park_id == park_id,
		AvailabilityPeriod.start_date <= today,
		AvailabilityPeriod.end_date >= today
	).first()
	
	return render_template('park_detail.html',
					   park=park,
					   trails=trails,
					   upcoming_events=upcoming_events,
					   biodiversity_items=biodiversity_items,
					   current_availability=current_availability)


@bp.route('/trails')
def trails_list():
	"""Lista todas as trilhas com filtros opcionais por parque e dificuldade"""
	# Obter parâmetros de filtro
	park_id = request.args.get('park_id', type=int)
	difficulty = request.args.get('difficulty', type=str)
	
	# Construir query base
	query = Trail.query.filter_by(is_open=True)
	
	# Aplicar filtros
	if park_id:
		query = query.filter_by(park_id=park_id)
	
	if difficulty and difficulty.lower() in ['fácil', 'facil', 'moderada', 'difícil', 'dificil']:
		# Normalizar dificuldade
		difficulty_map = {'facil': 'fácil', 'dificil': 'difícil'}
		normalized_difficulty = difficulty_map.get(difficulty.lower(), difficulty.lower())
		query = query.filter(Trail.difficulty.ilike(f'%{normalized_difficulty}%'))
	
	# Ordenar por nome
	trails = query.order_by(Trail.name).all()
	
	# Buscar todos os parques para o filtro
	parks = Park.query.order_by(Park.name).all()
	
	return render_template('trails.html',
					   trails=trails,
					   parks=parks,
					   selected_park_id=park_id,
					   selected_difficulty=difficulty)


@bp.route('/events')
def events_list():
	"""Lista eventos futuros com filtro opcional por parque"""
	# Obter parâmetro de filtro
	park_id = request.args.get('park_id', type=int)
	
	# Construir query base para eventos futuros ativos
	query = Event.query.filter(
		Event.is_active == True,
		Event.start_datetime >= datetime.utcnow()
	)
	
	# Aplicar filtro por parque se fornecido
	if park_id:
		query = query.filter_by(park_id=park_id)
	
	# Ordenar por data de início
	events = query.order_by(Event.start_datetime).all()
	
	# Buscar todos os parques para o filtro
	parks = Park.query.order_by(Park.name).all()
	
	return render_template('events.html',
					   events=events,
					   parks=parks,
					   selected_park_id=park_id)


@bp.route('/about')
def about():
	"""Página sobre o Terê Verde Online e uso consciente dos parques"""
	return render_template('about.html')
