import json, requests
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
    #url = "http://" + received_json['ip-address'] + ":5000" + received_json['api-routes']
    url = "http://192.168.1.139" + ":5000" + "/home/api/v1.0/raspberry-pi/api-calls"
    payload = ""
    headers = {'content-type': 'application/json'}
    req = requests.get(url, headers = headers, json = {"key": "value"})
    return req.json()


def read_devices():
    with open("Registered-Devices.json", "r") as json_file:
            data = json.load(json_file)
            json_file.close()
            return data

