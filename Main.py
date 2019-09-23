"""
A Robot communicating with Microsoft Robotics Developer Studio 4 via the Lokarria HTTP interface.
The robot will follow a given path using a Pure Pursuit algorithm implementation.

Author: William Larsson (oi17wln@cs.umu.se)
         2019-09-23
"""

from Robot import *
from Path import *
from ShowPath import *
from math import sqrt, atan2
import time


def convert_wcs_to_rcs(start, goal, heading):
    """
    Converts the current goal point position to a new position relative to the
    current position and heading angle
    :param start: current position in world coordinate space
    :param goal: goal position in world coordinate space
    :param heading: angle relative to the x-axis
    :return: Array with goal position as robot coordinate space
    """
    x_pos = (goal['X'] - start['X'])*cos(heading) + (goal['Y'] - start['Y'])*sin(heading)
    y_pos = -(goal['X'] - start['X'])*sin(heading) + (goal['Y'] - start['Y'])*cos(heading)

    return [{'X': x_pos, 'Y': y_pos}]


def distance_to_gp(goal_rcs):
    """
    The current distance from the robot to the goal point, in meters
    :param goal_rcs: current goal point
    :param robot_pos: current robot position (in wcs)
    :return: the distance between the two parameters
    """
    return sqrt(goal_rcs['Y']**2 + goal_rcs['X']**2)


def gp_found(p, robot, distance):
    """
    Finds the next goal point on the path
    :param p: The full path with all possible points
    :param robot: The robot following the path
    :param distance: The minimum distance between the robot and the goal point
    :return: Returns true if the point on the path is to be a goal point.
    """
    delta_x = p['X'] - robot.getPosition()['X']
    delta_y = p['Y'] - robot.getPosition()['Y']

    if sqrt(delta_y ** 2 + delta_x ** 2) > distance:
        return True
    else:
        return False


def calc_turn_rate(look_ahead, rcs, dist):
    """
    calculate the turn rate the robot needs to have to navigate to the next goal point
    :param look_ahead: Look ahead distance
    :param rcs: The goal point coordinates given in robot coordinate space
    :param dist: Distance between the robot and the goal point
    :return: How much to turn the robot, in radians
    """
    return look_ahead * ((2 * rcs[0]['Y']) / dist ** 2)  # distance * (2y/L^2)


if __name__ == "__main__":
    p = Path("Path-around-table.json")
    path = p.getPath()
    sp = ShowPath(path)

    look_ahead = 0.7
    robot = Robot("localhost", "50000")

    for p in path:
        if not gp_found(p, robot, look_ahead):
            continue
        else:
            sp.update(robot.getPosition(), p)
            rcs = convert_wcs_to_rcs(robot.getPosition(), p, robot.getHeading())
            dist = distance_to_gp(rcs[0])
            turn_rate = calc_turn_rate(look_ahead, rcs, dist)
            robot.setMotion(look_ahead/2, turn_rate)
            time.sleep(0.2)
    robot.setMotion(0, 0)
