#!/usr/bin/env python3
"""Analyse one sweep directory: ALTER statistics, workload latency by phase, figures.

Input  : <sweep_dir>/alter_results.csv + the workload CSVs it references
Output : <sweep_dir>/analysis/{alter_summary.csv, workload_by_phase.csv, summary.md, *.png}

Workload statements are assigned to a phase by comparing their [start, start+latency]
interval with the ALTER window [started_at_utc, ended_at_utc] of the same run:

    baseline : finished before the ALTER started
    during   : overlaps the ALTER window (includes statements that were blocked by it)
    after    : started after the ALTER ended

    python analyze_results.py results/sweep_20260930_120000
"""
import argparse
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PHASES = ["baseline", "during", "after"]
MIN_SAMPLE = 30   # below this many statements in a phase, p95/p99 are not meaningful
OPS = ["INSERT", "UPDATE", "DELETE"]


def locate(path_str, sweep_dir):
    p = Path(path_str)
    if p.exists():
        return p
    alt = sweep_dir / p.name
    return alt if alt.exists() else None


def label(row):
    return f"{row['change']}\n{row['requested_algorithm']}"


def alter_summary(alter):
    alter = alter.copy()
    alter["ok"] = alter["status"] == "success"
    rows = []
    for (change, algo), g in alter.groupby(["change", "requested_algorithm"], sort=False):
        ok = g[g["ok"]]["duration_seconds"]
        errs = g[~g["ok"]]["error"].dropna().unique()
        rows.append({
            "change": change, "algorithm": algo, "runs": len(g),
            "successes": int(g["ok"].sum()), "failures": int((~g["ok"]).sum()),
            "mean_s": ok.mean() if len(ok) else np.nan, "median_s": ok.median() if len(ok) else np.nan,
            "min_s": ok.min() if len(ok) else np.nan, "max_s": ok.max() if len(ok) else np.nan,
            "first_error": errs[0] if len(errs) else "",
        })
    return pd.DataFrame(rows)


def classify(wl, start, end):
    t0 = pd.to_datetime(wl["timestamp_utc"], utc=True, format="ISO8601")
    t1 = t0 + pd.to_timedelta(wl["latency_ms"], unit="ms")
    phase = np.where(t1 <= start, "baseline", np.where(t0 >= end, "after", "during"))
    return pd.Series(phase, index=wl.index)


def pct(series, q):
    return float(np.percentile(series, q)) if len(series) else np.nan


def workload_by_phase(alter, sweep_dir):
    rows, frames = [], []
    for _, run in alter.iterrows():
        path = locate(str(run.get("workload_csv", "")), sweep_dir) if isinstance(run.get("workload_csv"), str) and run["workload_csv"] else None
        if path is None:
            continue
        wl = pd.read_csv(path)
        if wl.empty:
            continue
        start = pd.Timestamp(run["started_at_utc"]).tz_convert("UTC")
        end = pd.Timestamp(run["ended_at_utc"]).tz_convert("UTC")
        wl["phase"] = classify(wl, start, end)
        wl["run_id"], wl["change"], wl["algorithm"] = run["run_id"], run["change"], run["requested_algorithm"]
        wl["alter_status"] = run["status"]
        frames.append(wl)
        for (op, phase), g in wl.groupby(["operation", "phase"]):
            ok = g[g["status"] == "success"]["latency_ms"]
            rows.append({
                "run_id": run["run_id"], "change": run["change"], "algorithm": run["requested_algorithm"],
                "alter_status": run["status"], "operation": op, "phase": phase,
                "count": len(g), "low_sample": len(g) < MIN_SAMPLE, "success": len(ok), "errors": int((g["status"] != "success").sum()),
                "avg_ms": g["latency_ms"].mean(), "p50_ms": pct(g["latency_ms"], 50),
                "p95_ms": pct(g["latency_ms"], 95), "p99_ms": pct(g["latency_ms"], 99),
                "max_ms": g["latency_ms"].max(),
            })
    return pd.DataFrame(rows), (pd.concat(frames, ignore_index=True) if frames else pd.DataFrame())


# ---------------------------------------------------------------- figures
def fig_alter_duration(summary, out):
    ok = summary[summary["successes"] > 0]
    if ok.empty:
        return False
    labels = [f"{r.change}\n{r.algorithm}" for r in ok.itertuples()]
    fig, ax = plt.subplots(figsize=(max(7, 0.7 * len(ok)), 5))
    ax.bar(range(len(ok)), ok["median_s"])
    ax.set_xticks(range(len(ok)), labels, rotation=90, fontsize=7)
    ax.set_ylabel("ALTER duration, median of successful runs (s)")
    ax.set_title("ALTER duration by change and requested algorithm (refused combinations omitted)")
    fig.tight_layout(); fig.savefig(out, dpi=140); plt.close(fig)
    return True


