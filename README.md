Shadowtime
==========

Shadowtime is a python module that can calculate where an object on earth will cast its shadow.

The program that can be used for calculating shadow analemmas or to calculate
and plot the expected annual amount of shadow flicker that can be 
expected in the vicinity of a wind turbine of a certain size given the
latitude.

Many governements require that such a computaion is done and that an entrepreneur wanting to raise a turbine
shows that a certain threashold number of hours isn't exceeded for the houses in the vicinity of the wind turbine.

## Installation
Very simple. Just clone the repository: 

    git clone https://github.com/davidosterberg/shadowtime.git

## Usage

The library is called shadowtime.py. There are a few examples in the examples directory. To execute these you go

cd ./examples
env PYTHONPATH=.. python2 sundial.py

## Modeling assumptions for the shadow flicker example

1. The wind turbine is modeled as a solid cylinder.
2. Earth is assumed to move in a circular orbit around the sun.
3. Earth axial tilt is a fixed number and that the earth surface is a perfect sphere. 
4. No local topography is accounted for. Earth is modeled as a perfect sphere. 
5. The sun is assumed to always shine. 

Never-the-less I don't see why these assumptions wouldn't bee sufficient for many simple cases. For more complicated
cases there exists commercial codes (e.g., WindPro) that can also output detailed reports.  

## Disclaimer
I am not at all an expert on this field. So no guarantees :).

