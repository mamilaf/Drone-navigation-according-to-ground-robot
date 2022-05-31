# Drone-navigation-according-to-ground-robot
Use-case:
The objective is to make the Tello drone move according to the
coordinates given by the Jetbot ground robot.
Jetbot moves into a specific coordinate and after reaching the end
point it requests tello to navigate on the same coordinate. The jetbot
communicates with the tello on the current state of the bot and only
when the jetbot stops and send the request the tello starts the
navigation to the end location of the bot. Once the tello reaches the
goal it can send an acknowledgement to the jetbot. The jetbot and the
tello are initially at the same location(x and y). Currently we are
focusing on navigating a known environment and does not include
obstacle avoidance for the jetbot.

System:
Jetbot and Tello drone
ROS2 environment
Odometry sensor for Jetbot and Tello (addition)
The navigation data is obtained from the jetbot and the initial and final
position is sent to the tello. The calculation of the shortest path is
done at the drone end. The jetbot decides and communicates when
the tello needs to take off and start the navigation. Jetbot acts as the
master and tello the slave.

Background:
We first aim to complete the implementation on the gazebo simulation
and then implement it on the bot in the real environment.
Expected challenges and wishes to learn:
Challenges expected in converting the position data obtained from
jetbot and finding the end goal position for the tello. With this project it
would be needed to learn to use the path planning algorithm with
Tello. We are not that familiar with working with the Jetbot and
Gazebo simulation.

Expected challenges and wishes to learn:
Challenges expected in converting the position data obtained from
jetbot and finding the end goal position for the tello. With this project it
would be needed to learn to use the path planning algorithm with
Tello. We are not that familiar with working with the Jetbot and
Gazebo simulation.

Team roles:
There are two team members and the work is splitted. Marco would
be working on the algorithm to find the shortest path and
implementing the same on the Tello drone end accepting data from
the jetbot. Rohin will implement the same on the simulation and also
work on navigating and sending the data from the jetbot.

Description of final experiment or demonstration:
We expect to start both the tello and jetbot from the same position.
The jetbot first navigates to a particular location and sends a request
to the tello to follow, taking the shortest path. The tello then navigates
to that location and sends the acknowledgement that it has arrived.
We expect to demonstrate using simulation and also try to implement
it on the actual jetbot and tello.

Implementation

The implementation was done in the simulation and we had to split it into multiple steps as we couldn't spawn and use turtlebot and tello in the same simulation. In each step we saved the values necessary for the next step into a csv file and then later used them by reading these files whenever necessary.

Part -I 

The jetbot was made to traverse in a predefined path. We sent the command to move the bot forward for some period of time and then turn and move again in another direction for some more time. We also captured the initial and final bot positions from the odometry data subscribed. These values were then copied to a csv file to be used in the next part.

Part -II

In the second part we open the csv file and read the coordinates shared from the previous section. We extract the initial x and y and also the final x and y coordinates. This is fed as input to the A star algorithm. The algorithm as described above in the execution finds the shortest path to the goal and returns the coordinates. These coordinates are reversed and saved to a csv file and will be used in the next part to move the tello.

Part -III

In this last part we use the data collected in the first and second section to navigate the tello to the goal position. We read the initial and final coordinates which also include the orientation and we also read the shortest path stored. From the list of path points, we take the next step to traverse towards. 

First we align the tello to match the orientation of the points in the path obtained. A slight error margin is considered in all cases. And once the orientation is done we then compare the x and y position one after the other. After all the alignment is done we expect that the tello has finally traversed to the next step. So we then take the next points from the list and so on.
