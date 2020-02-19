#!/usr/bin/env python

##########################################################################
#
# Written by Marco Iacobelli
#
##########################################################################
#
# History
# 17/02/2020 Changed for evaluating the level of support based on the count of boolean flags-- MI
#
# 11/02/2020 Changed for the use with argparse and added debugging (plotting) mode-- MI
#
# To be done:
# Tuning of the weights of each of the positional arguments
#
# Add contingency level factor (for e.g. overheads)
#
# python DesSupIndicator.py lc 100 if bookended 100 2 4 --dynsp


import argparse, numpy as np

def main(Projtype, Tobsreq, Obsmode, Obsstrategytype, Parallelobs, Nruns, Nsap, Arrconstr, Schedconstr, Resptel, Targlistupd, Npipxobs, Dynsp, Debug):
	"""
	Determine the degree of supportability of a project.
	Time constants for basic operations at each support step are hardcoded.
	Expected time unit is hour for consistency with the amount of requested hours.
	
	Parameters
	----------
	Projtype : str
		Type of proposal: LT (long-term), LC (single cycle)
	Tobsreq : float
		Overall number of observing hours of the project
	Obsduration : float
		Typical exposure per observation (hours)
	Obsmode : str
		Type of observing mode: IF (interferometric), BF (beamformed), TBB, IF+BF
	Obsstrategytype : str
		Type of observing strategy: bookended, interleaved, noLST-constrain, single-run, lucky-imaging
	Parallelobs : bool
		Parallel observing needed?
	Nruns : integer
		Overall number of runs requested by the project
	Nsap : int
		Requested number of SAPs per observation (default 1)
	Arrconstr : boolean
		Any array configuration constraint? (e.g. any station to not be missed)
	Schedconstr : boolean
		Restrictive scheduling constraints?
	Resptel : boolean
		Rapid response functionality requested?
	Targlistupd : boolean
		Requested updates to target lists during the cycle(s)?
	Npipxobs : integer, optional
		Number of pipelines per observation per run
	Dynsp : boolean
		Requested dynamic spectrum pipeline?
	Debug :
		Run in debug mode ?
	Returns
	-------
	result : float / plot
		The degree of supportability in one of the categories: low / standard / high
		Optionally, a bar plot of the contribution of each category to the degree of support
		
	"""
	objects = []
	scores = []
		
	if Obsmode.lower() == 'bf' or Obsmode.lower() == 'Medium': degreeofsupport_Obsmode = 'Medium'
	if Obsmode.lower() == 'if': degreeofsupport_Obsmode = 'Medium'
	if Obsmode.lower() == 'bf+if': degreeofsupport_Obsmode = 'High'
	#objects.append('Obsmode')
	scores.append(degreeofsupport_Obsmode)
	
	if Obsstrategytype.lower() == 'nolst-constraint': degreeofsupport_Obsstrategytype = 'Low' #low
	if Obsstrategytype.lower() == 'single-run': degreeofsupport_Obsstrategytype = 'Medium' #low typical beamformed observing strategy name
	if Obsstrategytype.lower() == 'bookended': degreeofsupport_Obsstrategytype = 'Medium' #medium
	if Obsstrategytype.lower() == 'interleaved': degreeofsupport_Obsstrategytype = 'High' #high
	if Obsstrategytype.lower() == 'lucky-imaging' : degreeofsupport_Obsstrategytype = 'High' #high
	#objects.append('Obsstrategytype')
	scores.append(degreeofsupport_Obsstrategytype)
		
	nruns_month_low = 4 # i.e. 1run/1week time on average in the semester
	nruns_month_medium = 8 # i.e. 1run/1week time on average in the semester
	nruns_month_high = 12 # i.e. 1run/1week time on average in the semester
	
	if Projtype.lower() == 'lc' and Nruns <= nruns_month_low: degreeofsupport_Projtype_Nruns = 'Low' # i.e. 1run/2weeks time on average in the semester
	if Projtype.lower() == 'lc' and Nruns > nruns_month_low and Nruns <= nruns_month_high: degreeofsupport_Projtype_Nruns = 'Medium'
	if Projtype.lower() == 'lc' and Nruns >= nruns_month_high: degreeofsupport_Projtype_Nruns = 'High' # i.e. 2runs/1week time on average in the semester
	if Projtype.lower() == 'lt' and Nruns <= nruns_month_low: degreeofsupport_Projtype_Nruns = 'Low' # i.e. 1run/1week time on average in the semester
	if Projtype.lower() == 'lt' and Nruns > nruns_month_low and Nruns <= nruns_month_medium: degreeofsupport_Projtype_Nruns = 'Medium' 
	if Projtype.lower() == 'lt' and Nruns >= nruns_month_high+4: degreeofsupport_Projtype_Nruns = 'High' # i.e. 3runs/1week time on average in the semester
	objects.append('Projtype_Nruns')
	scores.append(degreeofsupport_Projtype_Nruns)

	lc_time_offered = 774. #970.
	lt_time_offered = 1100. #1440.
	lc_time_medium = lc_time_offered*10./100. #; print lc_time_medium
	lt_time_medium = lt_time_offered*10./100. #; print lt_time_medium
	lc_time_high = lc_time_offered*25./100. ; #print lc_time_high
	lt_time_high = lt_time_offered*25./100. ; #print lt_time_high
	
	#if Projtype.lower() == 'lc' and Tobsreq < lc_time_medium: degreeofsupport_Projtype_Tobsreq = 0
	#if Projtype.lower() == 'lc' and Tobsreq >= lc_time_medium and Tobsreq < lc_time_high: degreeofsupport_Projtype_Tobsreq = 1
	if Projtype.lower() == 'lc' and Tobsreq > lc_time_high: degreeofsupport_Projtype_Tobsreq = 'High' ; scores.append(degreeofsupport_Projtype_Tobsreq)
	#if Projtype.lower() == 'lt' and Tobsreq < lt_time_medium: degreeofsupport = degreeofsupport_Projtype_Tobsreq = 0
	#if Projtype.lower() == 'lt' and Tobsreq >= lt_time_medium and Tobsreq < lt_time_high: degreeofsupport_Projtype_Tobsreq = 1
	if Projtype.lower() == 'lt' and Tobsreq > lt_time_high: degreeofsupport_Projtype_Tobsreq = 'High' ; scores.append(degreeofsupport_Projtype_Tobsreq)
	#objects.append('Projtype_Tobsreq')
	#scores.append(degreeofsupport_Projtype_Tobsreq)

	if Parallelobs: # i.e. if parallel observing is required
		degreeofsupport_Parallelobs = 'High'
		objects.append('Parallelobs')
		scores.append(degreeofsupport_Parallelobs)
	
	if Nsap <=2: degreeofsupport_Nsap = 'Low'
	if Nsap > 2 and Nsap <= 4: degreeofsupport_Nsap = 'Medium'
	if Nsap > 4: degreeofsupport_Nsap = 'High'
	objects.append('Nsap')
	scores.append(degreeofsupport_Nsap)
	
	tot_scores = []
	tot_scores.append( scores.count("Low") )
	tot_scores.append( scores.count("Medium") )
	tot_scores.append( scores.count("High") )
	if tot_scores.index(max(tot_scores)) == 0: tot_scores_no_expensive_items = 'Low'
	if tot_scores.index(max(tot_scores)) == 1: tot_scores_no_expensive_items = 'Medium'
	if tot_scores.index(max(tot_scores)) == 2: tot_scores_no_expensive_items = 'High'
	# if both counts of Medium and High are equals set to High
	if scores.count("Medium") == scores.count("High") and scores.count("Low") == 0: tot_scores_no_expensive_items = 'Medium'
	if scores.count("Medium") == scores.count("High") and scores.count("Low") != 1: tot_scores_no_expensive_items = 'High'
	
	expensive_items = []
	if Arrconstr: degreeofsupport_Arrconstr = 1 ; expensive_items.append(degreeofsupport_Arrconstr) ; objects.append('Arrconstr')
	if Schedconstr: degreeofsupport_Schedconstr = 1 ; expensive_items.append(degreeofsupport_Schedconstr) ; objects.append('Schedconstr')
	if Resptel: degreeofsupport_Resptel = 1 ; expensive_items.append(degreeofsupport_Resptel) ; objects.append('Resptel')
	if Targlistupd: degreeofsupport_Targlistupd = 1 ; expensive_items.append(degreeofsupport_Targlistupd) ; objects.append('Targlistupd')
	if Npipxobs >= 1: degreeofsupport_Npipxobs = 1 ; expensive_items.append(degreeofsupport_Npipxobs) ; objects.append('Npipxobs')
	if Dynsp: degreeofsupport_Dynsp = 1 ; expensive_items.append(degreeofsupport_Dynsp) ; objects.append('Dynsp')
	
	# sum up everything
	if Debug:
		print '\n Scores Low | Medium | High | Exp items'
		print scores.count("Low"),scores.count("Medium"),scores.count("High"),sum(expensive_items)
	
	if sum(expensive_items) <= 1 and tot_scores_no_expensive_items == 'Low': degreeofsupport = 'Low'
	if sum(expensive_items) <= 1 and tot_scores_no_expensive_items == 'Medium': degreeofsupport = 'Medium'
	if sum(expensive_items) <= 1 and tot_scores_no_expensive_items == 'High': degreeofsupport = 'High'
	
	if sum(expensive_items) > 1 and sum(expensive_items) <= 2 and tot_scores_no_expensive_items == 'Low': degreeofsupport = 'Medium'
	if sum(expensive_items) > 1 and sum(expensive_items) <= 2 and tot_scores_no_expensive_items == 'Medium': degreeofsupport = 'High'
	if sum(expensive_items) > 1 and sum(expensive_items) <= 2 and tot_scores_no_expensive_items == 'High': degreeofsupport = 'High'
	
	if sum(expensive_items) > 2 and tot_scores_no_expensive_items == 'Low': degreeofsupport == 'High'
	if sum(expensive_items) > 2 and tot_scores_no_expensive_items == 'Medium': degreeofsupport == 'High'
	if sum(expensive_items) > 2 and tot_scores_no_expensive_items == 'High': degreeofsupport == 'High'
	
	return degreeofsupport
	

