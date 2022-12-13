WorldOfTanks:
	echo "#!/bin/bash" > WorldOfTanks
	echo "pypy3 world_of_tanks.py \"\$$@\"" >> WorldOfTanks
	chmod u+x WorldOfTanks