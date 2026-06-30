"""

Unyt is a simple unit conversion utility. It uses affine transformations and a canonical unit approach to convert
between units. 

For each dimension, a canonical unit is chosen, and two affine transformations are performed to convert from a
start_unit to a dest_unit. A concrete example:

    LENGTH -> Meters as canonical unit

    Feet to Kilometers: Feet -> Meters --> Kilometers

"""
from typing import Annotated

import typer

from rich import print
from rich.console import Console
from rich.table import Table

from unyt.units import UNITS, BASE_UNITS

app = typer.Typer()
console = Console()

# Affine functions

def affine_transformation(value: float, scale: float, offset: float) -> float:
    return scale*value + offset


def inverse_affine_transformation(value: float, scale: float, offset: float) -> float:
    return (1/scale)*value - offset/scale

# CLI commands

@app.command()
def list_units(dimension: Annotated[str, typer.Option(help="Shows units only from the given dimension")] = "") -> None:
    """
    Lists currently available units
    """

    table = Table("Unit name", "Dimension", show_lines = True)

    if dimension == "":

        for unit in UNITS:
            table.add_row(unit, UNITS[unit].dimension)
    else:

        if dimension.upper() not in BASE_UNITS:
            print("[bold red]Dimension not supported![/bold red]")
            raise typer.Exit(code=1)
        for unit in UNITS:
            if UNITS[unit].dimension == dimension.upper(): table.add_row(unit, UNITS[unit].dimension)

    console.print(table)

@app.command()
def convert(start_unit: Annotated[str, typer.Argument(help="Unit to convert from")],
            dest_unit: Annotated[str, typer.Argument(help="Unit to convert to")],
            value: Annotated[float, typer.Argument(help="Numerical value to convert")]) -> None:

    """
    Performs a units conversion

    """

    start_unit = start_unit.lower()
    dest_unit  = dest_unit.lower()

    if start_unit == dest_unit:
        print("[bold red]Same unit conversion![/bold red]")
        raise typer.Exit(code=1)
    #check if supported
    if start_unit not in UNITS or dest_unit not in UNITS:
        print("[bold red]Unit not supported![/bold red]")
        raise typer.Exit(code=1)
    #check if dimensions match
    if UNITS[start_unit].dimension != UNITS[dest_unit].dimension:
        print("[bold red]Requested units do not share dimensions![/bold red]")
        raise typer.Exit(code=1)
    #conversion: start_unit --> base
    base_unit_measure: float = affine_transformation(value, 
                                                     UNITS[start_unit].scale,
                                                     UNITS[start_unit].offset
                                                     )
    #conversion: base --> dest_unit
    dest_unit_measure: float = inverse_affine_transformation(base_unit_measure,
                                                             UNITS[dest_unit].scale,
                                                             UNITS[dest_unit].offset
                                                             )

    print(f'[bold]{value} {start_unit}[/bold] equals [bold]{dest_unit_measure:.6f} {dest_unit}[/bold]')
    return



