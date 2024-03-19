from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET
import requests
import math
from datetime import datetime
from typing import List, Dict
from geopy.geocoders import Nominatim

app = Flask(__name__)

# Function to fetch ISS data from the provided URL
def fetch_iss_data(url: str) -> List[Dict]:
    try:
        response = requests.get(url)
        root = ET.fromstring(response.content)
        data = []
        for elem in root.findall('.//state'):
            state = {}
            for element in elem:
                state[element.tag] = float(element.text)
            data.append(state)
        return data
    except ValueError as e:
        return []

# Function to calculate average speed from state vectors
def calculate_average_speed(data: List[Dict]) -> float:
    try:
        total_speed = 0
        for state in data:
            speed = math.sqrt(state['x_dot'] ** 2 + state['y_dot'] ** 2 + state['z_dot'] ** 2)
            total_speed += speed
        return total_speed / len(data)
    except ZeroDivisionError:
        return 0

# Function to fetch the instantaneous speed for a specific epoch
def get_instantaneous_speed(epoch_data: Dict) -> float:
    try:
        speed = math.sqrt(epoch_data['x_dot'] ** 2 + epoch_data['y_dot'] ** 2 + epoch_data['z_dot'] ** 2)
        return speed
    except ValueError:
        return 0

# Route to return 'comment' list object from ISS data
@app.route('/comment', methods=['GET'])
def get_comment():
    return jsonify({'comment': 'This is a placeholder comment'})

# Route to return 'header' dict object from ISS data
@app.route('/header', methods=['GET'])
def get_header():
    return jsonify({'header': {'key1': 'value1', 'key2': 'value2'}})

# Route to return 'metadata' dict object from ISS data
@app.route('/metadata', methods=['GET'])
def get_metadata():
    return jsonify({'metadata': {'key1': 'value1', 'key2': 'value2'}})

# Route to return entire data set
@app.route('/epochs', methods=['GET'])
def get_epochs():
    url = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml'
    data = fetch_iss_data(url)
    return jsonify(data)

# Route to return modified list of Epochs given query parameters
@app.route('/epochs-modified', methods=['GET'])
def get_modified_epochs():
    limit = int(request.args.get('limit', default=10))
    offset = int(request.args.get('offset', default=0))
    url = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml'
    data = fetch_iss_data(url)
    modified_data = data[offset:offset+limit]
    return jsonify(modified_data)

# Route to return state vectors for a specific Epoch from the data set
@app.route('/epochs/<epoch>', methods=['GET'])
def get_epoch(epoch):
    url = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml'
    data = fetch_iss_data(url)
    epoch_data = [state for state in data if state['epoch'] == epoch]
    return jsonify(epoch_data)

# Route to return instantaneous speed for a specific Epoch in the data set
@app.route('/epochs/<epoch>/speed', methods=['GET'])
def get_speed(epoch):
    url = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml'
    data = fetch_iss_data(url)
    epoch_data = [state for state in data if state['epoch'] == epoch]
    speed = get_instantaneous_speed(epoch_data[0])
    return jsonify({'speed': speed})

# Route to return latitude, longitude, altitude, and geoposition for a specific Epoch in the data set
@app.route('/epochs/<epoch>/location', methods=['GET'])
def get_location(epoch):
    url = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml'
    data = fetch_iss_data(url)
    epoch_data = [state for state in data if state['epoch'] == epoch]
    # Implementation to calculate latitude, longitude, altitude, and geoposition (to be added)
    return jsonify({'latitude': 0, 'longitude': 0, 'altitude': 0, 'geoposition': 'N/A'})

# Route to return instantaneous speed, latitude, longitude, altitude, and geoposition for the Epoch that is nearest in time
@app.route('/now', methods=['GET'])
def get_current_data():
    url = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml'
    data = fetch_iss_data(url)
    current_time = datetime.now()
    closest_epoch = min(data, key=lambda x: abs(current_time - datetime.strptime(x['epoch'], '%Y-%m-%dT%H:%M:%S')))
    speed = get_instantaneous_speed(closest_epoch)
    # Implementation to calculate latitude, longitude, altitude, and geoposition for the closest epoch (to be added)
    return jsonify({'speed': speed, 'latitude': 0, 'longitude': 0, 'altitude': 0, 'geoposition': 'N/A'})

if __name__ == "__main__":
    app.run(debug=True)

