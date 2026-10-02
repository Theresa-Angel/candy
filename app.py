# Nassau Candy Distributor — Elite Profitability Intelligence Platform v3.0
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os, sys, subprocess
from scipy import stats

st.set_page_config(
    page_title="Nassau Candy Intelligence",
    page_icon="\U0001f36c",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
/* ── App background ── */
[data-testid="stAppViewContainer"]{background:radial-gradient(ellipse at top left,#0d0221 0%,#1a0533 40%,#0a1628 100%);}
[data-testid="stHeader"]{background:transparent;}

/* ── Sidebar background ── */
[data-testid="stSidebar"]{background:linear-gradient(180deg,#110022 0%,#0a1628 100%) !important;border-right:1px solid rgba(180,100,255,.25);}

/* ── ALL sidebar text white ── */
[data-testid="stSidebar"] *{color:#f0f0f0 !important;}

/* ── Sidebar labels (filter titles) ── */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stTextInput label,
[data-testid="stSidebar"] .stDateInput label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div{color:#f0f0f0 !important;}

/* ── Sidebar markdown headers ── */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4{color:#c77dff !important;}

/* ── Multiselect widget ── */
[data-testid="stSidebar"] [data-baseweb="select"] *{color:#f0f0f0 !important;background:rgba(30,10,60,.9) !important;}
[data-testid="stSidebar"] [data-baseweb="select"] [data-baseweb="tag"]{background:rgba(140,60,255,.35) !important;color:#f0f0f0 !important;}
[data-testid="stSidebar"] [data-baseweb="input"]{background:rgba(30,10,60,.9) !important;color:#f0f0f0 !important;}
[data-testid="stSidebar"] [data-baseweb="input"] input{color:#f0f0f0 !important;}

/* ── Multiselect dropdown menu ── */
[data-baseweb="popover"] *{background:#1a0a3a !important;color:#f0f0f0 !important;}
[data-baseweb="menu"] li:hover{background:rgba(140,60,255,.3) !important;}

/* ── Slider ── */
[data-testid="stSidebar"] [data-testid="stSlider"] *{color:#f0f0f0 !important;}
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] [role="slider"]{background:#c77dff !important;}

/* ── Text input ── */
[data-testid="stSidebar"] input{background:rgba(30,10,60,.9) !important;color:#f0f0f0 !important;border:1px solid rgba(180,100,255,.4) !important;border-radius:8px !important;}
[data-testid="stSidebar"] input::placeholder{color:rgba(255,255,255,.4) !important;}

/* ── Date input ── */
[data-testid="stSidebar"] [data-testid="stDateInput"] input{color:#f0f0f0 !important;background:rgba(30,10,60,.9) !important;}

/* ── Main content text ── */
[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] span,
[data-testid="stAppViewContainer"] div,
[data-testid="stAppViewContainer"] label{color:#f0f0f0;}

/* ── KPI cards ── */
.kpi-card{background:linear-gradient(135deg,rgba(140,60,255,.12),rgba(255,80,120,.10));border:1px solid rgba(180,100,255,.30);border-radius:18px;padding:20px 14px 16px;text-align:center;backdrop-filter:blur(12px);transition:transform .25s,box-shadow .25s;margin-bottom:4px;}
.kpi-card:hover{transform:translateY(-4px);box-shadow:0 10px 36px rgba(180,100,255,.22);}
.kpi-value{font-size:1.85rem;font-weight:900;background:linear-gradient(90deg,#c77dff,#ff6b9d);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.kpi-label{font-size:.70rem;color:rgba(255,255,255,.65) !important;text-transform:uppercase;letter-spacing:1.2px;margin-top:5px;}
.kpi-sub{font-size:.78rem;margin-top:3px;}

/* ── Section headers ── */
.sec-hdr{background:linear-gradient(90deg,rgba(140,60,255,.18),transparent);border-left:4px solid #c77dff;padding:10px 18px;border-radius:0 10px 10px 0;margin:28px 0 14px;font-size:1.05rem;font-weight:800;color:#c77dff !important;}

/* ── Info boxes ── */
.ibox{background:rgba(140,60,255,.08);border:1px solid rgba(140,60,255,.25);border-radius:12px;padding:14px 18px;margin-bottom:10px;}
.ibox.warn{background:rgba(255,80,50,.08);border-color:rgba(255,80,50,.30);}
.ibox.good{background:rgba(50,210,100,.08);border-color:rgba(50,210,100,.30);}

/* ── Divider ── */
hr{border-color:rgba(180,100,255,.18);}

/* ── Tabs ── */
[data-baseweb="tab-list"]{gap:4px;}
[data-baseweb="tab"]{background:rgba(140,60,255,.10) !important;border-radius:10px !important;color:rgba(255,255,255,.80) !important;font-weight:600 !important;}
[aria-selected="true"]{background:linear-gradient(135deg,rgba(140,60,255,.45),rgba(255,80,120,.35)) !important;color:#fff !important;}

/* ── Dataframe text ── */
[data-testid="stDataFrame"] *{color:#f0f0f0 !important;}

/* ── Scrollbars ── */
::-webkit-scrollbar{width:6px;height:6px;}
::-webkit-scrollbar-track{background:rgba(255,255,255,.03);}
::-webkit-scrollbar-thumb{background:rgba(180,100,255,.45);border-radius:3px;}
</style>
""", unsafe_allow_html=True)

# ── helpers ──
_D = dict(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
          font_color="#e8e0f0", margin=dict(l=10,r=10,t=48,b=10))
def dk(**kw):
    d = _D.copy(); d.update(kw); return d

DC = {"Chocolate":"#cd853f","Sugar":"#ff69b4","Other":"#7b68ee"}

# ── data ──
DATA = "data/nassau_candy_sales.csv"

@st.cache_data(show_spinner=False)
def load():
    if not os.path.exists(DATA):
        subprocess.run([sys.executable,"data/generate_data.py"],check=True)
    df = pd.read_csv(DATA, parse_dates=["Order Date","Ship Date"])
    df["GM"]          = (df["Gross Profit"]/df["Sales"]*100).round(2)
    df["PPU"]         = (df["Gross Profit"]/df["Units"]).round(4)
    df["PriceU"]      = (df["Sales"]/df["Units"]).round(4)
    df["CostR"]       = (df["Cost"]/df["Sales"]*100).round(2)
    df["Year"]        = df["Order Date"].dt.year
    df["Quarter"]     = df["Order Date"].dt.to_period("Q").astype(str)
    df["Month"]       = df["Order Date"].dt.to_period("M").astype(str)
    df["MonthNum"]    = df["Order Date"].dt.month
    df["DOW"]         = df["Order Date"].dt.day_name()
    df["RevCont"]     = df["Sales"]/df["Sales"].sum()*100
    df["ProfCont"]    = df["Gross Profit"]/df["Gross Profit"].sum()*100
    return df

with st.spinner("\U0001f36c Loading Nassau Candy Intelligence Platform..."):
    raw = load()


with st.sidebar:
    st.markdown("""<div style='text-align:center;padding:12px 0 4px;'>
      <span style='font-size:2.6rem;'>\U0001f36c</span>
      <div style='font-weight:900;font-size:1.1rem;background:linear-gradient(90deg,#c77dff,#ff6b9d);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;'>Nassau Candy</div>
      <div style='font-size:.70rem;color:rgba(255,255,255,.45);letter-spacing:1px;'>INTELLIGENCE PLATFORM v3.0</div>
    </div><hr style='border-color:rgba(180,100,255,.2);margin:8px 0;'>""", unsafe_allow_html=True)

    st.markdown("#### \U0001f39b\ufe0f Global Filters")
    mn = raw["Order Date"].min().date(); mx = raw["Order Date"].max().date()
    dr = st.date_input("\U0001f4c5 Date Range", value=(mn,mx), min_value=mn, max_value=mx)
    sdiv  = st.multiselect("\U0001f3ed Division",         sorted(raw["Division"].unique()),         default=sorted(raw["Division"].unique()))
    sreg  = st.multiselect("\U0001f5fa\ufe0f Region",    sorted(raw["Region"].unique()),           default=sorted(raw["Region"].unique()))
    sship = st.multiselect("\U0001f69a Ship Mode",        sorted(raw["Ship Mode"].unique()),        default=sorted(raw["Ship Mode"].unique()))
    sseg  = st.multiselect("\U0001f464 Segment",          sorted(raw["Customer Segment"].unique()), default=sorted(raw["Customer Segment"].unique()))
    mt    = st.slider("\u26a0\ufe0f Margin Risk Threshold (%)", 0, 60, 30)
    ps    = st.text_input("\U0001f50d Product Search", placeholder="e.g. Wonka Bar")
    st.markdown("---")
    st.markdown("<div style='font-size:.65rem;color:rgba(255,255,255,.3);'>Nassau Candy Intelligence v3.0<br>© 2025</div>", unsafe_allow_html=True)

df = raw.copy()
if len(dr)==2:
    df = df[(df["Order Date"].dt.date>=dr[0])&(df["Order Date"].dt.date<=dr[1])]
if sdiv:  df = df[df["Division"].isin(sdiv)]
if sreg:  df = df[df["Region"].isin(sreg)]
if sship: df = df[df["Ship Mode"].isin(sship)]
if sseg:  df = df[df["Customer Segment"].isin(sseg)]
if ps:    df = df[df["Product Name"].str.contains(ps,case=False,na=False)]


st.markdown("""<div style='background:linear-gradient(135deg,rgba(140,60,255,.15),rgba(255,80,120,.12),rgba(0,180,255,.08));
  border:1px solid rgba(180,100,255,.35);border-radius:22px;padding:28px 32px;margin-bottom:20px;
  display:flex;align-items:center;gap:20px;'>
  <span style='font-size:3.4rem;filter:drop-shadow(0 0 18px #c77dff);'>\U0001f36c</span>
  <div>
    <h1 style='margin:0;font-size:1.9rem;font-weight:900;
      background:linear-gradient(90deg,#c77dff,#ff6b9d,#00d4ff);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;'>
      Nassau Candy Distributor</h1>
    <p style='margin:4px 0 0;color:rgba(255,255,255,.55);font-size:.9rem;'>
      Product Line Profitability &amp; Margin Performance Intelligence Platform &nbsp;\u00b7&nbsp;
      <span style='color:#c77dff;'>8,000 orders</span> &nbsp;\u00b7&nbsp;
      <span style='color:#ff6b9d;'>15 products</span> &nbsp;\u00b7&nbsp;
      <span style='color:#00d4ff;'>5 factories</span> &nbsp;\u00b7&nbsp;
      <span style='color:#7fff7f;'>4 regions</span></p>
  </div></div>""", unsafe_allow_html=True)

tr   = df["Sales"].sum()
tp   = df["Gross Profit"].sum()
tc   = df["Cost"].sum()
am   = df["GM"].mean()
tu   = df["Units"].sum()
no   = df["Order ID"].nunique()
nc   = df["Customer ID"].nunique()
np_  = df["Product Name"].nunique()
ar   = df[df["GM"]<mt]["Product Name"].nunique()
yrs  = sorted(df["Year"].unique())
if len(yrs)>=2:
    ly,py = df[df["Year"]==yrs[-1]]["Sales"].sum(), df[df["Year"]==yrs[-2]]["Sales"].sum()
    yoy = (ly-py)/py*100 if py else 0
    _arrow = "\u2191" if yoy>=0 else "\u2193"
    yoys = f"{_arrow} {abs(yoy):.1f}% YoY"
    yoyc = "#7fff7f" if yoy>=0 else "#ff6b6b"
else:
    yoys,yoyc = "\u2014","#888"

cols8 = st.columns(8)
kdata = [
    ("\U0001f4b0",f"${tr/1e6:.2f}M","Total Revenue",yoys,yoyc),
    ("\U0001f4c8",f"${tp/1e6:.2f}M","Gross Profit",f"{tp/tr*100:.1f}% of rev","#c77dff"),
    ("\U0001f4b8",f"${tc/1e6:.2f}M","Total Cost",  f"{tc/tr*100:.1f}% of rev","#ff6b9d"),
    ("\U0001f4ca",f"{am:.1f}%",     "Avg Margin",  "portfolio avg","#00d4ff"),
    ("\U0001f4e6",f"{tu/1e3:.1f}k", "Units Sold",  "all products","#c77dff"),
    ("\U0001f6d2",f"{no:,}",        "Orders",      f"{nc} customers","#ff6b9d"),
    ("\U0001f6cd\ufe0f",f"{np_}",  "Active SKUs", "in portfolio","#00d4ff"),
    ("\u26a0\ufe0f",f"{ar}",       "At-Risk SKUs",f"below {mt}%","#ff6b6b"),
]
for col,(icon,val,lbl,sub,sc) in zip(cols8,kdata):
    col.markdown(f"""<div class='kpi-card'>
      <div style='font-size:1.3rem;margin-bottom:3px;'>{icon}</div>
      <div class='kpi-value'>{val}</div>
      <div class='kpi-label'>{lbl}</div>
      <div class='kpi-sub' style='color:{sc};'>{sub}</div>
    </div>""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)


t1,t2,t3,t4,t5,t6,t7 = st.tabs([
    "\U0001f4e6 Product Profitability",
    "\U0001f3ed Division Deep-Dive",
    "\U0001f52c Cost & Margin Diagnostics",
    "\U0001f4d0 Profit Concentration",
    "\U0001f4c5 Trend Analysis",
    "\U0001f5fa\ufe0f Geographic Intelligence",
    "\U0001f916 SKU Scoring Engine",
])


# ════ TAB 1 — PRODUCT PROFITABILITY ════
with t1:
    prod = (df.groupby(["Product Name","Division","Factory"])
              .agg(Sales=("Sales","sum"),GP=("Gross Profit","sum"),
                   Cost=("Cost","sum"),Units=("Units","sum"),Orders=("Order ID","nunique"))
              .reset_index())
    prod["Margin"]    = (prod["GP"]/prod["Sales"]*100).round(2)
    prod["PPU"]       = (prod["GP"]/prod["Units"]).round(3)
    prod["RevSh"]     = (prod["Sales"]/prod["Sales"].sum()*100).round(2)
    prod["ProfSh"]    = (prod["GP"]/prod["GP"].sum()*100).round(2)
    prod["CostR"]     = (prod["Cost"]/prod["Sales"]*100).round(2)
    prod["Risk"]      = prod["Margin"].apply(lambda x: "\U0001f7e2 Healthy" if x>=mt+10 else ("\U0001f7e1 Watch" if x>=mt else "\U0001f534 At Risk"))

    st.markdown("<div class='sec-hdr'>\U0001f3c6 Product Profitability Leaderboard</div>", unsafe_allow_html=True)
    sc_ = st.selectbox("Sort by",["GP","Margin","Sales","PPU","RevSh"],key="ps")
    ps_ = prod.sort_values(sc_,ascending=False)

    c1,c2 = st.columns([3,2])
    with c1:
        f = px.bar(ps_,x="GP",y="Product Name",orientation="h",
                   color="Margin",color_continuous_scale="RdYlGn",
                   text=ps_["Margin"].map("{:.1f}%".format),
                   hover_data=["Division","Factory","PPU","RevSh"],
                   title="Gross Profit by Product (colour = margin %)")
        f.update_traces(textposition="outside")
        f.update_layout(**dk(height=500,yaxis_categoryorder="total ascending",
                              coloraxis_colorbar=dict(title="Margin %",tickfont_color="#e8e0f0")))
        st.plotly_chart(f,use_container_width=True)
    with c2:
        f2 = px.scatter(prod,x="Sales",y="Margin",size="GP",color="Division",
                        hover_name="Product Name",hover_data=["Factory","PPU","CostR"],
                        color_discrete_map=DC,title="Revenue vs Margin (size = gross profit)")
        f2.add_hline(y=mt,line_dash="dash",line_color="#ff6b9d",
                     annotation_text=f"Risk {mt}%",annotation_font_color="#ff6b9d")
        f2.update_layout(**dk(height=500))
        st.plotly_chart(f2,use_container_width=True)

    st.markdown("<div class='sec-hdr'>\U0001f30a Revenue / Cost / Profit Grouped Bar — Top 10</div>", unsafe_allow_html=True)
    t10 = ps_.head(10)
    fg = go.Figure()
    for lbl,col_,clr in [("Revenue","Sales","#c77dff"),("Cost","Cost","#ff6b9d"),("Gross Profit","GP","#7fff7f")]:
        fg.add_trace(go.Bar(name=lbl,x=t10["Product Name"],y=t10[col_],marker_color=clr,
                            text=t10[col_].map(lambda v:f"${v/1e3:.0f}k"),textposition="outside"))
    fg.update_layout(**dk(barmode="group",height=420,xaxis_tickangle=-30,title="Revenue vs Cost vs Profit — Top 10 Products"))
    st.plotly_chart(fg,use_container_width=True)

    st.markdown("<div class='sec-hdr'>\u2600\ufe0f Sunburst & Treemap</div>", unsafe_allow_html=True)
    s1,s2 = st.columns(2)
    with s1:
        fsun = px.sunburst(prod,path=["Division","Product Name"],values="GP",
                           color="Margin",color_continuous_scale="RdYlGn",
                           title="Gross Profit Sunburst — Division \u2192 Product")
        fsun.update_layout(**dk(height=480))
        st.plotly_chart(fsun,use_container_width=True)
    with s2:
        ftree = px.treemap(prod,path=["Division","Factory","Product Name"],values="GP",
                           color="Margin",color_continuous_scale="RdYlGn",
                           title="Treemap — Division \u2192 Factory \u2192 Product")
        ftree.update_layout(**dk(height=480))
        st.plotly_chart(ftree,use_container_width=True)

    st.markdown("<div class='sec-hdr'>\U0001f367 Profit Share Donut</div>", unsafe_allow_html=True)
    fpie = px.pie(prod,values="GP",names="Product Name",hole=0.45,
                  color_discrete_sequence=px.colors.qualitative.Vivid,
                  title="Gross Profit Share by Product")
    fpie.update_layout(**dk(height=440))
    st.plotly_chart(fpie,use_container_width=True)

    st.markdown("<div class='sec-hdr'>\U0001f4cb Full Product Table</div>", unsafe_allow_html=True)
    disp = ps_[["Product Name","Division","Factory","Sales","GP","Margin","PPU","RevSh","ProfSh","CostR","Risk"]].copy()
    disp.columns=["Product","Division","Factory","Revenue","Gross Profit","Margin %","Profit/Unit","Rev Share %","Profit Share %","Cost Ratio %","Risk"]
    st.dataframe(disp.style
        .format({"Revenue":"${:,.0f}","Gross Profit":"${:,.0f}","Margin %":"{:.1f}%",
                 "Profit/Unit":"${:.3f}","Rev Share %":"{:.2f}%","Profit Share %":"{:.2f}%","Cost Ratio %":"{:.1f}%"})
        .background_gradient(subset=["Margin %"],cmap="RdYlGn"),
        height=400,use_container_width=True)


# ════ TAB 2 — DIVISION DEEP-DIVE ════
with t2:
    da = (df.groupby("Division")
            .agg(Revenue=("Sales","sum"),GP=("Gross Profit","sum"),Cost=("Cost","sum"),
                 Units=("Units","sum"),Orders=("Order ID","nunique"),Products=("Product Name","nunique"))
            .reset_index())
    da["Margin"]  = (da["GP"]/da["Revenue"]*100).round(2)
    da["RevSh"]   = (da["Revenue"]/da["Revenue"].sum()*100).round(2)
    da["PPU"]     = (da["GP"]/da["Units"]).round(3)
    da["ProfEff"] = (da["GP"]/da["Cost"]).round(3)

    st.markdown("<div class='sec-hdr'>\U0001f3c6 Division Snapshot</div>", unsafe_allow_html=True)
    dc_ = st.columns(len(da))
    cls = ["#c77dff","#ff6b9d","#00d4ff"]
    for i,(col,(_,row)) in enumerate(zip(dc_,da.iterrows())):
        c=cls[i%len(cls)]
        col.markdown(f"""<div class='kpi-card' style='border-color:{c}44;'>
          <div style='font-size:1.4rem;'>{"\U0001f36b" if row.Division=="Chocolate" else ("\U0001f36c" if row.Division=="Sugar" else "\u2728")}</div>
          <div class='kpi-value' style='background:linear-gradient(90deg,{c},{c}88);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;'>{row.Division}</div>
          <div class='kpi-label'>Margin: {row.Margin:.1f}%</div>
          <div class='kpi-sub'>Rev ${row.Revenue/1e6:.2f}M &middot; GP ${row.GP/1e6:.2f}M</div>
          <div class='kpi-sub'>{row.Orders:,} orders &middot; {row.Products} SKUs</div>
        </div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    d1,d2 = st.columns(2)
    with d1:
        fg2 = go.Figure()
        for lbl,k,clr in [("Revenue","Revenue","#c77dff"),("Gross Profit","GP","#7fff7f"),("Cost","Cost","#ff6b9d")]:
            fg2.add_trace(go.Bar(name=lbl,x=da["Division"],y=da[k],marker_color=clr,
                                 text=da[k].map(lambda v:f"${v/1e3:.0f}k"),textposition="outside"))
        fg2.update_layout(**dk(barmode="group",height=400,title="Revenue vs GP vs Cost by Division"))
        st.plotly_chart(fg2,use_container_width=True)
    with d2:
        feff = px.bar(da.sort_values("ProfEff",ascending=False),x="Division",y="ProfEff",
                      color="Division",color_discrete_map=DC,text="ProfEff",
                      title="Profit Efficiency (GP ÷ Cost) by Division")
        feff.update_traces(texttemplate="%{text:.3f}x",textposition="outside")
        feff.update_layout(**dk(height=400,showlegend=False))
        st.plotly_chart(feff,use_container_width=True)

    st.markdown("<div class='sec-hdr'>\U0001f3bb Margin Distribution Violin</div>", unsafe_allow_html=True)
    fvio = px.violin(df,x="Division",y="GM",color="Division",box=True,points="outliers",
                     color_discrete_map=DC,title="Gross Margin % Distribution by Division")
    fvio.add_hline(y=mt,line_dash="dash",line_color="#ff6b9d",
                   annotation_text=f"Risk {mt}%",annotation_font_color="#ff6b9d")
    fvio.update_layout(**dk(height=420))
    st.plotly_chart(fvio,use_container_width=True)

    st.markdown("<div class='sec-hdr'>\U0001f578\ufe0f Division Scorecard Radar</div>", unsafe_allow_html=True)
    rm = ["Margin","RevSh","PPU","ProfEff"]
    dn = da.copy()
    for m in rm:
        rng=dn[m].max()-dn[m].min()
        dn[m]=(dn[m]-dn[m].min())/(rng if rng else 1)*100
    frad = go.Figure()
    rc2=["#c77dff","#ff6b9d","#00d4ff"]
    for idx,row in dn.iterrows():
        v=[row[m] for m in rm]+[row[rm[0]]]
        frad.add_trace(go.Scatterpolar(r=v,theta=rm+[rm[0]],fill="toself",
                                        name=row["Division"],line_color=rc2[idx%3]))
    frad.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0,100],tickfont_color="#888")),
                        title="Normalised Division Scorecard Radar",**dk(height=440))
    st.plotly_chart(frad,use_container_width=True)

    st.markdown("<div class='sec-hdr'>\U0001f3ed Factory Gross Profit (Stacked)</div>", unsafe_allow_html=True)
    fa2 = (df.groupby(["Factory","Division"]).agg(Revenue=("Sales","sum"),GP=("Gross Profit","sum")).reset_index())
    fa2["Margin"]=(fa2["GP"]/fa2["Revenue"]*100).round(2)
    ffact = px.bar(fa2,x="Factory",y="GP",color="Division",barmode="stack",
                   color_discrete_map=DC,text="Margin",title="GP by Factory stacked by Division")
    ffact.update_traces(texttemplate="%{text:.1f}%",textposition="inside")
    ffact.update_layout(**dk(height=400))
    st.plotly_chart(ffact,use_container_width=True)

    st.markdown("<div class='sec-hdr'>\U0001f321\ufe0f Division \u00d7 Region Margin Heatmap</div>", unsafe_allow_html=True)
    dreg=(df.groupby(["Division","Region"]).agg(GP=("Gross Profit","sum"),Sales=("Sales","sum")).reset_index())
    dreg["Margin"]=(dreg["GP"]/dreg["Sales"]*100).round(2)
    piv=dreg.pivot(index="Division",columns="Region",values="Margin")
    fhm=px.imshow(piv,color_continuous_scale="RdYlGn",text_auto=".1f",aspect="auto",
                   title="Gross Margin % — Division x Region Heatmap")
    fhm.update_layout(**dk(height=320))
    st.plotly_chart(fhm,use_container_width=True)


# ════ TAB 3 — COST & MARGIN DIAGNOSTICS ════
with t3:
    pd_ = (df.groupby(["Product Name","Division","Factory"])
             .agg(Sales=("Sales","sum"),GP=("Gross Profit","sum"),
                  Cost=("Cost","sum"),Units=("Units","sum"))
             .reset_index())
    pd_["Margin"]=(pd_["GP"]/pd_["Sales"]*100).round(2)
    pd_["PPU"]   =(pd_["GP"]/pd_["Units"]).round(3)
    pd_["CostR"] =(pd_["Cost"]/pd_["Sales"]*100).round(2)

    st.markdown("<div class='sec-hdr'>\U0001f52c Cost vs Sales Scatter (OLS trendline)</div>", unsafe_allow_html=True)
    fcs=px.scatter(pd_,x="Cost",y="Sales",size="Units",color="Margin",
                   color_continuous_scale="RdYlGn",hover_name="Product Name",
                   hover_data=["Division","Factory","PPU"],
                   title="Cost vs Sales — size=volume, colour=margin %")
    # manual linear trendline (no statsmodels dependency)
    _m,_b = np.polyfit(pd_["Cost"],pd_["Sales"],1)
    _x = np.linspace(pd_["Cost"].min(),pd_["Cost"].max(),100)
    fcs.add_trace(go.Scatter(x=_x,y=_m*_x+_b,mode="lines",name="Trend",
                              line=dict(color="#ffdb58",width=2,dash="dot")))
    fcs.update_layout(**dk(height=500))
    st.plotly_chart(fcs,use_container_width=True)

    st.markdown("<div class='sec-hdr'>\U0001f4b8 Cost Ratio by Product</div>", unsafe_allow_html=True)
    fcr=px.bar(pd_.sort_values("CostR",ascending=False),x="Product Name",y="CostR",
               color="Division",color_discrete_map=DC,text="CostR",
               title="Cost Ratio % (Cost ÷ Sales) — higher = less margin")
    fcr.add_hline(y=100-mt,line_dash="dot",line_color="#ff6b9d",
                  annotation_text=f"Threshold {100-mt:.0f}%",annotation_font_color="#ff6b9d")
    fcr.update_traces(texttemplate="%{text:.1f}%",textposition="outside")
    fcr.update_layout(**dk(height=420,xaxis_tickangle=-35))
    st.plotly_chart(fcr,use_container_width=True)

    st.markdown("<div class='sec-hdr'>\u26a0\ufe0f Margin Risk Flags</div>", unsafe_allow_html=True)
    ar_=pd_[pd_["Margin"]<mt].sort_values("Margin")
    if ar_.empty:
        st.markdown("<div class='ibox good'>\u2705 <b>No products below risk threshold.</b> All margins healthy.</div>", unsafe_allow_html=True)
    else:
        rr1,rr2=st.columns([2,1])
        with rr1:
            frisk=px.bar(ar_,x="Product Name",y="Margin",color="Division",
                         color_discrete_map=DC,text="Margin",
                         title=f"At-Risk Products — Margin < {mt}%")
            frisk.add_hline(y=mt,line_dash="dot",line_color="#ff6b9d")
            frisk.update_traces(texttemplate="%{text:.1f}%",textposition="outside")
            frisk.update_layout(**dk(height=400,xaxis_tickangle=-30))
            st.plotly_chart(frisk,use_container_width=True)
        with rr2:
            st.markdown("**\U0001f534 Remediation**")
            for _,row in ar_.iterrows():
                if row.Margin<mt*0.6: act,bg="Discontinue","background:rgba(180,0,0,.3)"
                elif row.Margin<mt*0.8: act,bg="Renegotiate Cost","background:rgba(180,120,0,.3)"
                else: act,bg="Monitor","background:rgba(100,100,0,.3)"
                st.markdown(f"""<div style='{bg};border-radius:10px;padding:9px 12px;margin-bottom:7px;'>
                  <b>{row["Product Name"]}</b><br>
                  <small>Margin: <b style='color:#ff6b9d'>{row.Margin:.1f}%</b> &middot; {row.Division}<br>
                  \U0001f3ed {row.Factory}<br>
                  <span style='color:#ffdb58;'>&#9658; {act}</span></small></div>""", unsafe_allow_html=True)

    st.markdown("<div class='sec-hdr'>\U0001f4ca BCG Pricing Quadrant</div>", unsafe_allow_html=True)
    mm,ms=pd_["Margin"].median(),pd_["Sales"].median()
    def quad(r):
        if r.Sales>=ms and r.Margin>=mm: return "\u2b50 Star"
        elif r.Sales>=ms: return "\U0001f404 Cash Cow"
        elif r.Margin>=mm: return "\U0001f48e Gem"
        else: return "\U0001f415 Dog"
    pd_["Q"]=pd_.apply(quad,axis=1)
    fq=px.scatter(pd_,x="Sales",y="Margin",color="Q",size="GP",
                  hover_name="Product Name",hover_data=["Division","Factory"],
                  color_discrete_sequence=["#7fff7f","#ffdb58","#c77dff","#ff6b6b"],
                  title="BCG Pricing Quadrant — Stars, Cash Cows, Gems, Dogs")
    fq.add_vline(x=ms,line_dash="dash",line_color="rgba(255,255,255,.2)")
    fq.add_hline(y=mm,line_dash="dash",line_color="rgba(255,255,255,.2)")
    fq.update_layout(**dk(height=500))
    st.plotly_chart(fq,use_container_width=True)

    st.markdown("<div class='sec-hdr'>\U0001f4c9 Margin Distribution Histogram</div>", unsafe_allow_html=True)
    fhist=px.histogram(df,x="GM",color="Division",nbins=60,barmode="overlay",opacity=.7,
                       color_discrete_map=DC,title="Order-Level Gross Margin Distribution by Division")
    fhist.add_vline(x=mt,line_dash="dot",line_color="#ff6b9d",
                    annotation_text=f"Risk {mt}%",annotation_font_color="#ff6b9d")
    fhist.update_layout(**dk(height=380))
    st.plotly_chart(fhist,use_container_width=True)

    st.markdown("<div class='sec-hdr'>\U0001f4e6 Margin by Ship Mode (Box)</div>", unsafe_allow_html=True)
    fbox=px.box(df,x="Ship Mode",y="GM",color="Ship Mode",notched=True,points="outliers",
                color_discrete_sequence=["#c77dff","#ff6b9d","#00d4ff","#7fff7f"],
                title="Gross Margin % Distribution by Shipping Mode")
    fbox.add_hline(y=mt,line_dash="dash",line_color="#ff6b9d")
    fbox.update_layout(**dk(height=400,showlegend=False))
    st.plotly_chart(fbox,use_container_width=True)


# ════ TAB 4 — PROFIT CONCENTRATION ════
with t4:
    pp=(df.groupby(["Product Name","Division"]).agg(GP=("Gross Profit","sum"),Sales=("Sales","sum")).reset_index())
    pp=pp.sort_values("GP",ascending=False).reset_index(drop=True)
    pp["CumProfit"]=pp["GP"].cumsum()/pp["GP"].sum()*100
    pp["CumRev"]   =pp["Sales"].cumsum()/pp["Sales"].sum()*100
    pp["Rank"]=range(1,len(pp)+1)
    pp["CumPct"]=pp["Rank"]/len(pp)*100

    st.markdown("<div class='sec-hdr'>\U0001f4d0 Profit Pareto Chart</div>", unsafe_allow_html=True)
    fpar=make_subplots(specs=[[{"secondary_y":True}]])
    fpar.add_trace(go.Bar(x=pp["Product Name"],y=pp["GP"],name="Gross Profit",marker_color="#c77dff"),secondary_y=False)
    fpar.add_trace(go.Scatter(x=pp["Product Name"],y=pp["CumProfit"],name="Cumulative %",
                               line=dict(color="#ff6b9d",width=3)),secondary_y=True)
    fpar.add_hline(y=80,secondary_y=True,line_dash="dash",line_color="rgba(255,255,255,.4)",annotation_text="80% line")
    fpar.update_yaxes(title_text="Gross Profit ($)",secondary_y=False,tickfont_color="#e8e0f0")
    fpar.update_yaxes(title_text="Cumulative %",secondary_y=True,tickfont_color="#e8e0f0")
    fpar.update_layout(title="Profit Pareto Chart",**dk(height=440))
    st.plotly_chart(fpar,use_container_width=True)

    p80=pp[pp["CumProfit"]<=80]; r80=pp[pp["CumRev"]<=80]
    pc1,pc2,pc3=st.columns(3)
    for col,val,lbl in [(pc1,len(p80),"Products \u2192 80% of Profit"),
                         (pc2,len(r80),"Products \u2192 80% of Revenue"),
                         (pc3,len(pp)-len(p80),"Low-Contribution SKUs")]:
        col.markdown(f"""<div class='kpi-card'>
          <div class='kpi-value'>{val}</div><div class='kpi-label'>{lbl}</div>
        </div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<div class='sec-hdr'>\U0001f333 Revenue Pareto</div>", unsafe_allow_html=True)
    frpar=make_subplots(specs=[[{"secondary_y":True}]])
    pp2=pp.sort_values("Sales",ascending=False).reset_index(drop=True)
    pp2["CumRev2"]=pp2["Sales"].cumsum()/pp2["Sales"].sum()*100
    frpar.add_trace(go.Bar(x=pp2["Product Name"],y=pp2["Sales"],name="Revenue",marker_color="#00d4ff"),secondary_y=False)
    frpar.add_trace(go.Scatter(x=pp2["Product Name"],y=pp2["CumRev2"],name="Cumulative %",
                                line=dict(color="#7fff7f",width=3)),secondary_y=True)
    frpar.add_hline(y=80,secondary_y=True,line_dash="dash",line_color="rgba(255,255,255,.4)")
    frpar.update_layout(title="Revenue Pareto Chart",**dk(height=400))
    st.plotly_chart(frpar,use_container_width=True)

    st.markdown("<div class='sec-hdr'>\U0001f5fa\ufe0f Regional Profit Treemap</div>", unsafe_allow_html=True)
    rr=(df.groupby(["Region","State/Province"])
          .agg(Revenue=("Sales","sum"),Profit=("Gross Profit","sum"),Units=("Units","sum"))
          .reset_index())
    rr["Margin"]=(rr["Profit"]/rr["Revenue"]*100).round(2)
    frtm=px.treemap(rr,path=["Region","State/Province"],values="Profit",color="Margin",
                    color_continuous_scale="RdYlGn",hover_data=["Revenue","Units"],
                    title="Profit Contribution by Region & State")
    frtm.update_layout(**dk(height=500))
    st.plotly_chart(frtm,use_container_width=True)

    st.markdown("<div class='sec-hdr'>\U0001f321\ufe0f Region \u00d7 Division Revenue Heatmap</div>", unsafe_allow_html=True)
    rdh=(df.groupby(["Region","Division"]).agg(Revenue=("Sales","sum")).reset_index())
    rdpiv=rdh.pivot(index="Region",columns="Division",values="Revenue")
    frdh=px.imshow(rdpiv,color_continuous_scale="Purples",text_auto=",.0f",aspect="auto",
                   title="Revenue Heatmap — Region x Division")
    frdh.update_layout(**dk(height=340))
    st.plotly_chart(frdh,use_container_width=True)

    tp_prod=pp.iloc[0]["Product Name"]
    tp_sh=pp.iloc[0]["GP"]/pp["GP"].sum()*100
    fg_g=go.Figure(go.Indicator(
        mode="gauge+number+delta",value=tp_sh,
        title={"text":f"Top Product Profit Dependency<br><sup>{tp_prod}</sup>","font":{"color":"#e8e0f0","size":13}},
        delta={"reference":15,"decreasing":{"color":"#7fff7f"},"increasing":{"color":"#ff6b6b"}},
        gauge={"axis":{"range":[0,50],"tickcolor":"#e8e0f0"},
               "bar":{"color":"#c77dff"},
               "bgcolor":"rgba(0,0,0,0)",
               "steps":[{"range":[0,15],"color":"rgba(50,200,100,.2)"},
                         {"range":[15,30],"color":"rgba(240,190,10,.2)"},
                         {"range":[30,50],"color":"rgba(230,70,60,.2)"}],
               "threshold":{"line":{"color":"#ff6b9d","width":4},"thickness":.75,"value":30}},
        number={"suffix":"%","font":{"color":"#c77dff","size":32}}))
    fg_g.update_layout(**dk(height=360,title="Top SKU Profit Dependency Gauge"))
    st.plotly_chart(fg_g,use_container_width=True)


# ════ TAB 5 — TREND ANALYSIS ════
with t5:
    tr_=(df.groupby(["Month","Division"])
           .agg(Revenue=("Sales","sum"),GP=("Gross Profit","sum"))
           .reset_index().sort_values("Month"))
    tr_["Margin"]=(tr_["GP"]/tr_["Revenue"]*100).round(2)

    st.markdown("<div class='sec-hdr'>\U0001f4c8 Monthly Revenue Trend by Division</div>", unsafe_allow_html=True)
    fl=px.line(tr_,x="Month",y="Revenue",color="Division",markers=True,
               color_discrete_map=DC,title="Monthly Revenue Trend by Division")
    fl.update_layout(**dk(height=400,xaxis_tickangle=-45))
    st.plotly_chart(fl,use_container_width=True)

    st.markdown("<div class='sec-hdr'>\U0001f4b0 Monthly Gross Profit Trend by Division</div>", unsafe_allow_html=True)
    fl2=px.area(tr_,x="Month",y="GP",color="Division",
                color_discrete_map=DC,title="Monthly Gross Profit Area Chart by Division")
    fl2.update_layout(**dk(height=400,xaxis_tickangle=-45))
    st.plotly_chart(fl2,use_container_width=True)

    st.markdown("<div class='sec-hdr'>\U0001f4c9 Margin Volatility Band</div>", unsafe_allow_html=True)
    mv=(df.groupby("Month").apply(lambda g: pd.Series({
            "AvgM":g["GM"].mean(),"StdM":g["GM"].std()})).reset_index().sort_values("Month"))
    fv=go.Figure([
        go.Scatter(x=mv["Month"],y=mv["AvgM"]+mv["StdM"],fill=None,mode="lines",
                   line_color="rgba(199,125,255,0)",showlegend=False),
        go.Scatter(x=mv["Month"],y=mv["AvgM"]-mv["StdM"],fill="tonexty",mode="lines",
                   line_color="rgba(199,125,255,0)",fillcolor="rgba(199,125,255,.15)",showlegend=False),
        go.Scatter(x=mv["Month"],y=mv["AvgM"],mode="lines+markers",name="Avg Margin",
                   line=dict(color="#c77dff",width=2.5)),
    ])
    fv.add_hline(y=mt,line_dash="dot",line_color="#ff6b9d",annotation_text=f"Risk {mt}%",annotation_font_color="#ff6b9d")
    fv.update_layout(title="Gross Margin Volatility Band (±1σ)",**dk(height=400,xaxis_tickangle=-45))
    st.plotly_chart(fv,use_container_width=True)

    st.markdown("<div class='sec-hdr'>\U0001f321\ufe0f YoY Revenue Heatmap</div>", unsafe_allow_html=True)
    mh=(df.groupby(["Year","MonthNum"]).agg(Revenue=("Sales","sum")).reset_index())
    hp=mh.pivot(index="Year",columns="MonthNum",values="Revenue")
    mn_=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    hp.columns=[mn_[c-1] for c in hp.columns]
    fhp=px.imshow(hp,color_continuous_scale="YlOrRd",text_auto=",.0f",aspect="auto",
                  title="Monthly Revenue Heatmap by Year (YoY)")
    fhp.update_layout(**dk(height=320))
    st.plotly_chart(fhp,use_container_width=True)

    st.markdown("<div class='sec-hdr'>\U0001f4ca Quarterly Revenue vs GP (Grouped)</div>", unsafe_allow_html=True)
    qd=(df.groupby("Quarter").agg(Revenue=("Sales","sum"),GP=("Gross Profit","sum")).reset_index().sort_values("Quarter"))
    fq2=go.Figure()
    fq2.add_trace(go.Bar(name="Revenue",x=qd["Quarter"],y=qd["Revenue"],marker_color="#c77dff",text=qd["Revenue"].map(lambda v:f"${v/1e3:.0f}k"),textposition="outside"))
    fq2.add_trace(go.Bar(name="Gross Profit",x=qd["Quarter"],y=qd["GP"],marker_color="#7fff7f",text=qd["GP"].map(lambda v:f"${v/1e3:.0f}k"),textposition="outside"))
    fq2.update_layout(**dk(barmode="group",height=400,xaxis_tickangle=-45,title="Quarterly Revenue vs Gross Profit"))
    st.plotly_chart(fq2,use_container_width=True)

    st.markdown("<div class='sec-hdr'>\U0001f69a Profitability by Ship Mode</div>", unsafe_allow_html=True)
    sm=(df.groupby("Ship Mode").agg(Revenue=("Sales","sum"),GP=("Gross Profit","sum"),Orders=("Order ID","nunique")).reset_index())
    sm["Margin"]=(sm["GP"]/sm["Revenue"]*100).round(2)
    fs=px.bar(sm,x="Ship Mode",y=["Revenue","GP"],barmode="group",text_auto=True,
              color_discrete_map={"Revenue":"#c77dff","GP":"#7fff7f"},
              title="Revenue vs Gross Profit by Shipping Mode")
    fs.update_layout(**dk(height=380))
    st.plotly_chart(fs,use_container_width=True)

    st.markdown("<div class='sec-hdr'>\U0001f4c5 Day-of-Week Order Volume & Revenue</div>", unsafe_allow_html=True)
    dow_order=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    dw=(df.groupby("DOW").agg(Orders=("Order ID","nunique"),Revenue=("Sales","sum")).reset_index())
    dw["DOW"]=pd.Categorical(dw["DOW"],categories=dow_order,ordered=True)
    dw=dw.sort_values("DOW")
    fdow=make_subplots(specs=[[{"secondary_y":True}]])
    fdow.add_trace(go.Bar(x=dw["DOW"],y=dw["Orders"],name="Orders",marker_color="#c77dff"),secondary_y=False)
    fdow.add_trace(go.Scatter(x=dw["DOW"],y=dw["Revenue"],name="Revenue",line=dict(color="#ff6b9d",width=2.5),mode="lines+markers"),secondary_y=True)
    fdow.update_layout(title="Orders & Revenue by Day of Week",**dk(height=380))
    st.plotly_chart(fdow,use_container_width=True)


# ════ TAB 6 — GEOGRAPHIC INTELLIGENCE ════
with t6:
    st.markdown("<div class='sec-hdr'>\U0001f5fa\ufe0f Customer City Revenue Map</div>", unsafe_allow_html=True)
    cg=(df.groupby(["City","State/Province","Customer Lat","Customer Lon"])
          .agg(Revenue=("Sales","sum"),GP=("Gross Profit","sum"),Orders=("Order ID","nunique"))
          .reset_index())
    cg["Margin"]=(cg["GP"]/cg["Revenue"]*100).round(2)
    fm=px.scatter_geo(cg,lat="Customer Lat",lon="Customer Lon",size="Revenue",
                      color="Margin",color_continuous_scale="RdYlGn",
                      hover_name="City",hover_data={"State/Province":True,"Revenue":":$,.0f","GP":":$,.0f","Orders":True,"Margin":":.1f%"},
                      scope="usa",title="Customer Revenue & Margin by City",size_max=45)
    fm.update_layout(**dk(height=520,geo=dict(bgcolor="rgba(0,0,0,0)",
        lakecolor="rgba(0,50,100,.3)",landcolor="rgba(20,20,40,1)",
        showlakes=True,showland=True,coastlinecolor="rgba(255,255,255,.15)",
        countrycolor="rgba(255,255,255,.15)",subunitcolor="rgba(255,255,255,.1)")))
    st.plotly_chart(fm,use_container_width=True)

    st.markdown("<div class='sec-hdr'>\U0001f3ed Factory Locations (Gross Profit Bubble)</div>", unsafe_allow_html=True)
    fg_=(df.groupby(["Factory","Factory Lat","Factory Lon"])
           .agg(GP=("Gross Profit","sum"),Revenue=("Sales","sum"),Units=("Units","sum"))
           .reset_index())
    fg_["Margin"]=(fg_["GP"]/fg_["Revenue"]*100).round(2)
    ff=px.scatter_geo(fg_,lat="Factory Lat",lon="Factory Lon",size="GP",
                      color="Margin",color_continuous_scale="RdYlGn",
                      hover_name="Factory",hover_data={"Revenue":":$,.0f","GP":":$,.0f","Margin":":.1f%"},
                      scope="usa",title="Factory Locations — Bubble size = Gross Profit",size_max=55)
    ff.update_layout(**dk(height=480,geo=dict(bgcolor="rgba(0,0,0,0)",
        lakecolor="rgba(0,50,100,.3)",landcolor="rgba(20,20,40,1)",
        showlakes=True,showland=True,coastlinecolor="rgba(255,255,255,.15)",
        countrycolor="rgba(255,255,255,.15)",subunitcolor="rgba(255,255,255,.1)")))
    st.plotly_chart(ff,use_container_width=True)

    st.markdown("<div class='sec-hdr'>\U0001f4ca Region Performance Comparison</div>", unsafe_allow_html=True)
    rp=(df.groupby("Region").agg(Revenue=("Sales","sum"),GP=("Gross Profit","sum"),
                                   Units=("Units","sum"),Orders=("Order ID","nunique")).reset_index())
    rp["Margin"]=(rp["GP"]/rp["Revenue"]*100).round(2)
    r1c,r2c=st.columns(2)
    with r1c:
        frp=px.bar(rp.sort_values("Revenue",ascending=False),x="Region",y=["Revenue","GP"],
                   barmode="group",color_discrete_map={"Revenue":"#c77dff","GP":"#7fff7f"},
                   title="Revenue vs GP by Region")
        frp.update_layout(**dk(height=380))
        st.plotly_chart(frp,use_container_width=True)
    with r2c:
        frp2=px.pie(rp,values="GP",names="Region",hole=.42,
                    color_discrete_sequence=["#c77dff","#ff6b9d","#00d4ff","#7fff7f"],
                    title="Profit Share by Region")
        frp2.update_layout(**dk(height=380))
        st.plotly_chart(frp2,use_container_width=True)

    st.markdown("<div class='sec-hdr'>\U0001f321\ufe0f Region \u00d7 Product Margin Heatmap</div>", unsafe_allow_html=True)
    rpm=(df.groupby(["Region","Product Name"]).agg(GP=("Gross Profit","sum"),Sales=("Sales","sum")).reset_index())
    rpm["Margin"]=(rpm["GP"]/rpm["Sales"]*100).round(2)
    rpiv=rpm.pivot(index="Region",columns="Product Name",values="Margin")
    frh=px.imshow(rpiv,color_continuous_scale="RdYlGn",text_auto=".1f",aspect="auto",
                  title="Gross Margin % — Region x Product Heatmap")
    frh.update_layout(**dk(height=380))
    st.plotly_chart(frh,use_container_width=True)

    st.markdown("<div class='sec-hdr'>\U0001f464 Revenue by Customer Segment & Region</div>", unsafe_allow_html=True)
    sg=(df.groupby(["Customer Segment","Region"]).agg(Revenue=("Sales","sum"),GP=("Gross Profit","sum")).reset_index())
    sg["Margin"]=(sg["GP"]/sg["Revenue"]*100).round(2)
    fsg=px.bar(sg,x="Region",y="Revenue",color="Customer Segment",barmode="group",
               color_discrete_sequence=["#c77dff","#ff6b9d","#00d4ff"],
               title="Revenue by Customer Segment & Region")
    fsg.update_layout(**dk(height=380))
    st.plotly_chart(fsg,use_container_width=True)


# ════ TAB 7 — SKU SCORING ENGINE ════
with t7:
    st.markdown("<div class='sec-hdr'>\U0001f916 Composite SKU Health Score</div>", unsafe_allow_html=True)
    st.markdown("""<div class='ibox'>
      <b>Scoring Methodology:</b> Each SKU is scored 0-100 on four dimensions —
      <span style='color:#c77dff;'>Margin Quality</span>,
      <span style='color:#ff6b9d;'>Revenue Scale</span>,
      <span style='color:#00d4ff;'>Profit Efficiency (GP/Cost)</span>, and
      <span style='color:#7fff7f;'>Volume Consistency</span>.
      Scores are normalised min-max across the portfolio. Final score is a weighted composite.
    </div>""", unsafe_allow_html=True)

    sku=(df.groupby(["Product Name","Division","Factory"])
           .agg(Sales=("Sales","sum"),GP=("Gross Profit","sum"),
                Cost=("Cost","sum"),Units=("Units","sum"),Orders=("Order ID","nunique"))
           .reset_index())
    sku["Margin"]   =(sku["GP"]/sku["Sales"]*100).round(2)
    sku["PPU"]      =(sku["GP"]/sku["Units"]).round(3)
    sku["ProfEff"]  =(sku["GP"]/sku["Cost"]).round(3)
    sku["AvgOrdSz"] =(sku["Sales"]/sku["Orders"]).round(2)

    def norm(s):
        mn,mx=s.min(),s.max()
        return (s-mn)/(mx-mn)*100 if mx!=mn else pd.Series([50]*len(s),index=s.index)

    w1=st.slider("Weight: Margin Quality",0,100,35,key="w1")
    w2=st.slider("Weight: Revenue Scale", 0,100,25,key="w2")
    w3=st.slider("Weight: Profit Efficiency",0,100,25,key="w3")
    w4=st.slider("Weight: Volume",0,100,15,key="w4")
    total_w=w1+w2+w3+w4
    if total_w==0: total_w=1

    sku["S_Margin"] =norm(sku["Margin"])
    sku["S_Rev"]    =norm(sku["Sales"])
    sku["S_Eff"]    =norm(sku["ProfEff"])
    sku["S_Vol"]    =norm(sku["Units"])
    sku["Score"]    =((sku["S_Margin"]*w1+sku["S_Rev"]*w2+sku["S_Eff"]*w3+sku["S_Vol"]*w4)/total_w).round(1)
    sku["Grade"]    =sku["Score"].apply(lambda x: "A\u2b50" if x>=80 else ("B\U0001f44d" if x>=60 else ("C\u26a0\ufe0f" if x>=40 else "D\U0001f534")))

    sku_s=sku.sort_values("Score",ascending=False)

    sc1,sc2=st.columns([2,1])
    with sc1:
        fsc=px.bar(sku_s,x="Score",y="Product Name",orientation="h",
                   color="Score",color_continuous_scale=["#ff6b6b","#ffdb58","#7fff7f"],
                   text=sku_s["Score"].map("{:.1f}".format),
                   hover_data=["Division","Factory","Margin","PPU","Grade"],
                   title="SKU Composite Health Score (0-100)")
        fsc.add_vline(x=60,line_dash="dot",line_color="#ffdb58",annotation_text="Pass 60",annotation_font_color="#ffdb58")
        fsc.add_vline(x=80,line_dash="dot",line_color="#7fff7f",annotation_text="Grade A 80",annotation_font_color="#7fff7f")
        fsc.update_traces(textposition="outside")
        fsc.update_layout(**dk(height=520,yaxis_categoryorder="total ascending",
                                coloraxis_colorbar=dict(title="Score",tickfont_color="#e8e0f0")))
        st.plotly_chart(fsc,use_container_width=True)
    with sc2:
        st.markdown("**\U0001f3c5 SKU Grade Distribution**")
        gd=sku["Grade"].value_counts().reset_index(); gd.columns=["Grade","Count"]
        fgd=px.pie(gd,values="Count",names="Grade",hole=.42,
                   color_discrete_sequence=["#7fff7f","#00d4ff","#ffdb58","#ff6b6b"],
                   title="Grade Distribution")
        fgd.update_layout(**dk(height=300))
        st.plotly_chart(fgd,use_container_width=True)

        st.markdown("**\U0001f4cb Grade Cards**")
        for _,row in sku_s.iterrows():
            gclr={"A\u2b50":"#1e7e45","B\U0001f44d":"#1a4a7a","C\u26a0\ufe0f":"#7a5c00","D\U0001f534":"#7a1515"}.get(row.Grade,"#333")
            st.markdown(f"""<div style='background:{gclr}33;border:1px solid {gclr}88;border-radius:8px;
              padding:7px 10px;margin-bottom:5px;font-size:.82rem;'>
              <b>{row["Product Name"][:28]}</b>
              <span style='float:right;font-weight:700;font-size:.9rem;'>{row.Score:.0f} {row.Grade}</span><br>
              <small style='color:rgba(255,255,255,.6);'>{row.Division} &middot; Margin {row.Margin:.1f}%</small>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div class='sec-hdr'>\U0001f4ca Sub-Score Breakdown Heatmap</div>", unsafe_allow_html=True)
    sub_cols=["S_Margin","S_Rev","S_Eff","S_Vol"]
    sub_labels=["Margin","Revenue","Efficiency","Volume"]
    sub_piv=sku_s.set_index("Product Name")[sub_cols]
    sub_piv.columns=sub_labels
    fsh=px.imshow(sub_piv,color_continuous_scale="RdYlGn",text_auto=".0f",aspect="auto",
                  title="Sub-Score Breakdown — Each Dimension 0-100")
    fsh.update_layout(**dk(height=500))
    st.plotly_chart(fsh,use_container_width=True)

    st.markdown("<div class='sec-hdr'>\U0001f4e1 Score vs Margin vs Revenue (3D View)</div>", unsafe_allow_html=True)
    f3d=px.scatter_3d(sku_s,x="Sales",y="Margin",z="Score",color="Division",
                      size="GP",hover_name="Product Name",
                      color_discrete_map=DC,title="3D: Revenue vs Margin vs SKU Score")
    f3d.update_layout(**dk(height=560))
    st.plotly_chart(f3d,use_container_width=True)

    st.markdown("<div class='sec-hdr'>\U0001f4cb Full SKU Scoring Table</div>", unsafe_allow_html=True)
    stbl=sku_s[["Product Name","Division","Factory","Score","Grade","Margin","PPU","ProfEff","Sales","GP","Units","Orders"]].copy()
    stbl.columns=["Product","Division","Factory","Score","Grade","Margin %","Profit/Unit","Profit Eff","Revenue","Gross Profit","Units","Orders"]
    st.dataframe(stbl.style
        .format({"Score":"{:.1f}","Margin %":"{:.1f}%","Profit/Unit":"${:.3f}",
                 "Profit Eff":"{:.3f}x","Revenue":"${:,.0f}","Gross Profit":"${:,.0f}"})
        .background_gradient(subset=["Score"],cmap="RdYlGn")
        .background_gradient(subset=["Margin %"],cmap="RdYlGn"),
        height=420,use_container_width=True)


st.markdown("---")
st.markdown("""<div style='text-align:center;color:rgba(255,255,255,.28);font-size:.75rem;padding:14px 0;'>
  Nassau Candy Distributor &middot; Profitability Intelligence Platform v3.0 &middot;
  Powered by Streamlit &amp; Plotly &middot; &copy; 2025
</div>""", unsafe_allow_html=True)