if __name__ == "__main__":
	descriptiontext = "Determine the degree of supportability of a project. Expected time unit is hour.\n"
	parser = argparse.ArgumentParser(description=descriptiontext, formatter_class=argparse.RawTextHelpFormatter)
	
	parser.add_argument('projtype',help='Type of proposal: LT (long-term), LC (single cycle)', type=str, default='LC')
	parser.add_argument('tobsreq',help='Total number of observing hours of the project', type=float, default=0.)
	parser.add_argument('obsmode',help='Type of observing mode: IF (interferometric), BF (beamformed), TBB, IF+BF', type=str, default='if')
	parser.add_argument('obsstrategytype',help='Type of observing strategy: bookended, interleaved, noLST-constrain, single-run, lucky-imaging', type=str, default='noLST-constraint')
	parser.add_argument('nruns',help='Overall number of runs requested by the project '
						'(default 1)', type=int, default=1)
	parser.add_argument('nsap',help='Requested number of SAPs per observation [no analogue Tile Beam] (default 1)', type=int, default=1)
	parser.add_argument('npipxobs',help='Number of pipelines per observation per run (default 0)', type=int, default=0)
	parser.add_argument('--parallelobs',help='Parallel observing needed? T/F', action='store_true', default=False)
	parser.add_argument('--arrconstr',help='Any array configuration constraint? (e.g. any station to not be missed) T/F', action='store_true', default=False)
	parser.add_argument('--schedconstr',help='Restrictive scheduling constraints? T/F', action='store_true', default=False)
	parser.add_argument('--resptel',help='Rapid response functionality requested? T/F', action='store_true', default=False)
	parser.add_argument('--targlistupd',help='Requested updates to target lists during the cycle(s)? T/F', action='store_true', default=False)
	parser.add_argument('--dynsp',help='Requested dynamic spectrum pipeline? T/F', action='store_true', default=False)
	parser.add_argument('--debug',help='Run in debug mode and plot scores', action='store_true', default=False)
		
	args = parser.parse_args()
	Projtype = args.projtype
	Tobsreq = args.tobsreq
	Obsmode = args.obsmode
	Obsstrategytype = args.obsstrategytype
	Nruns = args.nruns
	Nsap = args.nsap
	Parallelobs = args.parallelobs
	Arrconstr = args.arrconstr
	Schedconstr = args.schedconstr
	Resptel = args.resptel
	Targlistupd = args.targlistupd
	Npipxobs = args.npipxobs
	Dynsp = args.dynsp
	Debug = args.debug
	
	main(Projtype, Tobsreq, Obsmode, Obsstrategytype, Parallelobs, Nruns, Nsap, Arrconstr, Schedconstr, Resptel, Targlistupd, Npipxobs, Dynsp, Debug)
