from flask import Flask
from users import db, User, Jobs, Department

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///firm.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()  # Создание таблиц, если их нет в базе данных

    # Добавление нескольких сотрудников в таблицу users
    user1 = User(surname='Иванов', name='Иван', age=25, position='Программист', speciality='Python Developer', address='Москва', email='ivanov@example.com')
    user1.set_password('password123')  # Установка пароля
    db.session.add(user1)

    user2 = User(surname='Петров', name='Петр', age=30, position='Дизайнер', speciality='UI/UX Designer', address='Санкт-Петербург', email='petrov@example.com')
    user2.set_password('qwerty123')  # Установка пароля
    db.session.add(user2)

    user3 = User(surname='Сидоров', name='Сидор', age=35, position='Менеджер', speciality='Project Manager', address='Екатеринбург', email='sidorov@example.com')
    user3.set_password('securepass123')  # Установка пароля
    db.session.add(user3)

    user3 = User(surname='Тестов', name='Тест', age=35, position='Тест', speciality='test', address='Тест', email='test@mail.ru')
    user3.set_password('test')  # Установка пароля
    db.session.add(user3)

    # Получим id сотрудников, чтобы использовать их в записях о работе
    user1 = User.query.filter_by(email='ivanov@example.com').first()
    user2 = User.query.filter_by(email='petrov@example.com').first()
    user3 = User.query.filter_by(email='sidorov@example.com').first()

    # Добавление нескольких записей в таблицу jobs
    job1 = Jobs(team_leader=user1, job='Разработка веб-приложения', work_size=40, is_finished=False)
    job1.collaborators.append(user2)
    job1.collaborators.append(user3)
    db.session.add(job1)

    job2 = Jobs(team_leader=user2, job='Дизайн лэндинга', work_size=20, is_finished=True)
    job2.collaborators.append(user1)
    job2.collaborators.append(user3)
    db.session.add(job2)

    job3 = Jobs(team_leader=user3, job='Управление проектом', work_size=30, is_finished=False)
    job3.collaborators.append(user1)
    job3.collaborators.append(user2)
    db.session.add(job3)

    # Добавление нескольких записей в таблицу departments
    department1 = Department(title='Отдел разработки', chief=user1, email='dev@example.com')
    department1.members.append(user2)
    department1.members.append(user3)
    db.session.add(department1)

    department2 = Department(title='Отдел дизайна', chief=user2, email='design@example.com')
    department2.members.append(user1)
    department2.members.append(user3)
    db.session.add(department2)

    department3 = Department(title='Отдел управления проектами', chief=user3, email='pm@example.com')
    department3.members.append(user1)
    department3.members.append(user2)
    db.session.add(department3)

    db.session.commit()  # Сохранение изменений в базе данных
