#!/usr/bin/env python3
"""Discovery extract: one run's data -> extract.json (every figure and quote the deck shows).

One script for both lines. Reads today's computed export ("..._With_Calculations.json");
on the platform the same logic reads the run's records.

    python3 system/tools/build_extract.py <export.json> -o <extract.json> [--quotes <quotes.json>]
    python3 system/tools/build_extract.py <export.json> --find "phrase"   # locate answers for a quote

Rules it applies (system/content-guidelines.md §5, <line>/overrides.md):
  - Every score 0-100: sentiment and Visibility (0-50) x2; pillars and criteria (0-10) x10 from the
    unrounded run averages (rla); sentiment by question (1-5) (x-1)x25.
  - Employer Rank: 10-item lists, 10 points for first ... 1 for tenth, 0 if not named, mean x10.
    The export's rank_score (rs) is the mean position with absence imputed at 11, so
    mean points = 11 - rs and Rank = (11 - rs) x 10.
  - Index from the line's weights. Position tags from the displayed (rounded) values:
    Leading = above each competitor, Lagging = below each, Inline otherwise (ties included).
  - Verdict bands on 0-100: Strong >=67, Mixed 50-66, Opening <50.
  - Quotes: each must appear word for word in a model answer, or the build stops.
"""
import argparse, json, re, sys, statistics

WEIGHTS = {  # mirrors brand/overrides.md and employer/overrides.md
    "brand":    {"presence": 0.35, "sentiment": 0.35, "pillars": 0.15, "criteria": 0.15},
    "employer": {"presence": 0.25, "sentiment": 0.25, "pillars": 0.25, "criteria": 0.25},
}
LABELS = {
    "brand":    {"presence": "Visibility", "pillars": "Brand Pillars", "criteria": "Purchase Criteria",
                 "subject": "brand", "index": "Revere AI Brand Index"},
    "employer": {"presence": "Rank", "pillars": "EVP Pillars", "criteria": "Choice Criteria",
                 "subject": "employer", "index": "Revere AI Employer Index"},
}


def norm(name):
    return re.sub(r"\s+", " ", str(name).replace("’", "'").replace("‘", "'")).strip().lower()


def r(x):
    return None if x is None else int(round(x))


def band(v):
    if v is None:
        return None
    return "Strong" if v >= 67 else "Mixed" if v >= 50 else "Opening"


def position(subject, others):
    others = [o for o in others if o is not None]
    if subject is None or not others:
        return None
    if all(subject > o for o in others):
        return "Leading"
    if all(subject < o for o in others):
        return "Lagging"
    return "Inline"


def node(data, sec):
    """category -> market -> llm -> persona (Discovery runs one of each)."""
    s = data[sec]
    assert len(s) == 1 and len(s[0]["m"]) == 1, f"{sec}: expected one category and one market"
    llm = s[0]["m"][0]["l"]
    assert len(llm) == 1, f"{sec}: expected one model"
    personas = llm[0]["p"] if "p" in llm[0] else [llm[0]]
    assert len(personas) == 1, f"{sec}: expected one persona"
    return personas[0]


