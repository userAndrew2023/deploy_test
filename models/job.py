import sqlalchemy
from sqlalchemy.util.preloaded import orm
from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase


class Jobs(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'jobs'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    team_leader_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    job_description = sqlalchemy.Column(sqlalchemy.String(500))
    work_size_hours = sqlalchemy.Column(sqlalchemy.Float)
    collaborators = sqlalchemy.Column(sqlalchemy.String(500))
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    team_leader = orm.relationship('User', foreign_keys=[team_leader_id])

    def __repr__(self):
        return f"<Job {self.id}>"
