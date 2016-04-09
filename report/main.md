# Embedded Software

## Abstract

We use Python3.5 and the Raspbian distribution to control our robot. We chose Python for  the significant body of preexisting software, the ease of development, and its compatibility across platforms.

## Networking

We communicate between Python code and Java code. Because of this, we required network protocols which are common enough to be well supported in both systems. We also require protocols which are fast enough to make our robot responsive to commands from the driver. We choose to use a combination of Protobuf and Websockets to communicate with the robot.

### Protobuf

Protocol Buffer, known as Protobuf for short, is a data format created by Google. This format produces efficiently packed messages which are quick to parse. Efficient Protocol buffer construction and parsing language bindings have been created. Many, including the Python and Java libraries, have C backends with first class support from Google. The Protobuf format contains many features which we do not need, but it does contain one that is invaluable to us. We can create and share a file that describes our communication. This mostly eliminates bugs communication between the Java basestation and the Python robot which might otherwise cost us valuable debugging time.

Our robot uses two kinds of Protobuf messages; one for the robot to send to the basestation and one for the basestation to send to the robot. The message to the robot exposes the different pieces of hardware. Each attribute is a specific piece of hardware. Each class of hardware is described as a Protobuf submessage. To expose higher level commands we use a list of a unions which may contain more complex procedures. The robot sends sensor data to the basestation in a similar manner. We only send update. Thanks to the protobuf format, any message that is not an update does not require any information to be sent. This reduces network stress and parsing time. We always send some kind of packet, even if it is empty, as a heartbeat.

### Websockets

We decided to use TCP sockets for communication over UDP because they are easier to develop with. TCP is a streaming protocol but Protobuf is not a streaming format. We chose Websockets to frame our messages. Like Protobuf, Websockets offer many features which we do not use. The main advantage of Websockets is its popularity. Like Protobuf this lifts implementation details from our code, saving us development time.

## Control

We encompass all the code that exists between the network messages and the robot hardware exists in a class aptly called Controller. This contains the main function that starts threads, connects sockets, and starts the event loop. It then contains all the subroutines that run every heartbeat, in response the basestation messages, and run periodic calculations.

### Threading

### Asyncio

## Hardware interface

Software that properly interfaces with correctly hardware is often difficult to always find. Hardware for the RaspberryPi is no exception. We acquired the software libraries we did after much research and debugging. In some cases, patching was required to make the library function correctly.

We handle configuration of the hardware in a single class called 'Robot'. The attributes each represent a specific piece of hardware. Each attribute is a class that is an abstraction of a type of hardware initialized with things like ports, channels, or scaling constants. We maintain these classes in a separate module to try to reign in the inconsistencies in software libraries. This class looks a lot like the Protobuf control file.

### Raspbian

We use the most commonly used Linux distribution for the RaspberryPi, Raspbian. We use this because it comes with a kernel that is specifically created to work with the RaspberryPi. Without Raspbian's extensions to the Linux kernel, we would not be able to correctly interface with the RaspberryPi's hardware.

### Wiringpi

### Spidev

### Mastro
