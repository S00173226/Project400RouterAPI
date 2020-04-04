import uuid

class Device:
    def __init__(self, deviceDesc, ipAddress, macAddress, apiRoutes, installerURL):
        self.id = str(uuid.uuid1())
        self.deviceDesc = deviceDesc
        self.ipAddress = ipAddress
        self.macAddress = macAddress
        self.apiRoutes = apiRoutes
        self.deviceFunctions = []
        self.installerURL = installerURL
    def jsonResponse(self):
        return dict(id = self.id, deviceDesc = self.deviceDesc, ipAddress = self.ipAddress, macAddress = self.macAddress, apiRoutes = self.apiRoutes, deviceFunctions = self.deviceFunctions, installerURL = self.installerURL)