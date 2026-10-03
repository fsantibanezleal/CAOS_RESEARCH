# Independent rational window constant

Let J be the symmetric integral operator with kernel |s-t| on [-1/2,1/2].
For nonzero omega, integrating the equation u''=2*cos(omega*s), with the
endpoint derivative determined by the integral of cos(omega*t), gives

    J cos(omega*s) = sin(omega/2)/omega
                     + 2*cos(omega/2)/omega^2
                     - 2*cos(omega*s)/omega^2.

For v0=cos(sqrt(2)*s), (I+J)v0 is the constant
sin(theta)/sqrt(2)+cos(theta), theta=sqrt(2)/2. Each integer-frequency
cosine e_j=cos(2*pi*j*s), j>=1, has integral zero. Therefore the quadratic
energy Q(v)=<v,(I+J)v> has no cross terms between v0 and e_j. Ordinary
cosine orthogonality and the displayed formula also remove cross terms
between different e_i,e_j, and Q(e_j)=1/2-1/(4*pi^2*j^2).

For v=v0+sum c_j e_j, integral v=sqrt(2)*sin(theta) and

    Q(v)=sin(theta)^2+sqrt(2)*sin(theta)*cos(theta)
                     +sum c_j^2*(1/2-1/(4*pi^2*j^2)).

Thus the normalized pair-correlation energy gives exactly

    H=3/2-cos(theta)/(sqrt(2)*sin(theta))
       -sum c_j^2*(1/2-1/(4*pi^2*j^2))/(2*sin(theta)^2).

This proves the scalar identity used in the standard-library audit. It is
also independently checked by the native-sinc I1,I2,J evaluation in run.py.
The global profile lower bound cos(theta)-sum |c_j| is positive, so smooth
positive compact approximations used by the analytic transfer exist.

The rational audit brackets sqrt(2) by isqrt(2*10^120)/10^60 and the next
integer over the same denominator, checking both exact squares. It brackets
arctan(1/5) and arctan(1/239) by forty alternating-series terms and the
first omitted term. Machin's identity pi=16*arctan(1/5)-4*arctan(1/239)
follows from tan(4*arctan(1/5))=120/119 and
tan(4*arctan(1/5)-arctan(1/239))=1, with that angle in (0,pi/2).
Twenty-four Taylor terms for sine and cosine at theta use remainders
theta^49/49! and theta^48/48!, respectively. Every arithmetic operation
uses integer Fraction interval endpoints; no floating rounding or FLINT
evaluation enters this second path.

The resulting exact outward decimal enclosure is

    0.6721710926412995494027803172404056748101
        <= H <=
    0.6721710926412995494027803172404056748102.

It proves H>=0.67217109258. This is a scalar/window proof, not the external
universal six-gap local inequality or the BGSTB analytic theorem.
