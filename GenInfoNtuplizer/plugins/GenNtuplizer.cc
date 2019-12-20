#ifndef GENNTUPLIZER_H
#define GENNTUPLIZER_H

#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/METReco/interface/GenMET.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/HepMCCandidate/interface/GenStatusFlags.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include <iostream>
#include "TTree.h"
#include "TLorentzVector.h"

using namespace edm;
using namespace reco;
using namespace std;

class GenNtuplizer : public edm::EDAnalyzer {
    public:

        explicit GenNtuplizer(const edm::ParameterSet&);
        virtual ~GenNtuplizer();

    private:
        //----edm control---
        virtual void beginJob();
        virtual void beginRun(edm::Run const&, edm::EventSetup const&);
        virtual void analyze(const edm::Event&, const edm::EventSetup&);
        virtual void endJob();
        virtual void endRun(edm::Run const&, edm::EventSetup const&);
        void initialize();

        // access to gen collections
        edm::EDGetTokenT<std::vector<reco::GenMET> >      genMETToken_;

        edm::EDGetTokenT<std::vector<reco::GenJet> >      genJetToken_;
        edm::EDGetTokenT<std::vector<reco::GenJet> >      genJetNoNuToken_;
        edm::EDGetTokenT<std::vector<reco::GenParticle> > genParticleToken_;

        // flags on things to do
        bool do_met_;
        bool do_genjets_;
        bool do_gammas_;
        bool do_taus_;
        bool do_electrons_;
        bool do_muons_;

        //-----output---
        TTree *tree_;

        float met_x_;
        float met_y_;
        float met_;

        // HT
        float HT_;
        float HT_5_;
        float HT_10_;
        float HT_20_;
        float HT_30_;
        
        // eta 2.5 restriction
        float HT_ER_;
        float HT_ER_5_;
        float HT_ER_10_;
        float HT_ER_20_;
        float HT_ER_30_;

        // jets - from higher to lower in momentum
        int ngenjet_;

        float genjet1_pt_;
        float genjet1_eta_;
        float genjet1_phi_;
        float genjet1_m_;

        float genjet2_pt_;
        float genjet2_eta_;
        float genjet2_phi_;
        float genjet2_m_;

        float genjet3_pt_;
        float genjet3_eta_;
        float genjet3_phi_;
        float genjet3_m_;

        float genjet4_pt_;
        float genjet4_eta_;
        float genjet4_phi_;
        float genjet4_m_;

        // same as above, no nu
        int ngenjet_nonu_;

        float genjet1_nonu_pt_;
        float genjet1_nonu_eta_;
        float genjet1_nonu_phi_;
        float genjet1_nonu_m_;

        float genjet2_nonu_pt_;
        float genjet2_nonu_eta_;
        float genjet2_nonu_phi_;
        float genjet2_nonu_m_;

        float genjet3_nonu_pt_;
        float genjet3_nonu_eta_;
        float genjet3_nonu_phi_;
        float genjet3_nonu_m_;

        float genjet4_nonu_pt_;
        float genjet4_nonu_eta_;
        float genjet4_nonu_phi_;
        float genjet4_nonu_m_;

        // photons
        int ngammas_;

        float gamma1_pt_;
        float gamma1_eta_;
        float gamma1_phi_;
        float gamma1_m_;

        float gamma2_pt_;
        float gamma2_eta_;
        float gamma2_phi_;
        float gamma2_m_;

        // taus
        int ntaus_;
        int ntaushad_;
        int ntause_;
        int ntausmu_;

        float tauh1_pt_;
        float tauh1_eta_;
        float tauh1_phi_;
        float tauh1_m_;

        float tauh2_pt_;
        float tauh2_eta_;
        float tauh2_phi_;
        float tauh2_m_;

        float taue1_pt_;
        float taue1_eta_;
        float taue1_phi_;
        float taue1_m_;

        float taue2_pt_;
        float taue2_eta_;
        float taue2_phi_;
        float taue2_m_;

