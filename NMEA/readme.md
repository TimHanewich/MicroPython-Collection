# NMEA (National Marine Electronics Association) Data Parsing
NMEA (National Marine Electronics Association) data is a standardized format for transmitting various types of data between marine navigation and communication equipment, such as GPS receivers, chartplotters, autopilots, and other marine devices. NMEA data is commonly used in the boating and maritime industry. The most widely used NMEA version is NMEA 0183, although NMEA 2000 is also prevalent for newer marine systems.

NMEA 0183 data is typically transmitted as ASCII text sentences, and each sentence consists of a start delimiter, data fields separated by commas, and an end delimiter (usually a newline character or carriage return). Here's an example of what NMEA 0183 data might look like for a GPS position fix:
```
$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47
```

The components of this NMEA sentence:
- $ is the start delimiter.
- GPGGA is the sentence identifier, indicating that this sentence contains Global Positioning System Fix Data.
- 123519 is the time in UTC (hhmmss.sss format).
- 4807.038 is the latitude in degrees and decimal minutes format (48 degrees 07.038 minutes North).
- N indicates North latitude.
- 01131.000 is the longitude in degrees and decimal minutes format (11 degrees 31.000 minutes East).
- E indicates East longitude.
- 1 is the GPS fix quality (1 = GPS fix, 0 = no fix).
- 08 is the number of satellites being tracked.
- 0.9 is the horizontal dilution of precision (HDOP).
- 545.4,M is the altitude above mean sea level in meters.
- 46.9,M is the height of the geoid (the reference for the altitude) in meters.
- The trailing *47 is a checksum value.

Different NMEA sentences exist for various types of data, such as GPS position, speed, heading, depth, and more. Each sentence has its own unique sentence identifier and structure.

## Sample Data
I captured 250 raw samples (decoded bytes) of NMEA readings from a [NEO-6M](https://www.amazon.com/gp/product/B07P8YMVNT/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1) GPS module, captured in UART, [here](./nmea_data.json).

## Script to Collect NMEA Data
I wrote [this simple script](./collect_nmea_data.py) for collecting NMEA data from a [NEO-6M](https://www.amazon.com/gp/product/B07P8YMVNT/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1) GPS module, captured in UART.