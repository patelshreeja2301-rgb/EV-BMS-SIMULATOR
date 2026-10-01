import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import math

# =========================================================
# VOLTGUARD BMS - SINGLE PAGE EV BATTERY SIMULATOR
# =========================================================

st.set_page_config(
    page_title="VoltGuard BMS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- CSS --------------------

st.markdown("""
<style>
/* Hide Streamlit's built-in top toolbar / Deploy / menu */
[data-testid="stToolbar"] {
    display: none !important;
}
/* Hide Streamlit menu and footer, but KEEP header/sidebar toggle visible */

[data-testid="stToolbar"] {
    display: none !important;
}

#MainMenu {
    display: none !important;
}

footer {
    display: none !important;
}

/* Keep Streamlit header visible so sidebar can be opened again */
header {
    visibility: visible !important;
    display: block !important;
}

/* Keep the dashboard itself fully visible */
html { scroll-behavior: smooth; }

.stApp {
    background: #f6f9fc;
    color: #17324d;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.2rem;
    padding-bottom: 3rem;
}

section[data-testid="stSidebar"] {
    background: #eef3f8;
    border-right: 1px solid #d7e1eb;
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 1.2rem;
}

.nav-title {
    color: #6a7c8f;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.2px;
    margin: 18px 0 9px 2px;
}

.nav-link {
    display: block;
    text-decoration: none !important;
    color: #17324d !important;
    background: #ffffff;
    border: 1px solid #d9e3ec;
    border-radius: 11px;
    padding: 11px 13px;
    margin: 7px 0;
    font-weight: 700;
}

.nav-link:hover {
    background: #eaf5ff;
    border-color: #74add1;
    color: #086a9e !important;
}

.hero {
    background: linear-gradient(120deg, #102f50, #174f7d);
    border-radius: 22px;
    padding: 30px 34px;
    color: white;
    box-shadow: 0 10px 30px rgba(16,47,80,.13);
}

.hero h1 {
    margin: 0;
    color: white;
    font-size: 38px;
}

.hero p {
    margin: 8px 0 0;
    color: #d4e2ef;
    font-size: 16px;
}

.online {
    margin-top: 18px;
    color: #48e0a5;
    font-weight: 800;
}

.section {
    scroll-margin-top: 20px;
    margin-top: 35px;
}

.section-title {
    color: #102f50;
    font-size: 25px;
    font-weight: 850;
    margin: 0 0 14px;
}

.section-sub {
    color: #6b7d90;
    margin-top: -7px;
    margin-bottom: 18px;
}

.metric-card {
    background: white;
    border: 1px solid #dce5ed;
    border-radius: 16px;
    padding: 20px;
    min-height: 128px;
    box-shadow: 0 5px 18px rgba(20,45,70,.07);
}

.metric-label {
    color: #6a7c8f;
    font-size: 13px;
    font-weight: 750;
}

.metric-value {
    color: #102f50;
    font-size: 31px;
    font-weight: 850;
    margin-top: 10px;
}

.metric-note {
    color: #8797a8;
    font-size: 12px;
    margin-top: 5px;
}

.panel {
    background: white;
    border: 1px solid #dce5ed;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 5px 18px rgba(20,45,70,.06);
}

.status-normal {
    background: #eaf8f2;
    border: 1px solid #9ddcc2;
    color: #08764d;
    border-radius: 14px;
    padding: 17px;
    text-align: center;
    font-size: 21px;
    font-weight: 850;
}

.status-danger {
    background: #fff0f0;
    border: 1px solid #efa7a7;
    color: #b42318;
    border-radius: 14px;
    padding: 17px;
    text-align: center;
    font-size: 21px;
    font-weight: 850;
}

.status-warning {
    background: #fff7e8;
    border: 1px solid #f1c66f;
    color: #925b00;
    border-radius: 14px;
    padding: 17px;
    text-align: center;
    font-size: 21px;
    font-weight: 850;
}

.info-row {
    background: #f7f9fc;
    border: 1px solid #e1e8ef;
    border-radius: 10px;
    padding: 12px 14px;
    margin: 7px 0;
    color: #526579;
}

.cell-card {
    background: white;
    border: 1px solid #d8e4ee;
    border-radius: 12px;
    padding: 13px 5px;
    text-align: center;
    box-shadow: 0 3px 10px rgba(20,45,70,.05);
}

.cell-name {
    color: #53687d;
    font-size: 12px;
    font-weight: 800;
}

.cell-value {
    color: #123b5c;
    font-size: 18px;
    font-weight: 850;
    margin-top: 5px;
}

.step-card {
    background: white;
    border: 1px solid #dce5ed;
    border-radius: 15px;
    padding: 17px;
    min-height: 150px;
    box-shadow: 0 4px 14px rgba(20,45,70,.05);
}

.step-number {
    width: 31px;
    height: 31px;
    line-height: 31px;
    text-align: center;
    border-radius: 50%;
    background: #123c5e;
    color: white;
    font-weight: 850;
    margin-bottom: 10px;
}

.step-title {
    color: #17324d;
    font-weight: 850;
    font-size: 15px;
}

.step-text {
    color: #718397;
    font-size: 12px;
    line-height: 1.55;
    margin-top: 5px;
}

.tech-box {
    background: white;
    border: 1px solid #dce5ed;
    border-radius: 14px;
    padding: 18px;
    text-align: center;
    min-height: 110px;
    box-shadow: 0 4px 14px rgba(20,45,70,.05);
}

.tech-icon {
    font-size: 26px;
}

.tech-name {
    color: #17324d;
    font-weight: 850;
    margin-top: 7px;
}

.tech-desc {
    color: #7b8b9c;
    font-size: 11px;
    margin-top: 4px;
}

.event {
    background: white;
    border-left: 4px solid #1a9b73;
    border-top: 1px solid #dce5ed;
    border-right: 1px solid #dce5ed;
    border-bottom: 1px solid #dce5ed;
    border-radius: 9px;
    padding: 11px 13px;
    margin: 7px 0;
    color: #4d6074;
}

.footer {
    text-align: center;
    color: #8a98a7;
    font-size: 12px;
    padding: 40px 0 15px;
}

.stButton > button {
    border-radius: 10px !important;
    min-height: 44px !important;
    font-weight: 750 !important;
    border: 1px solid #ccd9e4 !important;
    background: white !important;
    color: #17324d !important;
}

.stButton > button:hover {
    border-color: #5d9fc6 !important;
    background: #edf7fd !important;
    color: #075f91 !important;
}

div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #dce5ed;
    padding: 12px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# -------------------- STATE --------------------

if "soc" not in st.session_state:
    st.session_state.soc = 50.0
if "voltage" not in st.session_state:
    st.session_state.voltage = 50.0
if "current" not in st.session_state:
    st.session_state.current = 0.0
if "temperature" not in st.session_state:
    st.session_state.temperature = 36.5
if "mode" not in st.session_state:
    st.session_state.mode = "IDLE"
if "soh" not in st.session_state:
    st.session_state.soh = 96.0
if "cycles" not in st.session_state:
    st.session_state.cycles = 128
if "fault" not in st.session_state:
    st.session_state.fault = "NONE"
if "history" not in st.session_state:
    st.session_state.history = []
if "events" not in st.session_state:
    st.session_state.events = [
        "System initialized",
        "BMS monitoring enabled"
    ]

# -------------------- HELPERS --------------------

def event(message):
    stamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.events.insert(0, f"{stamp}  •  {message}")
    st.session_state.events = st.session_state.events[:15]

def record():
    st.session_state.history.append({
        "Time": datetime.now().strftime("%H:%M:%S"),
        "SOC (%)": round(st.session_state.soc, 1),
        "Voltage (V)": round(st.session_state.voltage, 2),
        "Current (A)": round(st.session_state.current, 1),
        "Temperature (°C)": round(st.session_state.temperature, 1),
        "Mode": st.session_state.mode
    })
    st.session_state.history = st.session_state.history[-100:]

def bms_status():
    if st.session_state.fault != "NONE":
        return st.session_state.fault
    if st.session_state.voltage > 52:
        return "OVER-VOLTAGE"
    if st.session_state.voltage < 48:
        return "UNDER-VOLTAGE"
    if st.session_state.current > 30:
        return "OVER-CURRENT"
    if st.session_state.temperature > 60:
        return "OVERHEATING"
    return "NORMAL"

def reset():
    st.session_state.soc = 50.0
    st.session_state.voltage = 50.0
    st.session_state.current = 0.0
    st.session_state.temperature = 36.5
    st.session_state.mode = "IDLE"
    st.session_state.fault = "NONE"
    st.session_state.history = []
    event("System reset to normal operating state")

def charge():
    st.session_state.fault = "NONE"
    st.session_state.mode = "CHARGING"
    st.session_state.current = 10.0

    if st.session_state.soc < 100:
        st.session_state.soc = min(100, st.session_state.soc + 5)
        st.session_state.voltage = 48 + st.session_state.soc * 0.04
        st.session_state.temperature = min(60, st.session_state.temperature + 0.2)

    if st.session_state.soc >= 100:
        st.session_state.mode = "FULL"
        st.session_state.current = 0
        event("Battery reached 100% SOC")

    record()

def drive():
    st.session_state.fault = "NONE"
    st.session_state.mode = "DRIVING"
    st.session_state.current = 20.0

    if st.session_state.soc > 0:
        st.session_state.soc = max(0, st.session_state.soc - 5)
        st.session_state.voltage = 48 + st.session_state.soc * 0.04
        st.session_state.temperature = min(60, st.session_state.temperature + 0.35)

    if st.session_state.soc <= 0:
        st.session_state.mode = "EMPTY"
        st.session_state.current = 0
        event("Battery reached 0% SOC")

    record()

def stop():
    st.session_state.mode = "IDLE"
    st.session_state.current = 0
    event("Simulation stopped")
    record()

def fault_over_voltage():
    st.session_state.mode = "FAULT TEST"
    st.session_state.fault = "OVER-VOLTAGE"
    st.session_state.voltage = 55.0
    st.session_state.current = 20.0
    event("BMS detected simulated OVER-VOLTAGE")
    record()

def fault_over_current():
    st.session_state.mode = "FAULT TEST"
    st.session_state.fault = "OVER-CURRENT"
    st.session_state.voltage = 50.0
    st.session_state.current = 45.0
    event("BMS detected simulated OVER-CURRENT")
    record()

def fault_overheat():
    st.session_state.mode = "FAULT TEST"
    st.session_state.fault = "OVERHEATING"
    st.session_state.voltage = 50.0
    st.session_state.current = 20.0
    st.session_state.temperature = 68.0
    event("BMS detected simulated OVERHEATING")
    record()

def clear_fault():
    st.session_state.fault = "NONE"
    st.session_state.mode = "IDLE"
    st.session_state.voltage = 50.0
    st.session_state.current = 0.0
    st.session_state.temperature = 36.5
    event("Fault cleared - system returned to normal")
    record()

# -------------------- SIDEBAR --------------------

with st.sidebar:
    st.markdown("## ⚡ VOLTGUARD")
    st.caption("EV BATTERY & BMS SIMULATOR")

    st.markdown('<div class="nav-title">PROJECT NAVIGATION</div>',
                unsafe_allow_html=True)

    # Same-page anchor navigation. No radio buttons and no separate pages.
    links = [
        ("🏠  Dashboard", "#dashboard"),
        ("🔋  Battery Monitor", "#battery"),
        ("🛡️  BMS Protection", "#bms"),
        ("⚡  Energy & Range", "#energy"),
        ("📊  Analytics", "#analytics"),
        ("⚠️  Event Log", "#events"),
        ("ℹ️  Project Info", "#about"),
    ]

    for label, target in links:
        st.markdown(
            f'<a class="nav-link" href="{target}">{label}</a>',
            unsafe_allow_html=True
        )

    st.divider()

    status = bms_status()
    if status == "NORMAL":
        st.success("SYSTEM NORMAL")
    else:
        st.error(f"BMS ALERT\n\n{status}")

    st.caption(f"Mode: {st.session_state.mode}")
    st.caption(f"SOC: {st.session_state.soc:.0f}%")

# -------------------- HERO --------------------

st.markdown('<div id="dashboard" class="section"></div>',
            unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>⚡ VOLTGUARD BMS</h1>
    <p>Electric Vehicle Battery Management & Monitoring System</p>
    <div class="online">● SYSTEM ONLINE</div>
</div>
""", unsafe_allow_html=True)

st.write("")

# -------------------- LIVE OVERVIEW --------------------

st.markdown('<div class="section-title">LIVE BATTERY OVERVIEW</div>',
            unsafe_allow_html=True)

a, b, c, d = st.columns(4)

with a:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🔋 STATE OF CHARGE</div>
        <div class="metric-value">{st.session_state.soc:.0f}%</div>
        <div class="metric-note">Available battery capacity</div>
    </div>
    """, unsafe_allow_html=True)

with b:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">⚡ PACK VOLTAGE</div>
        <div class="metric-value">{st.session_state.voltage:.2f} V</div>
        <div class="metric-note">Present battery voltage</div>
    </div>
    """, unsafe_allow_html=True)