        float taumu1_pt_;
        float taumu1_eta_;
        float taumu1_phi_;
        float taumu1_m_;

        float taumu2_pt_;
        float taumu2_eta_;
        float taumu2_phi_;
        float taumu2_m_;

        // leptons

        int neles_;

        float ele1_pt_;
        float ele1_eta_;
        float ele1_phi_;
        float ele1_m_;

        int nmus_;

        float mu1_pt_;
        float mu1_eta_;
        float mu1_phi_;
        float mu1_m_;


};

GenNtuplizer::GenNtuplizer(const edm::ParameterSet& iConfig) :
    genMETToken_      (consumes< std::vector<reco::GenMET> >      (iConfig.getParameter<edm::InputTag>("genMET"))),
    genJetToken_      (consumes< std::vector<reco::GenJet> >      (iConfig.getParameter<edm::InputTag>("genJets"))),
    genJetNoNuToken_  (consumes< std::vector<reco::GenJet> >      (iConfig.getParameter<edm::InputTag>("genJetsNoNu"))),
    genParticleToken_ (consumes< std::vector<reco::GenParticle> > (iConfig.getParameter<edm::InputTag>("genParticles"))),
    do_met_           (iConfig.getParameter<bool>("do_met")),
    do_genjets_       (iConfig.getParameter<bool>("do_genjets")),
    do_gammas_        (iConfig.getParameter<bool>("do_gammas")),
    do_taus_          (iConfig.getParameter<bool>("do_taus")),
    do_electrons_     (iConfig.getParameter<bool>("do_electrons")),
    do_muons_         (iConfig.getParameter<bool>("do_muons"))
{
    initialize();

    cout << "[INFO] : starting GenNtuplizer . Summary of settings " << endl;
    cout << "....... do_met       : " << boolalpha << do_met_       << noboolalpha << endl;
    cout << "....... do_genjets   : " << boolalpha << do_genjets_   << noboolalpha << endl;
    cout << "....... do_gammas    : " << boolalpha << do_gammas_    << noboolalpha << endl;
    cout << "....... do_taus      : " << boolalpha << do_taus_      << noboolalpha << endl;
    cout << "....... do_electrons : " << boolalpha << do_electrons_ << noboolalpha << endl;
    cout << "....... do_muons     : " << boolalpha << do_muons_     << noboolalpha << endl;

}

GenNtuplizer::~GenNtuplizer(){

}

