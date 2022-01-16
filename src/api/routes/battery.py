from flask import Blueprint
from flask import request
from src.api.utils.responses import response_with
import src.api.utils.responses as resp
from src.api.model.battery import Battery, BatterySchema
from src.api.model.station import Station, StationSchema
from src.api.model.users import User, UserSchema
from src.api.utils.database import db

battery_routes = Blueprint('battery_routes', __name__)


@battery_routes.route('/find-all-batteries', methods=['GET'])
def find_all_battery():
    fetched = Battery.query.all()
    battery_schema = BatterySchema(many=True)
    batteries = battery_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={'battery': batteries})


@battery_routes.route('/<int:id>', methods=['GET'])
def find_by_id(id):
    fetched = Battery.query.get_or_404(id)
    battery_schema = BatterySchema()
    batteries = battery_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={'battery': batteries})

@battery_routes.route('/<rfid>', methods=['GET'])
def find_by_rfid(rfid):
    fetched = Battery.query.filter_by(rfidCode=rfid).first()
    if not fetched:
        return response_with(resp.INVALID_INPUT_422)
    return response_with(resp.SUCCESS_200, value={'battery': fetched})

#api 1
@battery_routes.route('/find-user-by-rfid', methods=['GET'])
def find_by_rfid():
    rfid = request.args.get('code')
    fetched = Battery.query.filter_by(rfidCode=rfid).first()
    if not fetched:
        return response_with(resp.INVALID_INPUT_422)

    user = fetched.u_owner
    user_schema = UserSchema()
    users = user_schema.dump(user)
    return response_with(resp.SUCCESS_200, value={'user': users})


@battery_routes.route('/create-battery', methods=['POST'])
def create_battery():
    try:
        data = request.get_json()
        battery_schema = BatterySchema()
        user = User.query.get_or_404(data['idUser'])
        station = Station.query.get_or_404(data['idStation'])
        battery = battery_schema.load(data)
        rs = battery_schema.dump(battery.create())
        return response_with(resp.SUCCESS_201, value={"battery": rs})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@battery_routes.route('/update-battery/<int:idBattery>', methods=['PUT'])
def update_battery(idBattery):
    try:
        get_battery = Battery.query.get_or_404(idBattery)
        data = request.get_json()
        id_user = User.query.get_or_404(data['idUser']).id
        id_station = Station.query.get_or_404(data['idStation']).id
        get_battery.idUser = id_user
        get_battery.idStation = id_station
        get_battery.rfidCode = data['rfidCode']
        db.session.add(get_battery)
        db.session.commit()
        battery_schema = BatterySchema()
        battery = battery_schema.dump(get_battery)
        return response_with(resp.SUCCESS_200, value={'battery': battery})
    except Exception as e:
        print(e)
        print('huynq:')
        return response_with(resp.INVALID_INPUT_422)


#api 2
@battery_routes.route('/switch-pin/<int:idUser>', methods=['PUT'])
def switch_pin(idUser):
    try:
        get_user = User.query.get_or_404(idUser)
        data = request.get_json()
        old_pin = Battery.query.get_or_404(data['idOldPin'])
        new_pin = Battery.query.get_or_404(data['idNewPin'])
        get_user.wallet = data['leftMoney']
        db.session.add(get_user)
        db.session.commit()

        id_current_station = new_pin.idStation
        old_pin.idUser = 1
        old_pin.idStation = id_current_station
        db.session.add(old_pin)
        db.session.commit()

        new_pin.idUser = idUser
        db.session.add(new_pin)
        db.session.commit()
        user_schema = UserSchema()
        user = user_schema.dump(get_user)
        return response_with(resp.SUCCESS_200, value={'battery': user})
    except Exception as e:
        print(e)
        print('huynq:')
        return response_with(resp.INVALID_INPUT_422)