with c:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🔌 CURRENT</div>
        <div class="metric-value">{st.session_state.current:.1f} A</div>
        <div class="metric-note">Charge / discharge current</div>
    </div>
    """, unsafe_allow_html=True)

with d:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🌡️ TEMPERATURE</div>
        <div class="metric-value">{st.session_state.temperature:.1f} °C</div>
        <div class="metric-note">Battery thermal condition</div>
    </div>
    """, unsafe_allow_html=True)

# -------------------- SIMULATION CONTROLS --------------------

st.markdown('<div class="section-title">🎛️ SIMULATION CONTROLS</div>',
            unsafe_allow_html=True)
st.markdown('<div class="section-sub">Use these controls to demonstrate the complete battery operating cycle.</div>',
            unsafe_allow_html=True)

q1, q2, q3, q4 = st.columns(4)

with q1:
    if st.button("🔌  CHARGE BATTERY", use_container_width=True):
        charge()
        st.rerun()

with q2:
    if st.button("🚗  RUN VEHICLE", use_container_width=True):
        drive()
        st.rerun()

with q3:
    if st.button("⛔  STOP SIMULATION", use_container_width=True):
        stop()
        st.rerun()

with q4:
    if st.button("🔄  RESET SYSTEM", use_container_width=True):
        reset()
        st.rerun()

