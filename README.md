gitcoach 0.1
============

Gitlearn and gitcoach are a pair of tools for helping me, and hopefully 
other people, better understand large projects living in Git by trying
to identify codependent pieces of code.  

It works by examining the entire commit history of a project and building a
matrix to indicate how often different files are committed at the same time.

You start that by cd'ing into your repo and running 'gitlearn'. This creates
a big (sometimes quite big) file in the .git objdir called "coaching_data".
This can take some time, sometimes quite some time. 

Once you've done that, "gitcoach" will take a look at whatever you've modified
in your current commit, and make suggestions based on that information; basically,
if you changed this file, there's an 85% chance you'll have to change this other
file over here... 

