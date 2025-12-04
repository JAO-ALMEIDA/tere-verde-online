from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from datetime import datetime, date, time
from . import db
from .models import AdminUser, Park, Trail, Event, AvailabilityPeriod
from .forms import LoginForm, ParkForm, TrailForm, EventForm, AvailabilityPeriodForm

bp = Blueprint('admin', __name__, url_prefix='/admin')


def login_required(f):
    """Decorador para exigir login em rotas administrativas"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Você precisa fazer login para acessar esta área.', 'warning')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function


def get_current_admin():
    """Retorna o admin atual da sessão"""
    if 'admin_id' in session:
        return AdminUser.query.get(session['admin_id'])
    return None


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login para administradores"""
    form = LoginForm()
    
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        # Buscar admin por email
        admin = AdminUser.query.filter_by(email=email).first()
        
        if admin and admin.check_password(password):
            # Login bem-sucedido
            session['admin_id'] = admin.id
            flash(f'Bem-vindo, {admin.name}!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Email ou senha incorretos.', 'error')
    
    return render_template('login.html', form=form)


@bp.route('/logout')
def logout():
    """Logout do administrador"""
    session.pop('admin_id', None)
    flash('Logout realizado com sucesso.', 'success')
    return redirect(url_for('admin.login'))


@bp.route('/')
@login_required
def dashboard():
    """Dashboard administrativo com estatísticas"""
    parks_count = Park.query.count()
    trails_count = Trail.query.count()
    trails_open = Trail.query.filter_by(is_open=True).count()
    events_count = Event.query.count()
    events_active = Event.query.filter_by(is_active=True).count()
    events_upcoming = Event.query.filter(
        Event.is_active == True,
        Event.start_datetime >= datetime.utcnow()
    ).count()
    availability_periods_count = AvailabilityPeriod.query.count()
    
    return render_template('admin_dashboard.html',
                         parks_count=parks_count,
                         trails_count=trails_count,
                         trails_open=trails_open,
                         events_count=events_count,
                         events_active=events_active,
                         events_upcoming=events_upcoming,
                         availability_periods_count=availability_periods_count)


# ========== CRUD PARQUES ==========

@bp.route('/parks')
@login_required
def parks_list():
    """Lista todos os parques"""
    parks = Park.query.order_by(Park.name).all()
    return render_template('admin_parks.html', parks=parks)


@bp.route('/parks/new', methods=['GET', 'POST'])
@login_required
def park_create():
    """Criar novo parque"""
    form = ParkForm()
    
    if form.validate_on_submit():
        park = Park(
            name=form.name.data,
            description=form.description.data,
            type=form.type.data,
            location=form.location.data
        )
        db.session.add(park)
        db.session.commit()
        flash(f'Parque "{park.name}" criado com sucesso!', 'success')
        return redirect(url_for('admin.parks_list'))
    
    return render_template('admin_park_form.html', form=form, title='Criar Parque')


@bp.route('/parks/<int:park_id>/edit', methods=['GET', 'POST'])
@login_required
def park_edit(park_id):
    """Editar parque existente"""
    park = Park.query.get_or_404(park_id)
    form = ParkForm(obj=park)
    
    if form.validate_on_submit():
        park.name = form.name.data
        park.description = form.description.data
        park.type = form.type.data
        park.location = form.location.data
        db.session.commit()
        flash(f'Parque "{park.name}" atualizado com sucesso!', 'success')
        return redirect(url_for('admin.parks_list'))
    
    return render_template('admin_park_form.html', form=form, park=park, title='Editar Parque')


@bp.route('/parks/<int:park_id>/delete', methods=['POST'])
@login_required
def park_delete(park_id):
    """Excluir parque"""
    park = Park.query.get_or_404(park_id)
    park_name = park.name
    db.session.delete(park)
    db.session.commit()
    flash(f'Parque "{park_name}" excluído com sucesso!', 'success')
    return redirect(url_for('admin.parks_list'))


# ========== CRUD TRILHAS ==========

@bp.route('/trails')
@login_required
def trails_list():
    """Lista todas as trilhas"""
    trails = Trail.query.order_by(Trail.name).all()
    return render_template('admin_trails.html', trails=trails)


