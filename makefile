test:
	echo "#!/bin/bash" > WorldOfTanks
	echo "pypy3 test_q_wot.py \"\$$@\"" >> WorldOfTanks
	chmod u+x WorldOfTanks

test_local:
	echo "#!/bin/bash" > WorldOfTanks
	echo "pypy3/bin/pypy3.9 test_q_wot.py \"\$$@\"" >> WorldOfTanks
	chmod u+x WorldOfTanks