from flask import jsonify, make_response, request
from flask_restful import Resource, abort, reqparse

from data import db_session
from models.user import User


parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('age', required=True, type=int)
parser.add_argument('position', required=True)
parser.add_argument('speciality', required=True)
parser.add_argument('address', required=True)
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)


class UserResource(Resource):
    def get(self, user_id):
        session = db_session.create_session()
        self.abort_if_user_not_found(user_id)
        user = session.query(User).get(user_id)
        return jsonify({'data': user.to_dict(only=['id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email'])})

    def put(self, user_id):
        session = db_session.create_session()
        self.abort_if_user_not_found(user_id)
        user = session.query(User).get(user_id)
        args = parser.parse_args()
        print(args)
        for key, value in args.items():
            if value is not None:
                if key not in ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email']:
                    return make_response(jsonify({'error': 'Bad request'}), 400)
                setattr(user, key, value)
        session.merge(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def delete(self, user_id):
        session = db_session.create_session()
        self.abort_if_user_not_found(user_id)
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def abort_if_user_not_found(self, user_id):
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        if not user:
            abort(404, message=f"User {user_id} not found")


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'data': [item.to_dict(only=['id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email']) for item in users]})

    def post(self):
        session = db_session.create_session()
        if not request.json:
            return make_response(jsonify({'error': 'Empty request'}), 400)
        elif not all(key in request.json for key in
                     ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'password']):
            return make_response(jsonify({'error': 'Bad request'}), 400)
        args = parser.parse_args()
        args['hashed_password'] = User.set_password(args['password'])
        del args['password']
        user = User(**args)
        session.add(user)
        session.commit()

        return jsonify({'id': user.id})
