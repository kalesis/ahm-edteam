import json
import uuid

from datetime import datetime, timezone
from flask import Flask, request
from flask_restful import Resource, Api, abort
#from werkzeug.exceptions import abort

app = Flask(__name__)
api = Api(app)


def generate_uuid():
    identifier = uuid.uuid4()
    return json.dumps(identifier, default=str)


def get_utc_now():
    now = datetime.utcnow().replace(tzinfo=timezone.utc)
    return json.dumps(now, default=str)


MEASUREMENTS = [
    {
        'id':'88888-4aaa-7ssd-22222222222',
        'sys': 120,
        'dia': 80,
        'pul': 70,
        'created': get_utc_now(),
        'user_id': 'CCCCC-3333-sseee-33333333333'
    }, 
    {
        'id':'99999-4aaa-7ssd-22222222222',
        'sys': 170,
        'dia': 90,
        'pul': 70,
        'created': get_utc_now(),
        'user_id': 'AAAAA-3333-sseee-33333333333'
    }
]


class Measurement(Resource):
    def get(self, id):
        for measurement in MEASUREMENTS:
            if id == measurement.get('id'):
                return measurement, 200
        abort(404, message=f'Measurement ID={id} was not found')


class MeasurementList(Resource):
    def get(self):
        return MEASUREMENTS, 200
    
    def post(self):
        data= json.loads(request.data)
        measurement = {
            'id': generate_uuid(),
            'sys': data.get('sys'),
            'dia': data.get('dia'),
            'pul': data.get('pul'),
            'created': get_utc_now(),
            'user_id': 'CCCCC-3333-sseee-33333333333'
        }
        MEASUREMENTS.append(measurement)
        return measurement, 201


api.add_resource(Measurement, '/v1/measurements/<string:id>')
api.add_resource(MeasurementList, '/v1/measurements')

if __name__ == '__main__':
    app.run(debug=True)