@bp.route('/trails/new', methods=['GET', 'POST'])
@login_required
def trail_create():
    """Criar nova trilha"""
    form = TrailForm()
    form.park_id.choices = [(p.id, p.name) for p in Park.query.order_by(Park.name).all()]
    
    if form.validate_on_submit():
        trail = Trail(
            park_id=form.park_id.data,
            name=form.name.data,
            difficulty=form.difficulty.data,
            duration_estimated=form.duration_estimated.data,
            description=form.description.data,
            is_open=form.is_open.data
        )
        db.session.add(trail)
        db.session.commit()
        flash(f'Trilha "{trail.name}" criada com sucesso!', 'success')
        return redirect(url_for('admin.trails_list'))
    
    return render_template('admin_trail_form.html', form=form, title='Criar Trilha')


@bp.route('/trails/<int:trail_id>/edit', methods=['GET', 'POST'])
@login_required
def trail_edit(trail_id):
    """Editar trilha existente"""
    trail = Trail.query.get_or_404(trail_id)
    form = TrailForm(obj=trail)
    form.park_id.choices = [(p.id, p.name) for p in Park.query.order_by(Park.name).all()]
    
    if form.validate_on_submit():
        trail.park_id = form.park_id.data
        trail.name = form.name.data
        trail.difficulty = form.difficulty.data
        trail.duration_estimated = form.duration_estimated.data
        trail.description = form.description.data
        trail.is_open = form.is_open.data
        db.session.commit()
        flash(f'Trilha "{trail.name}" atualizada com sucesso!', 'success')
        return redirect(url_for('admin.trails_list'))
    
    return render_template('admin_trail_form.html', form=form, trail=trail, title='Editar Trilha')


@bp.route('/trails/<int:trail_id>/toggle', methods=['POST'])
@login_required
def trail_toggle(trail_id):
    """Alternar status aberta/fechada da trilha"""
    trail = Trail.query.get_or_404(trail_id)
    trail.is_open = not trail.is_open
    status = 'aberta' if trail.is_open else 'fechada'
    db.session.commit()
    flash(f'Trilha "{trail.name}" marcada como {status}!', 'success')
    return redirect(url_for('admin.trails_list'))

@bp.route('/trails/<int:trail_id>/delete', methods=['GET'])
@login_required
def trail_delete(trail_id):
    """Excluir trilha"""
    trail = Trail.query.get_or_404(trail_id)
    trail_name = trail.name
    db.session.delete(trail)
    db.session.commit()
    flash(f'Trilha "{trail_name}" excluída com sucesso!', 'success')
    return redirect(url_for('admin.trails_list'))



# ========== CRUD EVENTOS ==========

@bp.route('/events')
@login_required
def events_list():
    """Lista todos os eventos"""
    events = Event.query.order_by(Event.start_datetime.desc()).all()
    return render_template('admin_events.html', events=events)


@bp.route('/events/new', methods=['GET', 'POST'])
@login_required
def event_create():
    """Criar novo evento"""
    form = EventForm()
    form.park_id.choices = [(p.id, p.name) for p in Park.query.order_by(Park.name).all()]
    
    if form.validate_on_submit():
        event = Event(
            park_id=form.park_id.data,
            title=form.title.data,
            description=form.description.data,
            start_datetime=form.start_datetime.data,
            end_datetime=form.end_datetime.data,
            is_active=form.is_active.data
        )
        db.session.add(event)
        db.session.commit()
        flash(f'Evento "{event.title}" criado com sucesso!', 'success')
        return redirect(url_for('admin.events_list'))
    
    return render_template('admin_event_form.html', form=form, title='Criar Evento')


