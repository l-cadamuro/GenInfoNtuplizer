import ROOT
import sys
import collections
from scipy.signal import savgol_filter
from array import array
import numpy as np

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

def make_histogram(tIn, expr, cut, bounds, hname):
    hformat = 'h (%i, %f, %f)' % (bounds[0], bounds[1], bounds[2])
    tIn.Draw(expr + ' >> ' + hformat, cut)
    myh = ROOT.gPad.GetPrimitive("h");
    out_h = myh.Clone(hname)
    out_h.SetDirectory(0)
    return out_h


def make_extra_texts(testo = 'Thresholds at same rate', linepos = 0.505):
    xtxt = 0.15
    ytxt = 0.91
    textsize = 20

    cmsheader_1 = ROOT.TLatex(xtxt, ytxt, 'CMS')
    cmsheader_1.SetNDC(True)
    cmsheader_1.SetTextFont(63)
    cmsheader_1.SetTextSize(textsize)

    cmsheader_2 = ROOT.TLatex(xtxt + 0.08, ytxt, 'Phase-2 Simulation')
    cmsheader_2.SetNDC(True)
    cmsheader_2.SetTextFont(53)
    cmsheader_2.SetTextSize(textsize)

    # cmsheader_3 = ROOT.TLatex(0.9, ytxt, '14 TeV, 3000 fb^{-1}')
    cmsheader_3 = ROOT.TLatex(0.9, ytxt, '14 TeV')
    cmsheader_3.SetNDC(True)
    cmsheader_3.SetTextFont(43)
    cmsheader_3.SetTextAlign(31)
    cmsheader_3.SetTextSize(textsize-2)

    msg = ROOT.TLatex(0.88, ytxt-0.05, testo)
    msg.SetNDC(True)
    msg.SetTextFont(43)
    msg.SetTextAlign(31)
    msg.SetTextSize(textsize-2)

    # lw = 0.045
    # fakeL1 = ROOT.TLine(linepos, ytxt-0.05+0.01+0.01, linepos+lw, ytxt-0.05+0.01+0.01)
    lw = 0.03
    fakeL1 = ROOT.TLine(linepos, ytxt-0.05-0.01+0.01-0.003, linepos, ytxt-0.05-0.01+0.01+lw-0.003)
    fakeL1.SetNDC(True)
    fakeL1.SetLineStyle(1)
    fakeL1.SetLineWidth(2)
    fakeL1.SetLineColor(ROOT.kBlack)

    # fakeL2 = ROOT.TLine(linepos, ytxt-0.05-0.01+0.01, linepos+lw, ytxt-0.05-0.01+0.01)
    fakeL2 = ROOT.TLine(linepos+0.03, ytxt-0.05-0.01+0.01-0.003, linepos+0.03, ytxt-0.05-0.01+0.01+lw-0.003)
    fakeL2.SetNDC(True)
    fakeL2.SetLineStyle(7)
    fakeL2.SetLineWidth(2)
    fakeL2.SetLineColor(ROOT.kBlack)
    
    # cmsheader_1.Draw()
    # cmsheader_2.Draw()
    # cmsheader_3.Draw()

    etxts = [cmsheader_1, cmsheader_2, cmsheader_3, msg, fakeL1, fakeL2]
    return etxts

def setStyle(frame, c1):
    c1.SetFrameLineWidth(3)
    c1.SetBottomMargin(0.13)
    c1.SetLeftMargin(0.13)
    frame.GetXaxis().SetTitleSize(0.05)
    frame.GetYaxis().SetTitleSize(0.05)
    frame.GetXaxis().SetLabelSize(0.045)
    frame.GetYaxis().SetLabelSize(0.045)


