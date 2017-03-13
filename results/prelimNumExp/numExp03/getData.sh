
function singleRun {
  w=$1
  python main_parameterStudy_piezoWidth.py $w > ./data/cmpSignals_DC1_w${w}.dat
}


singleRun 0.200
singleRun 0.150
#singleRun 0.100
#singleRun 0.050
#singleRun 0.025
#singleRun 0.010
#singleRun 0.005