class Extract:
    def __init__(self, export):
        self.J = export
        self.d = export["data"]
        self.warnings = []
        d = self.d
        self.line = "employer" if "EVP" in d else "brand"
        if self.line == "brand" and "BP" not in d:
            sys.exit("No Brand Pillars section: Product mode is not supported until docs/01-audit.md Q2 is answered.")
        self.sec = ({"presence": "RD", "pillars": "EVP", "criteria": "ECC"} if self.line == "employer"
                    else {"presence": "V", "pillars": "BP", "criteria": "PC"})
        self.subject = d["brand"] if isinstance(d["brand"], str) else d["brand"][0]
        s = node(d, "S")
        self.brands = [self.subject] + [c["n"] for c in s["c"]]
        self.key = {norm(b): b for b in self.brands}

    def canon(self, name):
        b = self.key.get(norm(name))
        return b

    def warn(self, msg):
        self.warnings.append(msg)

    # ---- components, 0-100, per brand ------------------------------------------------
    def sentiment(self):
        s = node(self.d, "S")
        out = {self.subject: s["ts"] * 2}
        for c in s["c"]:
            out[c["n"]] = c["s"] * 2
        fav = s["favorabilities"]
        labels = self.d["S"][0].get("question_labels", [])
        qs = []
        for i, t in enumerate(fav["target"]["question_scores"]):
            row = {"i": i + 1, "question": labels[i] if i < len(labels) else None,
                   "subject": (t - 1) * 25,
                   "competitor_average": (fav["competitor_average"]["question_scores"][i] - 1) * 25,
                   "competitors": {c["name"]: (c["question_scores"][i] - 1) * 25 for c in fav["competitors"]}}
            qs.append(row)
        drivers = {}
        for k, lab in (("pd", "positive"), ("nd", "negative")):
            items = []
            for x in s.get(k, []):
                m = re.match(r"(.*):\s*(\d+)\s*/\s*(\d+)\s*$", x)
                items.append({"driver": m.group(1).strip(), "answers": int(m.group(2)), "of": int(m.group(3))} if m else {"driver": x})
            drivers[lab] = items
        return out, qs, drivers

    def presence(self):
        if self.line == "brand":
            v = node(self.d, "V")
            out = {self.subject: v["ts"] * 2}
            for c in v["c"]:
                out[c["n"]] = c["s"] * 2
            # appearance and position when named, from every ranked list
            seen = {b: [] for b in self.brands}
            lists = 0
            for kw, runs in v["keyword_executions"].items():
                for run in runs:
                    lists += 1
                    for b, pos in run["brand_positions"].items():
                        cb = self.canon(b)
                        if cb:
                            seen[cb].append(pos["position"] if pos.get("appeared") else None)
            detail = {b: {"appearance_rate": (sum(p is not None for p in ps) / len(ps)) if ps else None,
                          "mean_position_when_named": statistics.mean([p for p in ps if p is not None]) if any(p is not None for p in ps) else None}
                      for b, ps in seen.items()}
            return out, detail, {"lists": lists, "keywords": list(v["keyword_executions"].keys())}
        rd = node(self.d, "RD")
        rows = [dict(rd["tb"], n=rd["tb"]["n"])] + rd["ac"]
        out, detail = {}, {}
        for x in rows:
            b = self.canon(x["n"])
            if not b:
                self.warn(f"Rank: '{x['n']}' is not in the brand set; skipped")
                continue
            rs = x["rs"]
            if rs > 11 or rs < 1:
                self.warn(f"Rank: {b} rank score {rs} is outside 1-11")
            out[b] = max(0.0, min(100.0, (11 - rs) * 10))
            ar = x.get("ar")
            if ar is not None and ar > 1:
                self.warn(f"Rank: {b} appearance rate {ar} is above 1 (named more than once in a list?); check the raw lists")
            detail[b] = {"appearance_rate": ar, "rank_position_in_category": x.get("rp")}
        named = {norm(x["n"]) for x in rd.get("cl", [])}
        for b in self.brands:
            if b not in out:
                if norm(b) in named:
                    self.warn(f"Rank: {b} is named in the lists but missing from the competitor rows; check the export")
                else:  # never named in any ranked list: 0 points
                    out[b] = 0.0
                    detail[b] = {"appearance_rate": 0, "rank_position_in_category": None}
                    self.warn(f"Rank: {b} is never named in any ranked list; Rank 0 (read the raw lists to confirm)")
        top = rd.get("rl", {})
        return out, detail, {"keywords": self.d["RD"][0].get("kt"), "category_leader": top.get("n")}

    def scored_items(self, kind):
        """Pillars or criteria: per item per brand, from the unrounded run averages."""
        sec = self.sec[kind]
        p = node(self.d, sec)
        rla = p["rla"]
        rla_k = {norm(b): v for b, v in rla.items()}
        if kind == "pillars":
            items = [x["pillar_name"] for x in p["tb"]["sc"]]
            expl = {x["pillar_name"]: x.get("brand_explanation") for x in p["tb"]["sc"]}
            defs = {x["pillar_name"]: x.get("definition") for x in p["tb"]["sc"]}
        else:
            items = [x["criterion_name"] for x in p["tb"]["cs"]]
            expl = {x["criterion_name"]: x.get("target_brand_explanation") for x in p["tb"]["cs"]}
            defs = {}
        rows = []
        for it in items:
            row = {"item": it, "definition": defs.get(it), "subject_explanation": expl.get(it), "scores": {}}
            for b in self.brands:
                br = rla_k.get(norm(b))
                if br is None:
                    self.warn(f"{kind}: no run averages for {b}")
                    continue
                v = {norm(k): x for k, x in br.items()}.get(norm(it))
                if v is None:
                    self.warn(f"{kind}: {b} has no score for '{it}'")
                    continue
                row["scores"][b] = v["avg"] * 10
            rows.append(row)
        comp = {}
        for b in self.brands:
            vals = [row["scores"][b] for row in rows if b in row["scores"]]
            comp[b] = statistics.mean(vals) if vals else None
        return comp, rows

    def attributes(self):
        p = node(self.d, "PNA")
        pick = lambda xs: [{"attribute": x["n"], "signal": x["v"]} for x in xs]
        return {"praise": pick(p.get("pa", [])), "fault": pick(p.get("na", []))}

    def sources(self):
        src = self.d["src"]
        total = src["totalCitations"]
        types = {}
        for t in ("own", "competitors", "pr_media", "third_party"):
            types[t] = {"citations": src[t]["totalCitations"], "share": src[t]["totalCitations"] / total if total else None}
        doms = []
        for t in ("own", "competitors", "pr_media", "third_party"):
            for x in src[t]["domains"]:
                doms.append({"domain": x["domain"], "type": t, "citations": x["citations"], "share": x["citations"] / total})
        doms.sort(key=lambda x: -x["citations"])
        check = sum(v["citations"] for v in types.values())
        if check != total:
            self.warn(f"Sources: type totals {check} differ from totalCitations {total}")
        return {"total_citations": total, "unique_sources": src.get("totalSources"), "by_type": types,
                "own_domains": [x for x in doms if x["type"] == "own"],
                "top_outside_domains": [x for x in doms if x["type"] != "own"][:10]}

    # ---- quotes ----------------------------------------------------------------------
    def answers(self):
        s = node(self.d, "S")
        labels = self.d["S"][0].get("question_labels", [])
        for b in s["sq"]:
            for qi, q in enumerate(b["questions"]):
                for ri, resp in enumerate(q["responses"]):
                    yield {"brand": b["brand_name"], "question_index": qi + 1, "question": q.get("question") or (labels[qi] if qi < len(labels) else None),
                           "run": ri + 1, "text": resp["response"], "section": "sentiment"}

    def check_quotes(self, quotes):
        clean = lambda t: re.sub(r"\s+", " ", t.replace("’", "'").replace("“", '"').replace("”", '"')).strip()
        out, failed = [], []
        all_ans = list(self.answers())
        for q in quotes:
            parts = [clean(p) for p in re.split(r"\s*(?:\.\.\.|…)\s*", q["text"]) if p.strip()]
            hit = next((a for a in all_ans if all(p in clean(a["text"]) for p in parts)
                        and (not q.get("brand") or norm(a["brand"]) == norm(q["brand"]))), None)
            if hit is None:
                failed.append(q.get("id", q["text"][:40]))
            else:
                out.append(dict(q, verified=True, brand=hit["brand"], question=hit["question"], run=hit["run"]))
        if failed:
            sys.exit("Quote(s) not found word for word in any answer: " + ", ".join(failed))
        return out

    # ---- assemble --------------------------------------------------------------------
    def build(self, quotes=None):
        sent, by_q, drivers = self.sentiment()
        pres, pres_detail, pres_meta = self.presence()
        pil, pil_rows = self.scored_items("pillars")
        cri, cri_rows = self.scored_items("criteria")
        W = WEIGHTS[self.line]
        brands = {}
        for b in self.brands:
            c = {"presence": pres.get(b), "sentiment": sent.get(b), "pillars": pil.get(b), "criteria": cri.get(b)}
            missing = [k for k, v in c.items() if v is None]
            idx = None if missing else sum(W[k] * c[k] for k in W)
            if missing:
                self.warn(f"Index: {b} is missing {', '.join(missing)}; no Index")
            brands[b] = {"index": r(idx), "components": {k: r(v) for k, v in c.items()},
                         "contribution": None if missing else {k: round(W[k] * c[k], 1) for k in W}}
        order = sorted(self.brands, key=lambda b: -(brands[b]["index"] or -1))
        for i, b in enumerate(order):
            brands[b]["place"] = i + 1
        S = self.subject
        comps = [b for b in self.brands if b != S]

        def compare(rows):
            out = []
            for row in rows:
                disp = {b: r(v) for b, v in row["scores"].items()}
                others = [disp.get(b) for b in comps]
                top_b = max((b for b in comps if disp.get(b) is not None), key=lambda b: disp[b], default=None)
                vals = [disp[b] for b in comps if disp.get(b) is not None]
                out.append({"item": row["item"], "definition": row.get("definition"),
                            "subject_explanation": row.get("subject_explanation"),
                            "subject": disp.get(S), "band": band(disp.get(S)),
                            "competitors": {b: disp.get(b) for b in comps},
                            "set_average": r(statistics.mean(vals)) if vals else None,
                            "top_competitor": {"name": top_b, "value": disp.get(top_b)} if top_b else None,
                            "position": position(disp.get(S), others)})
            out.sort(key=lambda x: -(x["subject"] if x["subject"] is not None else -1))
            return out

        def component_view(key):
            disp = {b: brands[b]["components"][key] for b in self.brands}
            return {"subject": disp[S], "band": band(disp[S]),
                    "position": position(disp[S], [disp[b] for b in comps]),
                    "ranked": [{"brand": b, "value": disp[b], "subject": b == S}
                               for b in sorted(self.brands, key=lambda b: -(disp[b] if disp[b] is not None else -1))]}

        L = LABELS[self.line]
        ex = {
            "meta": {"subject": S, "line": self.line, "labels": L, "weights": W,
                     "category": self.d.get("cats"), "market": self.d.get("mkts"), "model": self.d.get("llms"),
                     "persona": "General", "brands": self.brands, "competitors": comps,
                     "source_file_title": self.J.get("_title")},
            "index": {"subject": brands[S]["index"], "band": band(brands[S]["index"]),
                      "place": brands[S]["place"], "of": len(self.brands),
                      "components": {k: {"value": brands[S]["components"][k], "band": band(brands[S]["components"][k]),
                                         "weight": W[k], "contribution": (brands[S]["contribution"] or {}).get(k)} for k in W},
                      "table": [{"brand": b, "index": brands[b]["index"], "place": brands[b]["place"],
                                 "components": brands[b]["components"], "subject": b == S} for b in order]},
            "presence": dict(component_view("presence"), detail={b: pres_detail.get(b) for b in self.brands}, **pres_meta),
            "sentiment": dict(component_view("sentiment"),
                              by_question=[{"i": q["i"], "question": q["question"], "subject": r(q["subject"]),
                                            "competitor_average": r(q["competitor_average"]),
                                            "competitors": {b: r(v) for b, v in q["competitors"].items()},
                                            "position": position(r(q["subject"]), [r(v) for v in q["competitors"].values()])}
                                           for q in by_q],
                              drivers=drivers, attributes=self.attributes()),
            "pillars": dict(component_view("pillars"), items=compare(pil_rows)),
            "criteria": dict(component_view("criteria"), items=compare(cri_rows)),
            "sources": self.sources(),
            "quotes": self.check_quotes(quotes) if quotes else [],
            "warnings": self.warnings,
        }
        # self-checks
        assert ex["index"]["table"][ex["index"]["place"] - 1]["brand"] == S
        for k in ("pillars", "criteria"):
            for it in ex[k]["items"]:
                assert it["position"] == position(it["subject"], list(it["competitors"].values()))
        return ex


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("export")
    ap.add_argument("-o", "--out")
    ap.add_argument("--quotes", help="JSON list of {id, text, brand?, slide?}; '...' marks an elision")
    ap.add_argument("--find", help="print answers containing this phrase")
    a = ap.parse_args()
    E = Extract(json.load(open(a.export)))
    if a.find:
        import signal; signal.signal(signal.SIGPIPE, signal.SIG_DFL)
        for x in E.answers():
            if a.find.lower() in x["text"].lower():
                print(f"[{x['brand']} · Q{x['question_index']} run {x['run']}] {x['question']}\n  {x['text']}\n")
        return
    quotes = json.load(open(a.quotes)) if a.quotes else None
    ex = E.build(quotes)
    if a.out:
        json.dump(ex, open(a.out, "w"), indent=1, ensure_ascii=False)
    i = ex["index"]
    print(f"{ex['meta']['subject']} ({ex['meta']['line']}): Index {i['subject']} ({i['band']}), {i['place']} of {i['of']}")
    for b in i["table"]:
        print(f"  {b['place']:>2}. {b['brand']:<24} {b['index']!s:>4}  " + "  ".join(f"{k} {v}" for k, v in b["components"].items()))
    for w in ex["warnings"]:
        print("  warning:", w)


if __name__ == "__main__":
    main()