files = {
    'singleTop_tch'               : '../test/ntuples/singleTop_tch.root',
    'ttbar'                       : '../test/ntuples/ttbar.root',
    'ggHH_bbtautaulep'            : '../test/ntuples/ggHH_bbtautau_alltaulep.root',
    ##
    'Hgg'                         : '../test/ntuples/Hgg.root',
    'ggHH_bbgg'                   : '../test/ntuples/ggHH_bbgg.root',
    ##
    'ggHH_bbtautau'               : '../test/ntuples/ggHH_bbtautau.root',
    ##
    'chargino-300_mLsp-292p5'     : '../test/ntuples/SMS-SMS-TChiWZ_ZToLL_mChargino-300_mLsp-292p5.root',
    'chargino-300_mLsp-250'       : '../test/ntuples/SMS-TChiWZ_ZToLL_mChargino-300_mLsp-250.root',
    'chargino-400_mLsp-375'       : '../test/ntuples/SMS-TChiWZ_ZToLL_mChargino-400_mLsp-375.root',
    'VBF_Hinv'                    : '../test/ntuples/VBF_Hinv.root',
    'ZHinv'                       : '../test/ntuples/ZHnunu.root',
    'ggHH_bbbb'                   : '../test/ntuples/ggHH_bbbb.root',
}

colors = {
    # 'singleTop_tch'    : ROOT.TColor.GetColor('#32CD32'),
    # 'ttbar'            : ROOT.TColor.GetColor('#228B22'),
    # 'ggHH_bbtautaulep' : ROOT.TColor.GetColor('#186218'),
    ###
    'singleTop_tch'    : ROOT.TColor.GetColor('#0EA7B5'),
    'ttbar'            : ROOT.TColor.GetColor('#0C457D'),
    'ggHH_bbtautaulep' : ROOT.TColor.GetColor('#E8702A'),
    ###
    'Hgg'       : ROOT.kRed,
    'ggHH_bbgg' : ROOT.kOrange+1,
    ###
    'ggHH_bbtautau' : ROOT.TColor.GetColor('#482E92'),
    ###
    'chargino-300_mLsp-292p5'     : ROOT.kBlue-6,
    'chargino-300_mLsp-250'       : ROOT.kBlue+3,
    'chargino-400_mLsp-375'       : ROOT.kBlue+2,
    'VBF_Hinv'                    : ROOT.kAzure,
    'ZHinv'                       : ROOT.kAzure, #ROOT.kBlue,
    # 'ggHH_bbbb'                   : ROOT.kAzure+5,
    'ggHH_bbbb'                   : ROOT.kMagenta+1,
}

# - leading mu: 22
# - leading e (isolated): 28
# - sub tau: 50
# - sub pho: 12
# - HT: 460
# - MET: 200
# - fourth jet: 40

# ### name -> value, [panels]
# ### all the thresholds here will be plotted
# thresholds = {
#     'lead mu'    : (22,  ['leptons']),
#     'lead e'     : (28,  ['leptons']),
#     'sub tau'    : (50,  ['taus']),
#     'sub pho'    : (12,  ['photons']),
#     'HT'         : (460, ['jetmet']),
#     'MET'        : (200, ['jetmet']),
#     'fourth jet' : (40,  ['jetmet']),
# }

do_legend = False

#phase2, phase1
thr_vals = {
    # 'lead mu'    : (22,  50),
    'lead mu'    : (15,  24),
    'lead e'     : (28,  62),
    # 'sub tau'    : (52,  115),
    'sub tau'    : (36,  90),
    'sub pho'    : (12,  20),
    'HT'         : (450, 650),
    'MET'        : (200, 390),
    'fourth jet' : (40,  85),
}

thr_cols = {
    'lead mu'    : ROOT.TColor.GetColor('#123524'),
    'lead e'     : ROOT.TColor.GetColor('#587246'),
    'sub tau'    : ROOT.TColor.GetColor('#2B1C58'),
    'sub pho'    : ROOT.kRed-3,
    'HT'         : ROOT.kMagenta+1,
    'MET'        : ROOT.kBlue+4,
    'fourth jet' : ROOT.kMagenta+1,
}

panels = collections.OrderedDict()
# panels['leptons'] = ['singleTop_tch', 'ttbar']
panels['leptons'] = ['singleTop_tch', 'ttbar', 'ggHH_bbtautaulep']
panels['photons'] = ['Hgg', 'ggHH_bbgg']
panels['taus']    = ['ggHH_bbtautau']
# panels['jetmet']  = ['chargino-300_mLsp-292p5', 'chargino-300_mLsp-250', 'chargino-400_mLsp-375', 'VBF_Hinv', 'ggHH_bbbb']
# panels['jetmet']  = ['chargino-300_mLsp-292p5', 'VBF_Hinv', 'ZHinv']
# panels['jetmet']  = ['chargino-300_mLsp-292p5', 'VBF_Hinv']
panels['jetmet']  = ['chargino-300_mLsp-292p5', 'ZHinv']
# panels['jetmet']  = ['chargino-300_mLsp-292p5']
# panels['jetmet']  = ['chargino-300_mLsp-292p5', 'chargino-300_mLsp-250', 'chargino-400_mLsp-375']
# panels['jetmet']  = ['chargino-300_mLsp-292p5', 'VBF_Hinv']