# -------------------- BATTERY MONITOR --------------------

st.markdown('<div id="battery" class="section"></div>',
            unsafe_allow_html=True)

st.markdown('<div class="section-title">🔋 BATTERY MONITOR</div>',
            unsafe_allow_html=True)
st.markdown('<div class="section-sub">Live electrical and thermal condition of the simulated battery.</div>',
            unsafe_allow_html=True)

m1, m2 = st.columns([1, 1])

with m1:
    st.markdown('<div class="panel"><b>STATE OF CHARGE</b></div>',
                unsafe_allow_html=True)
    st.progress(int(st.session_state.soc))
    st.markdown(f"### {st.session_state.soc:.0f}%")
    st.caption("SOC represents the estimated remaining charge.")

with m2:
    st.markdown('<div class="panel"><b>OPERATING PARAMETERS</b></div>',
                unsafe_allow_html=True)

    rows = [
        ("Battery Capacity", "100 Ah"),
        ("Nominal Voltage", "48 V"),
        ("Maximum Voltage", "52 V"),
        ("Maximum Current", "30 A"),
        ("Maximum Temperature", "60 °C"),
        ("Battery SOH", f"{st.session_state.soh:.1f}%"),
        ("Charge Cycles", str(st.session_state.cycles)),
        ("Operating Mode", st.session_state.mode)
    ]

    for name, value in rows:
        st.markdown(
            f'<div class="info-row"><b>{name}</b><span style="float:right;color:#17324d;font-weight:800">{value}</span></div>',
            unsafe_allow_html=True
        )

