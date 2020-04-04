import json, requests, RTRClasses as rc
def pipInstaller():
    return "Pip Installer Selected"
def aptInstaller():
    return "APT Installer Selected"
def npmInstaller():
    return "Npm Installer Selected"
def yumInstaller(install_link):
    return "Yum Installer Selected"
def dpkgInstaller(install_link):
    return "Dpkg Installer Selected"

def installer_call(install_link):
    response = ""
    installerFound = False
    try:
        if 'pip' in install_link == True:
            installerFound = True
            response = pipInstaller()
        elif ('apt' in install_link) == True:
            installerFound = True
            response = aptInstaller()
        elif "npm" in install_link == True:
            installerFound = True
            response = npmInstaller()
        elif "yum" in install_link == True:
            installerFound = True
            response = yumInstaller()
        elif "dpkg" in install_link == True:
            installerFound = True
            response = dpkgInstaller()

        if installerFound == False:
            raise ValueError("No compatible installer was found")
    except:
        raise ValueError("Error Occured Launching Installer")
    return response

def request_device_functions(received_json):
    url = "http://" + received_json['ip-address'] + ":5000" + received_json['api-routes']
    #url = "http://192.168.1.139" + ":5000" + "/home/api/v1.0/raspberry-pi/api-calls"
    payload = ""
    headers = {'content-type': 'application/json'}
    req = requests.get(url, headers = headers, json = {"key": "value"})
    return req.json()

def request_function_call(deviceIP, functionAPICall):
    url = "http://" + deviceIP + ":5000" + functionAPICall
    print(url)
    req = requests.get(url)
    return req.response()

def read_devices():
    with open("Registered-Devices.json", "r") as json_file:
            data = json.load(json_file)
            json_file.close()
            return data

def addDevice(received_json):
    data = read_devices()
    deviceID = ""
    for key in data['Registered-Devices']['device-type'].keys():
        print(key)
        if received_json['device-type'] == key:
            devices = []
            newDevice = rc.Device(deviceDesc=received_json['device-desc'], ipAddress=received_json['ip-address'],macAddress=received_json['mac-address'], apiRoutes=received_json['api-routes'], installerURL= received_json['installer-link'])
            data['Registered-Devices']['device-type'][key]['arrayOfDevices'].append(newDevice.jsonResponse())
            data['Registered-Devices']['device-type'][key]['count'] += 1
            deviceID = newDevice.id
        with open('Registered-Devices.json', 'w') as outfile:
            json.dump(data, outfile, indent=4, sort_keys=True)
    print("Device Added")
    DeviceAPIs = request_device_functions(received_json)
    print(DeviceAPIs)
    addAPI(DeviceAPIs, deviceID)

def addAPI(DeviceAPIs, deviceID):
    data = read_devices()
    for key in data['Registered-Devices']['device-type'].keys():
        for device in data['Registered-Devices']['device-type'][key]['arrayOfDevices']:
            if device['id'] == deviceID:
                device['deviceFunctions'].append(DeviceAPIs)
            with open('Registered-Devices.json', 'w') as outfile:
                json.dump(data, outfile, indent=4, sort_keys=True)
            print("Functions Added")

def deviceSearch(deviceName):
    data = read_devices()
    devicelist = []
    for key in data['Registered-Devices']['device-type'].keys():
        for device in data['Registered-Devices']['device-type'][key]['arrayOfDevices']:
            if device['deviceDesc'] == deviceName:
                devicelist.append(device)
    #print(devicelist)
    return devicelist
