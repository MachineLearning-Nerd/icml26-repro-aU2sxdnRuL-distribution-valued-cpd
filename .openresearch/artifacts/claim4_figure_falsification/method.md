# Method

The verifier reads the PNG directly from the hash-pinned arXiv archive. It isolates the two plot axes, calibrates F1 from internal 0.2 and 0.8 gridlines and ARL1 from the 10 and 100 gridlines, then erodes the red mask with a 9-by-9 structuring element. Filled IDD diamonds survive; same-color outlined NEWMA triangles and thin connecting lines do not. Orange outline squares locate Hotelling F1 points. The raw pixel positions and converted values are written to CSV.

The independent check uses a separate column-span algorithm, requires at least four independently recovered operating points, and verifies every independently extracted delay exceeds 2. The negative control deliberately treats the labelled logarithmic ARL1 axis as linear; it must produce impossible non-positive delays and be rejected.
