# drone

This is the repository for Sam and Paul's Engineering 4 project, which was built during the 2022-23 school year.

## Table of Contents
* [Introduction](#introduction)
* [Design](#design)
* [Code Prototypes](#code-prototypes)
* [CAD](#cad)

[//]: # (Need more here on my part -- probably an entry on final motor control code after dealing w/PID and another one on remote control)

<br>
<br>

## Additional Documentation

[Planning Document](docs/Planning.md)

<br>
<br>

## Introduction

The goal of this project was to create a drone using a Raspberry Pi Pico. The assignment criteria are as follows:
* Survivability: the payload (RPi Pico, sensors, etc) must survive and function post-flight.
* Custom circuit board: breadboards are for prototyping, not for finished products.  Solder headers onto your board so everything is compact but you can add/remove the Pico and other sensors.
* Data collection: your payload must collect data throughout the flight and save that data to the Pico’s onboard storage. Examples: spin rate (MPU6050), altitude (MPL3115A2), location (GPS).
* Data presentation: Show off that data you collected! Plot the data in some way that is meaningful to your project. 

We decided that a drone would be a reasonably challenging way to accomplish this task.

<br>

## Tools Used

CAD - [Onshape](https://www.onshape.com/en/)

Code - [VS Code](https://code.visualstudio.com/)

Wiring Diagram - [Fritzing](https://fritzing.org/)

<br>
<br>

## Design

[//]: # (Talk about how we took inspiration from the Tello drones and what our early design ideas were)

<br>

## CAD

The following CAD sketches were made in [Onshape](https://cvilleschools.onshape.com/documents/ce9d8d739d2d9f15e9173bc0/w/6c76af61bf90a62108bdc466/e/912e9d444323990bdd98e468?renderMode=0&uiState=63b58eecc68e6a59295096d6). 

<img src="docs/images/Arm.png" alt="Arm.png" width="330" height="250"><img src="docs/images/ArmBottom.png" alt="ArmBottom.png" width="330" height="250">

The arm is designed to be lightweight and stable. It accomplishes this with a tapered, hollowed out design. It has a cylinder on the end to fit the motor which acts secondarily as a foot with a small cut-out for wiring to fit through.

<img src="docs/images/Base.png" alt="Base.png" width="330" height="250"><img src="docs/images/Drone.png" alt="Drone.png" width="330" height="250">

The base is sized to fit our circuit board of components, which includes a Raspberry Pi Pico, two motor h-bridges, an accelerometer/gyro, and a PowerBoost. The CAD assembly allowed me to measure between the arms and make sure there was space to fit the LiPo battery underneath. The four holes in the middle of the base allow the battery to be tied to the drone.
