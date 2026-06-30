"""

Unyt is a simple unit conversion utility. It uses affine transformations and a canonical unit approach to convert
between units. 

For each dimension, a canonical unit is chosen, and two affine transformations are performed to convert from a
start_unit to a dest_unit. A concrete example:

    LENGHT -> Meters as canonical unit

    Feet to Kilometers: Feet -> Meters --> Kilometers

"""

import typer

from typing import Annotated
from dataclasses import dataclass

from rich import print
from rich.console import Console
from rich.table import Table

app = typer.Typer()
console = Console()

#Base units definitions. As reference, and used for CLI options

BASE_UNITS = {
        "LENGTH": "meters",
        "MASS": "kg",
        "TEMPERATURE": "kelvin"
        }

#Unit definitions

@dataclass(frozen=True)
class UnitDef:

    dimension: str
    scale: float
    offset: float = 0.0

#Currently implemented unit.

UNITS = { # --- LENGTH ----
        "meters": UnitDef(dimension = "LENGTH", scale = 1.0),
        "km":     UnitDef(dimension = "LENGTH", scale = 1000.0),
        "feet":   UnitDef(dimension = "LENGTH", scale = 0.3048),
        "miles":  UnitDef(dimension = "LENGTH", scale = 1609.344),
        "nautical_miles": UnitDef(dimension = "LENGTH", scale = 1852),
         # --- MASS ---
        "kg": UnitDef(dimension = "MASS", scale = 1.0),
        "g":  UnitDef(dimension = "MASS", scale = 0.001),
         # --- TEMPERATURE ---
         #kelvin does not require to assign offset, since 0 is the default. Done for consistency with other temps
         "kelvin": UnitDef(dimension = "TEMPERATURE", scale = 1.0, offset = 0.0),
         "celsius": UnitDef(dimension = "TEMPERATURE", scale = 1.0, offset = 273.15),
         "fahrenheit": UnitDef(dimension = "TEMPERATURE", scale = 5/9, offset = (5/9)*459.67) 
        }

# CLI commands

@app.command()
def list_units(dimension: Annotated[str, typer.Option(help="Shows units only from the given dimension")] = ""):
    """
    Lists currently available units
    """

    table = Table("Unit name", "Dimension", show_lines = True)

    if dimension == "":

        for unit in UNITS:
            table.add_row(unit, UNITS[unit].dimension)
    else:

        if dimension.upper() not in BASE_UNITS:
            raise ValueError("Dimension not supported!")
        for unit in UNITS:
            if UNITS[unit].dimension == dimension.upper(): table.add_row(unit, UNITS[unit].dimension)

    console.print(table)

@app.command()
def convert(start_unit: Annotated[str, typer.Argument(help="Unit to convert from")],
            dest_unit: Annotated[str, typer.Argument(help="Unit to convert to")],
            value: Annotated[float, typer.Argument(help="Numerical value to convert")]) -> int:

    """
    Performs a units conversion

    """

    start_unit = start_unit.lower()
    dest_unit  = dest_unit.lower()

    #check if supported
    if not start_unit in UNITS or not dest_unit in UNITS:
        print("[bold red]Unit not supported![/bold red]")
        raise typer.Exit(code=1)
    #check if dimensions match
    if not UNITS[start_unit].dimension == UNITS[dest_unit].dimension:
        print("[bold red]Requested units do not share dimensions![/bold red]")
        raise typer.Exit(code=1)
    #conversion: start_unit --> base
    base_unit_measure: float = UNITS[start_unit].scale*value + UNITS[start_unit].offset
    #conversion: base --> dest_unit
    dest_unit_measure: float = (1/UNITS[dest_unit].scale)*base_unit_measure - UNITS[dest_unit].offset/UNITS[dest_unit].scale

    print(f'[bold]{value} {start_unit}[/bold] equals [bold]{dest_unit_measure:.6f} {dest_unit}[/bold]')
    return



if __name__ == "__main__":
    app()
