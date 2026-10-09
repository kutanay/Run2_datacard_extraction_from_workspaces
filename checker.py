#!/usr/bin/env python3
import sys, ROOT
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

mass = sys.argv[1]
f = ROOT.TFile.Open(f"./extracted/M{mass}.root")
w = f.Get("w")

for y in (2016, 2017, 2018):
    p = f"H4GTag_{y}_hgg"
    print(f"\n===== {y} =====")
    print(f"n_exp_final_binCat0_proc_{p} =", w.function(f"n_exp_binCat0_proc_{p}".replace("n_exp_bin", "n_exp_final_bin")).getVal())
    pn = w.function(f"n_exp_binCat0_proc_{p}")
    pn.dump()
    pn.getParameters(ROOT.RooArgSet()).Print("v")
