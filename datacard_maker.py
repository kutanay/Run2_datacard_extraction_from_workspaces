#!/usr/bin/env python3
import ROOT, re, os
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")   # needs cmsenv

TEMPLATE = "template_datacard.txt"   # your pasted file

INFILE   = "./extracted/M{mass}.root"
os.makedirs("datacards", exist_ok=True)
OUTFILE  = "datacards/datacard_M{mass}.txt"
BIN      = "Cat0"
SIG      = ["H4GTag_2016_hgg", "H4GTag_2017_hgg", "H4GTag_2018_hgg"]
OLD_MASS = "30"

def is_factor(name):
    return name == "r" or name == "rp" or name.startswith("yield_")

def get_kappas(w, proc):
    """{nuisance: (kdown, kup)} from theta=-1/+1; factors (r, yield_*) untouched."""
    pn = w.function(f"n_exp_bin{BIN}_proc_{proc}")
    pars = [v for v in pn.getParameters(ROOT.RooArgSet()) if not is_factor(v.GetName())]
    for v in pars: v.setVal(0)
    nom = pn.getVal()
    if nom == 0:
        raise RuntimeError(f"{proc}: nominal is 0")
    out = {}
    for v in pars:
        v.setVal(1);  up = pn.getVal() / nom
        v.setVal(-1); dn = pn.getVal() / nom
        v.setVal(0)
        out[v.GetName()] = (dn, up)
    return out

def fmt(dn, up):
    if abs(dn * up - 1) < 1e-4 and abs(up - 1) > 1e-6:
        return f"{up:.3f}"
    return f"{dn:.3f}/{up:.3f}"

template = open(TEMPLATE).read().splitlines()

for mass in range(15, 65, 5):
    f = ROOT.TFile.Open(INFILE.format(mass=mass))
    w = f.Get("w")

    kappas = {p: get_kappas(w, p) for p in SIG}

    out = []
    for line in template:
        line = line.replace(f"M{OLD_MASS}", f"M{mass}")

        if re.search(r"\slnN\s", line):
            tok = line.split()
            name, cols = tok[0], tok[2:]
            for i, p in enumerate(SIG):
                if name in kappas[p]:
                    cols[i] = fmt(*kappas[p][name])
            line = f"{name:<52}lnN   " + " ".join(cols)

        out.append(line)

    open(OUTFILE.format(mass=mass), "w").write("\n".join(out) + "\n")
    used = sorted({n for p in SIG for n in kappas[p]})
    print(mass, "updated lnN:", used)
    f.Close()
