from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, DateTimeField, DateField, TimeField, PasswordField
from wtforms.validators import DataRequired, Email, Optional, Length
from datetime import datetime


class LoginForm(FlaskForm):
    """Formulário de login para administradores"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])


class ParkForm(FlaskForm):
    """Formulário para criar/editar parques"""
    name = StringField('Nome', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Descrição', validators=[Optional()])
    type = SelectField('Tipo', choices=[
        ('Nacional', 'Nacional'),
        ('Estadual', 'Estadual'),
        ('Municipal', 'Municipal')
    ], validators=[DataRequired()])
    location = StringField('Localização', validators=[Optional(), Length(max=200)])


class TrailForm(FlaskForm):
    """Formulário para criar/editar trilhas"""
    park_id = SelectField('Parque', coerce=int, validators=[DataRequired()])
    name = StringField('Nome', validators=[DataRequired(), Length(max=200)])
    difficulty = SelectField('Dificuldade', choices=[
        ('fácil', 'Fácil'),
        ('moderada', 'Moderada'),
        ('difícil', 'Difícil')
    ], validators=[DataRequired()])
    duration_estimated = StringField('Duração Estimada', validators=[Optional(), Length(max=50)])
    description = TextAreaField('Descrição', validators=[Optional()])
    is_open = BooleanField('Aberta', default=True)


class EventForm(FlaskForm):
    """Formulário para criar/editar eventos"""
    park_id = SelectField('Parque', coerce=int, validators=[DataRequired()])
    title = StringField('Título', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Descrição', validators=[Optional()])
    start_datetime = DateTimeField('Data/Hora de Início', 
                                   format='%Y-%m-%dT%H:%M',
                                   validators=[DataRequired()],
                                   default=datetime.now)
    end_datetime = DateTimeField('Data/Hora de Término',
                                 format='%Y-%m-%dT%H:%M',
                                 validators=[DataRequired()],
                                 default=datetime.now)
    is_active = BooleanField('Ativo', default=True)


class AvailabilityPeriodForm(FlaskForm):
    """Formulário para criar/editar períodos de disponibilidade"""
    park_id = SelectField('Parque', coerce=int, validators=[DataRequired()])
    season_name = StringField('Nome da Temporada', validators=[DataRequired(), Length(max=100)])
    open_time = TimeField('Horário de Abertura', validators=[DataRequired()], format='%H:%M')
    close_time = TimeField('Horário de Fechamento', validators=[DataRequired()], format='%H:%M')
    start_date = DateField('Data de Início', validators=[DataRequired()], format='%Y-%m-%d')
    end_date = DateField('Data de Término', validators=[DataRequired()], format='%Y-%m-%d')


