# scale-generator

Generate all possible scales with no more than 2 semitones in sequence.
We want to generate some scales.

The scales must cover a single octave, and they must satisfy the requirements:
-   No sequence of three notes can be semitones apart. (Two notes is fine,)

This is equivalent to the following:
-   Construct a sequence of numbers which sum to 12 (the number of semitones in
    an octave, where no two consecutive numbers are 1.
    -   These numbers would correspond to the intervals between consecutive
        notes.
