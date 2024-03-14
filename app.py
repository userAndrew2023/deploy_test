from flask import Flask, make_response, jsonify
from flask_restful import Api

from resources import user_resource, job_resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.json.ensure_ascii = False

api = Api(app)
api.add_resource(user_resource.UserListResource, '/api/v1/users')
api.add_resource(user_resource.UserResource, '/api/v1/users/<int:user_id>')
api.add_resource(job_resource.JobsListResource, '/api/v1/jobs')
api.add_resource(job_resource.JobResource, '/api/v1/jobs/<int:job_id>')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)