# -------------------- 12 CELL PACK --------------------

st.markdown('<div class="section-title">🔋 12-CELL BATTERY PACK</div>',
            unsafe_allow_html=True)
st.markdown(
    '<div class="section-sub">Each cell is monitored individually. Small voltage differences are intentionally shown to demonstrate cell balancing and pack monitoring.</div>',
    unsafe_allow_html=True
)

base = st.session_state.voltage / 12.0

# Different cell readings instead of repeating the same value.
offsets = [-0.018, 0.012, -0.009, 0.021, -0.006, 0.008,
           -0.014, 0.016, -0.004, 0.011, -0.012, -0.005]

cell_values = [base + x for x in offsets]

# In a fault test, show one clearly abnormal cell.
if st.session_state.fault == "OVER-VOLTAGE":
    cell_values[8] = 4.85
elif st.session_state.fault == "OVERHEATING":
    cell_values[5] = base
elif st.session_state.fault == "OVER-CURRENT":
    cell_values[2] = base

cell_cols = st.columns(6)

for i, value in enumerate(cell_values):
    with cell_cols[i % 6]:
        st.markdown(f"""
        <div class="cell-card">
            <div class="cell-name">CELL {i+1}</div>
            <div class="cell-value">{value:.3f} V</div>
        </div>
        """, unsafe_allow_html=True)

