# Method

The verifier reads the PNG directly from the hash-pinned arXiv archive. It isolates the two plot axes, calibrates F1 from the 0 and 1 gridlines and ARL1 from the 10 and 100 gridlines, then locates the filled red IDD diamonds by color and local fill density. Orange outline squares independently locate Hotelling F1 points. The raw pixel positions and converted values are written to CSV.

The independent check requires at least five filled IDD markers and verifies every extracted delay exceeds 2. The negative control deliberately treats the labelled logarithmic ARL1 axis as linear; it must produce impossible non-positive delays and be rejected.
