from flask import Blueprint, jsonify, request, abort
from flask_restful import Resource, Api
from users import db, Jobs, User
from jobs_parser import job_parser

jobs_resource_bp = Blueprint('jobs_resource', __name__)
api = Api(jobs_resource_bp)

class JobsListResource(Resource):
    def get(self):
        jobs = Jobs.query.all()
        jobs_list = [{'id': job.id, 'job': job.job, 'team_leader_id': job.team_leader_id,
                      'work_size': job.work_size, 'collaborators': [c.id for c in job.collaborators],
                      'is_finished': job.is_finished} for job in jobs]
        return jsonify(jobs_list)

    def post(self):
        args = job_parser.parse_args()

        team_leader_id = args['team_leader_id']
        team_leader = User.query.get(team_leader_id)

        if team_leader is None:
            abort(404, description='Team leader not found')

        collaborators_ids = args['collaborators']
        collaborators = User.query.filter(User.id.in_(collaborators_ids)).all()

        new_job = Jobs(
            team_leader_id=team_leader_id,
            team_leader=team_leader,
            job=args['job'],
            work_size=args['work_size'],
            collaborators=collaborators,
            is_finished=args['is_finished']
        )

        db.session.add(new_job)
        db.session.commit()

        return jsonify({'message': 'Job added successfully'})

class JobsResource(Resource):
    def get(self, job_id):
        job = Jobs.query.get(job_id)
        if job is None:
            abort(404)
        job_info = {'id': job.id, 'job': job.job, 'team_leader_id': job.team_leader_id,
                    'work_size': job.work_size, 'collaborators': [c.id for c in job.collaborators],
                    'is_finished': job.is_finished}
        return jsonify(job_info)

    def put(self, job_id):
        job = Jobs.query.get(job_id)
        if job is None:
            abort(404)

        args = job_parser.parse_args()

        team_leader_id = args['team_leader_id']
        team_leader = User.query.get(team_leader_id)

        if team_leader is None:
            abort(404, description='Team leader not found')

        collaborators_ids = args['collaborators']
        collaborators = User.query.filter(User.id.in_(collaborators_ids)).all()

        job.team_leader_id = team_leader_id
        job.team_leader = team_leader
        job.job = args['job']
        job.work_size = args['work_size']
        job.collaborators = collaborators
        job.is_finished = args['is_finished']

        db.session.commit()

        return jsonify({'message': 'Job edited successfully'})

    def delete(self, job_id):
        job = Jobs.query.get(job_id)
        if job is None:
            abort(404)

        db.session.delete(job)
        db.session.commit()

        return jsonify({'message': 'Job deleted successfully'})

api.add_resource(JobsListResource, '/jobs')
api.add_resource(JobsResource, '/jobs/<int:job_id>')
