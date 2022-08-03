# btc-model

The cycles of BTC can be modeled with exponential waves of both price and time to achieve a remarkably good fit.

With a support supercycle from when trading seriously began in Oct 2010 until a presumed peak in Nov 2021. Then the classic bubble cycles deviating from support. Including two usually unidentified crunched cycles during Oct and Nov 2010 that can be seen on a log-log scale. These first cycles in 2010 are usually considered noise to disregard by other models, but here they fit as well as the others.

There’s no data for this model yet to fit the other side of the supercycle wave. Where, like Elliott Waves, the support of a grand supercycle would be expected with this model. For now, a simple mirror of the supercycle is plotted. Which represents the worst case of no further support.

The next significant data point to fit would be a projected rounded bottom. Using the mirror as a local approximation, the bottom would be around $10K at the beginning of next year. Before the next cycle with a lower-high projected.

Layers of scales are used. With a linear fit of the supercycle and a sine wave fit of the cycles. Using ln(price)+3 and ln(years)+6 scales to work with non-negative values, and inverse-sine (asin) scales for waves.

1. [ln(p) vs t](plot/ln(p)%20vs%20t.png) with cycles becoming exponentially farther apart.
2. [ln(p) vs ln(t)](plot/ln(p)%20vs%20ln(t).png) with the crunched early two cycles.
3. [ln(ln(p)) vs ln(t)](plot/ln(ln(p))%20vs%20ln(t).png) with the supercycle being exponential, and a linear fit.
4. [asin(ln(ln(p))) vs ln(t)](plot/asin(ln(ln(p)))%20vs%20ln(t).png) with the amplitude of the cycles being a wave.
5. [asin(ln(ln(p))) vs asin(ln(t))](plot/asin(ln(ln(p)))%20vs%20asin(ln(t)).png) with the timing of cycles also being a wave.
6. [ln(ln(Δp)) vs asin(ln(t))](plot/ln(ln(dp))%20vs%20asin(ln(t)).png) with a remarkable sine fit of the cycle’s double-exponential deviation from support.

The formulas used can be seen here in [python](formulas.py). Using only the base and peak points plus the number of cycles as parameters.