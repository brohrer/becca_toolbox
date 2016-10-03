## Becca tools

The `becca_toolbox` repository is for some utilities and tools that are either 
a little too bulky or too fragile to justify bundling with the
core becca repo. 

### `ffmpeg_tools.py`

A convenience wrapper for building sequences of still images into
video using the [ffmpeg library](https://ffmpeg.org/). For an example
of how to bake it into a world and automatically create movies from
runs, check out `becca_world_chase_ball`.