thispanel = 'jetmet'
if len(sys.argv) > 1:
    thispanel = sys.argv[1]

if not thispanel in panels:
    print "[ERROR] I do not recognize this type of plot: ", thispanel
    raise RuntimeError("plot type")



do_smooth = -1 ## n smoothing, <= 0 for none
do_savgol_filter = True
do_fit = False
noerr = True

if thispanel == 'jetmet':
    do_savgol_filter = False    
    do_fit = True

draw_style = 'hist ][' #hist, p

# boundaries = {
#     'leptons' : (50*3, 0, 150),
#     'photons' : (70*2, 0, 140),
#     # 'taus'    : (50*3, 0, 100),
#     'taus'    : (195, 0, 130),
#     # 'jetmet'  : (140, 0, 500),
#     # 'jetmet'  : (140*3, 150, 800),
#     'jetmet'  : (140*3, 101, 799),
# }

boundaries = {
    'leptons' : (50*3, 0.1, 150.1),
    'photons' : (110, 0.1, 129.9),
    # 'taus'    : (50*3, 0, 100),
    'taus'    : (195, 0.1, 130.1),
    # 'jetmet'  : (140, 0, 500),
    # 'jetmet'  : (140*3, 150, 800),
    'jetmet'  : (140*3, 100.1, 799.9),
}

thresholds = {
    'leptons' : ('lead mu', 'lead e'),
    'photons' : ('sub pho', ),
    'taus'    : ('sub tau', ),
    # 'jetmet'  : ('fourth jet', 'MET'), ### NB: must be in synch with the vars plotted, see "toplot"
    'jetmet'  : ('MET', ), ### NB: must be in synch with the vars plotted, see "toplot"
}

frames = {
    'leptons'  : ROOT.TH1D('frame_leptons' , ';Lepton p_{T} [GeV]; Arbitrary units', *boundaries['leptons']),
    'photons'  : ROOT.TH1D('frame_photons' , ';Photon p_{T} [GeV]; Arbitrary units', *boundaries['photons']),
    'taus'     : ROOT.TH1D('frame_taus'    , ';Visible #tau_{h} p_{T} [GeV]; Arbitrary units', *boundaries['taus']),
    'jetmet'   : ROOT.TH1D('frame_jetmet'  , ';E_{T}^{miss} [GeV]; Arbitrary units', *boundaries['jetmet']),
}

## (window_size, order poly), [boundaries excluding low and high - empty for all] [regions where to make the smooth with ROOT and not with savgol, with an index starting from 0 in the pieces]
savgol_params = {
   'singleTop_tch' :    ( (31, 6) , [], []), #
    'ttbar'        :    ( (101, 6), [12], [0]), #
    'ggHH_bbtautaulep': ( (91, 4), [5], [0]), #
    ##
    'Hgg'          : ( (31, 5), [62, 80], [] ),#
    # 'ggHH_bbgg'    : ( (101, 11), [20, 40], [0]),# no savgol in the frist bin i.e. < 20
    'ggHH_bbgg'    : ( (101, 5), [15], [0]),# no savgol in the frist bin i.e. < 20
    ##
    'ggHH_bbtautau' : ( (101, 3), [], [] ),#
    ##
    'chargino-300_mLsp-292p5' : ( (201, 3) , [], []),
    'VBF_Hinv'                : ( (201, 3) , [], []),
}

fitas = {
    'chargino-300_mLsp-292p5' : ROOT.TF1("f1", "TMath::Exp([0] + [1]*x)", 0, 1000),
    'VBF_Hinv'                : ROOT.TF1("f2", "TMath::Exp([0] + [1]*x)", 0, 1000),
    'ZHinv'                   : ROOT.TF1("f3", "TMath::Exp([0] + [1]*x)", 0, 1000),
}

