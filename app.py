import streamlit as st
import pandas as pd
import numpy as np
import os
import time
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

import auth_service as auth
import cmms_service as cmms
import erp_service as erp
import feedback_service as fbk
import reporting_service as rpt
import prediction_pipeline as pred
import model_retraining as retrain_engine

# ── Page Config ──
st.set_page_config(
    page_title="AI Digital Twin | Port Crane Framework",
    page_icon="⚙",
    layout="wide",
    initial_sidebar_state="expanded"
)

ROOT_DIR = os.path.dirname(__file__)

# ── CSS ── (only styling, no layout via HTML)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

/* ===== HIDE STREAMLIT DEFAULT HEADER BAR ===== */
header[data-testid="stHeader"],
[data-testid="stHeader"],
.stAppHeader {
    display: none !important;
}

#stDecoration, [data-testid="stDecoration"], div[data-testid="stToolbar"] {
    display: none !important;
}

/* ===== CUSTOM SIDEBAR TOGGLE BUTTON (injected by JS) ===== */
#custom-sidebar-btn {
    position: fixed;
    top: 12px;
    left: 12px;
    z-index: 9999999;
    width: 38px;
    height: 38px;
    background: #1C2333;
    border: 1px solid #30363D;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    color: #00D9FF;
    font-size: 1.1rem;
    box-shadow: 0 4px 16px rgba(0,0,0,0.5);
    transition: background 0.2s, border-color 0.2s, box-shadow 0.2s;
    user-select: none;
}
#custom-sidebar-btn:hover {
    background: #21262D;
    border-color: #00D9FF;
    box-shadow: 0 0 12px rgba(0,217,255,0.4);
}

