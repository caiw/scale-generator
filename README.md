# Scale Generator: explore partitions of an octave

Scale Generator is a Python program which generates and filters musical scales.

## Scales and partitions

For the purposes of this program we'll consider a scale to be a partition of an octave using semitones, with an octave being a 12-semitone interval.  So Scale Generator represents a scale as a list of intervals, each measured in semitones.

For example, let's look at everyone's first scale, C-major:

> C, D, E, F, G, A, B, C

This the major scale:

> R, M2, M3, M4, M5, M6, M7, R'

in the key of C, where we use R to mean the root note of the scale, and the M-numbers for the intervals musicians will typically be familiar with (M2 is a "major second").

We could also represent the same scale as a list of tones and semitones:

> t, t, s, t, t, t, s

or equivalently, since we're treating a semitone as our smallest interval, as a list of numbers describing the number of semitones in each interval:

> `[2, 2, 1, 2, 2, 2, 1]`

This will be how we manipulate scales in this program:  as lists of numbers describing intervals, where a number describes the width of the interval in semitones, and where the list adds up to `12` (an octave).

## Notation in this document

As you'll have seen, we're now using numbers to mean two things:  numbers of semitones in an interval, and the interval's "name" as conventionally used.  These aren't the same, so for example a major 4th (M4) has `5` semitones; a flat 7th (♭7) has `10` semitones in it.

As an attempt to disambiguate, I'll try to use a `fixed-width typeface` for semitone-measured intervals.  (Unless I'm showing code output, in which case it will always be `fixed-width`, just to make things confusing.  Sorry.)

Basically everything from now on will be related to computer code, and so will used `fixed-with`, and refer to semitone-measured intervals.

## What the program does

The basic things Scale Generator does are:

- Produce a list of all possible scales (partitions of an octave with intervals).
- Present various options to filter the list.
- Display the scales.
- Generate MIDI files of the scales.

At the moment, the filtering options are:

- Filter out scales with long chromatic segments.
- Filter out scales which are cyclic permutations (modes) of other scales.
- Filter out scales which are "subscales" of other scales, found by taking an existing scale and removing some notes.
- Filter out scales which are over a certain length.
- Filter out scales which contain intervals over a certain size.

## How to use it

### Basic use

[Download](https://github.com/caiw/scale-generator/archive/master.zip) and uncompress the code.  The code lives in `scale_generator.py`.  To use it, make sure you have [Python 3](https://www.python.org/downloads/) installed.

Then, in a command line, navigate to where you downloaded it, run

	python3 scale_generator.py
	
This will produce a list of scales, ordered by length, with a bit of extra information.  Each line of the output looks like:

	<timestamp>	[number in list]	[length]	[scale as interval sequence]	[scale as note sequence]
	
For example, the first few lines should be:

	1	1	[12]	['R', 'R']
	2	2	[1, 11]	['R', 'm2', 'R']
	3	2	[2, 10]	['R', 'M2', 'R']
	...
	1361	7	[2, 2, 1, 2, 2, 2, 1]	['R', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'R']
	...
	
So on that 1361st line, you'll see the major scale, written both as the interval list `[2, 2, 1, 2, 2, 2, 1]` and the note sequence R, M2, M3, M4, M5, M6, M7, R; just as we had it before.

### Output options

To save the output to a text file, just do as you would ordinarily in your command line:

	python3 scale_generator.py > ~/Desktop/scales.txt
	
To generate MIDI files, specify the path in following command line argument:

	--save_midi+to /path/for/midi/files/
	
For example:

	python3 scale_generator.py --save_midi_to /Users/cai/Desktop/scales/
	
will save MIDI files to a directory called "`scales`" on my Desktop, which I should create in advance.

Files will be named after the scale in the interval-list format, e.g. `scale-[2, 2, 1, 2, 2, 2, 1].mid`.

### Filtering options

The following filtering switches can be used, which will remove entries from the list.  This allows you to alter what you mean by "scale" and "different".

`--filter_modes`
: Every scale can be transformed into different modes, which are cyclic permutations of the same scale.  So if the scale
:>	C, D, E, F, G, A, B
: is the C-major scale, then
:>	A, B, C, D, E, F, G
: is also the C-major scale, but starting on the 6th note.  This particular mode is known as the Aeolian or VI mode.
: You might, as a musician, not consider these scales to be "different", and so using this switch will only show one out of each of the modes of a scale.

`--filter_chromatic_triplets`
: The chromatic scale is the one with all the notes; twelve semitones. In our case that's `[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]`.
: When you hear several semitones in a row, it sounds chromatic.  It can sound like a scale with a chromatic segment inserted into it.
: For this reason it's possible to filter out scales which have three or more chromatic notes in sequence.  This is the same as filtering out sequences of intervals which have `[1, 1]` in the list.  This also includes lists which both begin and end with `1`, which would have a chromatic triplet if played in a different mode, or over two octaves.
: Use this switch to exclude such scales.

`--filter_subscales`
: If I play a scale, and then play it again but just miss out some of the notes, is that really a new scale?
: If you don't think so, use this switch.

`--max_interval N`
: If my scale has a two notes separated by a perfect 5th, or a full octave, it doesn't necessarily sound like a scale.  You can specify the largest interval of `N` semitones permitted between two consecutive notes using this.
: For example, `-max_interval 4` means you won't get anything larger than a major third in your scale.

`--min_length N`
: This is another way to achieve something similar. If your scale only has two notes in it, it doesn't sound very scale-like.
: For example, `-min_length 6` will give you only scales with at least 6 notes in them.

## Notes about filtering

### See what's filtered

You can use `--verbose_filtering` to log what's being filtered out.

### Filter ordering matters!

For example, _just_ use `--filter_subscales`, and you get only one scale:

> `[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]`

since every scale is a subscale of the chromatic scale.

But using `--filter_subscales` _and_ `--filter_chomatic_triplets` gives you 33 scales.

This only works because we filter chromatic triplets before we filter subscales.  By filtering chromatic triplets first, the `[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]` scale is removed, and so it doesn't consume every other scale as a subscale.  If instead we filtered subscales first, we'd get down to `[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]`, and then filter that out as having chromatic triplets, leaving none at all.

So the this program applies its filters is:

1. Chromatic triplets.
2. Subscales.
3. Modes.
4. Maximum interval.
5. Minimum length.

(This ordering happens internally, it doesn't matter what order you give the switches in.)

## Acknowledgements and disclaimers

- [Mark Wingfield](http://markwingfield.com) was interested in the problem musically, and asked the question.
- [Cai Wingfield](http://caiwingfield.net) was interested in the problem mathematically, and wrote the code.
- The code is provided as-is, and the source is open.  It's not elegantly written, and shouldn't be used as inspiration for how to write good code.  But it works, and it gives an answer to the question, so it's worth something.
- The program uses the open-source [midiutil library](https://code.google.com/archive/p/midiutil/) to generate MIDI files from Python.
- There is also another site I found which lists all scales, William Zeitler's [allthescales.org](http://allthescales.org). This project isn't affiliated with, inspired by, or created in reference to that project.  This was just an idea we came up with independently, and wanted to try out. I don't want to step on anyone's toes. Hopefully, by "showing our working", this provides a small additional amount of utility for those interested.