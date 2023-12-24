from flask import Blueprint, request, jsonify, abort
from users import Jobs, db
from flask_login import login_required

# Создаем Blueprint
jobs_bp = Blueprint('jobs', __name__, url_prefix='/api/jobs')

@jobs_bp.route('', methods=['GET'])
def get_all_jobs():
    # Получаем все работы
    jobs = Jobs.query.all()

    # Преобразуем данные в словарь
    jobs_dict = [{'id': job.id,
                  'team_leader': {'id': job.team_leader.id, 'name': job.team_leader.name, 'surname': job.team_leader.surname},
                  'job': job.job,
                  'work_size': job.work_size,
                  'start_date': job.start_date,
                  'end_date': job.end_date,
                  'is_finished': job.is_finished} for job in jobs]

    return jsonify(jobs_dict)

@jobs_bp.route('/<int:job_id>', methods=['GET'])
def get_job_by_id(job_id):
    # Получаем работу по id
    job = Jobs.query.get_or_404(job_id)

    # Преобразуем данные в словарь
    job_dict = {'id': job.id,
                'team_leader': {'id': job.team_leader.id, 'name': job.team_leader.name, 'surname': job.team_leader.surname},
                'job': job.job,
                'work_size': job.work_size,
                'start_date': job.start_date,
                'end_date': job.end_date,
                'is_finished': job.is_finished}

    return jsonify(job_dict)

@jobs_bp.route('', methods=['POST'])
@login_required
def create_job():
    # Получаем данные из запроса
    data = request.json

    # Создаем новую работу
    new_job = Jobs(
        team_leader_id=data['team_leader_id'],
        job=data['job'],
        work_size=data['work_size'],
        start_date=data['start_date'],
        end_date=data['end_date'],
        is_finished=data['is_finished']
    )

    # Добавляем работу в базу данных
    db.session.add(new_job)
    db.session.commit()

    return jsonify({'message': 'Работа успешно добавлена'})

@jobs_bp.route('/<int:job_id>', methods=['DELETE'])
@login_required
def delete_job(job_id):
    # Получаем работу по id
    job = Jobs.query.get_or_404(job_id)

    # Удаляем работу
    db.session.delete(job)
    db.session.commit()

    return jsonify({'message': 'Работа успешно удалена'})

@jobs_bp.route('/<int:job_id>', methods=['PUT'])
@login_required
def update_job(job_id):
    # Получаем работу по id
    job = Jobs.query.get_or_404(job_id)

    # Обновляем данные
    data = request.json
    job.team_leader_id = data['team_leader_id']
    job.job = data['job']
    job.work_size = data['work_size']
    job.start_date = data['start_date']
    job.end_date = data['end_date']
    job.is_finished = data['is_finished']

    # Сохраняем изменения
    db.session.commit()

    return jsonify({'message': 'Работа успешно обновлена'})