@bp.route('/events/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
def event_edit(event_id):
    """Editar evento existente"""
    event = Event.query.get_or_404(event_id)
    form = EventForm(obj=event)
    form.park_id.choices = [(p.id, p.name) for p in Park.query.order_by(Park.name).all()]
    
    if form.validate_on_submit():
        event.park_id = form.park_id.data
        event.title = form.title.data
        event.description = form.description.data
        event.start_datetime = form.start_datetime.data
        event.end_datetime = form.end_datetime.data
        event.is_active = form.is_active.data
        db.session.commit()
        flash(f'Evento "{event.title}" atualizado com sucesso!', 'success')
        return redirect(url_for('admin.events_list'))
    
    return render_template('admin_event_form.html', form=form, event=event, title='Editar Evento')


@bp.route('/events/<int:event_id>/toggle', methods=['POST'])
@login_required
def event_toggle(event_id):
    """Alternar status ativo/inativo do evento"""
    event = Event.query.get_or_404(event_id)
    event.is_active = not event.is_active
    status = 'ativo' if event.is_active else 'inativo'
    db.session.commit()
    flash(f'Evento "{event.title}" marcado como {status}!', 'success')
    return redirect(url_for('admin.events_list'))

@bp.route('/events/<int:event_id>/delete', methods=['GET'])
@login_required
def event_delete(event_id):
    """Excluir evento"""
    event = Event.query.get_or_404(event_id)
    event_title = event.title
    db.session.delete(event)
    db.session.commit()
    flash(f'Evento "{event_title}" excluído com sucesso!', 'success')
    return redirect(url_for('admin.events_list'))


# ========== CRUD DISPONIBILIDADE ==========

@bp.route('/availability')
@login_required
def availability_list():
    """Lista todos os períodos de disponibilidade"""
    periods = AvailabilityPeriod.query.order_by(AvailabilityPeriod.start_date.desc()).all()
    return render_template('admin_availability.html', periods=periods)


@bp.route('/availability/new', methods=['GET', 'POST'])
@login_required
def availability_create():
    """Criar novo período de disponibilidade"""
    form = AvailabilityPeriodForm()
    form.park_id.choices = [(p.id, p.name) for p in Park.query.order_by(Park.name).all()]
    
    if form.validate_on_submit():
        period = AvailabilityPeriod(
            park_id=form.park_id.data,
            season_name=form.season_name.data,
            open_time=form.open_time.data.strftime('%H:%M'),
            close_time=form.close_time.data.strftime('%H:%M'),
            start_date=form.start_date.data,
            end_date=form.end_date.data
        )
        db.session.add(period)
        db.session.commit()
        flash(f'Período de disponibilidade "{period.season_name}" criado com sucesso!', 'success')
        return redirect(url_for('admin.availability_list'))
    
    return render_template('admin_availability_form.html', form=form, title='Criar Período de Disponibilidade')


@bp.route('/availability/<int:period_id>/edit', methods=['GET', 'POST'])
@login_required
def availability_edit(period_id):
    """Editar período de disponibilidade existente"""
    period = AvailabilityPeriod.query.get_or_404(period_id)
    
    # Converter strings de horário para time objects para o formulário
    open_time_obj = time.fromisoformat(period.open_time) if period.open_time else None
    close_time_obj = time.fromisoformat(period.close_time) if period.close_time else None
    
    form = AvailabilityPeriodForm(
        park_id=period.park_id,
        season_name=period.season_name,
        open_time=open_time_obj,
        close_time=close_time_obj,
        start_date=period.start_date,
        end_date=period.end_date
    )
    form.park_id.choices = [(p.id, p.name) for p in Park.query.order_by(Park.name).all()]
    
    if form.validate_on_submit():
        period.park_id = form.park_id.data
        period.season_name = form.season_name.data
        period.open_time = form.open_time.data.strftime('%H:%M')
        period.close_time = form.close_time.data.strftime('%H:%M')
        period.start_date = form.start_date.data
        period.end_date = form.end_date.data
        db.session.commit()
        flash(f'Período de disponibilidade "{period.season_name}" atualizado com sucesso!', 'success')
        return redirect(url_for('admin.availability_list'))
    
    return render_template('admin_availability_form.html', form=form, period=period, title='Editar Período de Disponibilidade')


@bp.route('/availability/<int:period_id>/delete', methods=['POST'])
@login_required
def availability_delete(period_id):
    """Excluir período de disponibilidade"""
    period = AvailabilityPeriod.query.get_or_404(period_id)
    period_name = period.season_name
    db.session.delete(period)
    db.session.commit()
    flash(f'Período de disponibilidade "{period_name}" excluído com sucesso!', 'success')
    return redirect(url_for('admin.availability_list'))




