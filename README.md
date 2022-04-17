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
