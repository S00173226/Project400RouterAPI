from flask import abort, request, make_response, Flask, jsonify
import urllib3, requests, threading
import json, AutoInstaller as ai, RTRFunctions as rf, RTRClasses as rc

app = Flask(__name__)

@app.route('/device/<deviceName>/<functionCall>', methods=['GET'])
def deviceFunctionCall(deviceName, functionCall):
    listOfDevices = rf.deviceSearch(deviceName)
    for device in listOfDevices:
        print(device['deviceFunctions'])
        deviceFunctionsArray = device['deviceFunctions']
        for function in deviceFunctionsArray:
                print(function[functionCall])
                apiRoute = function['Parent'] + function[functionCall]
                deviceCall = rf.request_function_call(device['ipAddress'], apiRoute)
    return "API Triggered"

@app.route('/registerDevice', methods=['POST'])
def registerDevice():

    received_json=json.loads(request.data)
    t = threading.Thread(target=rf.addDevice(received_json))
    t.start()
    return "Registered"


@app.route('/deleteDevice', methods=['POST'])
def delete_device():
    received_json=json.loads(request.data)
    data = read_devices()
    for key in data['Registered-Devices']['device-type'].keys():
            print(key)
            if received_json['device-type'] == key:
                for device in data['Registered-Devices']['device-type'][key]['arrayOfDevices']:
                    print(device)
                    if received_json['mac-address'] == device['macAddress']:
                        data['Registered-Devices']['device-type'][key]['arrayOfDevices'].remove(device)
                        data['Registered-Devices']['device-type'][key]['count'] -= 1
    with open('Registered-Devices.json', 'w') as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)
    print("Device Removed")
    return "Removed"

@app.route('/databaseCheck', methods=['GET'])
def check_database():
    data = ai.read_devices()
    for key in data['Registered-Devices']['device-type'].keys():
            print(key)
            i = 0
            for i in range(data['Registered-Devices']['device-type'][key]['count']):
                duplicate_check = data['Registered-Devices']['device-type'][key]['arrayOfDevices'][i]
                for x in range(data['Registered-Devices']['device-type'][key]['count']):
                    if duplicate_check['id'] != data['Registered-Devices']['device-type'][key]['arrayOfDevices'][x]:
                        if duplicate_check['macAddress'] == data['Registered-Devices']['device-type'][key]['arrayOfDevices'][x]['macAddress']:
                            del data['Registered-Devices']['device-type'][key]['arrayOfDevices'][x]
                            data['Registered-Devices']['device-type'][key]['count'] -= 1
                            with open('Registered-Devices.json', 'w') as outfile:
                                json.dump(data, outfile, indent=4, sort_keys=True)
    print("Checked Duplicate Entries")
    return "Checked Duplicate Entries"



if __name__ == '__main__':
    app.run(host='192.168.1.136')