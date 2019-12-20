# echo "VBF_Hinv"
# crab submit -c crab_submit.py \
#  General.requestName=VBF_Hinv \
#  Data.outputDatasetTag=VBF_Hinv \
#  Data.inputDataset=/VBF_HToInvisible_M125_14TeV_powheg_pythia8/PhaseIITDRSpring19DR-NoPU_106X_upgrade2023_realistic_v3-v2/GEN-SIM-DIGI-RAW \
#  JobType.psetName="analyze_nominiAOD.py"

# echo "SMS-TChiWZ_ZToLL_mChargino-400_mLsp-375"
# crab submit -c crab_submit.py \
#  General.requestName=SMS-TChiWZ_ZToLL_mChargino-400_mLsp-375 \
#  Data.outputDatasetTag=SMS-TChiWZ_ZToLL_mChargino-400_mLsp-375 \
#  Data.inputDataset=/SMS-TChiWZ_ZToLL_mChargino-400_mLsp-375_TuneCUETP8M1_14TeV-madgraphMLM-pythia8/PhaseIISpr18AODMiniAOD-PU200_93X_upgrade2023_realistic_v5-v1/MINIAODSIM \
#  JobType.psetName="analyze_miniAOD.py"

# echo "SMS-SMS-TChiWZ_ZToLL_mChargino-300_mLsp-292p5"
# crab submit -c crab_submit.py \
#  General.requestName=SMS-SMS-TChiWZ_ZToLL_mChargino-300_mLsp-292p5 \
#  Data.outputDatasetTag=SMS-SMS-TChiWZ_ZToLL_mChargino-300_mLsp-292p5 \
#  Data.inputDataset=/SMS-TChiWZ_ZToLL_mChargino-300_mLsp-292p5_TuneCUETP8M1_14TeV-madgraphMLM-pythia8/PhaseIISpr18AODMiniAOD-PU200_93X_upgrade2023_realistic_v5-v1/MINIAODSIM \
#  JobType.psetName="analyze_miniAOD.py"

# echo "SMS-TChiWZ_ZToLL_mChargino-300_mLsp-250"
# crab submit -c crab_submit.py \
#  General.requestName=SMS-TChiWZ_ZToLL_mChargino-300_mLsp-250 \
#  Data.outputDatasetTag=SMS-TChiWZ_ZToLL_mChargino-300_mLsp-250 \
#  Data.inputDataset=/SMS-TChiWZ_ZToLL_mChargino-300_mLsp-250_TuneCUETP8M1_14TeV-madgraphMLM-pythia8/PhaseIISpr18AODMiniAOD-PU200_93X_upgrade2023_realistic_v5-v1/MINIAODSIM \
#  JobType.psetName="analyze_miniAOD.py"
 
# echo "singleTop_tch"
# crab submit -c crab_submit.py \
#  General.requestName=singleTop_tch \
#  Data.outputDatasetTag=singleTop_tch \
#  Data.inputDataset=/ST_tch_14TeV_antitop_incl-powheg-pythia8-madspin/PhaseIISpr18AODMiniAOD-PU200_93X_upgrade2023_realistic_v5_ext1-v1/MINIAODSIM \
#  JobType.psetName="analyze_miniAOD.py"

# echo "ttbar"
# crab submit -c crab_submit.py \
#  General.requestName=ttbar \
#  Data.outputDatasetTag=ttbar \
#  Data.inputDataset=/TTbar_14TeV_TuneCP5_Pythia8/PhaseIITDRSpring19DR-NoPU_106X_upgrade2023_realistic_v3-v1/GEN-SIM-DIGI-RAW \
#  JobType.psetName="analyze_nominiAOD.py"

# echo "Hgg"
# crab submit -c crab_submit.py \
#  General.requestName=Hgg \
#  Data.outputDatasetTag=Hgg \
#  Data.inputDataset=/GluGluHToGG_M125_14TeV_amcatnloFXFX_pythia8/PhaseIITDRSpring19DR-NoPU_106X_upgrade2023_realistic_v3-v1/GEN-SIM-DIGI-RAW \
#  JobType.psetName="analyze_nominiAOD.py"

# echo "ggHH_bbtautau"
# crab submit -c crab_submit.py \
#  General.requestName=ggHH_bbtautau \
#  Data.outputDatasetTag=ggHH_bbtautau \
#  Data.inputDataset=/GluGluToHHTo2B2Tau_node_SM_14TeV-madgraph/PhaseIITDRFall17DR-PU200_93X_upgrade2023_realistic_v2-v2/GEN-SIM-RECO \
#  JobType.psetName="analyze_nominiAOD.py"

# echo "ggHH_bbgg"
# crab submit -c crab_submit.py \
#  General.requestName=ggHH_bbgg \
#  Data.outputDatasetTag=ggHH_bbgg \
#  Data.inputDataset=/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/PhaseIISpr18AODMiniAOD-PU200_93X_upgrade2023_realistic_v5-v1/MINIAODSIM \
#  JobType.psetName="analyze_miniAOD.py"
 
# echo "ggHH_bbbb"
# crab submit -c crab_submit.py \
#  General.requestName=ggHH_bbbb \
#  Data.outputDatasetTag=ggHH_bbbb \
#  Data.inputDataset=/GluGluToHHTo4B_node_SM_14TeV-madgraph/PhaseIISpr18AODMiniAOD-PU200_93X_upgrade2023_realistic_v5-v1/MINIAODSIM \
#  JobType.psetName="analyze_miniAOD.py"

# echo "ZH_HToBB_ZToNuNu"
# crab submit -c crab_submit.py \
#  General.requestName=ZH_HToBB_ZToNuNu \
#  Data.outputDatasetTag=ZH_HToBB_ZToNuNu \
#  Data.inputDataset=/ZH_HToBB_ZToNuNu_M125_14TeV_powheg_pythia8_TuneCP5/PhaseIITDRSpring19DR-PU200_106X_upgrade2023_realistic_v3-v1/AODSIM \
#  JobType.psetName="analyze_nominiAOD.py"

echo "ggHH_bbtautau_alllep"
crab submit -c crab_submit.py \
 General.requestName=ggHH_bbtautau_alllep \
 Data.outputDatasetTag=ggHH_bbtautau_alllep \
 Data.inputDataset=/GluGluToHHTo2B2Tau_node_SM_14TeV-madgraph/PhaseIITDRFall17DR-PU200_93X_upgrade2023_realistic_v2-v2/GEN-SIM-RECO \
 JobType.psetName="analyze_nominiAOD.py"

echo "ggHH_bbtautau_alllep_vMiniAOD"
crab submit -c crab_submit.py \
 General.requestName=ggHH_bbtautau_alllep_vMiniAOD \
 Data.outputDatasetTag=ggHH_bbtautau_alllep_vMiniAOD \
 Data.inputDataset=/GluGluToHHTo2B2Tau_node_SM_14TeV-madgraph/PhaseIITDRFall17MiniAOD-PU200_93X_upgrade2023_realistic_v2-v3/MINIAODSIM \
 JobType.psetName="analyze_miniAOD.py"
