import sys
import time

from albatros import Copter
from albatros.enums import CopterFlightModes
from albatros.nav import PositionGPS

copter = Copter()

copter.wait_gps_fix()
copter.set_mode(CopterFlightModes.GUIDED)
while not copter.arm():
    print("waiting ARM")

if not copter.takeoff(alt_m=40):
    print("Unable to takeoff copter, aborting.")
    sys.exit(1)

while (current_altitude := copter.get_corrected_position().alt_m) < 20:
    print(f"Altitude: {current_altitude} m")
    time.sleep(1)

POSITIONS = [
    (-35.36138540, 149.16356964),
    (-35.36187039, 149.16695690),
    (-35.36334645, 149.16685347),
]

for lat, lon in POSITIONS:
    print(f"Flying to point {lat}, {lon}")
    target = PositionGPS(lat, lon, 20)
    copter.fly_to_gps_position(target.lat, target.lon, target.alt_m)
    while True:
        current_position = copter.get_corrected_position()
        if target.distance_to_point(current_position) < 5.0:
            break
        time.sleep(0.5)


if not copter.land():
    print("Unable to land copter, aborting.")
    sys.exit(1)

print("Landing drone")
while (current_altitude := copter.get_corrected_position().alt_m) > 2:
    print(f"Altitude: {current_altitude} m")
    time.sleep(1)