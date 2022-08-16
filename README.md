# Bitcoin Exponential Price and Time Wave Model

![asin(ln(ln(p))) vs asin(ln(t))](plot/scale/5.%20asin%28ln%28ln%28p%29%29%29%20vs%20asin%28ln%28t%29%29%20%5Bpreview%5D.png)

All of the price cycles of BTC can be formally modeled with exponential waves of both price and time. Achieving a remarkably good fit of their size and timing back to the very beginning of trading.

It is unprecedented how BTC started at zero, but was seen as having vast potential to be a global currency, and as a generational investment opportunity. Creating a singularity with a 'big bang' that lead to its value on exchanges increasing one million times in a decade. These extreme market conditions caused a regularity not usually seen in chaotic markets, showing raw speculation investor psychology, and a series of bubble cycles that have become expected and modeled.

There are two usually unidentified crunched cycles during Oct and Nov 2010. Hidden in data that is normally considered noise by other models. Here though, these early cycles are key to one continuous rapid expansion then cooling from a point. With all these cycles fitting a supercycle of both price and time. With a peak expansion in Nov 2021 then a contraction projected.

The [formulas used](src/model.py) for the model and to generate the plots are here in Python code. Using only the base and peak points plus the number of cycles as parameters.

# Scales

Layers of scales are used to visualize and build the model. Using ln(price)+3 and ln(years)+6 coordinates to work with non-negative values, and inverse-sine (asin) for waves.

## 1. ln(p) vs t

The cycles become exponentially farther apart.

![ln(p) vs t](plot/scale/1.%20ln%28p%29%20vs%20t.png)

## 2. ln(p) vs ln(t)

The crunched early two cycles are seen on a log-log scale.

![ln(p) vs ln(t)](plot/scale/2.%20ln%28p%29%20vs%20ln%28t%29.png)

Zooming in to see them on a lin-log scale.

![p vs d 2010](plot/zoom/p%20vs%20d%20%5B2010%5D.png)

## 3. ln(ln(p)) vs ln(t)

The supercycle is a double-exponential with a linear fit.

![ln(ln(p)) vs ln(t)](plot/scale/3.%20ln%28ln%28p%29%29%20vs%20ln%28t%29.png)

## 4. asin(ln(ln(p))) vs ln(t)

The amplitude of the cycles form a wave with a peak in 2021.

![asin(ln(ln(p))) vs ln(t)](plot/scale/4.%20asin%28ln%28ln%28p%29%29%29%20vs%20ln%28t%29.png)

## 5. asin(ln(ln(p))) vs asin(ln(t))

The timing of cycles also form a wave with a peak in 2021.

![asin(ln(ln(p))) vs asin(ln(t))](plot/scale/5.%20asin%28ln%28ln%28p%29%29%29%20vs%20asin%28ln%28t%29%29.png)

## 6. ln(ln(Δp)) vs asin(ln(t))

A remarkable sine fit of the cycle’s double-exponential deviation from the supercycle.

![ln(ln(Δp)) vs asin(ln(t))](plot/scale/6c.%20ln%28ln%28dp%29%29%20vs%20asin%28ln%28t%29%29.png)

# Projections

There’s no data for this model yet to fit the other side of the supercycle wave.

## Basic Projection

The model in its basic form would give a massive correction wave.

![p vs d basic projection](plot/future/p%20vs%20d%20%5Bbasic%5D.png)

## Mirror Projection

It seems more likely though that time would accelerate again. Mirroring the past. Plus there would be the support of a grand supercycle, like Elliott Waves

Plotted here is a linear approximation from the peak of supports with different APYs. Assuming that the grand supercycle would be an exponential price and time wave like the supercycle. Giving an idea of how rapidly the price would still be growing even after a large correction, because average market returns of around 10% would be apocalyptic. Around 50% would be a large correction that seems like the median projection of this model. While 75% would be optimistic.

![p vs d mirror apy](plot/future/p%20vs%20d%20%5Bmirror%20apy%5D.png)

## Local Approximation

The next significant data point to fit would be a projected rounded bottom. Using the mirror as a local approximation, the bottom would be around $10K at the beginning of next year. Before the next cycle with a lower-high projected in 2025. Though, the fit here of the model is not particularly good probably because of interference from the volatility of global markets.

![p vs d 2020-2025](plot/zoom/p%20vs%20d%20%5B2020-2025%5D.png)

## Improvements

More sophisticated and realistic models can be made. Without more data though justifying further projections is very difficult. The best use of the model likely will be continuing to fit future data to try to best project the next movement. With the next couple years being critical to testing the projection of a supercycle peak in 2021, and measuring the following movement.

The big question is whether BTC will continue its explosive growth, even after a possible large correction, and whether there will still be a cycle regularity. Perhaps, it is destined to because investor psychology will always lead to more cycles of exuberance seeing near limitless potential. Already reaching escape velocity on its way to the moon.
