from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'myreqname'
config.General.workArea    = 'crab3'
config.General.transferOutputs = True
config.General.transferLogs    = True

config.JobType.pluginName    = 'Analysis'
config.JobType.psetName      = 'analyze.py'

config.Data.inputDataset     = 'mydataset'
config.Data.inputDBS         = 'global'
config.Data.splitting        = 'FileBased'
config.Data.unitsPerJob      = 5
config.Data.outLFNDirBase    = '/store/user/%s/GenNtuples/' % (getUsernameFromSiteDB())
config.Data.publication      = False
config.Data.outputDatasetTag = 'outtag'

config.Site.storageSite      = 'T3_US_FNALLPC'