/* ===== APP BACKGROUND ===== */
.stApp { background-color: #0D1117 !important; }
.block-container { padding: 1.2rem 1.8rem 2rem 1.8rem !important; max-width: 100% !important; margin-top: 0 !important; }
.main .block-container { padding-top: 0.8rem !important; margin-top: 0 !important; }
.stApp > div:first-child { margin-top: 0 !important; padding-top: 0 !important; }
.appview-container { padding-top: 0 !important; }

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] { background: #161B22 !important; border-right: 1px solid #30363D !important; }
[data-testid="stSidebar"] .block-container { padding: 1.2rem 0.8rem !important; }
[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label,[data-testid="stSidebar"] p,[data-testid="stSidebar"] span { color: #8B949E !important; font-size: 0.82rem !important; }

/* ===== RADIO NAV ===== */
[data-testid="stRadio"] > label { display: none !important; }
[data-testid="stRadio"] > div { display: flex !important; flex-direction: column !important; gap: 2px !important; }
[data-testid="stRadio"] > div > label {
    display: flex !important; align-items: center !important;
    padding: 9px 12px !important; border-radius: 9px !important;
    cursor: pointer !important; color: #8B949E !important;
    font-size: 0.85rem !important; font-weight: 500 !important;
    transition: all 0.15s ease !important; background: transparent !important;
    border-left: 3px solid transparent !important;
}
[data-testid="stRadio"] > div > label:hover { background: rgba(255,255,255,0.05) !important; color: #E6EDF3 !important; }
div[data-testid="stRadio"] div[role="radiogroup"] label[aria-checked="true"] {
    background: rgba(0,217,255,0.1) !important; color: #00D9FF !important;
    border-left: 3px solid #00D9FF !important;
}
[data-testid="stRadio"] input[type="radio"] { display: none !important; }
[data-testid="stRadio"] > div > label > div:first-child { display: none !important; }

/* ===== SELECTBOX / DROPDOWN ===== */
[data-testid="stSelectbox"] > label,[data-testid="stSelectbox"] label {
    color: #8B949E !important; font-size: 0.72rem !important; font-weight: 600 !important;
    text-transform: uppercase !important; letter-spacing: 0.8px !important;
}
[data-testid="stSelectbox"] > div > div,[data-testid="stSelectbox"] [data-baseweb="select"] > div {
    background: #1C2333 !important; border: 1px solid #30363D !important;
    border-radius: 8px !important; color: #E6EDF3 !important; min-height: 40px !important;
}
[data-testid="stSelectbox"] [data-baseweb="select"] span,
[data-testid="stSelectbox"] [data-baseweb="select"] div { color: #E6EDF3 !important; }
[data-testid="stSelectbox"] svg { fill: #8B949E !important; }
/* Dropdown popup list */
[data-baseweb="popover"],[data-baseweb="popover"] ul,[data-baseweb="menu"],[role="listbox"] {
    background: #1C2333 !important; border: 1px solid #30363D !important;
    border-radius: 10px !important; box-shadow: 0 12px 40px rgba(0,0,0,0.6) !important;
}
[data-baseweb="menu"] li,[role="listbox"] li,[role="option"] {
    background: transparent !important; color: #CBD5E1 !important;
    font-size: 0.85rem !important; padding: 9px 14px !important;
}
[data-baseweb="menu"] li:hover,[role="option"]:hover,[role="option"][aria-selected="true"] {
    background: rgba(0,217,255,0.12) !important; color: #00D9FF !important;
}

/* ===== SLIDERS ===== */
[data-testid="stSlider"] > label,[data-testid="stSlider"] label {
    color: #CBD5E1 !important; font-size: 0.78rem !important; font-weight: 500 !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] > div > div { background: #30363D !important; }
[data-testid="stSlider"] [data-baseweb="slider"] [role="progressbar"] { background: linear-gradient(90deg,#007BCC,#00D9FF) !important; }
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
    background: #00D9FF !important; border: 3px solid #0D1117 !important;
    box-shadow: 0 0 0 2px #00D9FF !important;
}
[data-testid="stSlider"] p { color: #E6EDF3 !important; }
[data-testid="stSlider"] span { color: #8B949E !important; }
/* Fallback slider track */
.stSlider > div > div > div { background: #30363D !important; }
.stSlider > div > div > div > div { background: linear-gradient(90deg,#007BCC,#00D9FF) !important; }

/* ===== METRICS ===== */
[data-testid="stMetric"] { background: #161B22 !important; border: 1px solid #21262D !important; border-radius: 12px !important; padding: 16px 18px !important; transition: border-color 0.2s,transform 0.2s; }
[data-testid="stMetric"]:hover { border-color: #30363D !important; transform: translateY(-1px); }
[data-testid="stMetricLabel"] > div,[data-testid="stMetricLabel"] p,[data-testid="stMetricLabel"] span { color: #8B949E !important; font-size: 0.75rem !important; text-transform: uppercase; letter-spacing: 0.8px; }
[data-testid="stMetricValue"],[data-testid="stMetricValue"] > div { color: #E6EDF3 !important; font-size: 1.7rem !important; font-weight: 700 !important; }
[data-testid="stMetricDelta"],[data-testid="stMetricDelta"] > div { color: #00FF88 !important; font-size: 0.72rem !important; }
[data-testid="stMetricDelta"] svg { fill: #00FF88 !important; }

/* ===== BUTTONS ===== */
div.stButton > button {
    background: linear-gradient(135deg,#00D9FF,#007BCC) !important;
    color: #0D1117 !important; font-weight: 700 !important; font-size: 0.83rem !important;
    border: none !important; border-radius: 9px !important; padding: 10px 20px !important;
    width: 100% !important; transition: all 0.2s ease !important;
}
div.stButton > button:hover { filter: brightness(1.12) !important; transform: translateY(-2px) !important; box-shadow: 0 6px 24px rgba(0,217,255,0.3) !important; }
div.stButton > button[kind="primary"] { background: linear-gradient(135deg,#FF3B5C,#AA1133) !important; color: #fff !important; }
div.stButton > button[kind="primary"]:hover { box-shadow: 0 6px 24px rgba(255,59,92,0.3) !important; }

/* ===== TEXT / NUMBER INPUTS ===== */
.stTextInput > div > div > input,.stTextArea > div > div > textarea,.stNumberInput > div > div > input {
    background: #1C2333 !important; border: 1px solid #30363D !important;
    border-radius: 8px !important; color: #E6EDF3 !important; font-size: 0.85rem !important;
    caret-color: #00D9FF !important;
}
.stTextInput > div > div > input:focus,.stTextArea > div > div > textarea:focus,.stNumberInput > div > div > input:focus {
    border-color: #00D9FF !important; box-shadow: 0 0 0 3px rgba(0,217,255,0.15) !important; outline: none !important;
}
.stTextInput > div > div > input::placeholder,.stTextArea > div > div > textarea::placeholder { color: #4A5568 !important; }
.stTextInput > label,.stTextArea > label,.stNumberInput > label { color: #8B949E !important; font-size: 0.75rem !important; font-weight: 600 !important; }
.stNumberInput button { background: #21262D !important; border-color: #30363D !important; color: #CBD5E1 !important; }
.stNumberInput button:hover { background: #30363D !important; color: #E6EDF3 !important; }
.stNumberInput button svg { fill: #CBD5E1 !important; }

/* ===== DOWNLOAD BUTTON ===== */
[data-testid="stDownloadButton"] > button {
    background: #1C2333 !important; color: #00D9FF !important;
    border: 1px solid rgba(0,217,255,0.4) !important; border-radius: 9px !important;
    font-weight: 600 !important; width: 100% !important; transition: all 0.2s !important;
}
[data-testid="stDownloadButton"] > button:hover { background: rgba(0,217,255,0.1) !important; border-color: #00D9FF !important; transform: translateY(-1px) !important; }

/* ===== ALERTS ===== */
.stSuccess > div { background: rgba(0,255,136,0.06) !important; border: 1px solid rgba(0,255,136,0.3) !important; border-radius: 10px !important; color: #00FF88 !important; }
.stWarning > div { background: rgba(255,184,0,0.06) !important; border: 1px solid rgba(255,184,0,0.3) !important; border-radius: 10px !important; color: #FFB800 !important; }
.stError > div { background: rgba(255,59,92,0.06) !important; border: 1px solid rgba(255,59,92,0.3) !important; border-radius: 10px !important; color: #FF3B5C !important; }
.stInfo > div { background: rgba(0,217,255,0.06) !important; border: 1px solid rgba(0,217,255,0.3) !important; border-radius: 10px !important; color: #00D9FF !important; }
[data-testid="stAlert"] p,[data-testid="stAlert"] span { color: inherit !important; }
[data-testid="stAlert"] svg { fill: currentColor !important; }

/* ===== EXPANDER ===== */
[data-testid="stExpander"] { background: #161B22 !important; border: 1px solid #21262D !important; border-radius: 10px !important; }
[data-testid="stExpander"] details summary { color: #CBD5E1 !important; font-size: 0.85rem !important; font-weight: 600 !important; padding: 12px 16px !important; }
[data-testid="stExpander"] details summary svg { fill: #8B949E !important; }
details summary { color: #CBD5E1 !important; font-size: 0.85rem !important; font-weight: 600 !important; }

/* ===== DATAFRAME ===== */
[data-testid="stDataFrameContainer"] { background: #161B22 !important; border: 1px solid #21262D !important; border-radius: 10px !important; overflow: hidden !important; }
.dvn-scroller { background: #161B22 !important; }

/* ===== TABS ===== */
[data-testid="stTabs"] [data-baseweb="tab-list"] { background: transparent !important; border-bottom: 1px solid #21262D !important; }
[data-testid="stTabs"] [data-baseweb="tab"] { background: transparent !important; color: #8B949E !important; font-size: 0.83rem !important; font-weight: 500 !important; border-radius: 8px 8px 0 0 !important; padding: 8px 16px !important; }
[data-testid="stTabs"] [data-baseweb="tab"]:hover { color: #E6EDF3 !important; background: rgba(255,255,255,0.04) !important; }
[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"] { color: #00D9FF !important; border-bottom: 2px solid #00D9FF !important; }

/* ===== CHECKBOX ===== */
[data-testid="stCheckbox"] label { color: #CBD5E1 !important; font-size: 0.83rem !important; }
[data-testid="stCheckbox"] [data-baseweb="checkbox"] { background: #1C2333 !important; border-color: #30363D !important; border-radius: 5px !important; }
[data-testid="stCheckbox"] [data-baseweb="checkbox"][data-checked="true"] { background: #00D9FF !important; border-color: #00D9FF !important; }
[data-testid="stCheckbox"] svg { fill: #0D1117 !important; }

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #161B22; border-radius: 3px; }
::-webkit-scrollbar-thumb { background: #30363D; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #8B949E; }

/* ===== DIVIDER ===== */
hr { border-color: #21262D !important; }

/* ===== SECTION LABEL ===== */
.section-label { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 1.8px; color: #4A5568; margin-bottom: 8px; padding-left: 2px; font-weight: 700; }

/* ===== KPI BOX ===== */
.kpi-box { background: #161B22; border: 1px solid #21262D; border-radius: 14px; padding: 18px 20px; position: relative; overflow: hidden; transition: transform 0.2s,border-color 0.2s,box-shadow 0.2s; }
.kpi-box:hover { transform: translateY(-2px); border-color: #30363D; box-shadow: 0 8px 24px rgba(0,0,0,0.3); }
.kpi-accent { height: 3px; border-radius: 14px 14px 0 0; position: absolute; top: 0; left: 0; right: 0; }
.kpi-icon { width: 38px; height: 38px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; margin-bottom: 10px; }
.kpi-lbl { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 1px; color: #8B949E; font-weight: 500; }
.kpi-val { font-size: 2rem; font-weight: 800; line-height: 1.1; margin-top: 4px; }
.kpi-sub { font-size: 0.7rem; color: #8B949E; margin-top: 4px; }

/* ===== SECTION CARD ===== */
.s-card { background: #161B22; border: 1px solid #21262D; border-radius: 14px; padding: 18px 20px; margin-bottom: 14px; }
.s-card-title { font-size: 0.9rem; font-weight: 600; color: #E6EDF3; margin-bottom: 14px; }
.s-card-sub { font-size: 0.75rem; color: #8B949E; margin-bottom: 14px; }

/* ===== STATUS BADGES ===== */
.b-normal  { background: rgba(0,255,136,0.12); color: #00FF88; border: 1px solid rgba(0,255,136,0.35); padding: 4px 12px; border-radius: 20px; font-size: 0.72rem; font-weight: 700; display: inline-block; }
.b-warning { background: rgba(255,184,0,0.12); color: #FFB800; border: 1px solid rgba(255,184,0,0.35); padding: 4px 12px; border-radius: 20px; font-size: 0.72rem; font-weight: 700; display: inline-block; }
.b-high    { background: rgba(255,120,50,0.12); color: #FF7832; border: 1px solid rgba(255,120,50,0.35); padding: 4px 12px; border-radius: 20px; font-size: 0.72rem; font-weight: 700; display: inline-block; }
.b-critical{ background: rgba(255,59,92,0.12); color: #FF3B5C; border: 1px solid rgba(255,59,92,0.35); padding: 4px 12px; border-radius: 20px; font-size: 0.72rem; font-weight: 700; display: inline-block; animation: blink 1.5s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.5} }

/* ===== LIVE INDICATOR ===== */
.live-pill { display: inline-flex; align-items: center; gap: 6px; background: rgba(0,255,136,0.1); border: 1px solid rgba(0,255,136,0.4); color: #00FF88; border-radius: 20px; padding: 4px 12px; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.5px; }
.live-dot { width: 7px; height: 7px; border-radius: 50%; background: #00FF88; display: inline-block; animation: livep 1.4s ease-in-out infinite; }
@keyframes livep { 0%,100%{opacity:1;box-shadow:0 0 0 0 rgba(0,255,136,0.7)} 60%{opacity:0.6;box-shadow:0 0 0 5px rgba(0,255,136,0)} }

/* ===== SENSOR ROWS ===== */
.sens-row { display: flex; align-items: center; gap: 12px; padding: 11px 0; border-bottom: 1px solid #21262D; }
.sens-row:last-child { border-bottom: none; }
.sens-icon { width: 34px; height: 34px; border-radius: 9px; display: flex; align-items: center; justify-content: center; font-size: 1rem; flex-shrink: 0; color: #CBD5E1; }
.sens-label { font-size: 0.8rem; font-weight: 500; color: #CBD5E1; }
.sens-bar-bg { height: 5px; border-radius: 5px; background: #21262D; margin-top: 6px; }
.sens-bar-fg { height: 100%; border-radius: 5px; transition: width 0.4s ease; }
.sens-val { font-size: 0.88rem; font-weight: 700; font-family: 'JetBrains Mono', monospace; white-space: nowrap; }

/* ===== WO / INVENTORY ROWS ===== */
.wo-row { padding: 10px 0; border-bottom: 1px solid #21262D; }
.wo-row:last-child { border-bottom: none; }
.wo-id-lbl { font-size: 0.78rem; font-weight: 700; color: #00D9FF; font-family: 'JetBrains Mono', monospace; }
.inv-row { padding: 10px 0; border-bottom: 1px solid #21262D; }
.inv-row:last-child { border-bottom: none; }
</style>
""", unsafe_allow_html=True)

# ── Custom Sidebar Toggle Button (JS-injected, always visible) ──
st.markdown("""
<script>
(function() {
  // Create our custom floating button once
  function injectBtn() {
    if (document.getElementById('custom-sidebar-btn')) return;
    var btn = document.createElement('div');
    btn.id = 'custom-sidebar-btn';
    btn.title = 'Toggle Sidebar';
    btn.innerHTML = '&#9776;'; // hamburger ☰
    btn.onclick = function() {
      // Try to find and click Streamlit's own sidebar toggle
      var toggles = document.querySelectorAll(
        '[data-testid="collapsedControl"], [data-testid="stSidebarCollapseButton"], ' +
        'button[aria-label="Close sidebar"], button[aria-label="Open sidebar"], ' +
        'button[aria-label="Expand sidebar"], button[aria-label="Collapse sidebar"]'
      );
      if (toggles.length > 0) {
        toggles[0].click();
      } else {
        // Fallback: look for the sidebar and toggle its display
        var sb = document.querySelector('[data-testid="stSidebar"]');
        if (sb) sb.style.display = sb.style.display === 'none' ? '' : 'none';
      }
    };
    document.body.appendChild(btn);
  }

  // Run immediately and on DOM changes
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectBtn);
  } else {
    injectBtn();
  }
  // Re-inject after Streamlit re-renders
  setInterval(injectBtn, 600);
})();
</script>
""", unsafe_allow_html=True)


# ── Helpers ──
def load_data():
    cranes = pd.read_csv(os.path.join(ROOT_DIR, "cranes.csv")) if os.path.exists(os.path.join(ROOT_DIR, "cranes.csv")) else pd.DataFrame()
    sensor = pd.read_csv(os.path.join(ROOT_DIR, "sensor_data.csv")) if os.path.exists(os.path.join(ROOT_DIR, "sensor_data.csv")) else pd.DataFrame()
    return cranes, sensor

def health_badge(status):
    css = {"Normal": "b-normal", "Warning": "b-warning", "High Risk": "b-high", "Critical": "b-critical"}.get(status, "b-normal")
    return f'<span class="{css}">{status}</span>'

def priority_color(p):
    return {"Emergency": "#FF3B5C", "High": "#FF7832", "Medium": "#FFB800", "Low": "#00D9FF"}.get(p, "#8B949E")

def status_color(s):
    return {"Open": "#FFB800", "Completed": "#00FF88", "In Progress": "#00D9FF", "Cancelled": "#8B949E"}.get(s, "#8B949E")

def kpi_md(accent, icon_bg, icon, label, value, sub):
    return f"""
<div class="kpi-box">
  <div class="kpi-accent" style="background:{accent};"></div>
  <div class="kpi-icon" style="background:{icon_bg};">{icon}</div>
  <div class="kpi-lbl">{label}</div>
  <div class="kpi-val" style="color:{accent.split(',')[0].replace('linear-gradient(135deg,','').strip()};">{value}</div>
  <div class="kpi-sub">{sub}</div>
</div>"""

def sensor_row(icon, icon_bg, name, val, unit, bar_color, pct):
    pct = max(0, min(100, pct))
    return f"""
<div class="sens-row">
  <div class="sens-icon" style="background:{icon_bg};">{icon}</div>
  <div style="flex:1;">
    <div class="sens-label">{name}</div>
    <div class="sens-bar-bg"><div class="sens-bar-fg" style="width:{pct:.0f}%;background:{bar_color};"></div></div>
  </div>
  <div class="sens-val" style="color:{bar_color};">{val}<span style="font-size:0.68rem;color:#8B949E;font-weight:400;margin-left:3px;">{unit}</span></div>
</div>"""

CHART_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(22,27,34,1)",
    plot_bgcolor="rgba(22,27,34,1)",
    margin=dict(l=10, r=10, t=38, b=10),
    height=240,
    font=dict(family="Inter", color="#8B949E", size=11),
    xaxis=dict(showgrid=False, linecolor="#30363D", tickcolor="#30363D"),
    yaxis=dict(showgrid=True, gridcolor="#21262D", linecolor="#21262D"),
)

def area_fig(df, x, y, title, color, height=240):
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    layout = dict(CHART_LAYOUT)
    layout["height"] = height
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[x], y=df[y], mode="lines",
        line=dict(color=color, width=2.5),
        fill="tozeroy", fillcolor=f"rgba({r},{g},{b},0.07)",
        name=y
    ))
    fig.update_layout(**layout, title=dict(text=title, font=dict(size=12, color="#CBD5E1", family="Inter")))
    return fig

def crane_svg(health_status, sim_temp, sim_vib, sim_curr, sim_press):
    c = {"Normal": "#00FF88", "Warning": "#FFB800", "High Risk": "#FF7832", "Critical": "#FF3B5C"}.get(health_status, "#00FF88")
    dur = "0.7s" if health_status == "Critical" else ("1.5s" if health_status == "High Risk" else "2.5s")
    return f"""
<div class="s-card" style="margin-bottom:0;">
<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
  <div>
    <div class="s-card-title" style="margin-bottom:2px;">⬡ 2D Structural Digital Twin</div>
    <div class="s-card-sub" style="margin-bottom:0;">Ship-to-Shore (STS) Crane — Live subsystem overlay</div>
  </div>
  {health_badge(health_status)}
</div>
<svg width="100%" height="230" viewBox="0 0 620 230" xmlns="http://www.w3.org/2000/svg" style="display:block;">
  <defs>
    <pattern id="grid" width="22" height="22" patternUnits="userSpaceOnUse">
      <path d="M22 0L0 0 0 22" fill="none" stroke="#21262D" stroke-width="0.7"/>
    </pattern>
  </defs>
  <rect width="100%" height="100%" fill="url(#grid)" rx="8"/>
  <!-- Water line -->
  <rect x="0" y="200" width="620" height="30" fill="rgba(0,217,255,0.04)" rx="4"/>
  <line x1="0" y1="200" x2="620" y2="200" stroke="rgba(0,217,255,0.18)" stroke-width="1.5"/>
  <!-- Gantry legs -->
  <line x1="185" y1="198" x2="235" y2="52" stroke="#30363D" stroke-width="7" stroke-linecap="round"/>
  <line x1="330" y1="198" x2="280" y2="52" stroke="#30363D" stroke-width="7" stroke-linecap="round"/>
  <!-- Cross brace -->
  <line x1="200" y1="150" x2="315" y2="150" stroke="#21262D" stroke-width="4"/>
  <line x1="198" y1="125" x2="318" y2="170" stroke="#21262D" stroke-width="1.8" stroke-dasharray="4,3" opacity="0.6"/>
  <line x1="318" y1="125" x2="198" y2="170" stroke="#21262D" stroke-width="1.8" stroke-dasharray="4,3" opacity="0.6"/>
  <!-- Main boom -->
  <rect x="58" y="44" width="490" height="13" rx="4" fill="#1C2333" stroke="#30363D" stroke-width="1.5"/>
  <!-- Counterweight -->
  <line x1="95" y1="57" x2="95" y2="120" stroke="#30363D" stroke-width="5" stroke-linecap="round"/>
  <rect x="72" y="118" width="46" height="18" rx="3" fill="#1C2333" stroke="#30363D" stroke-width="1.5"/>
  <text x="95" y="130" font-size="7.5" fill="#8B949E" text-anchor="middle" font-family="Inter">CNTR WT</text>
  <!-- Trolley -->
  <rect x="340" y="38" width="46" height="20" rx="5" fill="#1C2333" stroke="{c}" stroke-width="2"/>
  <circle cx="353" cy="49" r="3.5" fill="{c}" opacity="0.9"/>
  <circle cx="374" cy="49" r="3.5" fill="{c}" opacity="0.9"/>
  <text x="357" y="67" font-size="8" fill="{c}" text-anchor="middle" font-weight="700" font-family="Inter">TROLLEY</text>
  <!-- Wire ropes -->
  <line x1="353" y1="58" x2="353" y2="150" stroke="#8B949E" stroke-width="1.3" stroke-dasharray="4,3"/>
  <line x1="371" y1="58" x2="371" y2="150" stroke="#8B949E" stroke-width="1.3" stroke-dasharray="4,3"/>
  <!-- Spreader -->
  <rect x="330" y="149" width="84" height="11" rx="3" fill="#1C2333" stroke="#30363D" stroke-width="1.5"/>
  <!-- Container -->
  <rect x="315" y="160" width="114" height="38" rx="4" fill="#0D1117" stroke="rgba(0,217,255,0.18)" stroke-width="1.5"/>
  <line x1="315" y1="173" x2="429" y2="173" stroke="rgba(0,217,255,0.09)" stroke-width="1"/>
  <line x1="372" y1="160" x2="372" y2="198" stroke="rgba(0,217,255,0.09)" stroke-width="1"/>
  <text x="372" y="183" font-size="8.5" fill="#8B949E" text-anchor="middle" font-family="Inter">CONTAINER 40FT</text>
  <!-- Hoist motor node -->
  <circle cx="220" cy="49" r="9" fill="{c}" opacity="0.12"/>
  <circle cx="220" cy="49" r="6" fill="{c}" opacity="0.9">
    <animate attributeName="r" values="5;8;5" dur="{dur}" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.9;0.35;0.9" dur="{dur}" repeatCount="indefinite"/>
  </circle>
  <text x="220" y="36" font-size="7.5" fill="{c}" text-anchor="middle" font-family="Inter" font-weight="700">MOTOR</text>
  <!-- Gearbox node -->
  <circle cx="265" cy="49" r="6" fill="#A855F7" opacity="0.85">
    <animate attributeName="opacity" values="0.85;0.35;0.85" dur="2.2s" repeatCount="indefinite"/>
  </circle>
  <text x="265" y="36" font-size="7.5" fill="#A855F7" text-anchor="middle" font-family="Inter" font-weight="700">GEARBOX</text>
  <!-- Active sensor beacon -->
  <circle cx="357" cy="22" r="4.5" fill="#00D9FF">
    <animate attributeName="r" values="3;7;3" dur="1.8s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="1;0.2;1" dur="1.8s" repeatCount="indefinite"/>
  </circle>
  <text x="372" y="26" font-size="8" fill="#00D9FF" font-family="Inter" font-weight="600">AI SENSOR NODE ACTIVE</text>
  <!-- Rails -->
  <rect x="148" y="196" width="96" height="4" rx="2" fill="#21262D"/>
  <rect x="294" y="196" width="96" height="4" rx="2" fill="#21262D"/>
  
  <!-- Telemetry Overlays -->
  <rect x="180" y="20" width="80" height="24" rx="4" fill="rgba(0,0,0,0.6)" stroke="#30363D" stroke-width="1"/>
  <text x="220" y="30" font-size="7" fill="#8B949E" text-anchor="middle" font-family="Inter">TEMP &amp; CURRENT</text>
  <text x="220" y="40" font-size="8" fill="#E6EDF3" text-anchor="middle" font-family="Inter" font-weight="700">{sim_temp:.1f}°C | {sim_curr:.1f}A</text>

  <rect x="250" y="60" width="60" height="24" rx="4" fill="rgba(0,0,0,0.6)" stroke="#30363D" stroke-width="1"/>
  <text x="280" y="70" font-size="7" fill="#8B949E" text-anchor="middle" font-family="Inter">VIBRATION</text>
  <text x="280" y="80" font-size="8" fill="#E6EDF3" text-anchor="middle" font-family="Inter" font-weight="700">{sim_vib:.2f} mm/s</text>

  <rect x="330" y="105" width="70" height="24" rx="4" fill="rgba(0,0,0,0.6)" stroke="#30363D" stroke-width="1"/>
  <text x="365" y="115" font-size="7" fill="#8B949E" text-anchor="middle" font-family="Inter">PRESSURE</text>
  <text x="365" y="125" font-size="8" fill="#E6EDF3" text-anchor="middle" font-family="Inter" font-weight="700">{sim_press:.0f} bar</text>

  <!-- Health label -->
  <rect x="220" y="210" width="160" height="16" rx="3" fill="rgba(0,0,0,0.5)"/>
  <text x="300" y="221" font-size="8.5" fill="{c}" text-anchor="middle" font-family="Inter" font-weight="700">SYSTEM STATE: {health_status.upper()}</text>
</svg>
</div>"""


# ── Session Init ──
if "user" not in st.session_state:
    st.session_state.user = {"user_id": "U-101", "name": "Sharma Dhruv", "email": "dhruv@port.com", "role": "Administrator"}
if "page" not in st.session_state:
    st.session_state.page = "Digital Twin"

cranes_df, sensor_df = load_data()
pipeline = pred.get_pipeline()


# ════════════════════════════════════════════════════════
#  SIDEBAR
# ════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;padding:4px 4px 18px 4px;border-bottom:1px solid #21262D;margin-bottom:14px;">
      <div style="width:38px;height:38px;border-radius:10px;background:rgba(0,217,255,0.1);display:flex;align-items:center;justify-content:center;font-size:1.2rem;flex-shrink:0;">⚙</div>
      <div>
        <div style="font-size:0.88rem;font-weight:700;color:#E6EDF3;">CraneTwin</div>
        <div style="font-size:0.68rem;color:#8B949E;">AI Digital Twin v2.0</div>
      </div>
    </div>
    <div class="section-label">Navigation</div>
    """, unsafe_allow_html=True)

    pages = [
        "⬡  Digital Twin",
        "◈  AI Analytics",
        "▤  CMMS",
        "⬢  ERP Inventory",
        "↻  Closed-Loop",
        "▧  Reports",
        "⊙  Users",
    ]
    page_keys = ["Digital Twin", "AI Analytics", "CMMS", "ERP Inventory", "Closed-Loop", "Reports", "Users"]
    nav_sel = st.radio("nav", pages, index=page_keys.index(st.session_state.page) if st.session_state.page in page_keys else 0, label_visibility="collapsed")
    st.session_state.page = page_keys[pages.index(nav_sel)]
    page = st.session_state.page

    st.markdown('<div style="height:1px;background:#21262D;margin:14px 0;"></div><div class="section-label">Target Crane</div>', unsafe_allow_html=True)
    crane_ids = cranes_df["crane_id"].tolist() if not cranes_df.empty else ["CR-001"]
    default_idx = min(2, len(crane_ids) - 1)
    selected_crane = st.selectbox("Crane", crane_ids, index=default_idx, label_visibility="collapsed")

    st.markdown('<div style="height:1px;background:#21262D;margin:14px 0;"></div><div class="section-label">Telemetry Simulator</div>', unsafe_allow_html=True)
    sim_vib  = st.slider("Vibration (mm/s)", 0.2, 3.5, 0.4, 0.1)
    sim_temp = st.slider("Temperature (°C)", 40.0, 110.0, 65.0, 1.0)
    sim_curr = st.slider("Motor Current (A)", 10.0, 80.0, 35.0, 1.0)
    sim_press = st.slider("Hydraulic Pressure (bar)", 50.0, 270.0, 150.0, 5.0)

    st.markdown('<div style="height:1px;background:#21262D;margin:14px 0;"></div><div class="section-label">Active User</div>', unsafe_allow_html=True)
    all_users_df = auth.get_all_users()
    user_names = all_users_df["name"].tolist() if not all_users_df.empty else ["Sharma Dhruv"]
    sel_name = st.selectbox("User", user_names, label_visibility="collapsed")
    if not all_users_df.empty and sel_name in all_users_df["name"].values:
        st.session_state.user = all_users_df[all_users_df["name"] == sel_name].iloc[0].to_dict()

    st.markdown(f"""
    <div style="background:#0D1117;border:1px solid #21262D;border-radius:10px;padding:10px 12px;margin-top:10px;">
      <div style="font-size:0.82rem;font-weight:600;color:#E6EDF3;">{st.session_state.user['name']}</div>
      <div style="font-size:0.7rem;color:#00D9FF;margin-top:2px;">{st.session_state.user['role']}</div>
    </div>
    """, unsafe_allow_html=True)


# ── AI Evaluation ──
crane_pred = pipeline.predict_latest_for_crane(selected_crane)
latest_sens = crane_pred["latest_sensor"] if crane_pred else {}
latest_sens["vibration"]    = sim_vib
latest_sens["temperature"]  = sim_temp
latest_sens["motor_current"] = sim_curr
latest_sens["hydraulic_pressure"] = sim_press
live_eval = pipeline.predict_sample(latest_sens)

health_st = live_eval["health_status"]
rul_val   = live_eval["estimated_rul"]
h_score   = live_eval["health_score"]
f_prob    = live_eval["failure_probability"]
anom      = live_eval["anomaly_score"]
conf      = live_eval["confidence"]
issue_txt = live_eval["issue"]
rec_txt   = live_eval["recommendation"]

accent_c  = {"Normal": "#00FF88", "Warning": "#FFB800", "High Risk": "#FF7832", "Critical": "#FF3B5C"}.get(health_st, "#00FF88")


# ════════════════════════════════════════════════════════
#  PAGE: DIGITAL TWIN
# ════════════════════════════════════════════════════════
if page == "Digital Twin":
    # ── Header ──
    now_str = datetime.now().strftime("%d %b %Y  %H:%M:%S")
    col_hd1, col_hd2 = st.columns([3, 1])
    with col_hd1:
        st.markdown(f"""
        <div style="padding-bottom:16px;border-bottom:1px solid #21262D;margin-bottom:20px;">
          <div style="font-size:1.35rem;font-weight:700;color:#E6EDF3;">⬡ Digital Twin Fleet Monitoring</div>
          <div style="font-size:0.8rem;color:#8B949E;margin-top:3px;">Real-time sensor telemetry, structural health &amp; subsystem status</div>
        </div>
        """, unsafe_allow_html=True)
    with col_hd2:
        st.markdown(f"""
        <div style="text-align:right;padding-bottom:16px;border-bottom:1px solid #21262D;margin-bottom:20px;">
          <div class="live-pill"><div class="live-dot"></div> LIVE</div>
          <div style="font-size:0.72rem;color:#8B949E;margin-top:6px;font-family:'JetBrains Mono',monospace;">{now_str}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── KPI Metrics (using native st.metric for proper layout) ──
    if not cranes_df.empty:
        total_c   = len(cranes_df)
        healthy_c = len(cranes_df[cranes_df["status"] == "Running"])
        warn_c    = len(cranes_df[cranes_df["status"] == "Warning"])
        crit_c    = len(cranes_df[cranes_df["status"] == "Critical"])
    else:
        total_c = healthy_c = warn_c = crit_c = 0

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("⚙ Total Fleet Cranes", total_c, "STS + RTG + RMG")
    m2.metric("✓ Operational", healthy_c, "Within safe parameters")
    m3.metric("▲ Warning State", warn_c, "Elevated readings")
    m4.metric("✖ Critical Alert", crit_c, "Immediate action required")

    st.markdown('<div style="height:18px;"></div>', unsafe_allow_html=True)

    # ── Crane SVG + Sensors ──
    col_sv, col_se = st.columns([1.6, 1.0], gap="medium")

    with col_sv:
        st.markdown(crane_svg(health_st, sim_temp, sim_vib, sim_curr, sim_press), unsafe_allow_html=True)

    with col_se:
        temp_pct    = min(100, max(0, (sim_temp - 40) / 70 * 100))
        vib_pct     = min(100, max(0, sim_vib / 3.5 * 100))
        curr_val    = float(latest_sens.get("motor_current", 35.0))
        curr_pct    = min(100, max(0, (curr_val - 10) / 70 * 100))
        press_val   = float(latest_sens.get("hydraulic_pressure", 150.0))
        press_pct   = min(100, max(0, (press_val - 50) / 220 * 100))
        runtime_val = float(latest_sens.get("runtime_hours", 1500))
        temp_color  = "#FF3B5C" if sim_temp > 85 else ("#FFB800" if sim_temp > 70 else "#00FF88")
        vib_color   = "#FF3B5C" if sim_vib > 2.0 else ("#FFB800" if sim_vib > 0.8 else "#00FF88")

        st.markdown(f"""
<div class="s-card" style="margin-bottom:0;">
  <div class="s-card-title">◈ Real-Time Sensor Readings</div>
  <div class="s-card-sub">{selected_crane} — Subsystem telemetry</div>
  {sensor_row("◈","rgba(255,59,92,0.12)","Motor Temperature",f"{sim_temp:.1f}","°C",temp_color,temp_pct)}
  {sensor_row("∿","rgba(168,85,247,0.12)","Vibration Spectrum",f"{sim_vib:.2f}","mm/s",vib_color,vib_pct)}
  {sensor_row("⚡","rgba(255,184,0,0.12)","Motor Current",f"{curr_val:.1f}","A","#FFB800",curr_pct)}
  {sensor_row("⊙","rgba(0,217,255,0.12)","Hydraulic Pressure",f"{press_val:.0f}","bar","#00D9FF",press_pct)}
  {sensor_row("⏱","rgba(0,255,136,0.12)","Cumulative Runtime",f"{int(runtime_val)}","hrs","#00FF88",min(100,runtime_val/4000*100))}
</div>
        """, unsafe_allow_html=True)

    # ── Trend Charts ──
    st.markdown('<div style="height:18px;"></div>', unsafe_allow_html=True)
    crane_hist = sensor_df[sensor_df["crane_id"] == selected_crane].tail(40).copy() if not sensor_df.empty else pd.DataFrame()

    if not crane_hist.empty:
        # Append the simulated live data point to the charts
        latest_row = crane_hist.iloc[-1].copy()
        latest_row["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        latest_row["temperature"] = sim_temp
        latest_row["vibration"] = sim_vib
        latest_row["motor_current"] = sim_curr
        latest_row["RUL"] = rul_val
        crane_hist = pd.concat([crane_hist, pd.DataFrame([latest_row])], ignore_index=True)

    col_g1, col_g2 = st.columns(2, gap="medium")
    with col_g1:
        if not crane_hist.empty:
            st.plotly_chart(area_fig(crane_hist, "timestamp", "temperature", "◈  Temperature Trend (°C)", "#FF3B5C"), width="stretch")
    with col_g2:
        if not crane_hist.empty:
            st.plotly_chart(area_fig(crane_hist, "timestamp", "vibration", "∿  Vibration Spectrum (mm/s)", "#A855F7"), width="stretch")

    # ── Motor current + hydraulic trend ──
    col_g3, col_g4 = st.columns(2, gap="medium")
    with col_g3:
        if not crane_hist.empty:
            st.plotly_chart(area_fig(crane_hist, "timestamp", "motor_current", "⚡  Motor Current (A)", "#FFB800"), width="stretch")
    with col_g4:
        if not crane_hist.empty:
            st.plotly_chart(area_fig(crane_hist, "timestamp", "RUL", "⏱  RUL Trend (hrs)", "#00FF88"), width="stretch")


# ════════════════════════════════════════════════════════
#  PAGE: AI ANALYTICS
# ════════════════════════════════════════════════════════
elif page == "AI Analytics":
    col_hd, col_badge = st.columns([3, 1])
    with col_hd:
        st.markdown(f"""
        <div style="padding-bottom:16px;border-bottom:1px solid #21262D;margin-bottom:20px;">
          <div style="font-size:1.35rem;font-weight:700;color:#E6EDF3;">◈ AI Predictive Analytics Engine</div>
          <div style="font-size:0.8rem;color:#8B949E;margin-top:3px;">Multi-output prediction — {selected_crane}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_badge:
        st.markdown(f"""
        <div style="text-align:right;padding-bottom:16px;border-bottom:1px solid #21262D;margin-bottom:20px;padding-top:8px;">
          {health_badge(health_st)}
        </div>
        """, unsafe_allow_html=True)

    # Metrics
    a1, a2, a3, a4 = st.columns(4)
    a1.metric("◇ Health Index", f"{h_score}%")
    a2.metric("⏱ Predicted RUL", f"{rul_val} hrs")
    a3.metric("▲ Failure Prob.", f"{f_prob}%")
    a4.metric("◈ Anomaly Score", f"{anom}")

    st.markdown('<div style="height:18px;"></div>', unsafe_allow_html=True)

    col_g, col_d = st.columns([1.1, 1.0], gap="medium")

    with col_g:
        # Gauge
        bar_c = "#FF3B5C" if f_prob > 60 else ("#FFB800" if f_prob > 30 else "#00FF88")
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=f_prob,
            number={"suffix": "%", "font": {"size": 34, "color": bar_c, "family": "Inter"}},
            title={"text": "Failure Probability", "font": {"size": 13, "color": "#8B949E", "family": "Inter"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#30363D", "tickfont": {"color": "#8B949E", "size": 10}},
                "bar": {"color": bar_c, "thickness": 0.22},
                "bgcolor": "#161B22",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 30], "color": "rgba(0,255,136,0.07)"},
                    {"range": [30, 65], "color": "rgba(255,184,0,0.07)"},
                    {"range": [65, 100], "color": "rgba(255,59,92,0.07)"},
                ],
                "threshold": {"line": {"color": bar_c, "width": 3}, "thickness": 0.75, "value": f_prob}
            }
        ))
        fig_gauge.update_layout(
            paper_bgcolor="#161B22", plot_bgcolor="#161B22",
            height=270, margin=dict(l=24, r=24, t=30, b=16),
            font=dict(family="Inter", color="#8B949E")
        )
        st.plotly_chart(fig_gauge, width="stretch")

        # Confidence bar
        st.markdown(f"""
        <div class="s-card">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
            <div style="font-size:0.82rem;font-weight:600;color:#E6EDF3;">▤ Model Confidence</div>
            <div style="font-size:0.88rem;font-weight:700;color:#00D9FF;font-family:'JetBrains Mono',monospace;">{conf*100:.1f}%</div>
          </div>
          <div style="height:6px;border-radius:6px;background:#21262D;">
            <div style="width:{conf*100:.0f}%;height:100%;border-radius:6px;background:linear-gradient(90deg,#00D9FF,#00FF88);"></div>
          </div>
          <div style="font-size:0.7rem;color:#8B949E;margin-top:7px;">RandomForest Ensemble · Trained on {len(sensor_df):,} readings</div>
        </div>
        """, unsafe_allow_html=True)

        # RUL sparkline
        crane_hist_ai = sensor_df[sensor_df["crane_id"] == selected_crane].tail(30) if not sensor_df.empty else pd.DataFrame()
        if not crane_hist_ai.empty:
            st.plotly_chart(area_fig(crane_hist_ai, "timestamp", "RUL", "⏱  Remaining Useful Life Trend (hrs)", "#00FF88"), width="stretch")

    with col_d:
        st.markdown(f"""
        <div class="s-card">
          <div class="s-card-title">◈ Component Fault Diagnostic</div>
          <div style="background:#0D1117;border:1px solid rgba(0,217,255,0.2);border-radius:10px;padding:14px;margin-bottom:12px;">
            <div style="font-size:0.68rem;text-transform:uppercase;letter-spacing:1px;color:#8B949E;margin-bottom:5px;">Identified Issue</div>
            <div style="font-size:0.88rem;font-weight:600;color:#00D9FF;">{issue_txt}</div>
          </div>
          <div style="background:#0D1117;border:1px solid rgba(0,255,136,0.2);border-radius:10px;padding:14px;">
            <div style="font-size:0.68rem;text-transform:uppercase;letter-spacing:1px;color:#8B949E;margin-bottom:5px;">AI Recommendation</div>
            <div style="font-size:0.83rem;color:#CBD5E1;line-height:1.6;">{rec_txt}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if health_st in ["High Risk", "Critical"] or sim_vib > 1.2 or sim_temp > 80:
            st.error(f"▲ CRITICAL THRESHOLD BREACHED — {health_st} on {selected_crane}")
            if st.button("⚙ Auto-Trigger Closed-Loop Work Order & Reserve Parts", type="primary"):
                succ, parts, cost, msg = erp.check_and_reserve_parts(issue_txt)
                if succ:
                    prio = "Emergency" if health_st == "Critical" else "High"
                    wo_id = cmms.create_work_order(selected_crane, issue_txt, prio, "Corrective Maintenance", parts, cost, technician=st.session_state.user['name'])
                    st.success(f"✓ WO-{wo_id} created! Parts: {parts} | Cost: ${cost:,.2f}")
                else:
                    st.warning(msg)

        # Health breakdown table
        st.markdown(f"""
        <div class="s-card" style="margin-top:14px;">
          <div class="s-card-title">▤ Prediction Breakdown</div>
          <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #21262D;">
            <span style="font-size:0.8rem;color:#8B949E;">Health Classification</span>
            <span style="font-size:0.8rem;font-weight:700;color:{accent_c};">{health_st}</span>
          </div>
          <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #21262D;">
            <span style="font-size:0.8rem;color:#8B949E;">Remaining Useful Life</span>
            <span style="font-size:0.8rem;font-weight:700;color:#00FF88;">{rul_val} hours</span>
          </div>
          <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #21262D;">
            <span style="font-size:0.8rem;color:#8B949E;">Health Score Index</span>
            <span style="font-size:0.8rem;font-weight:700;color:#00D9FF;">{h_score}%</span>
          </div>
          <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #21262D;">
            <span style="font-size:0.8rem;color:#8B949E;">Failure Probability</span>
            <span style="font-size:0.8rem;font-weight:700;color:#FF3B5C;">{f_prob}%</span>
          </div>
          <div style="display:flex;justify-content:space-between;padding:8px 0;">
            <span style="font-size:0.8rem;color:#8B949E;">Anomaly Detected</span>
            <span style="font-size:0.8rem;font-weight:700;color:{'#FF3B5C' if live_eval['is_anomaly'] else '#00FF88'};">{'YES' if live_eval['is_anomaly'] else 'NO'}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
#  PAGE: CMMS
# ════════════════════════════════════════════════════════
elif page == "CMMS":
    st.markdown("""
    <div style="padding-bottom:16px;border-bottom:1px solid #21262D;margin-bottom:20px;">
      <div style="font-size:1.35rem;font-weight:700;color:#E6EDF3;">▤ CMMS — Work Order Management</div>
      <div style="font-size:0.8rem;color:#8B949E;margin-top:3px;">Computerized Maintenance Management System — Full lifecycle tracking</div>
    </div>
    """, unsafe_allow_html=True)

    wos = cmms.get_work_orders()
    col_wl, col_wa = st.columns([1.5, 1.0], gap="medium")

    with col_wl:
        open_count = len(wos[wos["status"] == "Open"]) if not wos.empty else 0
        in_prog    = len(wos[wos["status"] == "In Progress"]) if not wos.empty else 0
        done_count = len(wos[wos["status"] == "Completed"]) if not wos.empty else 0

        w1, w2, w3 = st.columns(3)
        w1.metric("▫ Open", open_count)
        w2.metric("◈ In Progress", in_prog)
        w3.metric("✓ Completed", done_count)
        st.markdown('<div style="height:14px;"></div>', unsafe_allow_html=True)

        st.markdown('<div class="s-card"><div class="s-card-title">▤ Work Orders Log</div>', unsafe_allow_html=True)
        if not wos.empty:
            for _, row in wos.iterrows():
                p    = str(row.get("priority", ""))
                s    = str(row.get("status", ""))
                p_c  = priority_color(p)
                s_c  = status_color(s)
                st.markdown(f"""
<div class="wo-row">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
    <span class="wo-id-lbl">WO-{row.get('work_order_id','')}</span>
    <span style="font-size:0.7rem;font-weight:700;color:{p_c};background:rgba(0,0,0,0.3);padding:2px 8px;border-radius:5px;">{p}</span>
    <span style="font-size:0.7rem;font-weight:600;color:{s_c};">● {s}</span>
  </div>
  <div style="font-size:0.78rem;color:#CBD5E1;font-weight:500;">{row.get('crane_id','')} — {str(row.get('issue',''))[:55]}</div>
  <div style="font-size:0.7rem;color:#8B949E;margin-top:3px;">Parts: {str(row.get('assigned_parts','N/A'))[:40]} · Cost: ${float(row.get('total_cost',0)):,.0f}</div>
</div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#8B949E;padding:24px 0;text-align:center;">No work orders registered.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_wa:
        if not wos.empty:
            open_wos = wos[wos["status"].isin(["Open", "In Progress"])]
            if not open_wos.empty:
                st.markdown('<div class="s-card">', unsafe_allow_html=True)
                st.markdown('<div class="s-card-title">✓ Complete Work Order</div>', unsafe_allow_html=True)
                wo_sel    = st.selectbox("Select Work Order", open_wos["work_order_id"], label_visibility="visible")
                tech_     = st.text_input("Assigned Technician", value=st.session_state.user['name'])
                rep_hrs_  = st.number_input("Repair Time (hours)", min_value=0.5, max_value=48.0, value=2.5)
                findings_ = st.text_area("Findings & Root Cause", value="Bearing race wear detected. Replaced rollers.", height=80)
                actions_  = st.text_area("Actions Taken", value="Installed new bearing set, replaced oil filter.", height=80)
                if st.button("✓ Mark Completed & Update ERP"):
                    wo_row = wos[wos["work_order_id"] == wo_sel].iloc[0]
                    if pd.notna(wo_row["assigned_parts"]) and str(wo_row["assigned_parts"]).strip():
                        erp.release_parts(str(wo_row["assigned_parts"]))
                    cmms.update_work_order_status(wo_sel, "Completed", technician=tech_)
                    fbk.submit_feedback(wo_sel, wo_row["crane_id"], findings_, actions_, "Normal", rep_hrs_)
                    st.success(f"WO-{wo_sel} completed & feedback logged!")
                    time.sleep(0.7)
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)
        with st.expander("⊕ Create Manual Work Order"):
            with st.form("create_wo_form"):
                wo_c_id  = st.selectbox("Target Crane", crane_ids)
                wo_issue = st.selectbox("Fault Issue", list(erp.ISSUE_PARTS_MAPPING.keys()))
                wo_prio  = st.selectbox("Priority", ["Emergency", "High", "Medium", "Low"])
                wo_act   = st.selectbox("Action Type", ["Corrective Maintenance", "Preventive Maintenance", "Inspection & Repair"])
                submitted = st.form_submit_button("Submit Work Order")
                if submitted:
                    succ, parts, cost, msg = erp.check_and_reserve_parts(wo_issue)
                    wo_id = cmms.create_work_order(wo_c_id, wo_issue, wo_prio, wo_act, parts if succ else "None", cost if succ else 0.0, technician=st.session_state.user['name'])
                    st.success(f"Work Order WO-{wo_id} created!")
                    time.sleep(0.6)
                    st.rerun()


# ════════════════════════════════════════════════════════
#  PAGE: ERP INVENTORY
# ════════════════════════════════════════════════════════
elif page == "ERP Inventory":
    st.markdown("""
    <div style="padding-bottom:16px;border-bottom:1px solid #21262D;margin-bottom:20px;">
      <div style="font-size:1.35rem;font-weight:700;color:#E6EDF3;">⬢ ERP Spare Parts Inventory</div>
      <div style="font-size:0.8rem;color:#8B949E;margin-top:3px;">Auto-reserve, deduct &amp; reorder spare parts based on AI fault detection</div>
    </div>
    """, unsafe_allow_html=True)

    inv = erp.get_inventory()
    col_il, col_ir = st.columns([1.6, 1.0], gap="medium")

    with col_il:
        if not inv.empty:
            # Summary metrics
            i1, i2, i3 = st.columns(3)
            i1.metric("⬢ Total Parts", len(inv))
            i2.metric("▲ Low Stock", len(inv[inv["status"] == "Low Stock"]))
            i3.metric("◇ Inventory Value", f"${inv['unit_price'].sum():,.0f}")
            st.markdown('<div style="height:14px;"></div>', unsafe_allow_html=True)

            st.markdown('<div class="s-card"><div class="s-card-title">⬢ Spare Parts Stock Levels</div>', unsafe_allow_html=True)
            for _, row in inv.iterrows():
                stock    = int(row.get("stock_qty", 0))
                reserved = int(row.get("reserved_qty", 0))
                reorder  = int(row.get("reorder_level", 0))
                avail    = stock - reserved
                pct      = min(100, avail / max(stock + 5, 1) * 100)
                b_c      = "#FF3B5C" if avail <= reorder else ("#FFB800" if avail <= reorder * 2 else "#00FF88")
                st.markdown(f"""
<div class="inv-row">
  <div style="display:flex;align-items:flex-start;gap:14px;">
    <div style="flex:1.4;">
      <div style="font-size:0.83rem;font-weight:600;color:#CBD5E1;">{row.get('part_name','')}</div>
      <div style="font-size:0.7rem;color:#8B949E;margin-top:2px;">{row.get('category','')} · {row.get('part_number','')}</div>
    </div>
    <div style="min-width:100px;text-align:center;">
      <div style="font-size:1.2rem;font-weight:800;color:{b_c};">{avail}</div>
      <div style="font-size:0.65rem;color:#8B949E;">Available</div>
      <div style="height:3px;border-radius:3px;background:#21262D;margin-top:4px;">
        <div style="width:{pct:.0f}%;height:100%;border-radius:3px;background:{b_c};"></div>
      </div>
    </div>
    <div style="min-width:90px;text-align:center;">
      <div style="font-size:0.72rem;color:#8B949E;">{reserved} reserved</div>
      <div style="font-size:0.72rem;color:#8B949E;">Reorder @ {reorder}</div>
    </div>
    <div style="min-width:70px;text-align:right;font-size:0.82rem;font-weight:700;color:#00D9FF;">${row.get('unit_price',0):,.0f}</div>
  </div>
</div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with col_ir:
        low_stock = inv[inv["status"] == "Low Stock"] if not inv.empty else pd.DataFrame()
        if not low_stock.empty:
            st.error("▲ Low Stock Alert! Replenishment required.")
            for _, row in low_stock.iterrows():
                st.markdown(f"""
<div style="background:#161B22;border:1px solid rgba(255,59,92,0.25);border-radius:10px;padding:12px 14px;margin-bottom:8px;">
  <div style="font-size:0.83rem;font-weight:600;color:#FF3B5C;">{row.get('part_name','')}</div>
  <div style="font-size:0.71rem;color:#8B949E;margin-top:3px;">Stock: {row.get('stock_qty',0)} · Reorder Level: {row.get('reorder_level',0)}</div>
</div>
                """, unsafe_allow_html=True)
            reorder_id = st.selectbox("Part to Reorder", low_stock["spare_part_id"], label_visibility="visible")
            if st.button("⊕ Reorder +10 Units"):
                erp.reorder_part(reorder_id, 10)
                st.success("Reorder processed!")
                time.sleep(0.6)
                st.rerun()
        else:
            st.success("✓ All parts are well-stocked.")


# ════════════════════════════════════════════════════════
#  PAGE: CLOSED-LOOP
# ════════════════════════════════════════════════════════
elif page == "Closed-Loop":
    st.markdown("""
    <div style="padding-bottom:16px;border-bottom:1px solid #21262D;margin-bottom:20px;">
      <div style="font-size:1.35rem;font-weight:700;color:#E6EDF3;">↻ Closed-Loop Feedback & AI Retraining</div>
      <div style="font-size:0.8rem;color:#8B949E;margin-top:3px;">Chapter 7.4 — Technician feedback → model retraining → improved predictions</div>
    </div>
    """, unsafe_allow_html=True)

    col_fb1, col_fb2 = st.columns(2, gap="medium")

    with col_fb1:
        st.markdown('<div class="section-label" style="margin-bottom:10px;">▤ Maintenance Feedback Log</div>', unsafe_allow_html=True)
        fb_df = fbk.get_feedback()
        if not fb_df.empty:
            st.dataframe(fb_df, width="stretch")
        else:
            st.info("No feedback submitted yet. Complete a work order to log technician findings.")

    with col_fb2:
        st.markdown('<div class="section-label" style="margin-bottom:10px;">⚙ AI Retraining Engine</div>', unsafe_allow_html=True)
        st.markdown("""
<div class="s-card">
  <div class="s-card-title">How Closed-Loop Learning Works</div>
  <div style="font-size:0.82rem;color:#8B949E;line-height:1.7;">
    Technician feedback (actual fault types, repair time, post-maintenance condition) is fed back into the AI pipeline. The models are retrained on enriched data, improving prediction accuracy with each maintenance cycle.
  </div>
</div>
        """, unsafe_allow_html=True)

        if st.button("⚙ Trigger AI Model Retraining Loop", type="primary"):
            with st.spinner("Retraining AI models on updated data..."):
                score = retrain_engine.train_or_retrain_models()
            st.success(f"Retraining complete! Score: {score}")
            time.sleep(0.5)
            st.rerun()

        st.markdown('<div style="height:14px;"></div><div class="section-label" style="margin-bottom:10px;">▤ Retraining Audit Log</div>', unsafe_allow_html=True)
        ret_path = os.path.join(ROOT_DIR, "model_retraining.csv")
        if os.path.exists(ret_path):
            ret_df = pd.read_csv(ret_path)
            for _, row in ret_df.iterrows():
                st.markdown(f"""
<div class="s-card" style="margin-bottom:8px;padding:12px 14px;">
  <div style="display:flex;justify-content:space-between;align-items:center;">
    <span style="font-size:0.78rem;font-weight:700;color:#00D9FF;font-family:'JetBrains Mono',monospace;">{row.get('retrain_id','')}</span>
    <span style="font-size:0.68rem;color:#8B949E;">{row.get('retrain_date','')}</span>
  </div>
  <div style="font-size:0.75rem;color:#CBD5E1;margin-top:4px;">{row.get('model_version','')} · {row.get('performance_score','')}</div>
</div>
                """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
#  PAGE: REPORTS
# ════════════════════════════════════════════════════════
elif page == "Reports":
    st.markdown("""
    <div style="padding-bottom:16px;border-bottom:1px solid #21262D;margin-bottom:20px;">
      <div style="font-size:1.35rem;font-weight:700;color:#E6EDF3;">▧ Reports & Data Export</div>
      <div style="font-size:0.8rem;color:#8B949E;margin-top:3px;">Download raw datasets and generate printable HTML/PDF summary reports</div>
    </div>
    """, unsafe_allow_html=True)

    col_r1, col_r2 = st.columns(2, gap="medium")

    with col_r1:
        st.markdown('<div class="s-card"><div class="s-card-title">⬡ Download Raw Data (CSV)</div>', unsafe_allow_html=True)
        ret_df_r = pd.read_csv(os.path.join(ROOT_DIR, "model_retraining.csv")) if os.path.exists(os.path.join(ROOT_DIR, "model_retraining.csv")) else pd.DataFrame()
        downloads = [
            ("⚙ Crane Fleet Data",             cranes_df,                  "cranes.csv"),
            ("◈ Sensor Telemetry (last 200)",   sensor_df.tail(200) if not sensor_df.empty else pd.DataFrame(), "sensor_data.csv"),
            ("▤ CMMS Work Orders",              cmms.get_work_orders(),     "work_orders.csv"),
            ("⬢ ERP Spare Parts Inventory",     erp.get_inventory(),        "spare_parts.csv"),
            ("↻ Technician Feedback Log",       fbk.get_feedback(),         "maintenance_feedback.csv"),
            ("⚙ AI Retraining History",         ret_df_r,                   "model_retraining.csv"),
        ]
        for label, df_dl, fname in downloads:
            if not df_dl.empty:
                st.download_button(label, df_dl.to_csv(index=False), fname, "text/csv")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r2:
        st.markdown('<div class="s-card"><div class="s-card-title">▧ Summary Report Generator</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.82rem;color:#8B949E;margin-bottom:14px;line-height:1.6;">Generate a formatted HTML report covering fleet status, CMMS work orders, ERP inventory &amp; AI retraining history. Printable as PDF from your browser.</div>', unsafe_allow_html=True)
        if st.button("▤ Generate Full Summary Report"):
            wo_df_r  = cmms.get_work_orders()
            inv_df_r = erp.get_inventory()
            html_rpt = rpt.generate_pdf_summary_html(cranes_df, wo_df_r, inv_df_r, ret_df_r)
            st.download_button("⇩ Download HTML Report", html_rpt, "Digital_Twin_Port_Crane_Report.html", "text/html")
            st.components.v1.html(html_rpt, height=420, scrolling=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
#  PAGE: USERS
# ════════════════════════════════════════════════════════
elif page == "Users":
    st.markdown("""
    <div style="padding-bottom:16px;border-bottom:1px solid #21262D;margin-bottom:20px;">
      <div style="font-size:1.35rem;font-weight:700;color:#E6EDF3;">⊙ User & Access Control</div>
      <div style="font-size:0.8rem;color:#8B949E;margin-top:3px;">Role-based permissions management (FR-01 &amp; FR-10)</div>
    </div>
    """, unsafe_allow_html=True)

    col_u1, col_u2 = st.columns([1.3, 1.0], gap="medium")

    with col_u1:
        users_df = auth.get_all_users()
        st.markdown('<div class="s-card"><div class="s-card-title">⊙ Registered Users</div>', unsafe_allow_html=True)
        if not users_df.empty:
            role_colors = {"Administrator": "#FF3B5C", "Maintenance Engineer": "#FFB800", "Reliability Engineer": "#A855F7", "Port Operations Planner": "#00D9FF"}
            for _, row in users_df.iterrows():
                rc = role_colors.get(row.get("role", ""), "#8B949E")
                st.markdown(f"""
<div style="display:flex;align-items:center;gap:12px;padding:11px 0;border-bottom:1px solid #21262D;">
  <div style="width:34px;height:34px;border-radius:50%;background:rgba(0,217,255,0.1);display:flex;align-items:center;justify-content:center;font-size:0.95rem;flex-shrink:0;color:#00D9FF;">⊙</div>
  <div style="flex:1;">
    <div style="font-size:0.83rem;font-weight:600;color:#CBD5E1;">{row.get('name','')}</div>
    <div style="font-size:0.7rem;color:#8B949E;margin-top:2px;">{row.get('email','')}</div>
  </div>
  <div style="font-size:0.7rem;font-weight:700;padding:3px 10px;border-radius:6px;background:rgba(0,0,0,0.25);color:{rc};border:1px solid {rc}55;">{row.get('role','')}</div>
  <div style="font-size:0.7rem;color:#00FF88;flex-shrink:0;">● {row.get('status','Active')}</div>
</div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_u2:
        st.markdown('<div class="s-card"><div class="s-card-title">◈ Role Permission Matrix</div>', unsafe_allow_html=True)
        role_colors = {"Administrator": "#FF3B5C", "Maintenance Engineer": "#FFB800", "Reliability Engineer": "#A855F7", "Port Operations Planner": "#00D9FF"}
        for role, perms in auth.ROLE_PERMISSIONS.items():
            rc = role_colors.get(role, "#8B949E")
            perms_html = " ".join([f'<span style="background:rgba(0,217,255,0.07);border:1px solid rgba(0,217,255,0.18);border-radius:4px;padding:2px 7px;font-size:0.67rem;color:#8B949E;display:inline-block;margin:2px;">{p}</span>' for p in perms])
            st.markdown(f"""
<div style="padding:12px 0;border-bottom:1px solid #21262D;">
  <div style="font-size:0.8rem;font-weight:700;color:{rc};margin-bottom:7px;">{role}</div>
  <div style="line-height:2.2;">{perms_html}</div>
</div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