## obtained by first doing fit(expo)
fitas['chargino-300_mLsp-292p5'].SetParameters(-3.12233e-01, -9.58011e-03)
fitas['VBF_Hinv'].SetParameters(1.59611e+00, -1.71427e-02)
fitas['ZHinv'].SetParameters(1.59611e+00, -1.71427e-02)

### (expr, cut)
toplot = {
    # 'singleTop_tch'               : ('mu1_pt', 'nmus == 1 && neles == 0 && TMath::Abs(mu1_eta) < 2.4'),
    'singleTop_tch'               : ('ele1_pt > 0 ? ele1_pt : mu1_pt', '(neles + nmus) == 1 && (ele1_pt > 0 ? TMath::Abs(ele1_eta) < 2.4 : TMath::Abs(mu1_eta) < 2.4)'),
    'ttbar'                       : ('ele1_pt > 0 ? ele1_pt : mu1_pt', '(neles + nmus) == 1 && (ele1_pt > 0 ? TMath::Abs(ele1_eta) < 2.4 : TMath::Abs(mu1_eta) < 2.4)'), ## plot togehter ele and mu
    'ggHH_bbtautaulep'            : ('taue1_pt > 0 ? taue1_pt : taumu1_pt', '(ntause + ntausmu) == 1 && ntaushad == 1 && ntaus == 2 && (taue1_pt > 0 ? TMath::Abs(taue1_eta) < 2.4 : TMath::Abs(taumu1_eta) < 2.4)'), ## plot togehter ele and mu
    # 'ggHH_bbtautaulep'            : ('taumu1_pt', 'ntausmu == 1 && TMath::Abs(taumu1_eta) < 2.4'), ## plot togehter ele and mu
    # 'ttbar'                       : ('ele1_pt', 'neles == 1 && nmus == 0 && TMath::Abs(ele1_eta) < 2.4'),
    # 'ttbar'                       : ('mu1_pt',  'nmus == 1 && neles == 0 && TMath::Abs(mu1_eta) < 2.4'),
    ###
    'Hgg'                         : ('gamma2_pt', 'ngammas == 2 && TMath::Abs(gamma2_eta) < 2.4'),
    'ggHH_bbgg'                   : ('gamma2_pt', 'ngammas == 2 && TMath::Abs(gamma2_eta) < 2.4'),
    ###
    'ggHH_bbtautau'               : ('tauh2_pt',  'ntaushad == 2 && ntaus == 2 && TMath::Abs(tauh1_eta) < 2.4 && TMath::Abs(tauh2_eta) < 2.4'),
    ###
    'chargino-300_mLsp-292p5'     : ('met',          'met > 0'),  ### dummy cut
    'chargino-300_mLsp-250'       : ('met',          'met > 0'),  ### dummy cut
    'chargino-400_mLsp-375'       : ('met',          'met > 0'),  ### dummy cut
    'VBF_Hinv'                    : ('met',          'met > 0'),  ### dummy cut
    'ZHinv'                       : ('met',          'met > 0'),  ### dummy cut
    # 'ggHH_bbbb'                   : ('genjet4_nonu_pt',   'genjet4_nonu_pt > 0 && TMath::Abs(genjet4_nonu_eta) < 2.4 && TMath::Abs(genjet3_nonu_eta) < 2.4 && TMath::Abs(genjet2_nonu_eta) < 2.4 && TMath::Abs(genjet1_nonu_eta) < 2.4'),
    'ggHH_bbbb'                   : ('HT_ER_30',   '1==1'),
}

# texts_rate = {
#     # 'leptons' : 'Thresholds for a rate of 11.7 kHz (#mu), 23.9 kHz (e)',
#     'leptons' : 'Thresholds for a rate of 42 kHz (#mu), 23.9 kHz (e)',
#     'photons' : 'Thresholds for a rate of 50.2 kHz',
#     'taus'    : 'Thresholds for a rate of 6.6 kHz',
#     'jetmet'  : 'Thresholds for a rate of 18.1 kHz',
# }

texts_rate = {
    # 'leptons' : 'Thresholds for a rate of 11.7 kHz (#mu), 23.9 kHz (e)',
    'leptons' : 'Thresholds for a rate of 42 kHz (#mu), 24 kHz (e)',
    'photons' : 'Thresholds for a rate of 50 kHz',
    'taus'    : 'Thresholds for a rate of 6.6 kHz',
    'jetmet'  : 'Thresholds for a rate of 18 kHz',
}

