"""
 ShowPath plots the path, current robot position and look-ahead point
 Author Ola Ringdahl 2019-09-13
 Updated by William Larsson 2019-09-16 -- now works with my modified Robot.py / Path.py
"""

import matplotlib.pyplot as plt


class ShowPath:
    plt.style.use('seaborn-whitegrid')

    def __init__(self, path):
        """
        Constructor for ShowMap. Creates a figure window and plots the path
        :param path: the path you get from getPath()
        """
        self.fig, self.ax = plt.subplots(1, 1)
        self.lap = []
        x = []
        y = []
        for i in range(len(path)):
            x.append(path[i]['X'])
            y.append(path[i]['Y'])
        self.ax.plot(x, y)  # plot the path
        plt.pause(0.001)

    def update(self, robot_pos, look_ahead_point):
        """
        Update the figure with the current robot position and look-ahead point.
        Call this method after you computed the new look-ahead point
        :param robot_pos: The robot position from getPosition()
        :param look_ahead_point: The look-ahead point as a vector ([x,y])
        """

        # plot the current robot position:
        self.ax.plot(robot_pos['X'], robot_pos['Y'], 'or')
        # plot the current look-ahead point:
        lap, = self.ax.plot(look_ahead_point['X'], look_ahead_point['Y'], 'xg')
        plt.pause(0.001)
        lap.remove()  # only the newest look-ahead point is shown
