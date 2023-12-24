from flask import Flask, render_template, request, redirect, url_for, json, session, flash
import os
from functools import wraps 
from users import members_table, collaborators_table, db, User, Jobs, Department, create_session
from registration import RegistrationForm
from login import LoginForm

from sqlalchemy import create_engine, text, func
from sqlalchemy.orm import sessionmaker, aliased

from flask_wtf.csrf import CSRFProtect
from werkzeug.security import check_password_hash

from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from jobs_form import AddJobForm, EditJobForm

from api import jobs_bp
from api_user import user_bp
from users_resource import users_resource_bp
from jobs_resource import jobs_resource_bp

login_manager = LoginManager()
login_manager.login_view = 'login'  # Замените 'login' на имя вашего маршрута для входа в систему

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



app = Flask(__name__)
login_manager.init_app(app)
app.register_blueprint(jobs_bp)
app.register_blueprint(user_bp)
app.register_blueprint(users_resource_bp, url_prefix='/api/v2')
app.register_blueprint(jobs_resource_bp, url_prefix='/api/v2')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///firm.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/image'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['SECRET_KEY'] = 'radik'  # Замените на свой секретный ключ
def global_init(db_name):
    print(db_name)
    engine = create_engine(db_name)

    # Создаем таблицы, если они не существуют
    with app.app_context():
        db.create_all()
csrf = CSRFProtect(app)

# def login_required(view):
#     @wraps(view)
#     def wrapped_view(*args, **kwargs):
#         if 'user_id' not in session:
#             return redirect(url_for('login', next=request.url))
#         return view(*args, **kwargs)
#     return wrapped_view

@app.route('/')
@login_required
def base():
    return render_template('base.html')


@app.route('/index')
@login_required
def company_slogan():
    return 'Надежно и быстро'

@app.route('/promotion')
@login_required
def promotion():
    return '''
    Реклама кампании:<br>
    1. Надежно<br>
    2. Быстро<br>
    3. Качественно
    '''

@app.route('/image_promotion')
@login_required
def company_image():
    return render_template('image_promotion.html')

@app.route('/form')
@login_required
def form():
    return render_template('form.html')

@app.route('/results/<nickname>/<int:level>/<float:rating>')
def results(nickname, level, rating):
    return render_template('results.html', nickname=nickname, level=level, rating=rating)

@app.route('/photo')
@login_required
def photo():
    return render_template('photo.html', photo_filename=None)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload_photo', methods=['POST'])
