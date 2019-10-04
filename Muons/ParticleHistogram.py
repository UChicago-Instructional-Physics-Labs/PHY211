import numpy as np

def fitfunc(p, x):
    return p[0]*np.exp(-x*p[1])
def residual(p, x, y, dy):
    return (fitfunc(p, x)-y)/dy
# defining a function to fit data with


hist_bins_rebin = hist_bins[::rebin_factor]
    # hist_bins_rebin is the new set of bins; it basically takes every nth element from the original bins.
        # n is rebin_factor in this case. 
        # for syntax see https://docs.scipy.org/doc/numpy/reference/arrays.indexing.html
dat,bins = np.histogram(time_data,bins=hist_bins)
dat2,bins2 = np.histogram(time_data,bins=hist_bins_rebin)

import numpy.ma as ma
dat_nonzero = ma.masked_less_equal(dat[0:],0)
bin_nonzero = ma.masked_array(bins[0:-1], mask=dat_nonzero.mask).compressed()
dat_nonzero = dat_nonzero.compressed()
dat2_nonzero = ma.masked_less_equal(dat2[0:],0)
bin2_nonzero = ma.masked_array(bins2[0:-1], mask=dat2_nonzero.mask).compressed()
dat2_nonzero = dat2_nonzero.compressed()
    # this whole bit serves the function of tossing out bins with zeros in them.
    # this is to keep the optimization from throwing a fit
    # see https://docs.scipy.org/doc/numpy/reference/maskedarray.generic.html

from scipy import optimize
p01 = [max(dat), decay_chance]
pf1, cov1, info1, mesg1, success1 = optimize.leastsq(residual, p01, args = (bin_nonzero,dat_nonzero,np.sqrt(dat_nonzero)), full_output=1)
    # usual code for fitting the unbinned data
    # uses max(dat) as a quick guess for how high the exponential should go

from IPython.display import display, Math
    # used to render equations in a more readible fashion
    
print("Raw Bins:")
if cov1 is None:
    print('Fit did not converge')
    print('Success code:', success1)
    print(mesg1)
else:
    print('Fit Converged')
    chisq1 = sum(info1['fvec']*info1['fvec'])
    dof1 = len(dat)-len(pf1)
    pferr1 = [np.sqrt(cov1[i,i]) for i in range(len(pf1))]
    print("Chi-square for fit:")
    display(Math(r"\chi^2 = {:.2f}".format(chisq1)))
        # the {:.2f} here denotes that the variable we name (chisq) 
        # should be shown as a floating point number (f) with two decimal places (.2)
    print("Degrees of freedom:")
    display(Math(r"d.f. = {}".format(dof1)))
    print("Reduced chi-square:")
    display(Math(r"\frac{{\chi^2}}{{d.f.}} = {:.2f}".format(chisq1/dof1)))
        # to get ipython's Math to recognize curly brackets as LaTeX formatting, you need to use pairs of them
    print('Inital guess values:')
    display(Math(r"f(t) = {}e^{{-{}t}}".format(p01[0],p01[1])))
    print('Fit values:')
    display(Math(r"f(t) = ({:.2f}\pm{:.2f})e^{{(-{:.4f}\pm{:.4f})t}}".format(pf1[0],pferr1[0],pf1[1],pferr1[1])))
        
p02 = [max(dat2), decay_chance,]
pf2, cov2, info2, mesg2, success2 = optimize.leastsq(residual, p02, args = (bin2_nonzero,dat2_nonzero,np.sqrt(dat2_nonzero)), full_output=1)
# this fits the binned data
    
    
print('\n')
print("Binned Data:")
if cov2 is None:
    print('Fit did not converge')
    print('Success code:', success1)
    print(mesg1)
else:
    

    print('Fit Converged')
    chisq2 = sum(info2['fvec']*info2['fvec'])
    dof2 = len(dat2)-len(pf2)
    pferr2 = [np.sqrt(cov2[i,i]) for i in range(len(pf2))]
    print("Chi-square for fit:")
    display(Math(r"\chi^2 = {:.2f}".format(chisq2)))
    print("Degrees of freedom:")
    display(Math(r"d.f. = {}".format(dof2)))
    print("Reduced chi-square:")
    display(Math(r"\frac{{\chi^2}}{{d.f.}} = {:.2f}".format(chisq2/dof2)))
    print('Inital guess values:')
    display(Math(r"f(t) = {}e^{{-{}t}}".format(p02[0],p02[1])))
    print('Fit values:')
    display(Math(r"f(t) = ({0:.2f}\pm{1:.2f})e^{{(-{2:.4f}\pm{3:.4f})t}}".format(pf2[0],pferr2[0],pf2[1],pferr2[1])))

fig1 = plt.figure()
ax1 = fig1.add_subplot(211)
ax2 = fig1.add_subplot(212)
ax1.errorbar(bin_nonzero,dat_nonzero,np.sqrt(dat_nonzero), fmt='k.', label = 'Data')
ax2.errorbar(bin2_nonzero,dat2_nonzero,np.sqrt(dat2_nonzero), fmt='k^', label = 'Data')
# plot the data

T = np.linspace(0, time_range, time_range+1)
ax1.plot(T, fitfunc(pf1, T), 'r-', label = 'Fit', zorder=5)
ax1.plot(T, fitfunc(p01, T), 'b:', label = 'Guess', zorder=4)
ax2.plot(T, fitfunc(pf2, T), 'r-', label = 'Fit', zorder=5)
ax2.plot(T, fitfunc(p02, T), 'b:', label = 'Guess', zorder=4)
# plot the fits, along with our guesses

ax1.legend()
ax2.legend()
ax1.set_title('Raw Bins')
ax2.set_title('Binned Data\n Rebinning factor = {}'.format(rebin_factor))
ax1.set_xlabel("Lifetime")
ax2.set_xlabel("Lifetime")
ax1.set_ylabel("Counts")
ax2.set_ylabel("Counts")
plt.tight_layout()
#    plt.savefig('Decay Simulation.pdf')
plt.show()