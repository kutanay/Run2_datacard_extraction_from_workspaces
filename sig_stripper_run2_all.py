import ROOT

for mass in range(15, 61, 5):
    path = f"extracted/M{mass}.root"

    print(f"Running mass {mass}")

    f = ROOT.TFile(path)
    w = f.Get("w")

    for year in ["2016", "2017", "2018"]:
        output = f"Models/{year}/CMS-HGG_mva_13TeV_M{mass}_sigfit_new.root"

        wsig = ROOT.RooWorkspace("wsig_13TeV", "wsig_13TeV")

        sig = w.pdf(f"shapeSig_H4GTag_{year}_hgg_Cat0")
        norm = w.function(f"shapeSig_H4GTag_{year}_hgg_Cat0__norm")
        norm.SetName(f"shapeSig_H4GTag_{year}_hgg_Cat0_norm")

        getattr(wsig, "import")(
            sig,
            ROOT.RooFit.RenameConflictNodes(year),
            ROOT.RooFit.Silence()
        )
        getattr(wsig, "import")(norm, ROOT.RooFit.Silence())

        wsig.writeToFile(output)

        print(f"  Year: {year}")
        print(f"  Signal PDF: {sig.GetName()}")
        print(f"  Signal norm: {norm.GetName()}")
        print(f"  Signal norm value: {norm.getVal()}")
        print(f"  Written {output}")

    f.Close()
