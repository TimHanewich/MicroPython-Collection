# Joysticks
I purchased [these joysticks](https://a.co/d/068GS4Vr) on Amazon. They have a lot of problems! A bias, constantly moving input value when not touched, quickly reaching their fully saturated values with only a small bit of movement, and also not even "saturation" on each axis two directions.

## Solution
By this combination of hardware + software tricks, I managed to get them into a somewhat workable state.

### Hardware Side
1. On the Raspberry Pi Pico, do NOT plug them into `+5v` as it suggests! **Use 3.3v!** This is because the ADC pins on the pico only accept up to 3.3 volts.
2. After you plug it in and have it running for a while while powered on, move the joystick around a lot. It needs to be "broken in" at first to get set up. At first I was seeing crazy biases, but after moving it around, it was more stable and preditable.
3. If you are using a breadboard, be sure you have four good quality wires. I was using bad ones with shorts which was causing me problems until I replaced it, then was seeing more stable values.

### Software Side
I developed the `transform` function of the `joystick` module ([joystick.py](./joysticks.py) to use software transformation to solve three things):
1. **Offset**: when at rest, each axis will "rest" at a non-zero input value (not right in the middle). e.g. The input may be -8% or +4%. 
2. **Deadzon**: when at rest, not touched by a user, they will jump around a few percent in either direction.
3. **Ceiling**: I noticed one direction of an axis will saturate at 100%. But the other won't, it'll only get to 87% for example.

The `transform` function accounts and adjust for all three of those issues mathematically. Note that it *does not* solve for the values being very quickly saturated in either direction with only a small degree of movement - that is a *hardware* issue. So if you do choose to use these joysticks with these software corrections, note that **you will have to be very gentle on the sticks to get fine-grain input, otherwise it will quickly shoot to 100% in either direction!**

## Set Up
Once you have your joystick wired up, here is how I recommend calibrating it to work best:

First, set it up with no offset, no deadzone, and max ceiling (`1.0` = 100%):

```py
transformed1:float = transform(val1_fr, 0.0, 0.0, 0.0)
transformed2:float = transform(val2_fr, 0.0, 0.0, 0.0)
```

Note: `val1_fr` and `val2_fr` are -1.0 to 1.0, the "raw" input values from the joystick converted to a full range.

You'll get some values printed which show the unaltered inputs:

```
-9%, -9%
-9%, -10%
-10%, -8%
-10%, -9%
-9%, -9%
-9%, -8%
-9%, -9%
-9%, -9%
-10%, -8%
-10%, -9%
-10%, -9%
-10%, -9%
-10%, -9%
-10%, -7%
-10%, -8%
-9%, -9%
-9%, -8%
-9%, -9%
-9%, -9%
-9%, -9%
```

As you can see above, the bias for my first value is about -10% while the second is about -9%.

Plug in these biases to the `transform` function:
```py
transformed1:float = transform(val1_fr, -0.10, 0.0, 1.0)
transformed2:float = transform(val2_fr, -0.09, 0.0, 1.0)
```

Now, running it again, you'll see that bias has been subtracted out:

```
1%, 0%
0%, 0%
1%, 0%
1%, 0%
0%, 0%
1%, 0%
0%, 1%
1%, -1%
1%, 0%
0%, 2%
1%, 1%
0%, 0%
0%, 1%
0%, 1%
1%, 1%
0%, 1%
1%, 0%
0%, 1%
```

But as you can see, even with no input (I have not touched the stick!), it still jumps around a bit. We want to implement a **deadzone** so no movement shows up as no input!

Choose what deadzone you want (it depends on how much noise is there) and apply that. I'm using 5% here (`0.05` on both):

```py
transformed1:float = transform(val1_fr, -0.10, 0.05, 1.0)
transformed2:float = transform(val2_fr, -0.09, 0.05, 1.0)
```

Run it again, then you should see 0%'s until you provide input in either direciton that exceeds that deadzone.

Now, while it is running, each axis into the maximum direction for both direction (negative and positive). 

You can see below, in my case, one direction saturates to 100% while the other does not (max value is -89% for one, -90% for the other).

To fix this, we can drop the "ceiling", or the minimum input value required to be interpreted as "saturated", in both directions for sake of symmetry.

Change the `1.0` ceiling value to whatever ceiling you want to implement. I am using `0.85`, or 85% as the max ceiling as both axes are capable of eclipsing this.

```py
transformed1:float = transform(val1_fr, -0.10, 0.05, 0.85)
transformed2:float = transform(val2_fr, -0.09, 0.05, 0.85)
```

And now, run it again! You should now have a calibrated, working joystick. 

```
0%, 0%
0%, 0%
0%, 0%
0%, 0%
0%, 0%
47%, 0%
100%, 0%
100%, 0%
100%, 0%
100%, 0%
63%, 0%
0%, 0%
0%, 0%
-100%, 0%
-100%, 0%
-100%, 0%
-100%, 0%
-100%, 0%
-100%, 0%
-27%, 0%
0%, 0%
0%, 0%
0%, -100%
0%, -100%
0%, -100%
0%, -100%
0%, -100%
0%, 0%
0%, 0%
0%, 15%
0%, 100%
0%, 100%
0%, 100%
0%, 100%
0%, 100%
0%, 100%
0%, 0%
0%, 0%
0%, 0%
```

Again, note that you may still be surprised with how quickly it reaches saturation in either direction out of the box. That is a symptom of the cheap hardware and cannot be fixed with software. Any user using the sticks will have to be quite gentle and only move in small increments to get fine-grained input!