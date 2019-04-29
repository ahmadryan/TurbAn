#-------------------------------------------------------------------------------
# MODULES
#-------------------------------------------------------------------------------

# Load the necessary modules.

from numpy import *

import matplotlib.pyplot as plt

import matplotlib as mpl

#-------------------------------------------------------------------------------
# Brazil Histogram
#-------------------------------------------------------------------------------

# Define the function for generation of Brazil Histogram

def brzl_hist( x=None, y=None, z=[], xlim=None, ylim=None, ztype='', spc='', date='', bins=50, n_min=20, dens=False ) :

	# Check to make sure all required values are passed. If not, abort.
	# Note: 'z = None' produces standard bins of number of data

	if ( x is None ) :

		raise ValueError( 'x data not provided' )
		return

	if ( y is None ) :

		raise ValueError( 'y data not provided' )
		return

	# Change x, y, and z into numpy arrays

	x = array( x )
	y = array( y )
	z = array( z )

	# Determine if 1 or 2 bin values are given and separate values
	# if necessary.

	if ( hasattr( bins, 'len' ) ) :

		nx = bins[0]
		ny = bins[1]

	else :

		nx = bins
		ny = bins

	if( xlim is None ) :

		xlim = [ nanmin( x ), nanmax( x ) ]

	if( ylim is None ) :

		ylim = [ nanmin( y ), nanmax( y ) ]

	# If no z data have been provided, generate a standard histogram.
	# Otherwise, manually generate bins and bin the data.

	if len(z) == 0 :

		hst = plt.hist2d( x, y, bins=bins, range=[ xlim, ylim ] )

		# number of data points
		N = nansum( nansum( hst[0], axis=0 ) )

	else :

		# set number of data points to zero for running tally
		N = 0

		# Note: bins variables are lists of all leading edges plus
		# the lagging edge of the final bin.

		xbins = linspace( xlim[0], xlim[1], nx+1 )
		ybins = linspace( ylim[0], ylim[1], ny+1 )

		# For each bin, find all the z data whose corresponding
		# x and y values fall within that bin and save the medians
		# as an array to be plotted.

		zplot = array( [ [ float('nan') for n in range( nx ) ]
		                                for m in range( ny ) ] )

		tkx = []
		tky = []
		tkz = []

		# For each bin along the x-axis...

		for i in range( nx ) :

			# find the x data with beta values within that bin

			tkx = where( ( x >= xbins[i]   ) &
				     ( x <  xbins[i+1] )   )[0]

			# If no valid beta values were found,
			# move to the next bin.

			if len( tkx ) == 0 :

				continue

			# For each bin along the y-axis...

			for j in range( ny ) :

				# find the y data with anisotropy values
				# within that bin.

				tkxy = where( ( y[tkx] >= ybins[j]   ) &
				              ( y[tkx] <  ybins[j+1] )   )[0]

				# If any valid data were found, take the
				# median of those data (ignoring 'Nan's) and
				# assign that value to the corresponding
				# location in 'zplot' for plotting.

				if len( tkxy ) >= n_min :
					zplot[i,j] = nanmedian( z[tkx][tkxy] )

					# running tally of number of data points
					N += len( where( z[tkx][tkxy] != float('nan') )[0] )

		# Generate the histogram (not actually a matplotlib histogram)
		# Note: imshow() plots according to ( y, x )

		zplot = transpose( zplot )

		if ztype.lower() == 'pvi' :

			norm = mpl.colors.Normalize()

		else :

			norm = mpl.colors.LogNorm()

		hst = plt.imshow( zplot, aspect='equal', origin='lower',
		                  cmap=plt.cm.jet, norm=norm             )

	return hst