void GenNtuplizer::beginJob(){
    edm::Service<TFileService> fs;
    tree_ = fs -> make<TTree>("GenTree", "GenTree");

    // ----------------------- Missing ET

    tree_->Branch("met_x", &met_x_);
    tree_->Branch("met_y", &met_y_);
    tree_->Branch("met",   &met_);

    // ----------------------- HT

    tree_->Branch("HT",       &HT_);
    tree_->Branch("HT_5",     &HT_5_);
    tree_->Branch("HT_10",    &HT_10_);
    tree_->Branch("HT_20",    &HT_20_);
    tree_->Branch("HT_30",    &HT_30_);
    
    tree_->Branch("HT_ER",    &HT_ER_);
    tree_->Branch("HT_ER_5",  &HT_ER_5_);
    tree_->Branch("HT_ER_10", &HT_ER_10_);
    tree_->Branch("HT_ER_20", &HT_ER_20_);
    tree_->Branch("HT_ER_30", &HT_ER_30_);

    // ----------------------- gen jets

    tree_->Branch("ngenjet", &ngenjet_);

    tree_->Branch("genjet1_pt",  &genjet1_pt_);
    tree_->Branch("genjet1_eta", &genjet1_eta_);
    tree_->Branch("genjet1_phi", &genjet1_phi_);
    tree_->Branch("genjet1_m",   &genjet1_m_);

    tree_->Branch("genjet2_pt",  &genjet2_pt_);
    tree_->Branch("genjet2_eta", &genjet2_eta_);
    tree_->Branch("genjet2_phi", &genjet2_phi_);
    tree_->Branch("genjet2_m",   &genjet2_m_);

    tree_->Branch("genjet3_pt",  &genjet3_pt_);
    tree_->Branch("genjet3_eta", &genjet3_eta_);
    tree_->Branch("genjet3_phi", &genjet3_phi_);
    tree_->Branch("genjet3_m",   &genjet3_m_);

    tree_->Branch("genjet4_pt",  &genjet4_pt_);
    tree_->Branch("genjet4_eta", &genjet4_eta_);
    tree_->Branch("genjet4_phi", &genjet4_phi_);
    tree_->Branch("genjet4_m",   &genjet4_m_);


    tree_->Branch("ngenjet_nonu", &ngenjet_nonu_);

    tree_->Branch("genjet1_nonu_pt",  &genjet1_nonu_pt_);
    tree_->Branch("genjet1_nonu_eta", &genjet1_nonu_eta_);
    tree_->Branch("genjet1_nonu_phi", &genjet1_nonu_phi_);
    tree_->Branch("genjet1_nonu_m",   &genjet1_nonu_m_);

    tree_->Branch("genjet2_nonu_pt",  &genjet2_nonu_pt_);
    tree_->Branch("genjet2_nonu_eta", &genjet2_nonu_eta_);
    tree_->Branch("genjet2_nonu_phi", &genjet2_nonu_phi_);
    tree_->Branch("genjet2_nonu_m",   &genjet2_nonu_m_);

    tree_->Branch("genjet3_nonu_pt",  &genjet3_nonu_pt_);
    tree_->Branch("genjet3_nonu_eta", &genjet3_nonu_eta_);
    tree_->Branch("genjet3_nonu_phi", &genjet3_nonu_phi_);
    tree_->Branch("genjet3_nonu_m",   &genjet3_nonu_m_);

    tree_->Branch("genjet4_nonu_pt",  &genjet4_nonu_pt_);
    tree_->Branch("genjet4_nonu_eta", &genjet4_nonu_eta_);
    tree_->Branch("genjet4_nonu_phi", &genjet4_nonu_phi_);
    tree_->Branch("genjet4_nonu_m",   &genjet4_nonu_m_);

    // ----------------------- photons
    tree_->Branch("ngammas",    &ngammas_);

    tree_->Branch("gamma1_pt",  &gamma1_pt_);
    tree_->Branch("gamma1_eta", &gamma1_eta_);
    tree_->Branch("gamma1_phi", &gamma1_phi_);
    tree_->Branch("gamma1_m",   &gamma1_m_);

    tree_->Branch("gamma2_pt",  &gamma2_pt_);
    tree_->Branch("gamma2_eta", &gamma2_eta_);
    tree_->Branch("gamma2_phi", &gamma2_phi_);
    tree_->Branch("gamma2_m",   &gamma2_m_);

    // ----------------------- taus
    tree_->Branch("ntaus",      &ntaus_);
    tree_->Branch("ntaushad",   &ntaushad_);
    tree_->Branch("ntause",     &ntause_);
    tree_->Branch("ntausmu",    &ntausmu_);

    tree_->Branch("tauh1_pt",   &tauh1_pt_);
    tree_->Branch("tauh1_eta",  &tauh1_eta_);
    tree_->Branch("tauh1_phi",  &tauh1_phi_);
    tree_->Branch("tauh1_m",    &tauh1_m_);

    tree_->Branch("tauh2_pt",   &tauh2_pt_);
    tree_->Branch("tauh2_eta",  &tauh2_eta_);
    tree_->Branch("tauh2_phi",  &tauh2_phi_);
    tree_->Branch("tauh2_m",    &tauh2_m_);

    tree_->Branch("taue1_pt",   &taue1_pt_);
    tree_->Branch("taue1_eta",  &taue1_eta_);
    tree_->Branch("taue1_phi",  &taue1_phi_);
    tree_->Branch("taue1_m",    &taue1_m_);

    tree_->Branch("taue2_pt",   &taue2_pt_);
    tree_->Branch("taue2_eta",  &taue2_eta_);
    tree_->Branch("taue2_phi",  &taue2_phi_);
    tree_->Branch("taue2_m",    &taue2_m_);

    tree_->Branch("taumu1_pt",  &taumu1_pt_);
    tree_->Branch("taumu1_eta", &taumu1_eta_);
    tree_->Branch("taumu1_phi", &taumu1_phi_);
    tree_->Branch("taumu1_m",   &taumu1_m_);

    tree_->Branch("taumu2_pt",  &taumu2_pt_);
    tree_->Branch("taumu2_eta", &taumu2_eta_);
    tree_->Branch("taumu2_phi", &taumu2_phi_);
    tree_->Branch("taumu2_m",   &taumu2_m_);

    //----------------------- leptons

    tree_->Branch("neles",    &neles_);

    tree_->Branch("ele1_pt",  &ele1_pt_);
    tree_->Branch("ele1_eta", &ele1_eta_);
    tree_->Branch("ele1_phi", &ele1_phi_);
    tree_->Branch("ele1_m",   &ele1_m_);

    tree_->Branch("nmus",     &nmus_);

    tree_->Branch("mu1_pt",   &mu1_pt_);
    tree_->Branch("mu1_eta",  &mu1_eta_);
    tree_->Branch("mu1_phi",  &mu1_phi_);
    tree_->Branch("mu1_m",    &mu1_m_);

}

