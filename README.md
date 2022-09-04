# Frame-Cropping
Automatically crop frames from pictures of film.

## V1 Limitations

* does not work if frame contains sufficiently wide black bars; the middle of
  the frame will be treated as a delimiter, and the frame will be sliced off early
* will chop off black bars at top or bottom of frame
