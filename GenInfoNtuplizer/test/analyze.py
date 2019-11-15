# define basic process
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing
import os


process = cms.Process("GenNtuplizer")
# from Configuration.StandardSequences.Eras import eras
# process = cms.Process("L1", eras.Phase2_timing)

# import standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
# process.load('Configuration.StandardSequences.MagneticField_cff')
# process.load('Configuration.Geometry.GeometryExtended2023D41Reco_cff') ## this needs to match the geometry you are running on
# process.load('Configuration.Geometry.GeometryExtended2023D41_cff')     ## this needs to match the geometry you are running on

process.load('Configuration.StandardSequences.EndOfProcess_cff')

# input
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

###### cmd line opts for batch
options = VarParsing.VarParsing ('analysis')
options.inputFiles = []
options.outputFile = 'gen_prova.root'
options.register ('isMiniAOD',
                  0, # default value
                  VarParsing.VarParsing.multiplicity.singleton, # singleton or list
                  VarParsing.VarParsing.varType.int,          # string, int, or float
                  "is a miniAOD sample (0 for false, 1 for true)")

options.parseArguments()

isMiniAOD = False if options.isMiniAOD == 0 else True
print '... is this a miniAOD sample ? ', isMiniAOD

if options.inputFiles:
  Source_Files = cms.untracked.vstring(options.inputFiles)
else:
  Source_Files = cms.untracked.vstring(
    # '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/NoPU_106X_upgrade2023_realistic_v3-v2/130000/1B1BB01A-5960-E540-AABC-1FAFE6F0E50F.root'
    # '/store/mc/PhaseIITDRSpring19DR/GluGluHToGG_M125_14TeV_amcatnloFXFX_pythia8/GEN-SIM-DIGI-RAW/NoPU_106X_upgrade2023_realistic_v3-v1/40000/0FE19D47-13FA-1E45-8679-7787AA85CDAE.root',
    # 'file:../../../../../test_files/Hgg/0FE19D47-13FA-1E45-8679-7787AA85CDAE.root'
    # 'file:../../../../../test_files/HHbbtt/02848F03-40B8-E711-AA50-0025905B85A0.root'
    # '/store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2Tau_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v2/30000/02848F03-40B8-E711-AA50-0025905B85A0.root'
    # '/store/mc/PhaseIITDRSpring19DR/TTbar_14TeV_TuneCP5_Pythia8/GEN-SIM-DIGI-RAW/NoPU_106X_upgrade2023_realistic_v3-v1/230000/0023029B-F85F-AD4B-8D25-4D7255ABD76F.root'
    '/store/mc/PhaseIISpr18AODMiniAOD/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/MINIAODSIM/PU200_93X_upgrade2023_realistic_v5-v1/70000/08971661-9645-E811-B6FD-44A842CF05BF.root'
  )

process.source = cms.Source("PoolSource",
    fileNames = Source_Files,
)

process.TFileService = cms.Service('TFileService',
    fileName = cms.string(options.outputFile)
)

process.GenNtuplizer = cms.EDAnalyzer("GenNtuplizer",
    #
    genMET      = cms.InputTag("genMetTrue"),
    do_met      = cms.bool(True),
    # also note that in miniAOD there is a cut on slimmedGenJets with pT > 8 GeV -> HT is by construction HT8
    genJets     = cms.InputTag("slimmedGenJets" if isMiniAOD else "ak4GenJets"), # note: slimmedGenJets are nonu in miniAOD
    genJetsNoNu = cms.InputTag("slimmedGenJets" if isMiniAOD else "ak4GenJetsNoNu"), # note: slimmedGenJets are nonu in miniAOD
    do_genjets  = cms.bool(True),
    #
    genParticles = cms.InputTag("prunedGenParticles" if isMiniAOD else "genParticles"),
    do_gammas    = cms.bool(True),
    do_taus      = cms.bool(True),
    do_electrons = cms.bool(True),
    do_muons     = cms.bool(True),
)

process.Ntuples = cms.Path(
    process.GenNtuplizer
)

# Silence output
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

