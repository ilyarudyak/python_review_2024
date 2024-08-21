"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """
    DESIGNATION = 'pdes'
    NAME = 'name'
    HAZARDOUS = 'pha'
    DIAMETER = 'diameter'

    # TODO: How can you, and should you, change the arguments to this constructor?
    # If you make changes, be sure to update the comments in this file.
    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        # TODO: Assign information from the arguments passed to the constructor
        # onto attributes named `designation`, `name`, `diameter`, and `hazardous`.
        # You should coerce these values to their appropriate data type and
        # handle any edge cases, such as a empty name being represented by `None`
        # and a missing diameter being represented by `float('nan')`.
        self.designation = info.get(self.DESIGNATION) if info.get(self.DESIGNATION) else None
        self.name = info.get(self.NAME) if info.get(self.NAME) else None
        self.diameter = self._convert_to_float(info.get(self.DIAMETER)) if info.get(self.DIAMETER) else float('nan')
        self.hazardous = self._convert_to_bool(info.get(self.HAZARDOUS)) if info.get(self.HAZARDOUS) else None

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    def _convert_to_float(self, value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return float('nan')

    def _convert_to_bool(self, value):
        return value == 'Y'
    
    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        # TODO: Use self.designation and self.name to build a fullname for this object.
        return f'{self.designation} ({self.name})' if self.name else f'{self.designation}'

    def __str__(self):
        """Return `str(self)`."""
        # TODO: Use this object's attributes to return a human-readable string representation.
        # The project instructions include one possibility. Peek at the __repr__
        # method for examples of advanced string formatting.
        if self.hazardous is None:
            hazardous_str = 'unknown if hazardous'
        else:
            hazardous_str = 'hazardous' if self.hazardous else 'not hazardous'
        diameter_str = f"{self.diameter:.3f}" if self.diameter is not None else "unknown diameter"
        return f"NEO {self.fullname} has a diameter of {diameter_str} km and is {hazardous_str}"

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        diameter = self.diameter if self.diameter is not None else float('nan')
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={diameter}, hazardous={self.hazardous!r})"


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """
    DESIGNATION = 'des'
    TIME = 'cd'
    DISTANCE = 'dist'
    VELOCITY = 'v_rel'
    # TODO: How can you, and should you, change the arguments to this constructor?
    # If you make changes, be sure to update the comments in this file.
    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        # TODO: Assign information from the arguments passed to the constructor
        # onto attributes named `_designation`, `time`, `distance`, and `velocity`.
        # You should coerce these values to their appropriate data type and handle any edge cases.
        # The `cd_to_datetime` function will be useful.
        self._designation = info.get(self.DESIGNATION) if info.get(self.DESIGNATION) else None
        # TODO: Use the cd_to_datetime function for this attribute.
        self.time = cd_to_datetime(info.get(self.TIME)) if info.get(self.TIME) else None  
        self.distance = self._convert_to_float(info.get(self.DISTANCE)) if info.get(self.DISTANCE) else float('nan')
        self.velocity = self._convert_to_float(info.get(self.VELOCITY)) if info.get(self.VELOCITY) else float('nan')

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

    def _convert_to_float(self, value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return float('nan')

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        # TODO: Use this object's `.time` attribute and the `datetime_to_str` function to
        # build a formatted representation of the approach time.
        # TODO: Use self.designation and self.name to build a fullname for this object.
        return datetime_to_str(self.time) if self.time else None

    def __str__(self):
        """Return `str(self)`."""
        # TODO: Use this object's attributes to return a human-readable string representation.
        # The project instructions include one possibility. Peek at the __repr__
        # method for examples of advanced string formatting.
        full_name = self.neo.fullname if self.neo else 'unknown NEO'
        time_s = self.time_str if self.time else 'unknown time'
        distance_str = f"{self.distance:.2f}" if self.distance is not None else "unknown distance"
        velocity_str = f"{self.velocity:.2f}" if self.velocity is not None else "unknown velocity"
        # On 1911-10-15 19:16, '1036 (Ganymed)' approaches Earth at a distance of 0.38 au and a velocity of 17.09 km/s.
        return f"On {time_s}, '{full_name}' approaches Earth at a distance of {distance_str} au and a velocity of {velocity_str} km/s."   

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        distance = self.distance if self.distance is not None else float('nan')
        velocity = self.velocity if self.velocity is not None else float('nan')
        return f"CloseApproach(time={self.time_str!r}, distance={distance}, " \
               f"velocity={velocity}, neo={self.neo!r})"
