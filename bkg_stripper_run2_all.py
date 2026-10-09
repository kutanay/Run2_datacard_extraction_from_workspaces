import ROOT

for mass in range(15, 61, 5):
    path = f"extracted/M{mass}.root"
    output = f"Models/CMS-HGG_multipdf_fullrun2_M{mass}.root"

    print(f"Running mass {mass}")

    f = ROOT.TFile(path)
    w = f.Get("w")

    wbkg = ROOT.RooWorkspace("multipdf", "multipdf")

    bkg = w.pdf("shapeBkg_bkg_mass_Cat0")
    norm = w.var("shapeBkg_bkg_mass_Cat0__norm")
    norm.SetName("shapeBkg_bkg_mass_Cat0_norm")

    getattr(wbkg, "import")(
        bkg,
        ROOT.RooFit.RecycleConflictNodes(),
        ROOT.RooFit.Silence()
    )
    getattr(wbkg, "import")(norm, ROOT.RooFit.Silence())

    data = w.data("data_obs")
    mass_var = w.var("CMS_hgg_mass")

    data_stripped = ROOT.RooDataSet(
        "roohist_data_mass_H4GTag_Cat0",
        "roohist_data_mass_H4GTag_Cat0",
        data,
        ROOT.RooArgSet(mass_var)
    )

    getattr(wbkg, "import")(data_stripped, ROOT.RooFit.Silence())

    wbkg.writeToFile(output)

    print(f"Background PDF: {bkg.GetName()}")
    print(f"Background norm: {norm.GetName()}")
    print(f"Background norm value: {norm.getVal()}")
    print(f"Data entries: {data_stripped.numEntries()}")
    print(f"Written {output}")

    f.Close()