def fig_p95(phase_df, out):
    if phase_df.empty:
        return False
    # Only runs whose ALTER succeeded: for a refused ALTER the "during" window is a few ms and meaningless.
    g = phase_df[phase_df["phase"].isin(["baseline", "during"]) & (phase_df["alter_status"] == "success")]
    agg = (g.groupby(["change", "algorithm", "run_id", "phase"], sort=False)["p95_ms"].max().unstack("phase").dropna(subset=["during"]).reset_index())
    if agg.empty:
        return False
    agg["baseline"] = agg["baseline"].fillna(0)
    x = np.arange(len(agg))
    fig, ax = plt.subplots(figsize=(max(7, 0.7 * len(agg)), 5))
    ax.bar(x - 0.2, agg["baseline"], 0.4, label="baseline")
    ax.bar(x + 0.2, agg["during"], 0.4, label="during ALTER")
    ax.set_xticks(x, [f"{r.change}\n{r.algorithm}" for r in agg.itertuples()], rotation=90, fontsize=7)
    ax.set_yscale("log"); ax.set_ylabel("worst per-operation p95 latency (ms, log)")
    ax.set_title("Workload p95 latency: baseline vs during ALTER (successful ALTERs only)"); ax.legend()
    fig.tight_layout(); fig.savefig(out, dpi=140); plt.close(fig)
    return True


def fig_distribution(wl_all, out):
    if wl_all.empty:
        return False
    ok_runs = wl_all[wl_all["alter_status"] == "success"]
    data = [ok_runs[(ok_runs["phase"] == ph) & (ok_runs["status"] == "success")]["latency_ms"].values for ph in PHASES]
    if not any(len(d) for d in data):
        return False
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.boxplot([d if len(d) else [np.nan] for d in data], tick_labels=PHASES, showfliers=True)
    ax.set_yscale("log"); ax.set_ylabel("latency (ms, log) - successful statements")
    ax.set_title("Workload latency by phase (runs with successful ALTER, pooled)")
    fig.tight_layout(); fig.savefig(out, dpi=140); plt.close(fig)
    return True


def fig_errors(phase_df, out):
    if phase_df.empty:
        return False
    agg = phase_df.groupby(["change", "algorithm", "run_id"])["errors"].sum().reset_index()
    agg = agg[agg["errors"] > 0]
    if agg.empty:
        return False
    fig, ax = plt.subplots(figsize=(max(7, 0.7 * len(agg)), 5))
    ax.bar(range(len(agg)), agg["errors"], color="tab:red")
    ax.set_xticks(range(len(agg)), [f"{r.change}\n{r.algorithm}" for r in agg.itertuples()], rotation=90, fontsize=7)
    ax.set_ylabel("failed workload statements"); ax.set_title("Workload errors per run (runs without errors omitted)")
    fig.tight_layout(); fig.savefig(out, dpi=140); plt.close(fig)
    return True


# ---------------------------------------------------------------- report
def md_table(df, floatfmt="{:.3f}"):
    if df.empty:
        return "_no data_\n"
    cols = list(df.columns)
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        out.append("| " + " | ".join(floatfmt.format(v) if isinstance(v, float) and not np.isnan(v) else ("" if (isinstance(v, float) and np.isnan(v)) else str(v)) for v in r) + " |")
    return "\n".join(out) + "\n"


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("sweep_dir", type=Path)
    args = p.parse_args()
    alter_path = args.sweep_dir / "alter_results.csv"
    if not alter_path.exists():
        print(f"{alter_path} not found", file=sys.stderr)
        return 2
    alter = pd.read_csv(alter_path)
    if alter.empty:
        print("alter_results.csv is empty - nothing to analyse.", file=sys.stderr)
        return 2
    out_dir = args.sweep_dir / "analysis"
    out_dir.mkdir(exist_ok=True)

    summary = alter_summary(alter)
    phase_df, wl_all = workload_by_phase(alter, args.sweep_dir)
    summary.to_csv(out_dir / "alter_summary.csv", index=False)
    phase_df.to_csv(out_dir / "workload_by_phase.csv", index=False)

    made = {
        "fig_alter_duration.png": fig_alter_duration(summary, out_dir / "fig_alter_duration.png"),
        "fig_workload_p95.png": fig_p95(phase_df, out_dir / "fig_workload_p95.png"),
        "fig_latency_distribution.png": fig_distribution(wl_all, out_dir / "fig_latency_distribution.png"),
        "fig_workload_errors.png": fig_errors(phase_df, out_dir / "fig_workload_errors.png"),
    }

    meta = alter.iloc[0]
    during = phase_df[phase_df["phase"].isin(PHASES)].copy() if not phase_df.empty else phase_df
    view = (during.pivot_table(index=["change", "algorithm", "operation"], columns="phase",
                               values=["p95_ms", "errors"], aggfunc="max").reset_index()
            if not during.empty else pd.DataFrame())
    if not view.empty:
        view.columns = ["_".join(c for c in col if c) for col in view.columns]
    lines = [
        f"# Analysis of {args.sweep_dir.name}", "",
        f"- Server: `{meta['server_version']}`", f"- Dataset rows (target table): {meta['dataset_rows']}",
        f"- ALTER runs: {len(alter)}  (success: {(alter['status'] == 'success').sum()}, failure: {(alter['status'] != 'success').sum()})", "",
        "## ALTER duration and outcome", "", md_table(summary), "",
        "## Workload latency per phase (ms)", "",
        f"`low_sample=True` means fewer than {MIN_SAMPLE} statements in that phase: percentiles are not meaningful "
        "(typically the ALTER was too short to overlap many workload statements; use a larger dataset).", "",
        md_table(phase_df.drop(columns=["run_id"]) if not phase_df.empty else phase_df, "{:.2f}"), "",
        "## Figures", "",
    ] + [f"- {name}" if ok else f"- {name}: not generated (no applicable data)" for name, ok in made.items()]
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"analysis written to {out_dir}")
    print(summary.to_string(index=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
