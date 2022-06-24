# robotica

This project was created with the help of Electrical engineering, Mechanical engineering and Software engineering as a project for the fourth semester of the second year at NHL Stenden.

## Students whom worked on this project:

### Software engineering:
Daniël, Wietze, Luuk, Chris

### Electrical engineering:
Rob, Robbin

### Mechanical engineering:
Jolanda, Anne Frans, Jens, Durk, Klaas

## Usage
Executing `python robot.py -h` will return the current available arguments to run the program.

```
usage: robot.py [-h] -cam CAMERA

optional arguments:
  -h, --help            show this help message and exit
  -cam CAMERA, --camera CAMERA
                        Enter 'pi' for Raspberry Pi cam,
  -flag 1,2,3 
            1 to detect cookies, 2 to detect moving object and hunt 3 to go up the parcour with black line in autonomous mode      
   -bt
      Runs the bluetooth connection between the controller and Pi
```

Run `python(3) robot.py -cam pi` to start the program using the Pi camera, or run

## Additional information:

Upon receiving false information in regards to the competition, flag 3 can be subjected to discussion or disqualification.
Reason for this is the lack of understanding of the definition "autonoom" from the organisation and referee(s). Flag 3 works, but should not be implemented or implemented _only_ if the organisation and referee(s) understand what the definition "autonoom" is.
