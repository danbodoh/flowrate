# Flow Rate Gauge for Acaia Scales

This simple Python app features a gauge 
showing the flow rate in grams/second (or ounces/second),
as well as the weight and the scale timer.  It is designed for
use with Acaia scales, such as the Pyxis, and manual lever 
espresso machines, such as the Cafelat Robot.  I am using it to
experiment with flow-controlled espresso pulls.  I attempt to keep
a constant flow (1.3-1.5 g/s) by reducing the pressure from the 
initial 6-9 bar, until I reach the target weight (usually 40g from 18g in).
This type of pull ignores time and focuses on flow rate, pressure and yield.

Upon launching flowrate.py it continuously looks for an Acaia scale
and connects to the first one found.  When connected, the status line
at the bottom changes from "Unconnected" to show the battery level.

Tested on Ubuntu Linux 20.04 and Raspbian GNU/Linux 10 (buster).

## Dependencies

### Pyacaia

Requires [Pyacaia 0.4.0](http://github.com/lucapinello/pyacaia), 
which includes support for the Acaia Pyxis and additional API that I contributed.

`pip3 install pyacaia`

### tk_tools

The Gauge is implemented with the tk_tools Gauge.

`pip3 install tk_tools`

### engineering_notation

The engineering_notation library is also a dependency of tk_tools.

`pip3 install engineering_notation`
