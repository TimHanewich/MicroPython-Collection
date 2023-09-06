import time

class NMEAParser:

    def __init__(self) -> None:

        # utc time
        self.utc_hours:int = 0
        self.utc_minutes:int = 0
        self.utc_seconds:float = 0

        # From GPGGA
        self.position_last_updated_ticks_ms:int = 0
        self.latitude:float = 0.0
        self.longitude:float = 0.0
        self.satellites:int = 0
        self.altitude:float = 0.0 # altitude above sea level, in meters
        self.HDOP:float = 0.0 # Horizontal Dilution of Precision. Measures quality (accuracy) of the GPS fix. Lower values are more accurate.

        # from GPRMC
        self.speed_last_updated_ticks_ms:int = 0
        self.speed_knots:float = 0.0

    @property
    def speed_mph(self) -> float:
        return self.speed_knots * 1.15078


    def feed(self, data:str) -> None:
        if data != None:

            # get GPGGA line
            GPGGA:str = self._isolate_sentence(data, "GPGGA")
            if GPGGA != None:
                if self._validate_checksum(GPGGA):
                    parts:list[str] = GPGGA.split(",")

                    # UTC time
                    if len(parts) >= 2:
                        if (parts[1] != ""):
                            self.utc_hours = int(parts[1][0:2])
                            self.utc_minutes = int(parts[1][2:4])
                            self.utc_seconds = float(parts[1][4:])

                    # Latitude & longitude
                    if len(parts) >= 6:

                        # lat and long
                        if parts[2] != "" and parts[3] != "" and parts[4] != "" and parts[5] != "":

                            # latitude
                            lat_s:str = parts[2][0:2]
                            lat_d:float = float(parts[2][2:])
                            self.latitude = float(lat_s + "." + str(lat_d / 60.0).replace("0.", ""))
                            if parts[3].lower() == "s":
                                self.latitude = self.latitude * -1
                            
                            # longitude
                            lon_s:str = parts[4][0:3]
                            lon_d:float = float(parts[4][3:])
                            self.longitude = float(lon_s + "." + str(lon_d / 60.0).replace("0.", ""))
                            if parts[5].lower() == "w":
                                self.longitude = self.longitude * -1

                            # update last received time
                            self.position_last_updated_ticks_ms = time.ticks_ms()

                        # number of GPS satellites
                        if parts[7] != "":
                            self.satellites = int(parts[7])

                        # HDOP (Horizontal Dilution of Precision)
                        if parts[8] != "":
                            self.HDOP = float(parts[8])

                        # altitude above sea level, in meters
                        if parts[9] != "":
                            self.altitude = float(parts[9])

                            
                
            # get GPRMC line
            GPRMC:str = self._isolate_sentence(data, "GPRMC")
            if GPRMC != None:
                if self._validate_checksum(GPRMC):
                    parts:list[str] = GPRMC.split(",")

                    # speed, knots
                    if len(parts) >= 8:
                        if parts[7] != "":
                            self.speed_knots = float(parts[7])

                            # update last received time
                            self.speed_last_updated_ticks_ms = time.ticks_ms()

    def _validate_checksum(self, line:str) -> bool:

        loc1 = line.find("$")
        loc2 = line.find("*")
        if loc1 == -1 or loc2 == -1:
            return False
        
        # get checksum value
        cs_value:int = int(line[loc2+1:], 16) # convert to hex (base 16)
        
        # calculate XOR checksum
        mid:str = line[loc1+1:loc2]
        checksum:int = 0
        for char in mid:
            int_representation:int = ord(char)
            checksum = checksum ^ int_representation # XOR operation, carried through to each character in the sentence

        return checksum == cs_value

    def _isolate_sentence(self, full:str, sentence_type:str) -> str:
        
        # find start
        loc1 = full.find("$" + sentence_type)
        if loc1 == -1:
            return None
        
        # find end
        loc2 = full.find("\n", loc1 + 1)
        if loc2 == -1:
            loc2 = 99999
        
        return full[loc1:loc2]
