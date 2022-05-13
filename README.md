# robotica

## Usage
Executing `python robot.py -h` will return the current available arguments to run the program.

```
usage: robot.py [-h] -cam CAMERA

optional arguments:
  -h, --help            show this help message and exit
  -cam CAMERA, --camera CAMERA
                        Enter 'pi' for Raspberry Pi cam, 0-9 for regular webcam connection. Defaults to Pi.
```

Run `python robot.py -cam pi` to start the program using the Pi camera, or enter a numerical value to access a USB camera (try 0 or 1).