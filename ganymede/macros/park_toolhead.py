from kalico import Kalico, gcode_macro
import enum


class Location(enum.Enum):
    front = "FRONT"
    rear = "REAR"


@gcode_macro
def park_toolhead(k: Kalico, location: Location = Location.rear):
    if location == Location.front:
        park_y = k.status.toolhead.axis_minimum.y
    else:
        park_y = k.status.toolhead.axis_maximum.y

    if k.status.toolhead.position.z < k.status.toolhead.axis_maximum.z - 10:
        k.move(dz=10, speed=200)

    k.move(x=k.status.toolhead.axis_maximum.x - 20, y=park_y, speed=200)
