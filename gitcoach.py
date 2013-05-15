#!/usr/bin/env python

import sys, os, shutil, subprocess, pickle, numpy, signal, re, getopt


threshold = 0 # this is _entirely arbitrary_ 
data_file        = "/.git/coaching_data"  
git_toplevel_dir = ""
specific_file    = []
git_get_current_changes = "git ls-files --full-name --modified"
git_get_file_fullpathname = "git ls-files --full-name" 
get_git_toplevel_dir = "git rev-parse --show-toplevel"


def setup():
 
  try:
    opts,args = getopt.getopt(sys.argv[1:], "hf:t:")
  except getopt.GetoptError as err:
    print str(err)
    print_help()
    exit()

  global specific_file 
  global threshold
  for op,arg in opts:
    if op == "-t":
      threshold = float(arg)
      print ("Setting threshold to: " + str(threshold) )
    elif op == "-f":
      specific_file = subprocess.check_output(git_get_file_fullpathname.split() + [arg],  shell=False, universal_newlines=False)
    elif op == "-h":
      print_help()
      exit()

  # Figure out where we are, do some looking around before we do a ton of work.
  starting_directory = os.getcwd()

  # Some git commands don't work right or at all if you run them from the .git objdir,
  # so if we think we're in there, get out. This will break if somebody is storing
  # their repo under some handmade, non-objdir ".git" subdirectory, but if they're 
  # doing that, having this code fail is the least of their problems.

  if ".git" in starting_directory:
    safe_dir = re.sub( "\.git/*", "", starting_directory)
    os.chdir(safe_dir)

  # It's conceivable that this fails if somebody puts all their git repositories
  # under .git/something but if you've done that, you've got another set of problems
  # that code can't fix.

  try:
    global git_toplevel_dir
    git_toplevel_dir = subprocess.check_output( get_git_toplevel_dir.split(), shell=False, universal_newlines=False)
  except subprocess.CalledProcessError as e:
    print ( "\nAre you sure we're in a Git repository here? I can't find the top-level directory.")
    exit ( e.returncode )

  if len(git_toplevel_dir) == 0:
    print ("\nI can't find the top of your source tree with \"git rev-parse --show-toplevel\", so I can't continue.\n" )
    # This can happen if you're running gitlearn from under the .git object directory, but the 
    # "if .git" bit above should have taken care of that. I don't know what's going on here. Bailing out.
    exit (-1)

  os.chdir( git_toplevel_dir[:-1] )

  # do if file exists bit here.
  return()

def coach():

  # OK, let's get the list of stuff we've currently modified and dare to compare.

  # FIXME - this next bit is ** guaranteed to break ** if you've got source files 
  # with whitespace in their names. I know: who does that, right? But it's still 
  # a bug.

  try: 
    git_current_changes = subprocess.check_output( git_get_current_changes.split(), shell=False, universal_newlines=True)
  except subprocess.CalledProcessError as e:
    print ( "\nAre you sure you're in a Git repository here? I can't find your list of current changes.")
    exit ( e.returncode )

  # this is a bullshit way of doing this.
  
  if len(specific_file) == 0:
    current_changeset = git_current_changes.strip().split("\n")
  else:
    current_changeset = specific_file 


  print ("Current changes: " + str(current_changeset) )

  if len(current_changeset) == 1 and current_changeset[0] == '' :
    print ("Nothing to do, exiting.") 
    exit(0)

  input_file = git_toplevel_dir[:-1] + data_file
 
  try:
    input_stream = open(input_file, 'r')
  except IOError as e:
    print ("\nData file ( $REPO/.git/coaching_data ) either doesn't exist, or isn't accessible." + \
           "\nYou need to successfully run 'gitlearn' before you can run 'gitcoach' ." )
    exit ( -1 )
 
  try:
    name_table = pickle.load(input_stream)
    correlations_table = pickle.load(input_stream)
  except pickle.UnpicklingError as e:
    print ("\nI can't load the coaching_data file ( .git/coaching_data ). Try deleting it and" + \
           "\nre-running gitlearn to solve this problem.")
    exit(-1)

  total_files = len(name_table)

  suggestion_list = []
  suggestion_odds = []
  suggestion_data = [[]] # What nonsense. Consolidate these into one data structure later.

  for a_change in current_changeset:
    if a_change in name_table:             # may not be, if file is new
      correlation_index = name_table.index(a_change)
      for c in range(total_files):  # everything but the file you're examining.

        coincidence = correlations_table[c,correlation_index] / correlations_table[c,c]

        print ("At index " + str(correlation_index) + " -  " + str(c) + " --- " + str(coincidence) + " = " + str(correlations_table[correlation_index,c]) + " / + " + str(correlations_table[c,c]))

        f = name_table[c]

        if coincidence >= threshold:
          if f in current_changeset and suggestion_odds.__contains__(f) :
            if coincidence >= suggestion_odds.index(f):
              suggestion_odds[f] = coincidence
              suggestion_list.index(f).append(a_change)
          else:
            suggestion_list.append(f)
            suggestion_odds.append(coincidence)
            suggestion_data.append([a_change])
          
            
          
          if name_table[c] in current_changeset and coincidence > suggestion_odds[ suggestion_list.index(name_table[c] ) ]:
          	suggestion_odds[ suggestion_list.index(name_table[c]) ] = coincidence
          	##suggestion_data[suggestion_list.index(name_table[c])].append(a_change)

        if name_table[c] not in current_changeset and coincidence >= threshold:
          if name_table[c] not in suggestion_list:
            suggestion_list.append(name_table[c])
            suggestion_odds.append(coincidence)
           # suggestion_data.append([a_change])


          # An off by one error in here somewhere...

  if len(suggestion_list) == 0:
    print ("Nothing to see here, move along.")
    return()

  print("You might want to take a look at the following files:\n\n" )

  for x in range(len(suggestion_list)):
    print ( str(suggestion_odds[x] * 100) + "%\t" + str(suggestion_list[x]) + "\t\tSuggested by: " + str(suggestion_data[x] ) )

  return()

def finish():
  
  # clean up and exit - finish with a quote from either Yogi Berra or Casey Stengel.

  return()

def print_help():

  print ("\nGitcoach will tell you about the files that have, historically, been frequently committed\n" +\
         "to a Git repository at the same time as the files you've already modified. It presents this\n" +\
         "information in three columns: odds of coincident commits, file of interest, and the files\n" +\
         "you're working on that may be coincident.\n\n" +\
         "Usage:\n\n"+\
         "gitcoach [-f filename]    Tell me what files are associated with my current commit, or with\n" +\
         "                          the specified filename.")


def signal_handler(signal, frame):
  print ( "\nProcess interrupted. Goodbye.\n")
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)



setup()
coach()
finish()

exit(0)
