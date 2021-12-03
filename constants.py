"""
This file is used to store constant values required in the project.
"""
# [4]
# radius of earth in earth units
REFERENCE_VALUE_RADIUS = 1.00
# density of earth in earth units
REFERENCE_VALUE_DENSITY = 1.00
# escape velocity of earth in earth units
REFERENCE_VALUE_VELOCITY = 1.00
# temperature of earth in Kelvin
REFERENCE_VALUE_TEMPERATURE = 288.00
# Weight Exponent for radius
WEIGHT_EXPONENT_RADIUS = 0.57
# Weight Exponent for density
WEIGHT_EXPONENT_DENSITY = 1.07
# Weight Exponent for escape velocity
WEIGHT_EXPONENT_VELOCITY = 0.70
# Weight Exponent for temperature in Kelvin
WEIGHT_EXPONENT_TEMPERATURE = 5.58
# total number of planetary properties used to calculate ESI
NUMBER_OF_PARAMETERS_TO_CALCULATE_ESI = 4

# Earth Constants
# Source https://nssdc.gsfc.nasa.gov/planetary/factsheet/
# Mass in KG
MASS = 5.974 * (10 ** 24)
# Diameter in M
DIAMETER = 12756000
# Density in kg/m^3
DENSITY = 5516
# Gravity in m/s^2
GRAVITY = 9.8
# Escape Velocity in km/s
ESCAPE_VELOCITY = 11.2
# Rotation Period in hours
ROTATION_PERIOD = 23.9
# Length of day in hours
LENGTH_OF_DAY = 24.0
# Distance from Sun in KM
DISTANCE_FROM_SUN = 149.6 * (10 ** 6)
# Surface Pressure in bars
SURFACE_PRESSURE = 1
# Solar Flux in W/m^2
SOLAR_FLUX = 1373
# Gravitational Constant in m^3*kg^-1*s^-2
# Source https://www.physicsforums.com/threads/pressure-at-center-of-planet.66257/
G = 6.674 * (10 ** -11)


