**Unyt** is a simple CLI unit conversion utility. It uses affine transformations and a canonical unit approach to convert
between units.

Currently, it is far from complete with only a handful of units implemented. I built this mainly as an excuse to dive into
`Typer` and because I enjoy having hand-built tools in my system when possible. 

# Installation

I recommend you use `uv` to build and install this utility:

```bash
git clone https://github.com/OmarOul/unyt.git
cd unyt
uv tool install .
```
# Usage

Unyt comes with (currently) two commands.

1. `unyt list-units`: lists all currently available units. Option `--dimension` let's you pass a dimension
to only show units that belong to it. Example: `unyt list-units --dimension length`

2. `unyt convert start_unit dest_unit value`: converts a `value` expressed in `start_unit` to its corresponding
value when expressed in `dest_unit`

# How it works (some math!)

A conversion between two units can be done via an **affine transformation** or **linear transformation**
if the rule to move between them can be expressed as:

$$
y = ax + b
$$

Where $x$ represents the starting value and $y$ the converted value. Two practical examples:

**Length:**

$$
0.12 \text{ km to m}: \quad y = 1000x + 0 = 1000(0.12) + 0 = 120 \text{ m}
$$

Here $a = 1000$ (the **scale** factor between km and m) and $b = 0$, since length units share a common zero point.

**Temperature:**

$$
12°\text{C to °F}: \quad y = \frac{9}{5}x + 32 = \frac{9}{5}(12) + 32 = 53.6°\text{F}
$$

Here $a = \frac{9}{5}$ and $b = 32$. Temperature systems don't share a common zero, so an **offset** is required to get a correct result.

Notice that with this approach, we can do any conversion if:

1. It can be expressed in linear form.
2. We know the **scale** and **offset** between the two units.

The more immediate drawback is that we would need to store each pair of scale and offset for every possible unit conversion.
To avoid this, we choose a **reference** or **canonical** unit for each dimension, and then store only the scale and offset
that relate each unit to our canonical one. Then, we do two "hops": First from the starting unit to the reference one,
and then to the desired unit. A practical example:

Let's say we have a temperature in Celsius, $T_{C}$ and we want to know its Fahrenheit equivalent, $T_{F}$. We choose
Kelvin as our reference temperature. This means we need to store four parameters:

- $s_{C}$, $o_{C}$: Scale and Offset from Celsius to Kelvin
- $s_{F}$, $o_{F}$: Scale and Offset from Fahrenheit to Kelvin

Then, as a first step, we do our simple affine transformation to transform ºC into K:

$$
T_{K} = s_{C}T_{C} + o_{C}
$$

Now we have our Kelvins and we need to move into ºF. Since we stored the scale and offsets to move from ºF to Kelvin,
we need to invert the ºF -> Kelvin transformation to use the values we have.

$$
T_{K} = s_{F}T_{F} + o_{F} \quad \rightarrow \quad T_{F} = \frac{1}{s_{F}}(T_{K} - o_{F})
$$

And we arrive at our result.