@login_required
def upload_photo():
    if 'photo' not in request.files:
        return redirect(request.url)

    photo = request.files['photo']

    if photo.filename == '':
        return redirect(request.url)

    if photo and allowed_file(photo.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
        photo.save(filename)
        return render_template('photo.html', photo_filename=photo.filename)

    return redirect(request.url)

@app.route('/<title>')
def mars(title):
    return render_template('base_mars.html', title=title, company_slogan='Мы - Первые на Марсе', company_name='Исследователи Марса')

@app.route('/list_prof/<list>')
@login_required
def list_prof(list):
    positions = ['Директор', 'Менеджер', 'Программист', 'Дизайнер', 'Бухгалтер']

    return render_template('list_prof.html', list=list, positions=positions)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    # Обработка данных из формы
    nickname = request.form['inputLastName']  # Используем значение из inputLastName
    user_data = {
        'inputLastName': request.form['inputLastName'],
        'inputDOB': request.form['inputDOB'],
        'inputGender': request.form['inputGender'],
        'inputEducation': request.form['inputEducation'],
        'inputVacancy': request.form['inputVacancy'],
        'inputAddress': request.form['inputAddress'],
        'inputPhone': request.form['inputPhone'],
        'inputEmail': request.form['inputEmail'],
    }

    # Перенаправление на страницу результатов с передачей параметров
    return redirect(url_for('answer', user_data=user_data))

@app.route('/answer', methods=['POST'])
@login_required
def answer():
    user_data = {
        'inputLastName': request.form['inputLastName'],
        'inputDOB': request.form['inputDOB'],
        'inputGender': request.form['inputGender'],
        'inputEducation': request.form['inputEducation'],
        'inputVacancy': request.form['inputVacancy'],
        'inputAddress': request.form['inputAddress'],
        'inputPhone': request.form['inputPhone'],
        'inputEmail': request.form['inputEmail'],
    }
    check_data = [1 if value else 0 for value in user_data.values()]
    print(check_data)
    if 1 in check_data:
        return render_template('auto_answer.html', title='Answer', company_name='Исследователи Марса', company_slogan='Мы - первые на Марсе', user_data=user_data)
    else:
        return redirect(url_for('auto_answer'))


@app.route('/auto_answer')
@login_required
def auto_answer():
    user_data = {
        'inputLastName': 'Иванов Иван Иванович',
        'inputDOB': '01.01.1980',
        'inputGender': 'Мужской',
        'inputEducation': 'Высшее образование',
        'inputVacancy': 'Программист',
        'inputAddress': '123 улица, город, страна',
        'inputPhone': '+7 (123) 456-7890',
        'inputEmail': 'example@example.com',
    }

    return render_template('auto_answer.html', title='Auto_answer', company_name='Исследователи Марса', company_slogan='Мы - первые на Марсе', user_data=user_data)

# Загрузим данные о сотрудниках из JSON
with open('templates/crew.json', 'r', encoding='utf-8') as file:
    crew = json.load(file)

@app.route('/member')
@login_required
def member():
    return render_template('crew.html', title='Экипаж', company_name='Your Company', company_slogan='Best Company Ever!', crew=crew)

@app.route('/list_jobs')
@login_required
def list_jobs():
    jobs = Jobs.query.all()
    return render_template('jobs.html', jobs=jobs, User=User)

@login_required
def make_request():
    db_name = input("Введите имя базы данных: ")

    # Создаем подключение к базе данных
    engine = create_engine(f"sqlite:///instance/{db_name}.sqlite3")
    Session = sessionmaker(bind=engine)

    # Создаем приложение Flask
    with app.app_context():

        # Создаем сессию SQLAlchemy
        session = Session()

        # Сырой SQL-запрос для определения максимального размера команды
        max_team_size_query = text(
            """
            SELECT MAX(team_size) as max_size
            FROM (
                SELECT team_leader_id, COUNT(job_collaborators.user_id) as team_size
                FROM jobs
                JOIN job_collaborators ON jobs.id = job_collaborators.job_id
                GROUP BY team_leader_id
            )
            """
        )

        max_team_size_result = session.execute(max_team_size_query).fetchone()
        max_size = max_team_size_result[0]

        # Сырой SQL-запрос для получения тимлидов команд с максимальным размером
        largest_team_leaders_query = text(
            """
            SELECT u.surname, u.name
            FROM user u
            JOIN jobs j ON u.id = j.team_leader_id
            JOIN (
                SELECT job_id
                FROM job_collaborators
                GROUP BY job_id
                HAVING COUNT(DISTINCT user_id) = :max_size
            ) jc ON j.id = jc.job_id
            GROUP BY u.id
            """
        )


        largest_team_leaders_result = session.execute(largest_team_leaders_query, {'max_size': max_size}).fetchall()

        if largest_team_leaders_result:
            print("Тимлиды команд с наибольшим размером:")
            for leader in largest_team_leaders_result:
                print(f"{leader[0]} {leader[1]}")
        else:
            print("Нет данных о тимлидах команд с наибольшим размером.")

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Обработка данных из формы и создание нового пользователя
        new_user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        print(form.hidden_tag)
        return redirect(url_for('login'))  # Перенаправление на страницу входа после успешной регистрации
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.hashed_password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(url_for('list_jobs'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)

# Маршрут для выхода (завершения сессии)
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

def get_employees_with_hours_gt_25(session):
    session = create_session()
    user_alias = aliased(User)
    department_alias = aliased(Department)

    # Создаем подзапрос для вычисления суммарного времени работы по каждому сотруднику
    subquery = session.query(User.id, func.sum(Jobs.work_size).label('total_work_size')) \
                  .join(collaborators_table, User.id == collaborators_table.c.user_id) \
                  .join(Jobs, collaborators_table.c.job_id == Jobs.id) \
                  .group_by(User.id) \
                  .subquery()
    
    print(subquery)

    # Выполняем основной запрос
    result = session.query(user_alias.surname, user_alias.name) \
                    .join(members_table, user_alias.id == members_table.c.user_id) \
                    .join(department_alias, members_table.c.department_id == department_alias.id) \
                    .join(Jobs, members_table.c.user_id == Jobs.team_leader_id) \
                    .join(subquery, user_alias.id == subquery.c.id) \
                    .filter(department_alias.id == 1, subquery.c.total_work_size > 25) \
                    .all()
    return result

@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    form = AddJobForm()

    # Заполняем список ответственных и участников из базы данных
    form.team_leader.choices = [(user.id, f'{user.surname} {user.name}') for user in User.query.all()]
    form.collaborators.choices = [(user.id, f'{user.surname} {user.name}') for user in User.query.all()]

    if form.validate_on_submit():
        # Создаем новую работу на основе данных из формы
        new_job = Jobs(
            job=form.job_title.data,
            team_leader_id=form.team_leader.data,
            work_size=form.work_size.data,
            is_finished=form.is_finished.data
        )

        # Добавляем участников к работе
        collaborators = User.query.filter(User.id.in_(form.collaborators.data)).all()
        new_job.collaborators.extend(collaborators)

        # Добавляем работу в базу данных
        db.session.add(new_job)
        db.session.commit()

        return redirect(url_for('list_jobs'))

    return render_template('add_job.html', form=form)

@app.route('/edit_job/<int:job_id>', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    job = Jobs.query.get_or_404(job_id)

    # Проверяем, имеет ли текущий пользователь права на редактирование или удаление работы
    if current_user.id != job.team_leader_id and current_user.id != 1:
        flash('У вас нет прав для редактирования этой работы.', 'danger')
        return redirect(url_for('list_jobs'))

    form = EditJobForm(obj=job)

    # Заполняем поля формы данными из базы данных
    form.team_leader.choices = [(user.id, f'{user.surname} {user.name}') for user in User.query.all()]
    form.collaborators.choices = [(user.id, f'{user.surname} {user.name}') for user in User.query.all()]

    # Устанавливаем выбранные значения в поля team_leader и collaborators
    # form.team_leader.data = job.team_leader_id
    # form.collaborators.data = [collaborator.id for collaborator in job.collaborators]

    if form.validate_on_submit():
        # Преобразуем ID выбранных пользователей в экземпляры класса User перед сохранением в базу данных
        form.team_leader.data = User.query.get(form.team_leader.data)
        form.collaborators.data = [User.query.get(user_id) for user_id in form.collaborators.data]

        form.populate_obj(job)
        db.session.commit()
        flash('Работа успешно отредактирована.', 'success')
        return redirect(url_for('list_jobs'))

    return render_template('edit_job.html', form=form, job=job)

# Маршрут для удаления работы
@app.route('/delete_job/<int:job_id>', methods=['GET', 'POST'])
@login_required
def delete_job(job_id):
    job = Jobs.query.get_or_404(job_id)

    # Проверяем, имеет ли текущий пользователь права на удаление работы
    if current_user.id != job.team_leader_id and current_user.id != 1:
        flash('У вас нет прав для удаления этой работы.', 'danger')
        return redirect(url_for('list_jobs'))

    db.session.delete(job)
    db.session.commit()
    flash('Работа успешно удалена.', 'success')
    return redirect(url_for('list_jobs'))


db.init_app(app)

# TODO Переделать форму?

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Запрос к базе данных
        # make_request()

        # Еще один запрос
        # get_employees_with_hours_gt_25(session)

    app.run(debug=True, port=8080)
