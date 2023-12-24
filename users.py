
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy.orm import sessionmaker

db = SQLAlchemy()

def create_session():
    Session = sessionmaker(bind=db.engine)
    return Session()

# Таблица-ассоциация для связи "многие ко многим" между User и Jobs
collaborators_table = db.Table(
    'job_collaborators',
    db.Column('job_id', db.Integer, db.ForeignKey('jobs.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

# Таблица-ассоциация для связи "многие ко многим" между User и Department
members_table = db.Table(
    'department_members',
    db.Column('department_id', db.Integer, db.ForeignKey('departments.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    surname = db.Column(db.String(50))
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    position = db.Column(db.String(50))
    speciality = db.Column(db.String(50))
    address = db.Column(db.String(255))
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    hashed_password = db.Column(db.String(128))
    modified_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Добавляем связь "многие ко многим" с Jobs через таблицу-ассоциацию collaborators
    jobs = db.relationship('Jobs', secondary=collaborators_table, back_populates='collaborators')

    # Добавляем связь "многие ко многим" с Department через таблицу-ассоциацию members_table
    departments = db.relationship('Department', secondary=members_table, back_populates='members')

    def __repr__(self):
        return f'<User {self.surname} {self.name}>'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

class Jobs(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_leader_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    team_leader = db.relationship(User, foreign_keys=[team_leader_id])
    job = db.Column(db.String(255))
    work_size = db.Column(db.Float)

    # Добавляем связь "многие ко многим" с User через таблицу-ассоциацию collaborators
    collaborators = db.relationship('User', secondary=collaborators_table, back_populates='jobs')

    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    is_finished = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Job {self.id}: {self.job}>'

class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    chief_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    chief = db.relationship(User, foreign_keys=[chief_id])
    
    # Добавляем связь "многие ко многим" с User через таблицу-ассоциацию members_table
    members = db.relationship('User', secondary=members_table, back_populates='departments')

    email = db.Column(db.String(120))

    def __repr__(self):
        return f'<Department {self.title}>'