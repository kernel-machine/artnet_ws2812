
### HOW TO RUN WITH DOCKER (Docker)
    docker compose up

### HOW TO RUN MANUALLY
       pip install -r requirements.txt
       python main.py
### HOW TO USE
The software uses the UDP port 6454 for ArtNet.
Editing the file default.env is possible to change:
- The number of leds
- The size of the segment
- ArtNet universe.
#### DMX channels
- 1 Dimmer
- 2 Strobe
- 3 Red (segment 1)
- 4 Green (Segment 1)
- 5 Blue (Segment 1)
- 6 ...
 - 7  ...
- N-2 Red (segment 1)
- N-1 Green (Segment 1)
- N Blue (Segment 1)
### HOW TO WIRE
GPIO used is 21
