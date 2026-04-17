This collection of measurements consists of 15 .csv files. The number at the end of the filename represents a position on a 5x3 grid starting in the most top left position (the missing numbers were reserved for unused column 0)
So the grids cells would be numbered as such:
 2  3  4  5  6
 11 10 9  8  7
 14 15 16 17 18
Every file contains the same header: N; Pattern; Power; Rx Angle; Tx Angle; a; c; x; y; b
where N is the No. of entry (entries for N < 1000 correspond to a specific pattern from a large codebook, for 1000 =< N < 2000 they correspond to an greedy power maximalization method and for N >= 1000 they correspond to greedy minimalization method),
Pattern is the configuration of the RIS during the measurement (written in hex where binary 1 means that an element was turned on),
Power is the averaged power from trace vector returned by spectrum analyzer,
Rx Angle, Tx Angle, a, c, x, y, b are real space coordinates as drawn in geometry.png (Angles in degrees and distances in mili meters)