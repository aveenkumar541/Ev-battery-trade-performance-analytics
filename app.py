
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="EV Performance Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# THEME / UI
# ---------------------------------------------------------
st.markdown("""
<style>
    :root { --navy:#0b1220; --navy2:#111c33; --blue:#2563eb; --cyan:#06b6d4; --text:#0f172a; --muted:#64748b; --surface:#f4f7fb; }
    .stApp { background: radial-gradient(circle at 10% 0%, #e8f1ff 0, #f4f7fb 34%, #eef2f7 100%); color:var(--text); }
    section[data-testid="stSidebar"] { background: linear-gradient(180deg,#08111f 0%,#101b30 55%,#0b1220 100%); box-shadow: 10px 0 35px rgba(2,8,23,.20); }
    section[data-testid="stSidebar"] * { color:#f8fafc !important; }
    section[data-testid="stSidebar"] input, section[data-testid="stSidebar"] textarea { color:#0f172a !important; background:#fff !important; }
    .dashboard-title { font-size:34px; font-weight:900; color:#0b1220; margin-bottom:2px; letter-spacing:-.03em; text-shadow:0 3px 8px rgba(15,23,42,.12); }
    .dashboard-subtitle { color:#64748b; font-size:14px; margin-bottom:18px; }
    .section-title { color:#0b1220; font-size:21px; font-weight:850; margin:24px 0 10px; text-shadow:0 2px 4px rgba(15,23,42,.10); }
    .kpi-card { background:linear-gradient(145deg,#ffffff,#e8edf5); border:1px solid #d6deea; border-radius:20px; padding:17px 18px; min-height:148px; box-shadow:10px 12px 24px rgba(15,23,42,.11),-6px -6px 14px rgba(255,255,255,.92),inset 0 1px 0 rgba(255,255,255,.95); transform:translateY(0) perspective(700px) rotateX(0deg); transition:.25s ease; position:relative; overflow:hidden; }
    .kpi-card:before { content:""; position:absolute; width:130px; height:130px; right:-55px; top:-65px; border-radius:50%; background:radial-gradient(circle,rgba(37,99,235,.16),transparent 68%); }
    .kpi-card:hover { transform:translateY(-6px) perspective(700px) rotateX(1deg); box-shadow:15px 19px 35px rgba(15,23,42,.16),-8px -8px 18px rgba(255,255,255,.98); }
    .kpi-card.target-achieved { border:2px solid #16a34a; background:linear-gradient(145deg,#f0fdf4,#d9fbe4); box-shadow:9px 12px 26px rgba(22,163,74,.18), inset 0 1px 0 #fff; }
    .kpi-card.target-missed { border:2px solid #dc2626; background:linear-gradient(145deg,#fff8f8,#fee2e2); box-shadow:9px 12px 26px rgba(220,38,38,.17), inset 0 1px 0 #fff; }
    .target-badge { position:absolute; top:12px; right:12px; padding:4px 9px; border-radius:999px; font-size:10px; font-weight:900; letter-spacing:.03em; box-shadow:0 2px 5px rgba(15,23,42,.10); }
    .badge-green { background:#dcfce7; color:#166534 !important; } .badge-red { background:#fee2e2; color:#991b1b !important; } .badge-neutral { background:#e2e8f0; color:#475569 !important; }
    .kpi-label { color:#475569; font-size:12px; font-weight:800; text-transform:uppercase; letter-spacing:.04em; } .kpi-value { color:#0f172a; font-size:27px; font-weight:900; margin-top:7px; } .kpi-target { color:#64748b; font-size:12px; margin-top:6px; } .kpi-ach { color:#0f172a; font-size:12px; font-weight:750; margin-top:4px; }
    .target-entry { background:linear-gradient(145deg,#fff,#e9eef6); border:1px solid #d7e0eb; border-radius:16px; padding:12px 15px; box-shadow:7px 8px 17px rgba(15,23,42,.10); }
    .target-note { color:#64748b; font-size:12px; margin:5px 0 12px; }
    .chart-shell { position:relative; margin:10px 0 22px; padding:9px; border-radius:22px; background:linear-gradient(145deg,#ffffff 0%,#edf2f8 48%,#dfe7f1 100%); border:1px solid #d7e0eb; box-shadow:12px 16px 28px rgba(15,23,42,.13),-7px -7px 16px rgba(255,255,255,.96),inset 0 1px 0 rgba(255,255,255,.95); transform:perspective(1100px) rotateX(.25deg); transition:transform .25s ease,box-shadow .25s ease; }
    .chart-shell:before { content:""; position:absolute; inset:6px; border-radius:18px; pointer-events:none; border:1px solid rgba(255,255,255,.75); box-shadow:inset 0 -10px 24px rgba(15,23,42,.035); }
    .chart-shell:hover { transform:perspective(1100px) rotateX(0deg) translateY(-3px); box-shadow:15px 21px 38px rgba(15,23,42,.17),-8px -8px 18px rgba(255,255,255,1); }
    .chart-caption { padding:5px 9px 2px; color:#64748b; font-size:11px; font-weight:700; }
    div[data-testid="stMetric"] { background:linear-gradient(145deg,#fff,#eaf0f7); border:1px solid #dbe3ee; padding:14px; border-radius:15px; box-shadow:7px 9px 17px rgba(15,23,42,.08); }
    .data-table-wrap { border-radius:20px; overflow:auto; border:1px solid #d6dfeb; background:#fff; box-shadow:12px 15px 28px rgba(15,23,42,.12),-6px -6px 15px rgba(255,255,255,.95); }
    table.ev-table { width:100%; border-collapse:separate; border-spacing:0; min-width:1150px; font-size:12px; color:#172033; }
    .ev-table th { position:sticky; top:0; z-index:2; padding:13px 12px; text-align:left; color:#fff; background:linear-gradient(135deg,#0b1220,#172b4d); border-bottom:1px solid #253a5d; font-weight:850; white-space:nowrap; }
    .ev-table td { padding:11px 12px; border-bottom:1px solid #e8edf3; white-space:nowrap; background:#fff; }
    .ev-table tbody tr:nth-child(even) td { background:#f7f9fc; }
    .ev-table tbody tr:hover td { background:#eaf3ff; box-shadow:inset 0 1px 0 rgba(37,99,235,.08),inset 0 -1px 0 rgba(37,99,235,.08); }
    .ev-table .num { text-align:right; font-variant-numeric:tabular-nums; } .ev-table .positive { color:#15803d; font-weight:800; } .ev-table .warning { color:#b45309; font-weight:800; } .ev-table .danger { color:#b91c1c; font-weight:800; }
    .compare-card { background:linear-gradient(145deg,#fff,#edf2f8); border:1px solid #dbe3ee; border-radius:16px; padding:14px 16px; box-shadow:7px 9px 17px rgba(15,23,42,.07); }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------
MAIN_SHEET = "Main "

REQUIRED_MAIN = [
    "TFE name", "USCID", "Current Status", "Employee Type",
    "Mapped Zones", "FOM", "Skill Set", "Total Assigned",
    "Within TAT %\n(Recons)", "Visits\n(HRAT)",
    "Found & Not\n picked\n(HRAT)", "Found & Picked\n(HRAT)",
    "Picked Within \nTAT(20 Hrs)\n(Movement)", "Retro Done",
    "Total \n(Tickets)", "Rejected\n(Tickets)",
    "Done Outside TAT\n(Tickets)", "Total QC Done", "QC Pass%",
    "Peanlty collection", "SMP", "CAB ", "RIR"
]

SUM_COLS = [
    "Total Assigned", "Visits\n(HRAT)",
    "Found & Not\n picked\n(HRAT)", "Found & Picked\n(HRAT)",
    "Picked Within \nTAT(20 Hrs)\n(Movement)", "Retro Done",
    "Total \n(Tickets)", "Rejected\n(Tickets)",
    "Done Outside TAT\n(Tickets)", "Total QC Done",
    "Peanlty collection", "SMP", "CAB ", "RIR"
]
AVG_COLS = ["Within TAT %\n(Recons)", "QC Pass%"]

KPI_META = {
    "Total Tickets": ("Total \n(Tickets)", "number"),
    "Total Assigned": ("Total Assigned", "number"),
    "Rejected": ("Rejected\n(Tickets)", "number"),
    "Within TAT": ("Within TAT %\n(Recons)", "percent"),
    "QC Pass": ("QC Pass%", "percent"),
    "QC Done": ("Total QC Done", "number"),
    "Retro Done": ("Retro Done", "number"),
    "Penalty Collection": ("Peanlty collection", "currency"),
    "SMP": ("SMP", "number"),
    "CAB": ("CAB ", "number"),
    "RIR": ("RIR", "number"),
    "Visits (HRAT)": ("Visits\n(HRAT)", "number"),
    "Picked Within TAT": ("Picked Within \nTAT(20 Hrs)\n(Movement)", "number"),
    "Found & Not Picked": ("Found & Not\n picked\n(HRAT)", "number"),
    "Found & Picked": ("Found & Picked\n(HRAT)", "number"),
}

# Targets that are explicitly supported by the supplied workbook structure.
# The notebook renames the target sheet to:
# SMP = target, SMP DONE = achievement,
# PENELTY COLLECTION = target, Amount colloted = achievement.
TARGET_SHEET_NAMES = [
    "Ritesh Target SMP & PENELTY",
    "Ritesh Target SMP & PENELTY ",
]

def clean_number(s):
    return pd.to_numeric(
        s.astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("₹", "", regex=False)
        .str.replace("%", "", regex=False)
        .str.strip(),
        errors="coerce"
    )

def clean_percent(s):
    x = pd.to_numeric(
        s.astype(str).str.replace("%", "", regex=False).str.strip(),
        errors="coerce"
    )
    if x.dropna().size and x.dropna().max() <= 1:
        x = x * 100
    return x

def normalise_usci(s):
    return s.fillna("Unknown").astype(str).str.strip()

def aggregate_active(main):
    active = main[main["Current Status"].eq("active")].copy()
    if active.empty:
        # Keep dashboard usable when a selected filter intentionally contains
        # no active records.
        return pd.DataFrame(columns=["FOM", "USCID"] + SUM_COLS + AVG_COLS)

    summary = (
        active.groupby(["FOM", "USCID"], dropna=False)
        .agg({
            "Total Assigned": "sum",
            "Within TAT %\n(Recons)": "mean",
            "Visits\n(HRAT)": "sum",
            "Found & Not\n picked\n(HRAT)": "sum",
            "Found & Picked\n(HRAT)": "sum",
            "Picked Within \nTAT(20 Hrs)\n(Movement)": "sum",
            "Retro Done": "sum",
            "Total \n(Tickets)": "sum",
            "Rejected\n(Tickets)": "sum",
            "Done Outside TAT\n(Tickets)": "sum",
            "Total QC Done": "sum",
            "QC Pass%": "mean",
            "Peanlty collection": "sum",
            "SMP": "sum",
            "CAB ": "sum",
            "RIR": "sum",
        })
        .reset_index()
    )
    summary["FOM"] = summary["FOM"].fillna("Unknown").astype(str)
    summary["USCID"] = summary["USCID"].fillna("Unknown").astype(str)
    return summary

def parse_target_sheet(sheets):
    """Return target/achievement totals and optional USCID-level target data."""
    target_sheet = None
    for name in TARGET_SHEET_NAMES:
        if name in sheets:
            target_sheet = sheets[name].copy()
            break
    if target_sheet is None:
        return {
            "available": False,
            "data": pd.DataFrame(),
            "smp_target": None,
            "smp_achievement": None,
            "penalty_target": None,
            "penalty_achievement": None,
        }

    # Match the transformations used in the notebook.
    rename_map = {
        "Unnamed: 4": "SMP DONE",
        "Unnamed: 5": "SMP PENDING",
        "Unnamed: 7": "Amount colloted",
        "Unnamed: 8": "penalty pending",
    }
    target_sheet = target_sheet.rename(columns=rename_map)

    # The notebook removes the first row and last 3 mostly-null columns.
    if len(target_sheet) > 1:
        target_sheet = target_sheet.iloc[1:, :].copy()

    target_sheet.columns = [str(c).strip() for c in target_sheet.columns]

    # Find columns flexibly because source workbooks can contain whitespace.
    def find_col(candidates):
        lookup = {str(c).strip().lower(): c for c in target_sheet.columns}
        for candidate in candidates:
            if candidate.lower() in lookup:
                return lookup[candidate.lower()]
        return None

    usc_col = find_col(["USCID"])
    smp_target_col = find_col(["SMP"])
    smp_done_col = find_col(["SMP DONE"])
    penalty_target_col = find_col(["PENELTY COLLECTION", "PENALTY COLLECTION"])
    penalty_done_col = find_col(["Amount colloted", "Amount collected"])

    if smp_target_col:
        target_sheet["__SMP_TARGET"] = clean_number(target_sheet[smp_target_col]).fillna(0)
    else:
        target_sheet["__SMP_TARGET"] = 0
    if smp_done_col:
        target_sheet["__SMP_DONE"] = clean_number(target_sheet[smp_done_col]).fillna(0)
    else:
        target_sheet["__SMP_DONE"] = 0
    if penalty_target_col:
        target_sheet["__PENALTY_TARGET"] = clean_number(target_sheet[penalty_target_col]).fillna(0)
    else:
        target_sheet["__PENALTY_TARGET"] = 0
    if penalty_done_col:
        target_sheet["__PENALTY_DONE"] = clean_number(target_sheet[penalty_done_col]).fillna(0)
    else:
        target_sheet["__PENALTY_DONE"] = 0

    if usc_col:
        target_sheet["USCID"] = normalise_usci(target_sheet[usc_col])
    else:
        target_sheet["USCID"] = "Unknown"

    return {
        "available": True,
        "data": target_sheet,
        "smp_target": float(target_sheet["__SMP_TARGET"].sum()),
        "smp_achievement": float(target_sheet["__SMP_DONE"].sum()),
        "penalty_target": float(target_sheet["__PENALTY_TARGET"].sum()),
        "penalty_achievement": float(target_sheet["__PENALTY_DONE"].sum()),
    }

def prepare_workbook(excel_file):
    sheets = pd.read_excel(excel_file, sheet_name=None)

    if MAIN_SHEET not in sheets:
        candidates = [x for x in sheets if x.strip() == "Main"]
        if not candidates:
            raise ValueError("The workbook must contain the 'Main ' sheet.")
        main_name = candidates[0]
    else:
        main_name = MAIN_SHEET

    main = sheets[main_name].copy()
    missing = [c for c in REQUIRED_MAIN if c not in main.columns]
    if missing:
        raise ValueError(
            "Missing required columns in Main sheet:\n- " + "\n- ".join(missing)
        )

    main["Current Status"] = main["Current Status"].astype(str).str.lower().str.strip()
    main["USCID"] = normalise_usci(main["USCID"])

    # Exact notebook logic: len(x.split(',')) for strings.
    main["Mapped Zones_counts"] = main["Mapped Zones"].apply(
        lambda x: len(x.split(",")) if isinstance(x, str) else 0
    )

    main["Skill Set"] = main["Skill Set"].fillna("Unknown").astype(str)
    main["FOM"] = main["FOM"].fillna("Unknown").astype(str)
    main["Employee Type"] = main["Employee Type"].fillna("Unknown").astype(str)

    for c in SUM_COLS:
        main[c] = clean_number(main[c]).fillna(0)
    for c in AVG_COLS:
        main[c] = clean_percent(main[c])

    summary = aggregate_active(main)
    targets = parse_target_sheet(sheets)

    return {
        "sheets": sheets,
        "main": main,
        "summary": summary,
        "targets": targets,
    }

def apply_filters(main, selected_fom, selected_uscid, selected_employee,
                  selected_skill, selected_status):
    df = main.copy()
    if selected_fom != "All FOM":
        df = df[df["FOM"] == selected_fom]
    if selected_uscid != "All USCID":
        df = df[df["USCID"] == selected_uscid]
    if selected_employee != "All Employee Types":
        df = df[df["Employee Type"] == selected_employee]
    if selected_skill != "All Skill Sets":
        df = df[df["Skill Set"] == selected_skill]
    if selected_status != "All Status":
        df = df[df["Current Status"] == selected_status]
    return df

def get_target_totals(workbook, filtered_main):
    """Return target totals for the currently selected USCID/FOM scope."""
    t = workbook["targets"]
    if not t["available"]:
        return {}

    td = t["data"].copy()

    # Target sheet has USCID, not necessarily FOM. Therefore:
    # - USCID filter can be applied exactly.
    # - For a FOM-only scope, derive the allowed USCIDs from Main.
    if "USCID" in td.columns:
        allowed = set(filtered_main["USCID"].astype(str))
        if allowed:
            td = td[td["USCID"].astype(str).isin(allowed)]

    result = {
        "SMP": float(td["__SMP_TARGET"].sum()) if "__SMP_TARGET" in td else None,
        "Penalty Collection": float(td["__PENALTY_TARGET"].sum()) if "__PENALTY_TARGET" in td else None,
    }
    return result

def aggregate_for_dashboard(main_filtered):
    return aggregate_active(main_filtered)

def metric_value(summary, label):
    if summary.empty:
        return 0.0
    col, fmt = KPI_META[label]
    if fmt == "percent":
        return float(summary[col].mean()) if not summary[col].dropna().empty else 0.0
    return float(summary[col].sum()) if col in summary else 0.0

def format_value(value, fmt):
    value = 0 if value is None or pd.isna(value) else float(value)
    if fmt == "percent":
        return f"{value:,.2f}%"
    if fmt == "currency":
        return f"₹{value:,.2f}"
    return f"{value:,.0f}"

def achievement_pct(actual, target):
    if target is None or pd.isna(target) or float(target) == 0:
        return None
    return float(actual) / float(target) * 100

def comparison_delta(current, baseline, fmt):
    delta = float(current) - float(baseline)
    if fmt == "percent":
        text = f"{delta:+,.2f} pp"
    elif fmt == "currency":
        text = f"{delta:+,.2f}"
    else:
        text = f"{delta:+,.0f}"
    return delta, text

def make_funnel(df, config, title):
    labels, values, display = [], [], []
    for col, meta in config.items():
        value = df[col].mean() if meta["agg"] == "avg" else df[col].sum()
        value = 0 if pd.isna(value) else float(value)
        labels.append(meta["label"])
        values.append(value)
        if meta["format"] == "percent":
            display.append(f"{value:,.2f}%")
        elif meta["format"] == "currency":
            display.append(f"₹{value:,.2f}")
        else:
            display.append(f"{value:,.0f}")

    fig = go.Figure(
        go.Funnel(
            y=labels, x=values, text=display, textinfo="text",
            hovertemplate="<b>%{y}</b><br>Value: %{text}<extra></extra>",
            marker=dict(line=dict(width=1)),
        )
    )
    fig.update_layout(
        title=title, height=570, margin=dict(l=30, r=30, t=70, b=25),
        paper_bgcolor="white", plot_bgcolor="white", font=dict(color="#111827"),
    )
    return style_plotly(fig)

def style_plotly(fig):
    fig.update_layout(
        font=dict(color="#172033", family="Inter, Segoe UI, sans-serif"),
        title_font=dict(color="#0b1220", size=17),
        legend=dict(font=dict(color="#172033"), bgcolor="rgba(255,255,255,.55)", bordercolor="rgba(148,163,184,.25)", borderwidth=1),
        paper_bgcolor="rgba(255,255,255,0)", plot_bgcolor="rgba(255,255,255,0)",
        hoverlabel=dict(bgcolor="#0b1220", font_color="#ffffff", bordercolor="#2563eb"),
        margin=dict(l=45,r=28,t=58,b=45),
    )
    fig.update_xaxes(title_font=dict(color="#334155"), tickfont=dict(color="#334155"), gridcolor="rgba(148,163,184,.18)", zerolinecolor="rgba(100,116,139,.25)")
    fig.update_yaxes(title_font=dict(color="#334155"), tickfont=dict(color="#334155"), gridcolor="rgba(148,163,184,.18)", zerolinecolor="rgba(100,116,139,.25)")
    # Consistent EV dashboard palette and dimensional highlights.
    for tr in fig.data:
        if hasattr(tr, "marker") and tr.marker is not None:
            try:
                tr.marker.line = dict(width=1, color="rgba(255,255,255,.65)")
            except Exception:
                pass
    return fig

def render_chart(fig, key, height=None, caption=None):
    """Render a themed, raised 3D-style chart panel with maximize control."""
    is_max = st.session_state.get("max_chart") == key
    button_label = "↙ Restore chart" if is_max else "⛶ Maximize chart"
    if st.button(button_label, key=f"max_{key}", use_container_width=False):
        st.session_state["max_chart"] = None if is_max else key
        st.rerun()
    if height:
        fig.update_layout(height=max(700, height) if is_max else height)
    st.markdown('<div class="chart-shell">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": True, "displaylogo": False, "responsive": True})
    if caption:
        st.markdown(f'<div class="chart-caption">{caption}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def comparison_status(delta, higher_is_better=True):
    if abs(delta) < 1e-9:
        return "flat", "No change"
    good = delta > 0 if higher_is_better else delta < 0
    return ("up", "↑ Improving") if good else ("down", "↓ Declining")

# ---------------------------------------------------------
# USER-DEFINED TARGETS
# ---------------------------------------------------------
# These targets can be entered directly in the website. They are
# intentionally separate from workbook targets so the user can override
# or add operational targets without changing the Excel file.
DEFAULT_TARGETS = {
    "Total Tickets": None,
    "Total Assigned": None,
    "Rejected": None,
    "Within TAT": None,
    "QC Pass": None,
    "QC Done": None,
    "Retro Done": None,
    "SMP": None,
    "Penalty Collection": None,
    "CAB": None,
    "RIR": None,
    "Visits (HRAT)": None,
    "Picked Within TAT": None,
    "Found & Not Picked": None,
    "Found & Picked": None,
}

if "custom_targets" not in st.session_state:
    st.session_state["custom_targets"] = DEFAULT_TARGETS.copy()

def set_target(label, value):
    if value is None:
        st.session_state["custom_targets"][label] = None
    else:
        st.session_state["custom_targets"][label] = float(value)

def target_is_higher_better(label):
    # For rejection and outside-TAT type KPIs, lower is better.
    return label not in {"Rejected"}

# ---------------------------------------------------------
# SIDEBAR — MULTI-FILE INPUT
# ---------------------------------------------------------
st.sidebar.markdown("## ⚡ EV Performance")
st.sidebar.caption("Operational performance analytics")

uploaded_files = st.sidebar.file_uploader(
    "Upload one or more Target Vs Achievement workbooks",
    type=["xlsx", "xls"],
    accept_multiple_files=True,
    help="Upload multiple reporting-period files to compare performance.",
)

if not uploaded_files:
    st.markdown('<div class="dashboard-title">EV Performance Dashboard</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="dashboard-subtitle">'
        "Upload one or more EV performance workbooks from the sidebar."
        "</div>",
        unsafe_allow_html=True,
    )
    st.info(
        "Single-file mode gives the full operational dashboard. "
        "Upload 2+ files to enable period-to-period performance comparison."
    )
    c1, c2, c3 = st.columns(3)
    c1.metric("Data source", "Excel workbook(s)")
    c2.metric("Primary sheet", "Main")
    c3.metric("Dashboard mode", "Interactive + comparison")
    st.stop()

# ---------------------------------------------------------
# LOAD ALL WORKBOOKS
# ---------------------------------------------------------
workbooks = {}
for uploaded in uploaded_files:
    try:
        workbooks[uploaded.name] = prepare_workbook(uploaded)
    except Exception as e:
        st.sidebar.error(f"{uploaded.name}: {e}")

if not workbooks:
    st.error("No valid workbook could be loaded.")
    st.stop()

file_names = list(workbooks.keys())
current_file = st.sidebar.selectbox("Current / latest file", file_names, index=len(file_names)-1)
current_book = workbooks[current_file]
main = current_book["main"]
summary = current_book["summary"]

# Comparison selection
baseline_file = None
if len(file_names) >= 2:
    prior_options = [x for x in file_names if x != current_file]
    baseline_file = st.sidebar.selectbox(
        "Compare current with",
        prior_options,
        index=0,
        help="Choose the baseline/previous workbook for increase-decrease analysis.",
    )

st.sidebar.divider()

# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------
fom_options = ["All FOM"] + sorted(summary["FOM"].dropna().unique().tolist())
selected_fom = st.sidebar.selectbox("FOM", fom_options)

filtered_for_uscid = summary if selected_fom == "All FOM" else summary[summary["FOM"] == selected_fom]
uscid_options = ["All USCID"] + sorted(filtered_for_uscid["USCID"].dropna().unique().tolist())
selected_uscid = st.sidebar.selectbox("USCID", uscid_options)

employee_options = ["All Employee Types"] + sorted(main["Employee Type"].dropna().astype(str).unique().tolist())
selected_employee = st.sidebar.selectbox("Employee Type", employee_options)

skill_options = ["All Skill Sets"] + sorted(main["Skill Set"].dropna().astype(str).unique().tolist())
selected_skill = st.sidebar.selectbox("Skill Set", skill_options)

status_options = ["All Status"] + sorted(main["Current Status"].dropna().astype(str).unique().tolist())
selected_status = st.sidebar.selectbox("Current Status", status_options)

st.sidebar.divider()
with st.sidebar.expander("🎯 Set KPI Targets", expanded=False):
    st.caption("Enter targets directly in the website. Cards turn green when achieved and red when missed.")
    for target_label in ["Total Tickets", "Total Assigned", "Rejected", "Within TAT",
                         "QC Pass", "QC Done", "Retro Done", "SMP",
                         "Penalty Collection", "CAB", "RIR", "Visits (HRAT)"]:
        fmt = KPI_META[target_label][1]
        current_target = st.session_state["custom_targets"].get(target_label)

        # Workbook target is used as the initial/default target for supported KPIs.
        workbook_target = None
        if target_label == "SMP":
            workbook_target = current_book["targets"].get("smp_target")
        elif target_label == "Penalty Collection":
            workbook_target = current_book["targets"].get("penalty_target")

        if current_target is None and workbook_target is not None:
            current_target = workbook_target

        step = 0.1 if fmt == "percent" else 1.0
        if fmt == "currency":
            step = 100.0

        entered = st.number_input(
            f"{target_label} target",
            min_value=0.0,
            value=float(current_target or 0.0),
            step=step,
            key=f"target_input_{target_label}",
        )
        st.session_state["custom_targets"][target_label] = entered if entered > 0 else None

main_filtered = apply_filters(
    main, selected_fom, selected_uscid,
    selected_employee, selected_skill, selected_status
)
filtered = aggregate_for_dashboard(main_filtered)

# Target scope
target_totals = get_target_totals(current_book, main_filtered)

st.sidebar.caption(f"Loaded files: {len(workbooks)}")
st.sidebar.caption(f"Filtered active USCID groups: {len(filtered):,}")
st.sidebar.caption(f"Filtered source rows: {len(main_filtered):,}")

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
scope = "All FOM" if selected_fom == "All FOM" else selected_fom
if selected_uscid != "All USCID":
    scope += f" • {selected_uscid}"
if selected_employee != "All Employee Types":
    scope += f" • {selected_employee}"
if selected_skill != "All Skill Sets":
    scope += f" • {selected_skill}"

st.markdown('<div class="dashboard-title">EV Performance Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="dashboard-subtitle">'
    f"Operational performance • {scope} • <b>{current_file}</b>"
    f"</div>",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# KPI CARDS — TARGET VS ACHIEVEMENT
# ---------------------------------------------------------
st.markdown('<div class="section-title">KPI Performance</div>', unsafe_allow_html=True)

kpi_labels = [
    "Total Tickets", "Total Assigned", "Rejected", "Within TAT",
    "QC Pass", "QC Done", "Retro Done", "SMP",
    "Penalty Collection", "CAB", "RIR", "Visits (HRAT)"
]

target_map = {
    label: st.session_state["custom_targets"].get(label)
    for label in KPI_META
}
# Workbook targets remain available automatically for the two supported target-sheet KPIs.
if target_map.get("SMP") is None:
    target_map["SMP"] = target_totals.get("SMP")
if target_map.get("Penalty Collection") is None:
    target_map["Penalty Collection"] = target_totals.get("Penalty Collection")

cards = []
for label in kpi_labels:
    col, fmt = KPI_META[label]
    actual = metric_value(filtered, label)
    target = target_map.get(label)
    ach = achievement_pct(actual, target)

    status_class = "neutral"
    badge_class = "badge-neutral"
    badge_text = "TARGET NOT SET"

    if target is not None:
        higher_better = target_is_higher_better(label)
        achieved = actual >= target if higher_better else actual <= target
        if achieved:
            status_class = "target-achieved"
            badge_class = "badge-green"
            badge_text = "✓ TARGET ACHIEVED"
        else:
            status_class = "target-missed"
            badge_class = "badge-red"
            badge_text = "✕ TARGET MISSED"

    cards.append((label, fmt, actual, target, ach, status_class, badge_class, badge_text))

cols = st.columns(4)
for i, (label, fmt, actual, target, ach, status_class, badge_class, badge_text) in enumerate(cards):
    target_text = "Target: —"
    ach_text = "Achievement vs target: —"
    if target is not None:
        target_text = f"Target: {format_value(target, fmt)}"
        ach_text = (
            f"Achievement: {ach:,.1f}%"
            if ach is not None else "Achievement: —"
        )

    with cols[i % 4]:
        st.markdown(
            f"""
            <div class="kpi-card {status_class}">
                <div class="target-badge {badge_class}">{badge_text}</div>
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{format_value(actual, fmt)}</div>
                <div class="kpi-target">{target_text}</div>
                <div class="kpi-ach">{ach_text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------
# MULTI-FILE COMPARISON
# ---------------------------------------------------------
if baseline_file:
    st.markdown('<div class="section-title">Period Comparison — Increase / Decrease</div>', unsafe_allow_html=True)
    baseline_book = workbooks[baseline_file]

    # Apply the same user-selected filters where values exist in the baseline.
    base_main = baseline_book["main"]
    base_fom_options = set(base_main["FOM"].astype(str))
    base_uscid_options = set(base_main["USCID"].astype(str))
    base_employee_options = set(base_main["Employee Type"].astype(str))
    base_skill_options = set(base_main["Skill Set"].astype(str))
    base_status_options = set(base_main["Current Status"].astype(str))

    base_df = base_main.copy()
    if selected_fom != "All FOM" and selected_fom in base_fom_options:
        base_df = base_df[base_df["FOM"] == selected_fom]
    elif selected_fom != "All FOM":
        base_df = base_df.iloc[0:0]

    if selected_uscid != "All USCID" and selected_uscid in base_uscid_options:
        base_df = base_df[base_df["USCID"] == selected_uscid]
    elif selected_uscid != "All USCID":
        base_df = base_df.iloc[0:0]

    if selected_employee != "All Employee Types" and selected_employee in base_employee_options:
        base_df = base_df[base_df["Employee Type"] == selected_employee]
    elif selected_employee != "All Employee Types":
        base_df = base_df.iloc[0:0]

    if selected_skill != "All Skill Sets" and selected_skill in base_skill_options:
        base_df = base_df[base_df["Skill Set"] == selected_skill]
    elif selected_skill != "All Skill Sets":
        base_df = base_df.iloc[0:0]

    if selected_status != "All Status" and selected_status in base_status_options:
        base_df = base_df[base_df["Current Status"] == selected_status]
    elif selected_status != "All Status":
        base_df = base_df.iloc[0:0]

    base_summary = aggregate_for_dashboard(base_df)

    compare_labels = [
        "Total Tickets", "Total Assigned", "Rejected", "Within TAT",
        "QC Pass", "QC Done", "Retro Done", "SMP", "Penalty Collection",
        "CAB", "RIR", "Visits (HRAT)", "Picked Within TAT",
        "Found & Not Picked", "Found & Picked"
    ]

    compare_rows = []
    for label in compare_labels:
        fmt = KPI_META[label][1]
        cur = metric_value(filtered, label)
        prev = metric_value(base_summary, label)
        delta, delta_text = comparison_delta(cur, prev, fmt)

        # For operational KPIs, higher is generally better except Rejected
        # and Outside-TAT type measures. We don't show a false universal
        # "good/bad" judgement; direction is explicitly shown.
        direction = "↑ Increasing" if delta > 0 else ("↓ Decreasing" if delta < 0 else "→ Flat")
        compare_rows.append({
            "KPI": label,
            "Baseline": format_value(prev, fmt),
            "Current": format_value(cur, fmt),
            "Change": delta_text,
            "Direction": direction,
            "_delta": delta,
        })

    compare_df = pd.DataFrame(compare_rows)

    c1, c2, c3 = st.columns(3)
    improved_count = int((compare_df["_delta"] > 0).sum())
    decreased_count = int((compare_df["_delta"] < 0).sum())
    flat_count = int((compare_df["_delta"] == 0).sum())
    c1.metric("KPIs increasing", improved_count)
    c2.metric("KPIs decreasing", decreased_count)
    c3.metric("KPIs unchanged", flat_count)

    st.dataframe(
        compare_df.drop(columns=["_delta"]).style,
        use_container_width=True,
        hide_index=True,
    )

    # Visual comparison for key performance measures.
    comp_plot = compare_df[compare_df["KPI"].isin([
        "Total Tickets", "Total Assigned", "Rejected",
        "QC Done", "Retro Done", "SMP", "CAB", "RIR"
    ])].copy()

    fig_compare = px.bar(
        comp_plot,
        x="KPI",
        y=["Baseline", "Current"],
        barmode="group",
        title=f"Baseline vs Current — {baseline_file} → {current_file}",
    )
    # Convert display strings back to numeric for plotting.
    plot_numeric = []
    for label in comp_plot["KPI"]:
        fmt = KPI_META[label][1]
        plot_numeric.append({
            "KPI": label,
            "Baseline": metric_value(base_summary, label),
            "Current": metric_value(filtered, label),
        })
    fig_compare = px.bar(
        pd.DataFrame(plot_numeric),
        x="KPI",
        y=["Baseline", "Current"],
        barmode="group",
        title="Baseline vs Current — Key KPIs",
        text_auto=True,
    )
    style_plotly(fig_compare)
    render_chart(fig_compare, "comparison", 450)

# ---------------------------------------------------------
# PERFORMANCE OVERVIEW
# ---------------------------------------------------------
st.markdown('<div class="section-title">Performance Overview</div>', unsafe_allow_html=True)

fom_perf = (
    filtered.groupby("FOM", dropna=False)
    .agg(
        Assigned=("Total Assigned", "sum"),
        Tickets=("Total \n(Tickets)", "sum"),
        Rejected=("Rejected\n(Tickets)", "sum"),
        QC_Done=("Total QC Done", "sum"),
        Retro_Done=("Retro Done", "sum"),
    )
    .reset_index()
)

fig_fom = px.bar(
    fom_perf, x="FOM",
    y=["Assigned", "Tickets", "QC_Done", "Retro_Done"],
    barmode="group", title="FOM-wise Operational Performance",
)
style_plotly(fig_fom)

status_counts = (
    main_filtered["Current Status"].value_counts()
    .rename_axis("Status").reset_index(name="Count")
)
fig_status = px.pie(
    status_counts, names="Status", values="Count",
    hole=0.58, title="USC Status Distribution",
)
style_plotly(fig_status)

col_a, col_b = st.columns([1.6, 1])
with col_a:
    render_chart(fig_fom, "fom_performance", 430)
with col_b:
    render_chart(fig_status, "status_distribution", 430)

# ---------------------------------------------------------
# SECONDARY PERFORMANCE CHARTS
# ---------------------------------------------------------
col_c, col_d = st.columns(2)

tat_df = (
    filtered.groupby("FOM", dropna=False)
    .agg(
        Within_TAT=("Within TAT %\n(Recons)", "mean"),
        Outside_TAT=("Done Outside TAT\n(Tickets)", "sum"),
    )
    .reset_index()
)
fig_tat = px.bar(
    tat_df, x="FOM", y=["Within_TAT", "Outside_TAT"],
    barmode="group", title="TAT Performance by FOM",
)
style_plotly(fig_tat)
fig_tat.update_yaxes(title="Value / %")

qc_df = (
    filtered.groupby("FOM", dropna=False)
    .agg(QC_Pass=("QC Pass%", "mean"), QC_Done=("Total QC Done", "sum"))
    .reset_index()
)
fig_qc = px.bar(
    qc_df, x="FOM", y=["QC_Pass", "QC_Done"],
    barmode="group", title="QC Performance by FOM",
)
style_plotly(fig_qc)
fig_qc.update_yaxes(title="Value / %")

with col_c:
    render_chart(fig_tat, "tat_performance", 390)
with col_d:
    render_chart(fig_qc, "qc_performance", 390)

# ---------------------------------------------------------
# NOTEBOOK CHARTS
# ---------------------------------------------------------
status_uscs = (
    main_filtered.groupby("Current Status")["USCID"]
    .nunique().reset_index(name="USCID")
)
fig_status_bar = px.bar(
    status_uscs, x="Current Status", y="USCID",
    color="Current Status", title="USCID by Current Status", text="USCID",
)
fig_status_bar.update_traces(textposition="outside", textfont=dict(color="#111827"))
style_plotly(fig_status_bar)

zone_perf = (
    main_filtered.groupby("USCID", dropna=False)["Mapped Zones_counts"]
    .sum().sort_values(ascending=False).head(20).reset_index()
)
fig_zones = px.bar(
    zone_perf, x="Mapped Zones_counts", y="USCID",
    orientation="h", title="Top 20 USCID by Mapped Zones",
    text="Mapped Zones_counts",
)
fig_zones.update_traces(textposition="outside", textfont=dict(color="#111827"))
style_plotly(fig_zones)

treemap_df = (
    main_filtered[["Skill Set", "FOM", "USCID"]]
    .dropna(subset=["Skill Set", "FOM", "USCID"])
    .groupby(["Skill Set", "FOM"])["USCID"]
    .nunique().reset_index(name="USCID")
)
fig_tree = px.treemap(
    treemap_df, path=["Skill Set", "FOM"], values="USCID",
    color="USCID", title="USCID Distribution — Skill Set & FOM",
)
style_plotly(fig_tree)

chart_row1, chart_row2 = st.columns(2)
with chart_row1:
    render_chart(fig_status_bar, "status_bar", 390)
with chart_row2:
    render_chart(fig_zones, "mapped_zones", 520)
render_chart(fig_tree, "skill_fom_treemap", 520)

# ---------------------------------------------------------
# FUNNELS
# ---------------------------------------------------------
funnel1_config = {
    "Total \n(Tickets)": {"label": "Total Tickets", "format": "number", "agg": "sum"},
    "Total Assigned": {"label": "Total Assigned", "format": "number", "agg": "sum"},
    "Rejected\n(Tickets)": {"label": "Rejected", "format": "number", "agg": "sum"},
    "SMP": {"label": "SMP", "format": "number", "agg": "sum"},
    "Within TAT %\n(Recons)": {"label": "Within TAT %", "format": "percent", "agg": "avg"},
    "Done Outside TAT\n(Tickets)": {"label": "Outside TAT", "format": "number", "agg": "sum"},
    "QC Pass%": {"label": "QC %", "format": "percent", "agg": "avg"},
    "Total QC Done": {"label": "QC Done", "format": "number", "agg": "sum"},
    "Retro Done": {"label": "Retro Done", "format": "number", "agg": "sum"},
    "Peanlty collection": {"label": "Penalty Collection", "format": "currency", "agg": "sum"},
}

st.markdown('<div class="section-title">Operational Funnel</div>', unsafe_allow_html=True)
render_chart(
    make_funnel(filtered, funnel1_config, f"Operational Funnel — {scope}"),
    "operational_funnel", 570
)

funnel2_config = {
    "CAB ": {"label": "CAB", "format": "number", "agg": "sum"},
    "RIR": {"label": "RIR", "format": "number", "agg": "sum"},
    "Visits\n(HRAT)": {"label": "Visits (HRAT)", "format": "number", "agg": "sum"},
    "Picked Within \nTAT(20 Hrs)\n(Movement)": {
        "label": "Picked Within TAT (20 Hrs)", "format": "number", "agg": "sum"
    },
    "Found & Not\n picked\n(HRAT)": {
        "label": "Found & Not Picked", "format": "number", "agg": "sum"
    },
    "Found & Picked\n(HRAT)": {
        "label": "Found & Picked", "format": "number", "agg": "sum"
    },
}

st.markdown('<div class="section-title">HRAT / Movement Funnel</div>', unsafe_allow_html=True)
render_chart(
    make_funnel(filtered, funnel2_config, f"HRAT Operational Funnel — {scope}"),
    "movement_funnel", 570
)

# ---------------------------------------------------------
# PERFORMANCE TABLE
# ---------------------------------------------------------
st.markdown('<div class="section-title">USCID Performance Detail</div>', unsafe_allow_html=True)

table_df = filtered[
    [
        "FOM", "USCID", "Total \n(Tickets)", "Total Assigned",
        "Rejected\n(Tickets)", "SMP", "Within TAT %\n(Recons)",
        "Done Outside TAT\n(Tickets)", "QC Pass%", "Total QC Done",
        "Retro Done", "Peanlty collection", "CAB ", "RIR",
    ]
].copy()

table_df = table_df.rename(columns={
    "Total \n(Tickets)": "Total Tickets",
    "Rejected\n(Tickets)": "Rejected",
    "Within TAT %\n(Recons)": "Within TAT %",
    "Done Outside TAT\n(Tickets)": "Outside TAT",
    "QC Pass%": "QC %",
    "Total QC Done": "QC Done",
    "Peanlty collection": "Penalty Collection",
    "CAB ": "CAB",
})

def render_html_table(df):
    display_df = df.copy()
    fmt_map = {
        "Total Tickets": lambda x: f"{x:,.0f}", "Total Assigned": lambda x: f"{x:,.0f}",
        "Rejected": lambda x: f"{x:,.0f}", "SMP": lambda x: f"{x:,.0f}",
        "Within TAT %": lambda x: f"{x:,.2f}%", "Outside TAT": lambda x: f"{x:,.0f}",
        "QC %": lambda x: f"{x:,.2f}%", "QC Done": lambda x: f"{x:,.0f}",
        "Retro Done": lambda x: f"{x:,.0f}", "Penalty Collection": lambda x: f"₹{x:,.2f}",
        "CAB": lambda x: f"{x:,.0f}", "RIR": lambda x: f"{x:,.0f}",
    }
    for col, fn in fmt_map.items():
        if col in display_df:
            display_df[col] = display_df[col].apply(lambda v: fn(float(v)) if pd.notna(v) else "—")
    html = ['<div class="data-table-wrap"><table class="ev-table"><thead><tr>']
    html += [f'<th>{c}</th>' for c in display_df.columns]
    html.append('</tr></thead><tbody>')
    for _, row in display_df.iterrows():
        html.append('<tr>')
        for c, v in row.items():
            cls = 'num' if c in fmt_map else ''
            if c == 'Rejected': cls += ' danger'
            elif c in {'Within TAT %','QC %'}: cls += ' positive'
            html.append(f'<td class="{cls.strip()}">{v}</td>')
        html.append('</tr>')
    html.append('</tbody></table></div>')
    st.markdown(''.join(html), unsafe_allow_html=True)

render_html_table(table_df)

st.caption(
    "Source logic follows the supplied EV Performance notebook: active records are "
    "grouped by FOM and USCID with sum/mean aggregation. The mapped-zone count also "
    "follows the notebook's comma-split logic."
)
