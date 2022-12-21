echo "Hi Professor Glenn! Happy Holidays!"
echo "This test script will take about a minute to run, and will show you a Greedy vs Random agent,"
echo "then a pretrained q-learning agent against the random agent, then the q-learning agent against the greedy agent."
echo "More information is availble in the README."
echo

echo "Results of 10k battles of Greedy agent vs Random agent:"
./WorldOfTanks --get-baselines --greedy-v-random

echo
echo "Results of 10k battles of pre-trained (on 100k battles) Q-learning agent vs random agent:"
./WorldOfTanks --train-q-learning --q-v-random --use-pretrained

echo
echo "Results of 10k battles of pre-trained (on 100k battles) Q-learning agent vs greedy agent:"
./WorldOfTanks --train-q-learning --q-v-greedy --use-pretrained

echo
echo "More options, including training your own model, available in the README."