from dataclasses import dataclass
from typing import Final

@dataclass(frozen=True, slots=True)
class UnitDef:

    dimension: str
    scale: float
    offset: float = 0.0

    def __post_init__(self) -> None:
        if self.scale <= 0:
            raise ValueError(f"scale must be positive, got {self.scale}")

#Currently implemented units.

UNITS: Final[dict[str, UnitDef]] = { # --- LENGTH ----
        "meters": UnitDef(dimension = "LENGTH", scale = 1.0),
        "km":     UnitDef(dimension = "LENGTH", scale = 1000.0),
        "feet":   UnitDef(dimension = "LENGTH", scale = 0.3048),
        "miles":  UnitDef(dimension = "LENGTH", scale = 1609.344),
        "nautical_miles": UnitDef(dimension = "LENGTH", scale = 1852.0),
         # --- MASS ---
        "kg": UnitDef(dimension = "MASS", scale = 1.0),
        "g":  UnitDef(dimension = "MASS", scale = 0.001),
         # --- TEMPERATURE ---
         #kelvin does not require to assign offset, since 0 is the default. Done for consistency with other temps
         "kelvin": UnitDef(dimension = "TEMPERATURE", scale = 1.0, offset = 0.0),
         "celsius": UnitDef(dimension = "TEMPERATURE", scale = 1.0, offset = 273.15),
         "fahrenheit": UnitDef(dimension = "TEMPERATURE", scale = 5/9, offset = (5/9)*459.67) 
        }

BASE_UNITS: Final[dict[str, str]] = {
        "LENGTH": "meters",
        "MASS": "kg",
        "TEMPERATURE": "kelvin"
        }


