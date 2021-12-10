from flask import Blueprint
from flask import request
from src.api.utils.responses import response_with
import src.api.utils.responses as resp
from src.api.model.users import User, UserSchema
from src.api.utils.database import db

user_routes = Blueprint('user_routes', __name__)


@user_routes.route('/find-all-users', methods=['GET'])
def find_all_user():
    fetched = User.query.all()
    user_schema = UserSchema(many=True)
    users = user_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={'users': users})


@user_routes.route('/<int:id>', methods=['GET'])
def find_by_id(id):
    fetched = User.query.get_or_404(id)
    user_schema = UserSchema()
    users = user_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={'users': users})


@user_routes.route('/create-user', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        user_schema = UserSchema()
        user = user_schema.load(data)
        rs = user_schema.dump(user.create())
        return response_with(resp.SUCCESS_201, value={"user": rs})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@user_routes.route('/update-user/<int:idUser>', methods=['PUT'])
def update_user(idUser):
    try:
        get_user = User.query.get_or_404(idUser)
        data = request.get_json()
        get_user.name = data['name']
        get_user.idn = data['idn']
        db.session.add(get_user)
        db.session.commit()
        user_schema = UserSchema()
        user = user_schema.dump(get_user)
        return response_with(resp.SUCCESS_200, value={'user': user})
    except Exception as e:
        print(e)
        print('hoang')
        return response_with(resp.INVALID_INPUT_422)