void GenNtuplizer::beginRun(edm::Run const&, edm::EventSetup const&){
}

void GenNtuplizer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup){

    initialize();

    if (do_met_){
        edm::Handle<std::vector<reco::GenMET> > genMETs;
        iEvent.getByToken(genMETToken_, genMETs);
        const auto& mets = *genMETs.product(); //const std::vector<reco::GenMET>

        if (mets.size() != 1)
            std::cout << "... this event has N != 1 MET values ?? " << mets.size() << std::endl;

        if (mets.size() > 0)
        {
            const auto& met = mets.at(0); // reco::GenMET
            met_x_ = met.px();
            met_y_ = met.py();
            met_   = met.pt();
        }

        // std::cout << "... this event has " << mets.size() << " MET values" << std::endl;
        // for (uint imet = 0; imet < mets.size(); ++imet){
        //     const auto& met = mets.at(imet); // reco::GenMET
        //     cout << "...... imet " << imet << " px = " << met.px() << " py = " << met.py() << endl;
        // }
    }

    if (do_genjets_)
    {
        edm::Handle<std::vector<reco::GenJet> > genJetsH;
        edm::Handle<std::vector<reco::GenJet> > genJetsNoNuH;

        iEvent.getByToken(genJetToken_,     genJetsH);
        iEvent.getByToken(genJetNoNuToken_, genJetsNoNuH);

        const auto& genjets     = *genJetsH.product();
        const auto& genjetsnonu = *genJetsNoNuH.product();

        // gen jets
        ngenjet_ = genjets.size();

        for (uint igj = 0; igj < genjets.size(); ++igj)
        {
            if (igj > 3) // only 4 leading gen jets
                break;

            const auto& gjet = genjets.at(igj);

            if (igj == 0)
            {
                genjet1_pt_    = gjet.pt();
                genjet1_eta_   = gjet.eta();
                genjet1_phi_   = gjet.phi();
                genjet1_m_     = gjet.mass();
            }

            if (igj == 1)
            {
                genjet2_pt_    = gjet.pt();
                genjet2_eta_   = gjet.eta();
                genjet2_phi_   = gjet.phi();
                genjet2_m_     = gjet.mass();
            }

            if (igj == 2)
            {
                genjet3_pt_    = gjet.pt();
                genjet3_eta_   = gjet.eta();
                genjet3_phi_   = gjet.phi();
                genjet3_m_     = gjet.mass();
            }

            if (igj == 3)
            {
                genjet4_pt_    = gjet.pt();
                genjet4_eta_   = gjet.eta();
                genjet4_phi_   = gjet.phi();
                genjet4_m_     = gjet.mass();
            }
        } // gen jets


        // gen jets no nu
        ngenjet_nonu_ = genjetsnonu.size();

        for (uint igj = 0; igj < genjetsnonu.size(); ++igj)
        {
            if (igj > 3) // only 4 leading gen jets
                break;

            const auto& gjet = genjetsnonu.at(igj);

            if (igj == 0)
            {
                genjet1_nonu_pt_    = gjet.pt();
                genjet1_nonu_eta_   = gjet.eta();
                genjet1_nonu_phi_   = gjet.phi();
                genjet1_nonu_m_     = gjet.mass();
            }

            if (igj == 1)
            {
                genjet2_nonu_pt_    = gjet.pt();
                genjet2_nonu_eta_   = gjet.eta();
                genjet2_nonu_phi_   = gjet.phi();
                genjet2_nonu_m_     = gjet.mass();
            }

            if (igj == 2)
            {
                genjet3_nonu_pt_    = gjet.pt();
                genjet3_nonu_eta_   = gjet.eta();
                genjet3_nonu_phi_   = gjet.phi();
                genjet3_nonu_m_     = gjet.mass();
            }

            if (igj == 3)
            {
                genjet4_nonu_pt_    = gjet.pt();
                genjet4_nonu_eta_   = gjet.eta();
                genjet4_nonu_phi_   = gjet.phi();
                genjet4_nonu_m_     = gjet.mass();
            }
        } // gen jets no nu


        // now HT - summed from nony jets only
        
        HT_        = 0;
        HT_5_      = 0;
        HT_10_     = 0;
        HT_20_     = 0;
        HT_30_     = 0;
        
        HT_ER_     = 0;
        HT_ER_5_   = 0;
        HT_ER_10_  = 0;
        HT_ER_20_  = 0;
        HT_ER_30_  = 0;

        for (uint igj = 0; igj < genjetsnonu.size(); ++igj)
        {
            const auto& gjet = genjetsnonu.at(igj);

            HT_ += gjet.pt();
            if (gjet.pt() > 5)  HT_5_   += gjet.pt();
            if (gjet.pt() > 10) HT_10_  += gjet.pt();
            if (gjet.pt() > 20) HT_20_  += gjet.pt();
            if (gjet.pt() > 30) HT_30_  += gjet.pt();

            if (std::abs(gjet.eta()) < 2.5){
                HT_ER_ += gjet.pt();
                if (gjet.pt() > 5)  HT_ER_5_   += gjet.pt();
                if (gjet.pt() > 10) HT_ER_10_  += gjet.pt();
                if (gjet.pt() > 20) HT_ER_20_  += gjet.pt();
                if (gjet.pt() > 30) HT_ER_30_  += gjet.pt();
            }
        }

    } // do gen jets


    // gen particles
    if (do_gammas_ || do_muons_ || do_electrons_ || do_taus_)
    {
        edm::Handle<std::vector<reco::GenParticle> > genParticleH;
        iEvent.getByToken(genParticleToken_, genParticleH);

        const auto& genparticles = *genParticleH.product();

        std::vector<std::pair<double, int>> pt_idx_gammas;
        std::vector<std::pair<double, int>> pt_idx_taus;
        std::vector<std::pair<double, int>> pt_idx_muons;
        std::vector<std::pair<double, int>> pt_idx_electrons;

        for (uint igp = 0; igp < genparticles.size(); ++igp)
        {
            const auto& genpart = genparticles.at(igp);
            int apdgId        = std::abs(genpart.pdgId());
            int status        = genpart.status();
            const auto& flags = genpart.statusFlags();

            if (do_gammas_ && apdgId == 22 && flags.isLastCopy() && flags.fromHardProcess()) // photons for Hgg, bbgg
            {
                pt_idx_gammas.push_back(make_pair(genpart.pt(), igp));
            }

            if (do_taus_ && apdgId == 15 && flags.isLastCopy() && flags.fromHardProcess()) // taus
            {
                pt_idx_taus.push_back(make_pair(genpart.pt(), igp));
            }

            if (do_electrons_ && apdgId == 11 && flags.isLastCopy() && flags.fromHardProcess()) // ele
            {
                pt_idx_electrons.push_back(make_pair(genpart.pt(), igp));
            }

            if (do_muons_ && apdgId == 13 && flags.isLastCopy() && flags.fromHardProcess()) // mu
            {
                pt_idx_muons.push_back(make_pair(genpart.pt(), igp));
            }

        }

        // photons
        if (do_gammas_)
        {
            ngammas_ = pt_idx_gammas.size();
            sort(pt_idx_gammas.begin(), pt_idx_gammas.end()); // pt low to high
            
            if (pt_idx_gammas.size() >= 1)
            {
                int ipart = (pt_idx_gammas.rbegin())->second;
                const auto& genpart = genparticles.at(ipart);
                gamma1_pt_   = genpart.pt();
                gamma1_eta_  = genpart.eta();
                gamma1_phi_  = genpart.phi();
                gamma1_m_    = genpart.mass();
            }

            if (pt_idx_gammas.size() >= 2)
            {
                int ipart = (pt_idx_gammas.rbegin()+1)->second;
                const auto& genpart = genparticles.at(ipart);
                gamma2_pt_   = genpart.pt();
                gamma2_eta_  = genpart.eta();
                gamma2_phi_  = genpart.phi();
                gamma2_m_    = genpart.mass();
            }
        } // do_gammas

        if (do_taus_)
        {
            ntaus_    = pt_idx_taus.size();

            // build the visible tauh for each tau found
            // std::vector<std::tuple<double, bool, TLorentzVector>> tauhs;
            std::vector<std::tuple<double, int, TLorentzVector>> tauhs;
            
            for (uint itau = 0; itau < pt_idx_taus.size(); ++itau)
            {
                int ipart = pt_idx_taus.at(itau).second;
                const auto& gentau = genparticles.at(ipart);

                TLorentzVector vTauh(0,0,0,0);

                // cout << " **** TAU : " << itau << " has " << gentau.numberOfDaughters() << " daughters" << endl;
                // bool is_had_tau = true;
                int tau_decay_type = 2; // 0 : e, 1 : mu, 2 : tauh

                for (uint idau = 0; idau < gentau.numberOfDaughters(); ++idau)
                {
                    const reco::Candidate* dau = gentau.daughter(idau);
                    int apdgId = std::abs(dau->pdgId());
                    // int status        = genpart.status();
                    // const auto& flags = genpart.statusFlags();

                    // cout << " ..... : dau " << idau << " id = " << apdgId << endl;
                    if (apdgId == 12 || apdgId == 14 || apdgId == 16)
                        continue;

                    // if (apdgId == 11 || apdgId == 13)
                    //     is_had_tau = false;

                    if (apdgId == 11)
                        tau_decay_type = 0;

                    if (apdgId == 13)
                        tau_decay_type = 1;

                    if (apdgId == 15)
                        cout << " [ERROR] : tau from hard scatter has a pdgid 15 daughter" << endl;

                    TLorentzVector vObj(0,0,0,0);                    
                    vObj.SetPtEtaPhiM(dau->pt(), dau->eta(), dau->phi(), dau->mass());
                    vTauh += vObj;
                }

                // tauhs.push_back(make_tuple(vTauh.Pt(), is_had_tau, vTauh));
                tauhs.push_back(make_tuple(vTauh.Pt(), tau_decay_type, vTauh));
            }

            // sort(tauhs.begin(), tauhs.end());
            // reverse(tauhs.begin(), tauhs.end()); // from highest to lowest pt

            // sort(tauhs.begin(), tauhs.end(),
            //     [](const std::tuple<double, bool, TLorentzVector> & a, const std::tuple<double, bool, TLorentzVector> & b) -> bool
            //     {
            //         return std::get<0>(a) > std::get<0>(b);
            //     }
            // ); // pt high to low in this way

            sort(tauhs.begin(), tauhs.end(),
                [](const std::tuple<double, int, TLorentzVector> & a, const std::tuple<double, int, TLorentzVector> & b) -> bool
                {
                    return std::get<0>(a) > std::get<0>(b);
                }
            ); // pt high to low in this way

            for (uint itau = 0; itau < tauhs.size(); ++itau) 
            {
                // if (!std::get<1> (tauhs.at(itau))) // not had tau
                //     continue;

                if (std::get<1> (tauhs.at(itau)) == 2) // had tau
                {                
                    ntaushad_ += 1;
                    TLorentzVector vtau = std::get<2> (tauhs.at(itau));

                    if (tauh1_pt_ < 0)
                    {
                        tauh1_pt_   = vtau.Pt();
                        tauh1_eta_  = vtau.Eta();
                        tauh1_phi_  = vtau.Phi();
                        tauh1_m_    = vtau.M();
                    }
                    else if (tauh2_pt_ < 0)
                    {
                        tauh2_pt_   = vtau.Pt();
                        tauh2_eta_  = vtau.Eta();
                        tauh2_phi_  = vtau.Phi();
                        tauh2_m_    = vtau.M();
                    }
                    // other tauh not saved
                }

                if (std::get<1> (tauhs.at(itau)) == 1) // mu tau
                {                
                    ntausmu_ += 1;
                    TLorentzVector vtau = std::get<2> (tauhs.at(itau));

                    if (taumu1_pt_ < 0)
                    {
                        taumu1_pt_   = vtau.Pt();
                        taumu1_eta_  = vtau.Eta();
                        taumu1_phi_  = vtau.Phi();
                        taumu1_m_    = vtau.M();
                    }
                    else if (taumu2_pt_ < 0)
                    {
                        taumu2_pt_   = vtau.Pt();
                        taumu2_eta_  = vtau.Eta();
                        taumu2_phi_  = vtau.Phi();
                        taumu2_m_    = vtau.M();
                    }
                    // other tauh not saved
                }

                if (std::get<1> (tauhs.at(itau)) == 0) // 3 tau
                {                
                    ntause_ += 1;
                    TLorentzVector vtau = std::get<2> (tauhs.at(itau));

                    if (taue1_pt_ < 0)
                    {
                        taue1_pt_   = vtau.Pt();
                        taue1_eta_  = vtau.Eta();
                        taue1_phi_  = vtau.Phi();
                        taue1_m_    = vtau.M();
                    }
                    else if (taue2_pt_ < 0)
                    {
                        taue2_pt_   = vtau.Pt();
                        taue2_eta_  = vtau.Eta();
                        taue2_phi_  = vtau.Phi();
                        taue2_m_    = vtau.M();
                    }
                    // other tauh not saved
                }
            }
        } // do taus

        if (do_electrons_)
        {
            neles_ = pt_idx_electrons.size();
            sort(pt_idx_electrons.begin(), pt_idx_electrons.end()); // pt low to high

            if (pt_idx_electrons.size() >= 1)
            {
                int ipart = (pt_idx_electrons.rbegin())->second;
                const auto& genpart = genparticles.at(ipart);
                ele1_pt_   = genpart.pt();
                ele1_eta_  = genpart.eta();
                ele1_phi_  = genpart.phi();
                ele1_m_    = genpart.mass();
            }
        } // do_electrons

        if (do_muons_)
        {
            nmus_ = pt_idx_muons.size();
            sort(pt_idx_muons.begin(), pt_idx_muons.end()); // pt low to high

            if (pt_idx_muons.size() >= 1)
            {
                int ipart = (pt_idx_muons.rbegin())->second;
                const auto& genpart = genparticles.at(ipart);
                mu1_pt_   = genpart.pt();
                mu1_eta_  = genpart.eta();
                mu1_phi_  = genpart.phi();
                mu1_m_    = genpart.mass();
            }
        }
    }

    tree_->Fill();
}

