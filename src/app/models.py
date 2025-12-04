from datetime import datetime, date
from . import db
from passlib.hash import bcrypt


class AdminUser(db.Model):
    """Modelo para usuários administradores"""
    __tablename__ = 'admin_users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def set_password(self, plain_password: str):
        """Define a senha do usuário usando bcrypt"""
        self.password_hash = bcrypt.hash(plain_password)
    
    def check_password(self, plain_password: str) -> bool:
        """Verifica se a senha fornecida corresponde à senha hash"""
        return bcrypt.verify(plain_password, self.password_hash)
    
    def __repr__(self):
        return f'<AdminUser {self.email}>'


class Park(db.Model):
    """Modelo para parques"""
    __tablename__ = 'parks'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    type = db.Column(db.String(50), nullable=False)  # Nacional, Estadual, Municipal
    location = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relacionamentos
    trails = db.relationship('Trail', backref='park', lazy='dynamic', cascade='all, delete-orphan')
    events = db.relationship('Event', backref='park', lazy='dynamic', cascade='all, delete-orphan')
    availability_periods = db.relationship('AvailabilityPeriod', backref='park', lazy='dynamic', cascade='all, delete-orphan')
    biodiversity_items = db.relationship('BiodiversityItem', backref='park', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Park {self.name}>'


class Trail(db.Model):
    """Modelo para trilhas"""
    __tablename__ = 'trails'
    
    id = db.Column(db.Integer, primary_key=True)
    park_id = db.Column(db.Integer, db.ForeignKey('parks.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)  # fácil, moderada, difícil
    duration_estimated = db.Column(db.String(50))  # ex: "2h", "4h"
    description = db.Column(db.Text)
    is_open = db.Column(db.Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f'<Trail {self.name}>'


class Event(db.Model):
    """Modelo para eventos"""
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    park_id = db.Column(db.Integer, db.ForeignKey('parks.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f'<Event {self.title}>'


class AvailabilityPeriod(db.Model):
    """Modelo para períodos de disponibilidade dos parques"""
    __tablename__ = 'availability_periods'
    
    id = db.Column(db.Integer, primary_key=True)
    park_id = db.Column(db.Integer, db.ForeignKey('parks.id'), nullable=False)
    season_name = db.Column(db.String(100), nullable=False)  # ex: "Alta Temporada Verão"
    open_time = db.Column(db.String(10), nullable=False)  # ex: "08:00"
    close_time = db.Column(db.String(10), nullable=False)  # ex: "17:00"
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    
    def __repr__(self):
        return f'<AvailabilityPeriod {self.season_name} - {self.park.name if self.park else ""}>'


class BiodiversityItem(db.Model):
    """Modelo para itens de biodiversidade (fauna e flora)"""
    __tablename__ = 'biodiversity_items'
    
    id = db.Column(db.Integer, primary_key=True)
    park_id = db.Column(db.Integer, db.ForeignKey('parks.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # fauna, flora
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<BiodiversityItem {self.name} ({self.type})>'
