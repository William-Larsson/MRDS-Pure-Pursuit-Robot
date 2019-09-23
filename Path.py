"""
Path.py is an class that handles path related data given from a JSON-file, storing said data
in lists that's more easily accessible.

Updated by William Larsson, changes for better object orientation as well as adding getTimeStamp/-Status 2019-09-16
"""
import json

# Load the path from a file and convert it into a list of coordinates
class Path:
    def __init__(self, file_name):
        with open(file_name) as path_file:
            data = json.load(path_file)
        self.path = data

    def getPath(self):
        vecArray = [{'X': p['Pose']['Position']['X'],
                     'Y': p['Pose']['Position']['Y'],
                     'Z': p['Pose']['Position']['Z']}
                    for p in self.path]
        return vecArray

    def getTimesstamp(self):
        vecArray = [{'T': p['Timestamp']}
                    for p in self.path]
        return vecArray

    def getStatus(self):
        vecArray = [{'S': p['Status']}
                    for p in self.path]
        return vecArray
