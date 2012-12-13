#!/usr/bin/python

import sys, os, shutil, subprocess, pickle, numpy, signal, re

threshold = 0.8 # this is _entirely arbitrary_ 
data_file        = "/.git/coaching_data"  
git_toplevel_dir = ""

git_get_current_changes = "git ls-files --full-name --modified" 

def setup():

  get_git_toplevel_dir = "git rev-parse --show-toplevel"
  # Violating the "never cut and paste code" maxim, I know. FIXME 

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

  current_changeset = git_current_changes.strip().split("\n")

  print ("Current changes: " + str(current_changeset) )

  if len(current_changeset) == 0:
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
    names = pickle.load(input_stream)
    correlations = pickle.load(input_stream)
  except pickle.UnpicklingError as e:
    print ("\nI can't load the coaching_data file ( .git/coaching_data ). Try deleting it and" + \
           "\nre-running gitlearn to solve this problem.")
    exit(-1)

  total_files = len(names)

  for a_change in current_changeset:
    print ("Looking for " + a_change )
    if a_change in names:
      index = names.index(a_change)
      for c in range(total_files):  # everything but the file you're examining.

        coincidence = correlations[index,c] / correlations[c,c]

        if coincidence < threshold  :
          print ( str(coincidence) + "%\t" + str(names[index]) + "\n" )

  return()

def finish():
  
  # clean up and exit - finish with a quote from either Yogi Berra or Casey Stengel.

  return()

def signal_handler(signal, frame):
  print ( "\nProcess interrupted. Goodbye.\n")
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

setup()
coach()
finish()

exit(0)
