from flask_restful import reqparse

job_parser = reqparse.RequestParser()
job_parser.add_argument('team_leader_id', type=int, required=True, help='Team leader ID is required')
job_parser.add_argument('job', type=str, required=True, help='Job title is required')
job_parser.add_argument('work_size', type=float, required=True, help='Work size is required')
job_parser.add_argument('collaborators', type=list, required=True, help='Collaborators list is required')
job_parser.add_argument('is_finished', type=bool, required=True, help='is_finished flag is required')