st.write("")

cv1, cv2, cv3 = st.columns(3)

with cv1:
    st.metric("Minimum Cell", f"{min(cell_values):.3f} V")

with cv2:
    st.metric("Maximum Cell", f"{max(cell_values):.3f} V")

with cv3:
    st.metric("Cell Imbalance", f"{max(cell_values)-min(cell_values):.3f} V")

# -------------------- BMS PROTECTION --------------------

st.markdown('<div id="bms" class="section"></div>',
            unsafe_allow_html=True)

st.markdown('<div class="section-title">🛡️ BMS PROTECTION CENTER</div>',
            unsafe_allow_html=True)
st.markdown(
    '<div class="section-sub">The virtual BMS checks voltage, current, temperature and SOC and raises a protection event when a limit is crossed.</div>',
    unsafe_allow_html=True
)

status = bms_status()

if status == "NORMAL":
    st.markdown("""
    <div class="status-normal">
        🟢 BMS STATUS: NORMAL
        <div style="font-size:13px;font-weight:500;margin-top:5px">
        All monitored parameters are within the configured limits.
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="status-danger">
        🔴 BMS PROTECTION: {status}
        <div style="font-size:13px;font-weight:500;margin-top:5px">
        Abnormal condition detected. Demonstration fault is active.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# -------------------- FAULT LAB --------------------

st.markdown("### ⚠️ Fault Demonstration Lab")
st.caption("Click any test once. The dashboard will immediately show the abnormal value and BMS response.")

f1, f2, f3, f4 = st.columns(4)

with f1:
    if st.button("⚡ TEST OVER-VOLTAGE", use_container_width=True):
        fault_over_voltage()
        st.rerun()

with f2:
    if st.button("🔌 TEST OVER-CURRENT", use_container_width=True):
        fault_over_current()
        st.rerun()

with f3:
    if st.button("🌡️ TEST OVERHEATING", use_container_width=True):
        fault_overheat()
        st.rerun()

with f4:
    if st.button("✅ CLEAR ACTIVE FAULT", use_container_width=True):
        clear_fault()
        st.rerun()

if status != "NORMAL":
    if status == "OVER-VOLTAGE":
        st.error(f"OVER-VOLTAGE DETECTED  |  Voltage = {st.session_state.voltage:.1f} V  |  Limit = 52 V")
    elif status == "OVER-CURRENT":
        st.error(f"OVER-CURRENT DETECTED  |  Current = {st.session_state.current:.1f} A  |  Limit = 30 A")
    elif status == "OVERHEATING":
        st.error(f"OVERHEATING DETECTED  |  Temperature = {st.session_state.temperature:.1f} °C  |  Limit = 60 °C")

st.write("")

p1, p2, p3, p4 = st.columns(4)

with p1:
    st.metric("Voltage Protection", "SAFE" if st.session_state.voltage <= 52 else "TRIPPED")

with p2:
    st.metric("Current Protection", "SAFE" if st.session_state.current <= 30 else "TRIPPED")

with p3:
    st.metric("Thermal Protection", "SAFE" if st.session_state.temperature <= 60 else "TRIPPED")

with p4:
    st.metric("SOC Protection", "SAFE" if 0 <= st.session_state.soc <= 100 else "TRIPPED")

# -------------------- ENERGY & RANGE --------------------

st.markdown('<div id="energy" class="section"></div>',
            unsafe_allow_html=True)

st.markdown('<div class="section-title">⚡ ENERGY & RANGE</div>',
            unsafe_allow_html=True)
st.markdown(
    '<div class="section-sub">A simple energy model converts battery capacity and SOC into available energy and an estimated driving range.</div>',
    unsafe_allow_html=True
)

total_energy = 48 * 100 / 1000
available_energy = total_energy * st.session_state.soc / 100
power_kw = abs(st.session_state.voltage * st.session_state.current) / 1000
consumption = 0.12
range_km = available_energy / consumption

e1, e2, e3, e4 = st.columns(4)

with e1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🔋 PACK ENERGY</div>
        <div class="metric-value">{total_energy:.2f} kWh</div>
        <div class="metric-note">Nominal stored energy</div>
    </div>
    """, unsafe_allow_html=True)

