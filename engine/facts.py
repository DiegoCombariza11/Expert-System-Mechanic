from experta import Fact, Field

class vehicle(Fact):
    """Info about a vehicle."""
    make = Field(str, mandatory=False)
    model = Field(str, mandatory=False)
    year = Field(int, mandatory=False)
    color = Field(str, mandatory=False)
    mileage = Field(int, mandatory=False)
    price = Field(float, mandatory=False)
    fuel_type = Field(str, mandatory=False)  # e.g., 'gasoline', 'diesel', 'electric'
    transmission = Field(str, mandatory=False)  # e.g., 'manual', 'automatic'
    sintoma = Field(str, mandatory=False)  # síntoma del vehículo



