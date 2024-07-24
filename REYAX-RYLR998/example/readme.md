# REYAX RYLR998 Example
I'm providing a simple example script that can be used as a demonstration of the [reyax.py](../reyax.py) module in action.

## systemA
[The systemA folder](./systemA/) contains the source code for the microcontroller in this example that will be serving primarily as a receiver. System A boots up, sets up an SSD-1306 OLED display, the RYLR998 class, confirms it is connected, shows a RYLR998 configuration screen, and then proceeds to continuously listen for and display received messages.

Showing the RYLR998 configuration page before proceeding to listen for messages:
![config](https://i.imgur.com/jRl8427.jpeg)

Displaying a received message:
![msg](https://i.imgur.com/xDJv3wE.jpeg)

## systemB
[The systemB folder](./systemB/) contains the source code for the microcontroller in this example that will be serving primarily as a transmitter. System B boots up, sets up the RYLR998 class, prints its configurations, and continues to transmit a random integer every 6 seconds.