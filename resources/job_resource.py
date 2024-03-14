from flask import jsonify, make_response, request
from flask_restful import Resource, abort, reqparse

from data import db_session
from models.job import Jobs

parser = reqparse.RequestParser()
parser.add_argument('team_leader_id', required=True, type=int)
parser.add_argument('job_description', required=True)
parser.add_argument('work_size_hours', required=True, type=float)
parser.add_argument('collaborators', required=True)
parser.add_argument('is_finished', required=False)


class JobResource(Resource):
    def get(self, job_id):
        session = db_session.create_session()
        self.abort_if_job_not_found(job_id)
        job = session.query(Jobs).get(job_id)
        return jsonify({'data': job.to_dict()})

    def put(self, job_id):
        session = db_session.create_session()
        self.abort_if_job_not_found(job_id)
        job = session.query(Jobs).get(job_id)
        args = parser.parse_args()
        for key, value in args.items():
            if value is not None:
                if key not in ['team_leader_id', 'job_description', 'work_size_hours', 'collaborators', 'is_finished']:
                    return make_response(jsonify({'error': 'Bad request'}), 400)
                setattr(job, key, value)
        session.merge(job)
        session.commit()
        return jsonify({'success': 'OK'})

    def delete(self, job_id):
        session = db_session.create_session()
        self.abort_if_job_not_found(job_id)
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})

    def abort_if_job_not_found(self, job_id):
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        if not job:
            abort(404, message=f"Job {job_id} not found")


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'data': [item.to_dict() for item in jobs]})

    def post(self):
        session = db_session.create_session()
        if not request.json:
            return make_response(jsonify({'error': 'Empty request'}), 400)
        elif not all(key in request.json for key in
                     ['team_leader_id', 'job_description', 'work_size_hours', 'collaborators', 'speciality', 'address', 'email', 'password']):
            return make_response(jsonify({'error': 'Bad request'}), 400)
        args = parser.parse_args()
        job = Jobs(**args)
        session.add(job)
        session.commit()

        return jsonify({'id': job.id})
