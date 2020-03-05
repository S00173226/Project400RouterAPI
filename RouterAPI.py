from flask import abort, request, make_response, Flask, jsonify
import urllib3
import json
import uuid

from yaml import Loader, Dumper

app = Flask(__name__)

@app.route('/registerDevice', methods=['POST'])
def registerDevice():

        received_json=json.loads(request.data)
        data = read_devices()
        print(data)
        print(data['Registered-Devices']['device-type'])
        for key in data['Registered-Devices']['device-type'].keys():
            print(key)
            if received_json['device-type'] == key:
                devices = []
                newDevice = {
                    'id': str(uuid.uuid1()),
                    'device-desc' : received_json['device-desc'],
                    'ip-address': received_json['ip-address'],
                    'mac-address' : received_json['mac-address'],
                    'api-routes' : received_json['api-routes'],
                    'device-functions' : {},
                    'installer-url' : received_json['installer-link']
                }
                data['Registered-Devices']['device-type'][key]['arrayOfDevices'].append(newDevice)
                data['Registered-Devices']['device-type'][key]['count'] += 1
            with open('Registered-Devices.json', 'w') as outfile:
                json.dump(data, outfile, indent=4, sort_keys=True)
        print("Registered")
        return "Registered"


def read_devices():
    with open("Registered-Devices.json", "r") as json_file:
            data = json.load(json_file)
            json_file.close()
            return data

@app.route('/deleteDevice', methods=['POST'])
def delete_device():
    received_json=json.loads(request.data)
    data = read_devices()
    for key in data['Registered-Devices']['device-type'].keys():
            print(key)
            if received_json['device-type'] == key:
                for device in data['Registered-Devices']['device-type'][key]['arrayOfDevices']:
                    print(device)
                    if received_json['mac-address'] == device['mac-address']:
                        data['Registered-Devices']['device-type'][key]['arrayOfDevices'].remove(device)
                        data['Registered-Devices']['device-type'][key]['count'] -= 1
    with open('Registered-Devices.json', 'w') as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)
    print("Device Removed")
    return "Removed"

@app.route('/databaseCheck', methods=['GET'])
def check_database():
    data = read_devices()
    for key in data['Registered-Devices']['device-type'].keys():
            print(key)
            i = 0
            for i in range(data['Registered-Devices']['device-type'][key]['count']):
                duplicate_check = data['Registered-Devices']['device-type'][key]['arrayOfDevices'][i]
                for x in range(data['Registered-Devices']['device-type'][key]['count']):
                    if duplicate_check['id'] != data['Registered-Devices']['device-type'][key]['arrayOfDevices'][x]:
                        if duplicate_check['mac-address'] == data['Registered-Devices']['device-type'][key]['arrayOfDevices'][x]['mac-address']:
                            del data['Registered-Devices']['device-type'][key]['arrayOfDevices'][x]
                            data['Registered-Devices']['device-type'][key]['count'] -= 1
                            with open('Registered-Devices.json', 'w') as outfile:
                                json.dump(data, outfile, indent=4, sort_keys=True)
    print("Checked Duplicate Entries")
    return "Checked Duplicate Entries"



if __name__ == '__main__':
    app.run(debug=True)