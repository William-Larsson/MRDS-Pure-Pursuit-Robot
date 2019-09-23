"""
Example demonstrating how to communicate with Microsoft Robotic Developer
Studio 4 via the Lokarria http interface. 

Author: Erik Billing (billing@cs.umu.se)

Updated by Ola Ringdahl 2014-09-11
Updated by Lennart Jern 2016-09-06 (converted to Python 3)
Updated by Filip Allberg and Daniel Harr 2017-08-30 (actually converted to Python 3)
Updated by Thomas Johansson 2019-08-22 from Lokarriaexample.py to a class implementation
Updated by Thomas Johansson fixed some errors in getHeading, getPosition. getHeading now returns an angle 2019-09-04
"""

import http.client, json, time
from math import sin,cos,pi,atan2
import quaternion, Path

HEADERS = {"Content-type": "application/json", "Accept": "text/json"}


class UnexpectedResponse(Exception):
    pass


class Robot:
    
    def __init__(self, host, port):
        self.url = host + ':' + port

    # Returns the heading angle, in radians, counterclockwise from the x-axis
    # Note that the sign changes at pi radians, i.e. the heading goes from 0
    # to pi, then from -pi back to 0 for a complete circuit.
    def getHeading(self):
        pose = self._getPose()['Pose']['Orientation']
        heading = quaternion.heading(pose) 
        return atan2(heading["Y"], heading["X"])

    # Returns the XY position as a two-element list
    def getPosition(self):
        pose = self._getPose()
        return pose['Pose']['Position']

    # Sends a speed and turn rate
    # command to the MRDS server
    # speed is given in m/s, turn rate in radians/s
    def setMotion(self, linear_speed, turn_rate):
        mrds = http.client.HTTPConnection(self.url)
        params = json.dumps({'TargetLinearSpeed': linear_speed, 'TargetAngularSpeed': turn_rate})
        mrds.request('POST', '/lokarria/differentialdrive', params, HEADERS)
        response = mrds.getresponse()
        status = response.status
        # response.close()
        if status == 204:
            return response
        else:
            raise UnexpectedResponse(response)        
        pass 

    # Requests the current laser scan from the MRDS server and parses it into a dict
    def getLaser(self):
        mrds = http.client.HTTPConnection(self.url)
        mrds.request('GET', '/lokarria/laser/echoes')
        response = mrds.getresponse()
        if response.status == 200:
            laserData = response.read()
            response.close()
            return json.loads(laserData.decode())
        else:
            return response        
        pass

    # Requests the current laser properties from the MRDS server and parses it into a dict
    def getLaserAngles(self):
        mrds = http.client.HTTPConnection(self.url)
        mrds.request('GET', '/lokarria/laser/properties')
        response = mrds.getresponse()
        if response.status == 200:
            laserData = response.read()
            response.close()
            properties = json.loads(laserData.decode())
            beamCount = int((properties['EndAngle']-properties['StartAngle'])/properties['AngleIncrement'])
            a = properties['StartAngle']  # +properties['AngleIncrement']
            angles = []
            while a <= properties['EndAngle']:
                angles.append(a)
                a += pi/180  # properties['AngleIncrement']
            # angles.append(properties['EndAngle']-properties['AngleIncrement']/2)
            return angles
        else:
            raise UnexpectedResponse(response)
        
    # Local methods, not usually used outside of this class    
    def _getPose(self):     
        """Reads the current position and orientation from the MRDS"""
        mrds = http.client.HTTPConnection(self.url)
        mrds.request('GET', '/lokarria/localization')
        response = mrds.getresponse()
        if response.status == 200:
            poseData = response.read()
            response.close()
            return json.loads(poseData.decode())
        else:
            return UnexpectedResponse(response)        
        pass
