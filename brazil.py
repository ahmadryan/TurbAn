#-------------------------------------------------------------------------------
# Brazil Plot
#-------------------------------------------------------------------------------

# Define the function for generation of Brazil plots

def plot_br( spc='', x=None, y=None, z=[], ztype='', date='', bins=50,
  xscale='log', yscale='lin', n_min=20, mach_ind=[], dens_ind=[], dens=False ) :

	# Check to make sure all required values are passed. If not, abort.
	# Note: 'z = None' produces standard bins of number of data

	if ( x is None ) :

		raise ValueError( 'x data not provided' )
		return

	if ( y is None ) :

		raise ValueError( 'y data not provided' )
		return

	# Clear previous histogram(s)

	plt.clf( )
	plt.figure( )

	# Set axis limits based on species. If species is not recognized,
	# raise an error and abort.

	if ( spc == 'p' or spc == 'i' ) :

		xlim = [ 0. , 3.  ]
		ylim = [ 0.2, 2.3 ]

		# For plot title(s)

		if spc == 'p' :

			species = 'Proton'

		else :

			species = 'Ion'

	elif ( spc == 'e' ) :

		xlim = [ -1.1, 2.  ]
		ylim = [  0.4, 1.6 ]

		# For plot title(s)

		species = 'Electron'

	else :

		raise ValueError( 'species not recognized' )
		return

	# Change x, y, and z into numpy arrays

	x = array( x )
	y = array( y )
	z = array( z )

	# If the x and/or y axis is logarithmic, adjust the corresponding data

	if ( xscale == 'log' ) :

		x = log10( x )

	if ( yscale == 'log' ) :

		y = log10( y )

	# Determine if 1 or 2 bin values are given and separate values
	# if necessary.

	if ( hasattr( bins, 'len' ) ) :

		nx = bins[0]
		ny = bins[1]

	else :

		nx = bins
		ny = bins

	# If no z data have been provided, generate a standard histogram.
	# Otherwise, manually generate bins and bin the data.

	if len(z) == 0 :

		hst = plt.hist2d( x, y, bins=bins, range=[ xlim, ylim ],
		                  cmap=plt.cm.jet, norm=mpl.colors.LogNorm(), cmin=n_min )

		# number of data points
		N = nansum( nansum( hst[0], axis=0 ) )

		title = species +\
		              ' Temperature Anisotropy vs. Parallel Plasma Beta'

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

	# Make plot ticks and adjust for logscale axes if necessary

	xvals = linspace( int( xlim[0] ), xlim[1], 4 )

	yvals = linspace( ylim[0], ylim[1], 4 )

	if ( xscale == 'log' ) :

		xlabels = [ round( xx, 1 ) for xx in 10**xvals ]

	else :

		xlabels = [ int(xx) for xx in xvals ]

	if ( yscale == 'log' ) :

		ylabels = [ int(yy) for yy in 10**yvals ]

	else :

		ylabels = [ round( yy, 2 ) for yy in yvals ]

	# If necessary, transform the label locations

	if len(z) > 0 :

		xratio = nx / ( xlim[1] - xlim[0] )
		yratio = ny / ( ylim[1] - ylim[0] )

		plt.xticks( ( xvals - xlim[0] )*xratio, xlabels )

		plt.yticks( ( yvals - ylim[0] )*yratio, ylabels )

		hline = ( 1. - ylim[0] ) * yratio

	else :

		plt.xticks( xvals, xlabels )

		plt.yticks( yvals, ylabels )

		hline = 1.

	# Generate the axis labels

	xtext1 = r'$\beta_{\parallel {\rm %s}} \equiv 2\,\mu_0\,n_{\rm %s}\,$'\
	                                                          % ( spc, spc )
	xtext2 = r'$k_{\rm B}\,T_{\parallel {\rm %s}}\,/\,B^2$' % ( spc )

	xtext = xtext1 + xtext2

	ytext1 = r'$R_{\rm %s} \equiv T_{\perp {\rm %s}}\,/\,$' % ( spc, spc )
	ytext2 = r'$T_{\parallel {\rm %s}}$' % ( spc )

	ytext = ytext1 + ytext2

	plt.xlabel( xtext, fontsize=14 )

	plt.ylabel( ytext, fontsize=14 )

	# Interpret the ztype (if applicable)

	if ( ztype.lower() == 't_tot' or ztype.lower() == 'temp_tot' ) :

		zlabel = r'$T_{tot \, {\rm %s}}$' % ( spc )
		zfile  = 't_tot_'

		title  = species + ' Total Temperature'

	elif ( ztype.lower() == 't_per' or ztype.lower() == 't_perp' or
	       ztype.lower() == 'temp_per' or ztype.lower() == 'temp_perp' ) :

		zlabel = r'$T_{\perp \, {\rm %s}}$' % ( spc )
		zfile  = 't_per_'

		title  = species + ' Perpendicular Temperature'

	elif ( ztype.lower() == 't_par' or ztype.lower() == 't_para' or
	       ztype.lower() == 'temp_par' or ztype.lower() == 'temp_para' ) :

		zlabel = r'$T_{\parallel \, {\rm %s}}$' % ( spc )
		zfile  = 't_par_'

		title  = species + ' Parallel Temperature'

	elif ( ztype.lower() == 'curr_mag' or ztype.lower() == 'curr_tot' ) :

		zlabel = r'$J$' 
		zfile  = 'j_mag'

		title  = 'Total Current (' + species + ' Cadence)'

	elif ( ztype.lower() == 'pvi' ) :

		zlabel = r'$|\Delta B | / \sigma$'
		zfile  = 'pvi_'

		title  = 'PVI of Magnetic Field (' + species + ' Cadence)'

	elif ( ztype.lower() == '' ) :

		zlabel = ''
		zfile  = ''

	else :

		zlabel = ztype.lower()
		zfile  = ztype.lower() + '_'

	# Generate the colorbar

	cbar = plt.colorbar()

	cbar.set_label( zlabel, horizontalalignment='left',
	                        rotation='horizontal',fontsize=14 )

	'''

	if ztype.lower() == 'pvi' :

		ticks = cbar.ax.get_yticks()

		tick_labels = [ t.get_text() for t in cbar.ax.get_yticklabels() ]

		tick_labels[0] = '< ' + u'$\\mathdefault{8\\times10^{-1}}$'

		cbar.ax.set_yticklabels( tick_labels )

	'''

	# Clean up plot

	if ( ylim[0] < 1. and ylim[1] > 1. ) :

		plt.axhline( hline, color='k', lw=0.6 )

	title += ' (N = ' + str(int(N)) + ')'

	plt.title( title )

	plt.tight_layout()

	# If species is protons, change 'spc' to 'i' for file save

	if ( spc == 'p' ) :

		spc = 'i'

	#if plotting current, remove the species label

	if ( zfile == 'j_mag' ):

		spc = ''

	# Save and show the figure

	plt.savefig( 'plots/brazil_' + zfile + date + spc + '.pdf' )

	plt.show()


