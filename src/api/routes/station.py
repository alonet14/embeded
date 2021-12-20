from flask import Blueprint
from flask import request
from src.api.utils.responses import response_with
import src.api.utils.responses as resp
from src.api.model.station import Station, StationSchema
from src.api.utils.database import db

station_routes = Blueprint('station_routes', __name__)

@station_routes.route('/find-all-stations', methods=['GET'])
def find_all_station():
    fetched = Station.query.all()
    station_schema = StationSchema(many=True)
    stations = station_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={'station': stations})


@station_routes.route('/<int:id>', methods=['GET'])
def find_by_id(id):
    fetched = Station.query.get_or_404(id)
    station_schema = StationSchema()
    stations = station_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={'station': stations})


@station_routes.route('/create-station', methods=['POST'])
def create_station():
    try:
        data = request.get_json()
        station_schema = StationSchema()
        station = station_schema.load(data)
        rs = station_schema.dump(station.create())
        return response_with(resp.SUCCESS_201, value={"station": rs})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@station_routes.route('/update-station/<int:idStation>', methods=['PUT'])
def update_station(idStation):
    try:
        get_station = Station.query.get_or_404(idStation)
        data = request.get_json()
        get_station.location = data['location']
        db.session.add(get_station)
        db.session.commit()
        station_schema = StationSchema()
        station = station_schema.dump(get_station)
        return response_with(resp.SUCCESS_200, value={'station': station})
    except Exception as e:
        print(e)
        print('huynq:')
        return response_with(resp.INVALID_INPUT_422)