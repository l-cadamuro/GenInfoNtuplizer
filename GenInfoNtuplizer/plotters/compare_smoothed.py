import ROOT
ROOT.gROOT.SetBatch(True)
flist = ['histo_photons.root', 'histo_taus.root', 'histo_jetmet.root', 'histo_leptons.root']
c1 = ROOT.TCanvas()
pad1 = ROOT.TPad("pad1", "The pad 80% of the height",0.0,0.2,1.0,1.0)
pad2 = ROOT.TPad("pad2", "The pad 20% of the height",0.0,0.0,1.0,0.2)
pad1.Draw()
pad2.Draw()
pad2.SetGridy()

smooth_tag = 's_' # at the beginning of file name

for fname in flist:
    fIn = ROOT.TFile.Open(fname)
    histos = [l.GetName() for l in fIn.GetListOfKeys()] #  if isinstance(l, ROOT.TH1)
    print histos
    non_smooth = [h for h in histos if h[:2] != smooth_tag]
    smooth     = [h for h in histos if h[:2] == smooth_tag]

    print 'non_smooth : ', non_smooth
    print 'smooth : ', smooth

    for h in non_smooth:
        print h
        print smooth_tag + h
        hIn_ns = fIn.Get(h)
        hIn_s  = fIn.Get(smooth_tag + h)

        # hIn_ns.SetDirectory(0)
        # hIn_s.SetDirectory(0)

        hIn_ns.SetLineColor(ROOT.kBlack)
        hIn_ns.SetLineWidth(1)
        hIn_ns.SetMarkerColor(ROOT.kBlack)
        
        hIn_s.SetLineColor(ROOT.kRed)
        hIn_s.SetLineWidth(1)
        hIn_s.SetMarkerColor(ROOT.kRed)
        
        # hIn_ns.Draw()
        # hIn_s.Draw('same')
        # rp = ROOT.TRatioPlot(hIn_s, hIn_ns);
        
        # rp.Draw()
        # rp.GetLowerRefGraph().GetYaxis().SetRangeUser(0,2)
        # rp.Draw()

        pad1.cd()
        hIn_ns.Draw()
        hIn_s.Draw('same')

        pad2.cd()
        hr = hIn_ns.Clone('ratio_%s' % hIn_ns.GetName())
        hr.Divide(hIn_s)
        hr.Draw()

        c1.Update()
        c1.Print('smooth_comp/%s.pdf' % (h.replace('-', '_')) , 'pdf')