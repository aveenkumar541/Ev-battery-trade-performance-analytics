# EV Performance Streamlit Dashboard

## New features

- **Maximize chart** button on every Plotly chart.
- **Target vs Achievement in KPI cards**:
  - SMP target vs achievement
  - Penalty Collection target vs achievement
  - Shows achievement percentage where the supplied target sheet supports it.
- **Multiple workbook upload**:
  - Upload 2 or more reporting-period Excel files.
  - Select the current/latest file.
  - Select a baseline/previous file.
  - Compare KPIs with baseline/current/change/direction.
  - Shows increasing, decreasing and unchanged KPI counts.
- Existing FOM, USCID, Employee Type, Skill Set and Current Status filters remain available.
- All Plotly chart text is styled dark for readability.
- Existing notebook charts, funnels and performance detail table are retained.

## Target logic

The supplied notebook contains a `Ritesh Target SMP & PENELTY` sheet. The notebook renames:
- `SMP` as the target
- `SMP DONE` as the achievement
- `PENELTY COLLECTION` as the penalty target
- `Amount colloted` as the penalty achievement

The dashboard uses those target fields in the KPI cards when available.

## Comparison logic

When multiple files are uploaded:
1. Choose the **Current / latest file**.
2. Choose the file to compare against in **Compare current with**.
3. The same dashboard filters are applied to both files.
4. The comparison table shows baseline, current, change and direction.

For a 3+ file workflow, you can upload all periods and change the current/baseline selections to compare any two periods.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```


## v3 UI enhancements

- Set KPI targets directly from the Streamlit sidebar.
- KPI cards automatically show:
  - green = target achieved
  - red = target missed
  - neutral = target not set
- SMP and Penalty Collection can still inherit targets from the workbook target sheet.
- Added 3D-style neumorphic cards, shadows, hover lift effects and chart containers.

## v4 UI upgrade
- Raised 3D/neumorphic chart panels with perspective, layered shadows and hover lift.
- Consistent light EV analytics theme across Plotly charts.
- Dark, high-contrast chart typography and hover labels for readability.
- Professionally styled responsive USCID performance table with sticky header, zebra rows, hover state and numeric alignment.
- Existing target-achievement green/red KPI cards, multi-file comparison and chart maximize controls retained.
# Ev-battery-trade-performance-analytics
