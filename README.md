# ATGM336H_NMEA_ROS2
ROS2 pkg for ATGM336H GPS Module

This pkg contains gps_node which publishes following NMEA protocol topics;
- `/gps/gpgga`: Message from GNGGA String
    | data type |     Data    | Description |
    | --- | --- | --- |
    | float64   | utc_seconds | UTC time status of position <br /> (hours/minutes/seconds/ decimal seconds)|
    | float64   | lat         | Latitude (DDmm.mm) |
    | float64   | lon         | Latitude direction (N = North, S = South) |
    | string    | lat_dir     | Longitude (DDDmm.mm) |
    | string    | lon_dir     | Longitude direction (E = East, W = West) |
    | uint32    | gps_qual    | refer to [Table: GPS Quality Indicators](https://docs.novatel.com/OEM7/Content/Logs/GPGGA.htm?Highlight=GPGGA#GPSQualityIndicators) |
    | uint32    | num_sats    | Number of satellites in use. May be different to the number in view |
    | float32   | hdop        | Horizontal dilution of precision |
    | float32   | alt         | Antenna altitude above/below mean sea level |         
    | string    | altitude_units | Units of antenna altitude (M = metres) |
    | float32   | undulation    | Undulation - the relationship between the geoid and the WGS84 ellipsoid |
    | string    | undulation_units | Units of undulation (M = metres) | 
    | uint32    | diff_age  | Age of correction data (in seconds) <br /> The maximum age reported here is limited to 99 seconds |
    | string    | station_id    | Differential base station ID |
    

- `/gpa/gpgsa`: Message from GPGSA String
    | data type |     Data    | Description |
    | --- | --- | --- |
    | string   | auto_manual_mode | A = Automatic 2D/3D <br /> M = MAnual, forced to operate in 2D or 3D |
    | uint8   | fix_mode         | Mode: 1 = Fix not available <br /> 2 = 2D <br /> 3 = 3D <br />|
    | uint8[]   | sv_ids         | PRN numbers of satellites used in solution (null for unused fields), total of 12 fields <br /> GPS = 1 to 32 <br /> SBAS = 33 to 64 (add 87 for PRN number) <br /> GLO = 65 to 96|
    | float32    | pdop     | Position dilution of precision |
    | float32    | hdop     | Horizontal dilution of precision|
    | float32    | vdop    | Vertical dilution of precision|
    
- `/gpa/gpgsv`: Message from GPGSV String <br />
    - Total number of satellites in view and data about satellites
    -  Because the NMEA sentence is limited to 4 satellites per message, several of these messages may need to be synthesized to get data about all visible

    | data type |     Data    | Description |
    | --- | --- | --- |
    | uint8   | n_msgs | Total number of messages (1-9) |
    | uint8   | msg_number  | Message number (1-9) |
    | uint8   | n_satellites | Total number of satellites in view. <br /> May be different than the number of satellites in use (see also the [GPGGA log](https://docs.novatel.com/OEM7/Content/Logs/GPGGA.htm))|
    | GpgsvSatellite[]    | satellites  <br /> - prn <br /> - elev <br /> - azimuth <br/> - SNR  | `prn:` Satellite PRN number <br /> - GPS = 1 to 32  <br /> - Galileo = 1 to 36  <br /> - BeiDou = 1 to 63  <br />  - NavIC = 1 to 14  <br />  - QZSS = 1 to 10  <br /> - SBAS = 33 to 64 (add 87 for PRN#s)  <br />  - GLONASS = 65 to 96  <br /> `elev:` Elevation, degrees, 90 maximum  <br /> `azimuth:` Azimuth, degrees True, 000 to 359 <br /> `SNR:` SNR (C/No) 00-99 dB, null when not tracking|
    



- `/gpg/gprmc`: Message from GNRMC String
    | data type |     Data    | Description |
    | --- | --- | --- |
    | float64   | utc_seconds |  UTC of position hhmmss.s|
    | float64   | position_status  | Position status (A = data valid, V = data invalid) |
    | float64   | lat         | Latitude (DDmm.mm) |
    | float32    | lon     | Longitude (DDDmm.mm) |
    | string    | lat_dir     | Latitude direction: (N = North, S = South) |
    | string    | lon_dir    | Longitude direction: (E = East, W = West) |
    | float32 | speed | Speed over ground, knots |
    | float32 | track | Track made good, degrees True |
    | string  | date | Date: dd/mm/yy (xxxxxx)|
    | float32 | mag_var |Magnetic variation, degrees <br /> Note that this field is the actual magnetic variation and will always be positive. <br /> The direction of the magnetic variation is always positive. |
    | string  | mag_var_direction | Magnetic variation direction E/W <br /> Easterly variation (E) subtracts from True course. <br /> Westerly variation (W) adds to True course. |
    | string  | mode_indicator | Positioning system mode indicator, see Table: [NMEA Positioning System Mode Indicator](https://docs.novatel.com/OEM7/Content/Logs/GPRMC.htm?Highlight=GPRMC#NMEAPositioningSystemModeIndicator)|


- `/gpg/sentence`: A message representing a single NMEA0183 sentence.


### Install:
    
    sudo apt-get install ros-$ROS_DISTRO-nmea_msgs

    mkdir -p ~/ros2_ws/src
    cd ~/ros2_ws/src
    git clone https://github.com/NDHANA94/ATGM336H_NMEA_ROS2.git
    cd ~/ros2_ws
    colcon build
    

### Execute:
    
    cd ~/ros2_ws
    source install/setup.bash
    ros2 run atgm336h5n3x nmea_node --dev /dev/ttyUSB0
    