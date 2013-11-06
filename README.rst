===============================
gitcoach
===============================

.. image:: https://badge.fury.io/py/gitcoach.png
    :target: http://badge.fury.io/py/gitcoach
    
.. image:: https://travis-ci.org/tarmstrong/gitcoach.png?branch=master
        :target: https://travis-ci.org/tarmstrong/gitcoach

.. image:: https://pypip.in/d/gitcoach/badge.png
        :target: https://crate.io/packages/gitcoach?version=latest


Gitlearn and gitcoach are a pair of tools for helping me, and hopefully 
other people, better understand large projects living in Git by trying
to identify codependent pieces of code.  

* Free software: BSD license
* Documentation: http://gitcoach.rtfd.org.

Installation
------------

The easiest way to install gitcoach is through pip::

    $ pip install gitcoach

Usage
-----

To generate the prediction data, run `gitlearn`. This might take a long time::

    usage: gitlearn [-h]

    Generate coaching data for gitcoach.

    optional arguments:
      -h, --help  show this help message and exit

The `gitcoach` utility::

    usage: gitcoach [-h] [--file FILE] [--commit COMMIT] [--threshold THRESHOLD]

    Find co-dependent files based on git history. Two files are co-dependent if
    they have been modified in the same commits often enough.

    optional arguments:
    -h, --help            show this help message and exit
    --file FILE, -f FILE  Find suggestions for a specific file
    --commit COMMIT, -c COMMIT
                            Find suggestions for files modified in a specific
                            commit.
    --threshold THRESHOLD, -t THRESHOLD
                            Threshold for co-incidence ratio (default=0.8).