with e2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">⚡ AVAILABLE ENERGY</div>
        <div class="metric-value">{available_energy:.2f} kWh</div>
        <div class="metric-note">Based on current SOC</div>
    </div>
    """, unsafe_allow_html=True)

with e3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">📈 POWER</div>
        <div class="metric-value">{power_kw:.2f} kW</div>
        <div class="metric-note">Voltage × current</div>
    </div>
    """, unsafe_allow_html=True)

with e4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🚗 ESTIMATED RANGE</div>
        <div class="metric-value">{range_km:.1f} km</div>
        <div class="metric-note">Using 120 Wh/km model</div>
    </div>
    """, unsafe_allow_html=True)

st.progress(int(st.session_state.soc))
st.caption(f"Energy available: {available_energy:.2f} kWh  •  Estimated range: {range_km:.1f} km")

# -------------------- ANALYTICS --------------------

st.markdown('<div id="analytics" class="section"></div>',
            unsafe_allow_html=True)

st.markdown('<div class="section-title">📊 BATTERY ANALYTICS</div>',
            unsafe_allow_html=True)
st.markdown(
    '<div class="section-sub">Recorded readings can be reviewed as trends instead of only single values.</div>',
    unsafe_allow_html=True
)

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)

    tabs = st.tabs(["SOC Trend", "Voltage Trend", "Current Trend", "Temperature Trend"])

    configs = [
        ("SOC (%)", "State of Charge", "#16845f"),
        ("Voltage (V)", "Battery Voltage", "#147cae"),
        ("Current (A)", "Battery Current", "#d07a16"),
        ("Temperature (°C)", "Battery Temperature", "#c24f68")
    ]

    for tab, (col, title, color) in zip(tabs, configs):
        with tab:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                y=df[col],
                x=list(range(1, len(df) + 1)),
                mode="lines+markers",
                line=dict(color=color, width=3),
                marker=dict(size=6)
            ))
            fig.update_layout(
                title=title,
                height=350,
                paper_bgcolor="white",
                plot_bgcolor="#f7f9fc",
                font=dict(color="#17324d"),
                xaxis_title="Reading",
                yaxis_title=col,
                margin=dict(l=30, r=20, t=55, b=35)
            )
            st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Run CHARGE or RUN VEHICLE to generate live readings and graphs.")

# -------------------- DATA --------------------

st.markdown('<div class="section-title">📋 DATA LOG</div>',
            unsafe_allow_html=True)

if st.session_state.history:
    data = pd.DataFrame(st.session_state.history)
    st.dataframe(data, use_container_width=True, hide_index=True)

    st.download_button(
        "⬇️ DOWNLOAD BATTERY DATA (CSV)",
        data=data.to_csv(index=False),
        file_name="battery_data.csv",
        mime="text/csv",
        use_container_width=True
    )
else:
    st.info("No readings recorded yet.")

# -------------------- EVENT LOG --------------------

st.markdown('<div id="events" class="section"></div>',
            unsafe_allow_html=True)

st.markdown('<div class="section-title">⚠️ EVENT LOG</div>',
            unsafe_allow_html=True)

for item in st.session_state.events:
    st.markdown(f'<div class="event">● {item}</div>',
                unsafe_allow_html=True)

# -------------------- PROJECT INFO --------------------

st.markdown('<div id="about" class="section"></div>',
            unsafe_allow_html=True)

st.markdown('<div class="section-title">ℹ️ PROJECT ARCHITECTURE</div>',
            unsafe_allow_html=True)

st.markdown(
    '<div class="section-sub">This is the actual working logic of the project, from battery model to BMS decision and data visualization.</div>',
    unsafe_allow_html=True
)

steps = [
    ("01", "Battery Model", "Defines capacity, voltage, SOC and thermal parameters."),
    ("02", "Simulation Engine", "Updates charging and discharging behaviour."),
    ("03", "Sensor Layer", "Provides simulated voltage, current and temperature readings."),
    ("04", "BMS Logic", "Compares readings with safety limits."),
    ("05", "Protection", "Detects abnormal conditions and raises faults."),
    ("06", "Analytics", "Stores readings and converts them into useful trends."),
    ("07", "Dashboard", "Presents the complete system in one interactive interface.")
]

cols = st.columns(4)

for i, (num, title, desc) in enumerate(steps):
    with cols[i % 4]:
        st.markdown(f"""
        <div class="step-card">
            <div class="step-number">{num}</div>
            <div class="step-title">{title}</div>
            <div class="step-text">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.write("")

st.markdown("### 🧩 Technology Stack")

tech = [
    ("🐍", "Python", "Simulation logic"),
    ("🖥️", "Streamlit", "Interactive dashboard"),
    ("📊", "Pandas", "Battery data logging"),
    ("📈", "Plotly", "Interactive graphs"),
    ("💾", "CSV", "Data export")
]

tcols = st.columns(5)

for col, (icon, name, desc) in zip(tcols, tech):
    with col:
        st.markdown(f"""
        <div class="tech-box">
            <div class="tech-icon">{icon}</div>
            <div class="tech-name">{name}</div>
            <div class="tech-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.write("")
st.success(
    "SOFTWARE PROJECT  •  NO HARDWARE REQUIRED  •  NO AI/ML REQUIRED"
)

st.markdown("""
<div class="footer">
    ⚡ VOLTGUARD BMS<br>
    EV BATTERY MANAGEMENT & MONITORING SYSTEM<br><br>
    Interactive software simulation project
</div>
""", unsafe_allow_html=True)
