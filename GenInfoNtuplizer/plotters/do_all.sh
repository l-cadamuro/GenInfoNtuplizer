for i in leptons photons taus jetmet; do echo $i ; python make_TDR_plot.py $i; echo "" ; done
