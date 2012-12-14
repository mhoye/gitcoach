install:
	chmod +x gitcoach.py gitlearn.py
	cp gitcoach.py /usr/local/bin/gitcoach
	cp gitlearn.py /usr/local/bin/gitlearn

uninstall: 
	if [ -e /usr/local/bin/gitcoach ] ; then rm /usr/local/bin/gitcoach ; fi
	if [ -e /usr/local/bin/gitlearn ] ; then rm /usr/local/bin/gitlearn ; fi

