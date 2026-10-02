# 🍬 Nassau Candy Distributor — Profitability Intelligence Platform

> **A full-stack Streamlit analytics dashboard for product line profitability, margin diagnostics, geographic intelligence, and SKU scoring across Nassau Candy's entire distribution network.**

---

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Dataset](#dataset)
- [Installation](#installation)
- [Running the App](#running-the-app)
- [Dashboard Tabs](#dashboard-tabs)
- [Key KPIs](#key-kpis)
- [Filters & Controls](#filters--controls)
- [SKU Scoring Engine](#sku-scoring-engine)
- [Tech Stack](#tech-stack)

---

## Overview

Nassau Candy Distributor distributes 15 confectionery products across 4 US regions, sourced from 5 factories. This platform transforms raw order data into actionable profitability intelligence — answering questions like:

- Which products **truly** drive profit vs. just driving volume?
- Which divisions have structural margin problems?
- Where is the company over-dependent on a single SKU?
- Which products should be repriced, renegotiated, or discontinued?

---

## Project Structure

```
CANDY/
│
├── app.py                      # Main Streamlit dashboard (743 lines, 7 tabs, 30+ charts)
├── requirements.txt            # Pinned Python dependencies
├── README.md                   # This file
│
└── data/
    ├── generate_data.py        # Synthetic dataset generator (8,000 orders, 2021–2024)
    └── nassau_candy_sales.csv  # Generated on first run (auto-created)
```

---

## Dataset

The dataset is **auto-generated** on first launch if the CSV does not exist. It simulates 8,000 orders across 4 years (2021–2024) with realistic seasonal patterns, year-on-year growth trends, and margin noise.

### Fields

| Field | Description |
|-------|-------------|
| Row ID | Unique row identifier |
| Order ID | Unique order identifier |
| Order Date | Date the order was placed |
| Ship Date | Date the order was shipped |
| Ship Mode | Shipping method (Standard / Second / First / Same Day) |
| Ship Days | Transit days |
| Customer ID | Unique customer identifier |
| Customer Segment | Retail, Wholesale, or Online |
| Country/Region | United States |
| City / State/Province | Customer delivery location |
| Customer Lat / Lon | Coordinates for geo mapping |
| Region | East, West, Central, or South |
| Division | Chocolate, Sugar, or Other |
| Product ID / Product Name | Product identifier and full name |
| Factory | Supplying factory name |
| Factory Lat / Lon | Factory coordinates |
| Sales | Total order revenue |
| Units | Units ordered |
| Gross Profit | Sales − Cost |
| Cost | Manufacturing & delivery cost |

### Products & Factories

| Division | Product | Factory |
|----------|---------|---------|
| Chocolate | Wonka Bar - Nutty Crunch Surprise | Lot's O' Nuts |
| Chocolate | Wonka Bar - Fudge Mallows | Lot's O' Nuts |
| Chocolate | Wonka Bar - Scrumdiddlyumptious | Lot's O' Nuts |
| Chocolate | Wonka Bar - Milk Chocolate | Wicked Choccy's |
| Chocolate | Wonka Bar - Triple Dazzle Caramel | Wicked Choccy's |
| Sugar | Laffy Taffy | Sugar Shack |
| Sugar | SweeTARTS | Sugar Shack |
| Sugar | Nerds | Sugar Shack |
| Sugar | Fun Dip | Sugar Shack |
| Sugar | Everlasting Gobstopper | Secret Factory |
| Sugar | Hair Toffee | The Other Factory |
| Other | Fizzy Lifting Drinks | Sugar Shack |
| Other | Lickable Wallpaper | Secret Factory |
| Other | Wonka Gum | Secret Factory |
| Other | Kazookles | The Other Factory |

### Factory Coordinates

| Factory | Latitude | Longitude |
|---------|----------|-----------|
| Lot's O' Nuts | 32.881893 | -111.768036 |
| Wicked Choccy's | 32.076176 | -81.088371 |
| Sugar Shack | 48.119140 | -96.181150 |
| Secret Factory | 41.446333 | -90.565487 |
| The Other Factory | 35.117500 | -89.971107 |

---

## Installation

### 1. Prerequisites

- Python 3.9 or higher
- pip

### 2. Clone / download the project

Place the `CANDY/` folder anywhere on your machine.

### 3. Install dependencies

```bash
cd "C:\Users\there\OneDrive\Documents\Desktop\CANDY"
pip install -r requirements.txt
```

### Dependencies

```
streamlit==1.31.0
pandas==2.1.4
numpy==1.26.3
plotly==5.18.0
scipy==1.12.0
openpyxl==3.1.2
scikit-learn==1.4.0
```

---

## Running the App

```bash
cd "C:\Users\there\OneDrive\Documents\Desktop\CANDY"
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

> **First run:** The dataset (`nassau_candy_sales.csv`) is generated automatically. This takes a few seconds.

---

## Dashboard Tabs

### 📦 Tab 1 — Product Profitability
- Horizontal gross profit bar chart (colour-coded by margin %)
- Revenue vs Margin bubble chart (size = gross profit)
- Grouped Revenue / Cost / Gross Profit bar — Top 10 products
- Sunburst: Division → Product (gross profit)
- Treemap: Division → Factory → Product
- Profit share donut chart
- Full sortable product table with margin risk badges

### 🏭 Tab 2 — Division Deep-Dive
- Division snapshot KPI cards (Chocolate, Sugar, Other)
- Grouped Revenue vs GP vs Cost bar chart
- Profit Efficiency (GP ÷ Cost) comparison
- Margin distribution violin plot
- Normalised scorecard radar chart (4 dimensions)
- Stacked factory gross profit bar
- Division × Region margin heatmap

### 🔬 Tab 3 — Cost & Margin Diagnostics
- Cost vs Sales OLS trendline scatter
- Cost Ratio % bar chart by product
- At-risk product flags with remediation recommendations (Reprice / Renegotiate / Monitor)
- BCG-style pricing quadrant (Stars, Cash Cows, Gems, Dogs)
- Order-level margin distribution histogram
- Margin distribution box plot by ship mode

### 📐 Tab 4 — Profit Concentration
- Profit Pareto chart (dual-axis: GP bars + cumulative %)
- Revenue Pareto chart
- Pareto summary KPI cards (products → 80% of profit/revenue)
- Regional profit treemap (Region → State)
- Region × Division revenue heatmap
- Top SKU profit dependency gauge

### 📅 Tab 5 — Trend Analysis
- Monthly revenue line chart by division
- Monthly gross profit area chart by division
- Gross margin volatility band (average ± 1σ)
- Year-over-year revenue heatmap (month × year)
- Quarterly revenue vs gross profit grouped bar
- Profitability by shipping mode
- Orders & revenue by day of week (dual axis)

### 🗺️ Tab 6 — Geographic Intelligence
- Customer city scatter geo map (size = revenue, colour = margin)
- Factory bubble geo map (size = gross profit)
- Region revenue vs GP bar + profit share donut
- Region × Product margin heatmap
- Revenue by customer segment & region

### 🤖 Tab 7 — SKU Scoring Engine
- Adjustable-weight composite SKU health score (0–100)
- Grade distribution donut (A/B/C/D)
- Per-SKU grade cards with margin detail
- Sub-score heatmap (Margin, Revenue, Efficiency, Volume)
- 3D scatter: Revenue × Margin × Score
- Full scoring table with gradient formatting

---

## Key KPIs

| KPI | Formula |
|-----|---------|
| Gross Margin % | Gross Profit ÷ Sales × 100 |
| Profit per Unit | Gross Profit ÷ Units |
| Cost Ratio % | Cost ÷ Sales × 100 |
| Profit Efficiency | Gross Profit ÷ Cost |
| Revenue Contribution | Product Sales ÷ Total Sales × 100 |
| Profit Contribution | Product GP ÷ Total GP × 100 |
| SKU Score | Weighted composite of Margin, Revenue, Efficiency, Volume (0–100) |

---

## Filters & Controls

All sidebar filters apply **live across every chart** in every tab:

| Filter | Type | Description |
|--------|------|-------------|
| Order Date Range | Date picker | Filter all data by order date |
| Division | Multi-select | Chocolate, Sugar, Other |
| Region | Multi-select | East, West, Central, South |
| Ship Mode | Multi-select | Standard / Second / First / Same Day |
| Customer Segment | Multi-select | Retail, Wholesale, Online |
| Margin Risk Threshold | Slider (0–60%) | Products below this are flagged at-risk |
| Product Search | Text input | Fuzzy filter by product name |

---

## SKU Scoring Engine

The scoring engine in Tab 7 ranks every SKU on a **0–100 composite score** built from four normalised dimensions:

| Dimension | Default Weight | What it measures |
|-----------|---------------|-----------------|
| Margin Quality | 35% | Gross margin % normalised across portfolio |
| Revenue Scale | 25% | Total revenue contribution |
| Profit Efficiency | 25% | Gross profit per dollar of cost |
| Volume | 15% | Total units sold |

Weights are **fully adjustable** via sliders. Grades are assigned as:

| Grade | Score Range |
|-------|------------|
| A ⭐ | 80–100 |
| B 👍 | 60–79 |
| C ⚠️ | 40–59 |
| D 🔴 | 0–39 |

---

## Tech Stack

| Library | Purpose |
|---------|---------|
| [Streamlit](https://streamlit.io) | Web app framework |
| [Plotly](https://plotly.com/python/) | Interactive charts (30+ chart types) |
| [Pandas](https://pandas.pydata.org) | Data manipulation |
| [NumPy](https://numpy.org) | Numerical operations & noise generation |
| [SciPy](https://scipy.org) | Statistical analysis |
| [scikit-learn](https://scikit-learn.org) | Available for ML extensions |

---

*Nassau Candy Distributor · Profitability Intelligence Platform v3.0 · © 2025*
