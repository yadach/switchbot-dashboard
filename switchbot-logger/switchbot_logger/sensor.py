from bluepy import btle


# https://qiita.com/c60evaporator/items/7c3156a6bbb7c6c59052
class SwitchbotScanDelegate(btle.DefaultDelegate):
    def __init__(self, macaddr):
        btle.DefaultDelegate.__init__(self)
        self.sensorValue = None
        self.macaddr = macaddr

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if dev.addr == self.macaddr:
            for _, desc, value in dev.getScanData():
                if desc == "16b Service Data":
                    self._decodeSensorData(value)

    def _decodeSensorData(self, valueStr):
        valueBinary = bytes.fromhex(valueStr[4:])
        batt = valueBinary[2] & 0b01111111
        isTemperatureAboveFreezing = valueBinary[4] & 0b10000000
        temp = (valueBinary[3] & 0b00001111) / 10 + (valueBinary[4] & 0b01111111)
        if not isTemperatureAboveFreezing:
            temp = -temp
        humid = valueBinary[5] & 0b01111111
        self.sensorValue = {
            "SensorType": "SwitchBot",
            "Temperature": temp,
            "Humidity": humid,
            "BatteryVoltage": batt,
        }