# linepos = {
#     'leptons' : 0.18,
#     'photons' : 0.4,
#     'taus'    : 0.4,
#     'jetmet'  : 0.4,
# }

linepos = {
    'leptons' : 0.18+0.05,
    'photons' : 0.4+0.02,
    'taus'    : 0.4+0.02,
    'jetmet'  : 0.4+0.02,
}

c1 = ROOT.TCanvas('c1', 'c1', 600, 600)
c1.SetFrameLineWidth(3)
# c1.SetLogy()

thishistos = collections.OrderedDict()
orighistos = collections.OrderedDict()

print '>>>> plot for', thispanel
for sample in panels[thispanel]:
    print "... doing", sample
    fIn = ROOT.TFile.Open(files[sample])
    tIn = fIn.Get('GenNtuplizer/GenTree')
    print "....... sample contains", tIn.GetEntries(), 'events'
    hIn = make_histogram(tIn=tIn, expr=toplot[sample][0], cut=toplot[sample][1], bounds=boundaries[thispanel], hname=sample)
    print "....... passing the selection cuts", hIn.Integral(-1,-1)
    if hIn.Integral() > 0:
        hIn.Scale(100./hIn.Integral())
    else:
        print ".... [ERROR] histo for", sample, 'is empty'
    hIn.SetLineColor(colors[sample])
    hIn.SetMarkerColor(colors[sample])
    hIn.SetMarkerStyle(8)
    hIn.SetMarkerSize(0.6)

    if 'hist' in draw_style:
        hIn.SetLineWidth(4)

    newHisto = hIn.Clone('s_' + hIn.GetName())
    newHisto.SetDirectory(0)
    if do_smooth > 0:
        newHisto.Smooth(do_smooth)
    # thishistos[sample] = hIn

    if do_savgol_filter:
        params = savgol_params[sample][0]
        pieces = savgol_params[sample][1]
        veto   = savgol_params[sample][2]
        if pieces:

            print '... smooth in pieces', pieces
            yhat = []
            for idx in range(len(pieces) + 1):

                if idx == 0:
                    pi   = pieces[idx]
                    y1 = [newHisto.GetBinContent(i) for i in range(1, newHisto.GetNbinsX()+1) if newHisto.GetBinCenter(i) < pi]
                    bounds = [newHisto.GetBinLowEdge(0), pi]
                elif idx == len(pieces):
                    pim1 = pieces[idx-1]
                    y1 = [newHisto.GetBinContent(i) for i in range(1, newHisto.GetNbinsX()+1) if newHisto.GetBinCenter(i) >= pim1]
                    bounds = [pim1, newHisto.GetBinLowEdge(newHisto.GetNbinsX()+1)]
                else:
                    pi   = pieces[idx]
                    pim1 = pieces[idx-1]
                    y1 = [newHisto.GetBinContent(i) for i in range(1, newHisto.GetNbinsX()+1) if newHisto.GetBinCenter(i) >= pim1 and newHisto.GetBinCenter(i) < pi]
                    bounds = [pim1, pi]
                    
                ### no savgol
                if idx in veto:

                    print "... skipping the piece at ", idx, sample

                    # oldrange = (newHisto.GetXaxis().GetFirst(), newHisto.GetXaxis().GetLast())
                    # newHisto.GetXaxis().SetRangeUser(bounds[0], bounds[1]),
                    # newHisto.Smooth(10, 'R')
                    # newHisto.GetXaxis().SetRange(oldrange[0], oldrange[1])
                    
                    yhat = yhat + list(y1)

                    continue


                par0 = min(params[0], len(y1))
                if par0 % 2 == 0 : par0 = par0 -1 # odd
                yhat1 = savgol_filter(y1, par0, params[1])
                yhat = yhat + list(yhat1)

        else:
            print '... smooth in a block'
            y = [newHisto.GetBinContent(i) for i in range(1, newHisto.GetNbinsX()+1)]
            yhat = savgol_filter(y, params[0], params[1])
            print len(y), len(yhat)

        print newHisto.GetNbinsX()+1
        for i in range(1, newHisto.GetNbinsX()+1):
            newHisto.SetBinContent(i, yhat[i-1])

    if do_fit:
        newHisto.Fit(fitas[sample], 'N')
        # newHisto.Fit('expo')
        for i in range(1, newHisto.GetNbinsX()+1):
            newHisto.SetBinContent(i, fitas[sample].Eval(newHisto.GetBinCenter(i)))

    thishistos[sample] = newHisto
    orighistos[sample] = hIn

