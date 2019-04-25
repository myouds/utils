#!/usr/bin/env python

import sys
from subprocess import check_output, check_call, CalledProcessError

def debug(msg):
	if verbose:
		print msg

git = "/usr/bin/git"

#
# Command line arguments
# Currently only 1 possible argument so no need for
# real argument parsing
#
verbose = True if "-v" in sys.argv else False

#
# First, prune remote branches that no
# longer exist on the server
#
debug("About to prune remote branches")

try:
	check_call([git, "remote", "prune", "origin"])
except CalledProcessError as e:
	print "Failed to prune remote branches:" + str(e)
	exit(1)

#
# Now build lists of local and remote branches
#
debug("About to build lists of remote and local branches")

try:
	output = check_output([git, "branch", "-a"])
	debug("Output from git branch -a:\n" + output)
except CalledProcessError as e:
	print "Failed to list all branches:" + str(e)
	exit(2)

locals, remotes = [], []
current = None
for branch in output.splitlines():
	branch = branch.strip()
	#
	# If the output line starts with a "*" then
	# this is the currently checked out branch
	#
	if branch.startswith("* "):
		branch = branch[2:]
		current = branch
	#
	# Append to the appropriate list
	#
	remotes.append(branch) if branch.startswith("remotes/") else locals.append(branch)

debug("Current branch: " + current)
debug("Local branches:\n\t" + "\n\t".join(locals))
debug("Remote branches:\n\t" + "\n\t".join(remotes))

#
# Go through each local branch and check if there is a
# corresponding remote branch. If not, delete the local branch
#
for branch in locals:
	if "remotes/origin/" + branch in remotes:
		debug("Local branch " + branch + " has a corresponding remote branch")
	elif branch == current:
		print "Cannot delete current branch: " + branch
	else:
		debug("Deleting branch " + branch)
		try:
			check_call([git, "branch", "-D", branch])
		except CalledProcessError as e:
			print "Failed to delete branch" + branch + ":" + str(e)
			exit(3)

exit(0)