void GenNtuplizer::endJob(){
}

void GenNtuplizer::endRun(edm::Run const&, edm::EventSetup const&){
}



void GenNtuplizer::initialize()
{
    // initialize here the Tree
    met_x_  = -999;
    met_y_  = -999;
    met_    = -999;


    HT_        = 0;
    HT_5_      = 0;
    HT_10_     = 0;
    HT_20_     = 0;
    HT_30_     = 0;
    
    HT_ER_     = 0;
    HT_ER_5_   = 0;
    HT_ER_10_  = 0;
    HT_ER_20_  = 0;
    HT_ER_30_  = 0;


    ngenjet_             = 0;

    genjet1_pt_          = -999.;
    genjet1_eta_         = -999.;
    genjet1_phi_         = -999.;
    genjet1_m_           = -999.;
                     
    genjet2_pt_          = -999.;
    genjet2_eta_         = -999.;
    genjet2_phi_         = -999.;
    genjet2_m_           = -999.;
                     
    genjet3_pt_          = -999.;
    genjet3_eta_         = -999.;
    genjet3_phi_         = -999.;
    genjet3_m_           = -999.;
                     
    genjet4_pt_          = -999.;
    genjet4_eta_         = -999.;
    genjet4_phi_         = -999.;
    genjet4_m_           = -999.;
           

    ngenjet_nonu_        = 0;  

    genjet1_nonu_pt_     = -999.;
    genjet1_nonu_eta_    = -999.;
    genjet1_nonu_phi_    = -999.;
    genjet1_nonu_m_      = -999.;
                     
    genjet2_nonu_pt_     = -999.;
    genjet2_nonu_eta_    = -999.;
    genjet2_nonu_phi_    = -999.;
    genjet2_nonu_m_      = -999.;
                     
    genjet3_nonu_pt_     = -999.;
    genjet3_nonu_eta_    = -999.;
    genjet3_nonu_phi_    = -999.;
    genjet3_nonu_m_      = -999.;
                     
    genjet4_nonu_pt_     = -999.;
    genjet4_nonu_eta_    = -999.;
    genjet4_nonu_phi_    = -999.;
    genjet4_nonu_m_      = -999.;


    ngammas_      = 0;

    gamma1_pt_    = -999.;               
    gamma1_eta_   = -999.;                
    gamma1_phi_   = -999.;                
    gamma1_m_     = -999.;              

    gamma2_pt_    = -999.;
    gamma2_eta_   = -999;
    gamma2_phi_   = -999;
    gamma2_m_     = -999;


    ntaus_      = 0;
    ntaushad_   = 0;
    ntausmu_    = 0;
    ntause_     = 0;

    tauh1_pt_    = -999.;               
    tauh1_eta_   = -999.;                
    tauh1_phi_   = -999.;                
    tauh1_m_     = -999.;              

    tauh2_pt_    = -999.;
    tauh2_eta_   = -999;
    tauh2_phi_   = -999;
    tauh2_m_     = -999;
    
    taue1_pt_  = -999;
    taue1_eta_ = -999;
    taue1_phi_ = -999;
    taue1_m_   = -999;

    taue2_pt_   = -999;
    taue2_eta_  = -999;
    taue2_phi_  = -999;
    taue2_m_    = -999;

    taumu1_pt_  = -999;
    taumu1_eta_ = -999;
    taumu1_phi_ = -999;
    taumu1_m_   = -999;

    taumu2_pt_  = -999;
    taumu2_eta_ = -999;
    taumu2_phi_ = -999;
    taumu2_m_   = -999;

    neles_ = 0;

    ele1_pt_   = -999.;
    ele1_eta_  = -999.;
    ele1_phi_  = -999.;
    ele1_m_    = -999.;


    nmus_ = 0;

    mu1_pt_    = -999.;
    mu1_eta_   = -999.;
    mu1_phi_   = -999.;
    mu1_m_     = -999.;


}

#include <FWCore/Framework/interface/MakerMacros.h>
DEFINE_FWK_MODULE(GenNtuplizer);

#endif // GENNTUPLIZER_H