mmaxs = [h.GetMaximum() for h in thishistos.values()]
mmax = max(mmaxs)

plotmax = 1.15*mmax
if thispanel == 'leptons':
    plotmax = 1.5*mmax

frames[thispanel].SetMaximum(plotmax)
frames[thispanel].SetMinimum(0)

setStyle(frames[thispanel], c1)

frames[thispanel].Draw()
for h in thishistos.values():
    if noerr:
        for i in range (1, h.GetNbinsX()+1):
            h.SetBinError(i, 0)
    h.Draw("%s same" % draw_style)

line_thrs = []
### now plot the thresholds
for idx, thr in enumerate(thresholds[thispanel]):
    thrval_phase2 = thr_vals[thr][0]
    thrval_phase1 = thr_vals[thr][1]

    top_p2 = mmax
    top_p1 = 0.9*top_p2

    if thispanel == 'leptons':
        # top_p2 = (1.35-0.15*idx)*mmax ## for two nearby thresholds
        top_p2 = (1.35-0.25*idx)*mmax ## for two nearby thresholds
        top_p1 = 0.9*top_p2 ## for two nearby thresholds

    line_p2 = ROOT.TLine(thrval_phase2, 0, thrval_phase2, top_p2)
    line_p2.SetLineColor(thr_cols[thr])
    line_p2.SetLineStyle(1)
    line_p2.SetLineWidth(4)

    line_p1 = ROOT.TLine(thrval_phase1, 0, thrval_phase1, top_p1)
    line_p1.SetLineColor(thr_cols[thr])
    line_p1.SetLineStyle(7) #dash : 7, dots : 3
    line_p1.SetLineWidth(4)

    line_thrs.append(line_p1)
    line_thrs.append(line_p2)

    ## now make small arrows to indicate the threshold
    ## they must be wide some % of the plot range

    pw = (boundaries[thispanel][2]-boundaries[thispanel][1])*0.05

    # arrayoffset = 0.1*idx # to scale down when you have > 1 arrow in a plot
    arrayoffset = 0 # to scale down when you have > 1 arrow in a plot

    arr_p2 = ROOT.TArrow(thrval_phase2, (0.95-arrayoffset)*top_p2, thrval_phase2+pw, (0.95-arrayoffset)*top_p2, 0.02, '|>')
    arr_p1 = ROOT.TArrow(thrval_phase1, (0.95-arrayoffset)*top_p1, thrval_phase1+pw, (0.95-arrayoffset)*top_p1, 0.02, '|>')

    arr_p2.SetLineColor(line_p2.GetLineColor())
    arr_p1.SetLineColor(line_p1.GetLineColor())

    arr_p2.SetFillColor(line_p2.GetLineColor())
    arr_p1.SetFillColor(line_p1.GetLineColor())

    arr_p2.SetLineStyle(line_p2.GetLineStyle())
    arr_p1.SetLineStyle(line_p1.GetLineStyle())

    arr_p2.SetLineWidth(line_p2.GetLineWidth())
    arr_p1.SetLineWidth(line_p1.GetLineWidth())

    line_thrs.append(arr_p1)
    line_thrs.append(arr_p2)

for l in line_thrs:
    l.Draw()

etxts = make_extra_texts(testo = texts_rate[thispanel], linepos = linepos [thispanel])
for e in etxts:
    e.Draw()


if do_legend:
    leg = ROOT.TLegend(0.5, 0.5, 0.88, 0.88)
    for sample in panels[thispanel]:
        leg.AddEntry(thishistos[sample], sample, 'l')
    leg.Draw()

c1.Print('histo_%s.pdf' % thispanel, 'pdf')

## now save all histos to file
fOut = ROOT.TFile.Open('histo_%s.root' % thispanel, 'recreate')
for h in thishistos.values():
    h.Write()

for h in orighistos.values():
    h.Write()

