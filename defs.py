# -*- coding: utf-8 -*-

import pandas as pd
import json


def create_json(df, cats, name, singleLine, enc):
    """
    Creates customized json file from a pandas dataframe and saves it with the
    selected naming.
    """

    d = df.reset_index()

    d = (
        d.groupby(cats[:-1])
        .apply(lambda x: x[["year", "total"]].to_dict("r"))
        .reset_index()
        .rename(columns={0: "indicatorGroupValues"})
    )

    d = (
        d.groupby(cats[:-2])
        .apply(lambda x: x[["indicatorGroup", "indicatorGroupValues"]].to_dict("r"))
        .reset_index()
        .rename(columns={0: "indicatorGroups"})
    )

    if "region" in cats:
        d = (
            d.groupby(cats[:-3])
            .apply(lambda x: x[["region", "indicatorGroups"]].to_dict("r"))
            .reset_index()
            .rename(columns={0: "regions"})
        )

        d = (
            d.groupby(cats[:-4])
            .apply(lambda x: x[["indicator", "regions"]].to_dict("r"))
            .reset_index()
            .rename(columns={0: "indicators"})
        )

    else:
        d = (
            d.groupby(cats[:-3])
            .apply(lambda x: x[["indicator", "indicatorGroups"]].to_dict("r"))
            .reset_index()
            .rename(columns={0: "indicators"})
        )

    d["scenarios"] = "scenarios"
    d = (
        d.groupby(["scenarios"])
        .apply(lambda x: x[["scenario", "indicators"]].to_dict("r"))
        .reset_index()
        .rename(columns={0: "data"})
    )
    d = d.set_index("scenarios")

    with open("output/" + name + ".js", "w+", encoding=enc) as file:
        d.to_json(file, force_ascii=False)

    if singleLine:
        js_str = open("output/" + name + ".js", "r", encoding=enc).read()
        open("output/" + name + ".js", "w", encoding=enc).write(
            "export default " + js_str
        )
    else:
        js_str = open("output/" + name + ".js", "r", encoding=enc).read()
        with open("output/" + name + ".js", "w", encoding=enc) as file:
            js_str = json.dumps(json.loads(js_str), indent=2)
            file.write("export default " + js_str)
