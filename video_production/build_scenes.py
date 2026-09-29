import os

SCENES_DIR = r"E:\Niyan\video_production\scenes"
os.makedirs(SCENES_DIR, exist_ok=True)

# Shared CSS styles
COMMON_STYLE = """
:root {
  --bg: #07090e;
  --surface: #0e131f;
  --surface-raised: #151d2e;
  --border: #1f2b42;
  --border-subtle: #172033;
  --text-primary: #f8fafc;
  --text-secondary: #94a3b8;
  --text-muted: #64748b;
  --accent: #0284c7;
  --accent-light: #38bdf8;
  --accent-glow: rgba(56, 189, 248, 0.25);
  --success: #10b981;
  --warning: #f59e0b;
  --danger: #ef4444;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  width: 1920px;
  height: 1080px;
  overflow: hidden;
  background: var(--bg);
  color: var(--text-primary);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Inter", Helvetica, Arial, sans-serif;
  display: flex;
  flex-direction: column;
  position: relative;
  user-select: none;
}

/* Background Grid Pattern */
.bg-grid {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  background-image: 
    linear-gradient(to right, rgba(31, 43, 66, 0.3) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(31, 43, 66, 0.3) 1px, transparent 1px);
  background-size: 60px 60px;
  pointer-events: none;
  z-index: 1;
}

.glow-ambient {
  position: absolute;
  top: -20%; left: 30%; width: 800px; height: 800px;
  background: radial-gradient(circle, rgba(2, 132, 199, 0.12) 0%, transparent 70%);
  filter: blur(80px);
  pointer-events: none;
  z-index: 1;
}

/* Top Navigation Bar */
.top-header {
  height: 72px;
  background: rgba(14, 19, 31, 0.95);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
  z-index: 10;
  backdrop-filter: blur(12px);
}

.brand-section {
  display: flex;
  align-items: center;
  gap: 16px;
}

.logo-badge {
  background: linear-gradient(135deg, #0284c7, #38bdf8);
  color: #07090e;
  font-weight: 900;
  font-size: 22px;
  letter-spacing: 2px;
  padding: 6px 14px;
  border-radius: 6px;
  box-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
}

.system-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: 0.5px;
}

.system-subtitle {
  font-size: 13px;
  color: var(--accent-light);
  font-weight: 500;
}

.header-telemetry {
  display: flex;
  align-items: center;
  gap: 28px;
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 13px;
}

.telem-pill {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 14px;
  background: var(--surface-raised);
  border: 1px solid var(--border);
  border-radius: 20px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--success);
  box-shadow: 0 0 10px var(--success);
}

.status-dot.active-pulse {
  animation: pulse-dot 1.8s infinite;
}

@keyframes pulse-dot {
  0% { transform: scale(0.9); opacity: 0.7; }
  50% { transform: scale(1.3); opacity: 1; box-shadow: 0 0 14px var(--success); }
  100% { transform: scale(0.9); opacity: 0.7; }
}

/* Main Layout */
.main-viewport {
  flex: 1;
  display: flex;
  z-index: 5;
  height: calc(1080px - 72px - 56px);
}

/* Sidebar */
.sidebar {
  width: 280px;
  background: rgba(14, 19, 31, 0.7);
  border-right: 1px solid var(--border);
  padding: 30px 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.nav-pillar {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 18px;
  border-radius: 8px;
  border: 1px solid transparent;
  color: var(--text-muted);
  font-weight: 600;
  font-size: 14px;
  letter-spacing: 1px;
  transition: all 0.3s ease;
}

.nav-pillar.active {
  background: rgba(2, 132, 199, 0.15);
  border-color: var(--accent-light);
  color: var(--accent-light);
  box-shadow: 0 0 15px rgba(2, 132, 199, 0.2);
}

.pillar-num {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 12px;
  opacity: 0.6;
}

/* Center Content */
.content-area {
  flex: 1;
  padding: 40px 50px;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

.scene-heading-box {
  margin-bottom: 24px;
}

.scene-tag {
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: var(--accent-light);
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.scene-title {
  font-size: 32px;
  font-weight: 800;
  letter-spacing: -0.5px;
  color: var(--text-primary);
}

/* Bottom Bar */
.bottom-bar {
  height: 56px;
  background: rgba(14, 19, 31, 0.95);
  border-top: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
  z-index: 10;
  font-size: 13px;
  color: var(--text-muted);
  font-family: ui-monospace, monospace;
}

.timer-badge {
  background: var(--surface-raised);
  padding: 4px 12px;
  border-radius: 4px;
  border: 1px solid var(--border);
  color: var(--accent-light);
  font-weight: 700;
}

/* UI Card Primitives */
.card {
  background: rgba(18, 24, 36, 0.85);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
  backdrop-filter: blur(8px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
}

.metric-label {
  font-size: 13px;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 6px;
}

.metric-value {
  font-size: 28px;
  font-weight: 800;
  font-family: ui-monospace, monospace;
  color: var(--text-primary);
}
"""

def make_html(clip_id, title, pillar_active, tag, content_body, script_js=""):
    active_ovr = "active" if pillar_active == "OVERVIEW" else ""
    active_diag = "active" if pillar_active == "DIAGNOSE" else ""
    active_solve = "active" if pillar_active == "SOLVE" else ""
    active_adapt = "active" if pillar_active == "ADAPT" else ""
    active_ver = "active" if pillar_active == "VERIFY" else ""
    active_all = "active" if pillar_active == "ALL" else ""

    timer_str = f"{(clip_id-1)*24//60:02d}:{(clip_id-1)*24%60:02d} / 06:00"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
{COMMON_STYLE}
</style>
</head>
<body>
<div class="bg-grid"></div>
<div class="glow-ambient"></div>

<header class="top-header">
  <div class="brand-section">
    <div class="logo-badge">NIYAM-X</div>
    <div>
      <div class="system-title">Sovereign Adaptive Optimization Engine</div>
      <div class="system-subtitle">High-Performance Industrial Mathematical Core</div>
    </div>
  </div>
  <div class="header-telemetry">
    <div class="telem-pill">
      <div class="status-dot active-pulse"></div>
      <span>SOLVER ENGINE: ONLINE</span>
    </div>
    <div class="telem-pill">
      <span>BACKEND: C++20 / CUDA 12.8</span>
    </div>
    <div class="telem-pill">
      <span style="color:var(--text-secondary)">SIH 2026 | PS 26119 | TRINETRA 05</span>
    </div>
  </div>
</header>

<div class="main-viewport">
  <aside class="sidebar">
    <div style="font-size:11px; text-transform:uppercase; letter-spacing:1.5px; color:var(--text-muted); margin-bottom:4px;">Workflow Architecture</div>
    <div class="nav-pillar {active_ovr}">
      <span class="pillar-num">00</span>
      <span>PLATFORM</span>
    </div>
    <div class="nav-pillar {active_diag} {active_all}">
      <span class="pillar-num">01</span>
      <span>DIAGNOSE</span>
    </div>
    <div class="nav-pillar {active_solve} {active_all}">
      <span class="pillar-num">02</span>
      <span>SOLVE</span>
    </div>
    <div class="nav-pillar {active_adapt} {active_all}">
      <span class="pillar-num">03</span>
      <span>ADAPT</span>
    </div>
    <div class="nav-pillar {active_ver} {active_all}">
      <span class="pillar-num">04</span>
      <span>VERIFY</span>
    </div>

    <div style="margin-top:auto; padding:16px; background:rgba(21, 29, 46, 0.6); border-radius:8px; border:1px solid var(--border-subtle); font-size:12px; font-family:monospace;">
      <div style="color:var(--accent-light); font-weight:700; margin-bottom:4px;">RUNTIME ENVIRONMENT</div>
      <div style="color:var(--text-muted);">PRECISION: FP64 / Mixed</div>
      <div style="color:var(--text-muted);">COMPUTE: NVIDIA CUDA</div>
      <div style="color:var(--text-muted);">ALGO: PDHG / Sparse</div>
    </div>
  </aside>

  <main class="content-area">
    <div class="scene-heading-box">
      <div class="scene-tag">CLIP {clip_id:02d} // {tag}</div>
      <h1 class="scene-title">{title}</h1>
    </div>

    {content_body}
  </main>
</div>

<footer class="bottom-bar">
  <div>NIYAM-X SOVEREIGN OPTIMIZATION SYSTEM &bull; TEAM TRINETRA 05</div>
  <div style="display:flex; align-items:center; gap:16px;">
    <span>SCENE {clip_id:02d} OF 15</span>
    <span class="timer-badge">{timer_str}</span>
  </div>
</footer>

<script>
{script_js}
</script>
</body>
</html>
"""
    return html

# ----------------- SCENE CONTENT DEFINITIONS -----------------

# SCENE 1
s1_content = """
<div style="flex:1; display:grid; grid-template-columns: 1.2fr 1fr; gap:30px; align-items:center;">
  <div style="display:flex; flex-direction:column; gap:20px;">
    <div class="card" style="border-left:4px solid var(--accent-light);">
      <div style="font-size:24px; font-weight:800; color:var(--text-primary); margin-bottom:12px;">The Industrial Planning Challenge</div>
      <p style="font-size:16px; line-height:1.6; color:var(--text-secondary); margin-bottom:16px;">
        Refineries, electrical grids, transport logistics, and heavy manufacturing depend on large-scale mathematical optimization. When volatile crude prices, sudden outages, or demand shifts occur, static legacy solvers struggle.
      </p>
      <div style="display:flex; gap:16px;">
        <div style="padding:10px 16px; background:rgba(2, 132, 199, 0.15); border-radius:6px; border:1px solid var(--border); font-family:monospace; font-size:14px; color:var(--accent-light);">
          min c<sup>T</sup>x &nbsp;|&nbsp; Ax &le; b &nbsp;|&nbsp; l &le; x &le; u
        </div>
        <div style="padding:10px 16px; background:rgba(16, 185, 129, 0.15); border-radius:6px; border:1px solid var(--border); font-family:monospace; font-size:14px; color:var(--success);">
          10,000+ Decision Variables
        </div>
      </div>
    </div>

    <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:16px;">
      <div class="card" style="text-align:center;">
        <div style="font-size:28px; margin-bottom:8px;">🏭</div>
        <div style="font-weight:700; font-size:15px; margin-bottom:4px;">Refineries</div>
        <div style="font-size:12px; color:var(--text-muted);">Crude Blend & Scheduling</div>
      </div>
      <div class="card" style="text-align:center;">
        <div style="font-size:28px; margin-bottom:8px;">⚡</div>
        <div style="font-weight:700; font-size:15px; margin-bottom:4px;">Power Grids</div>
        <div style="font-size:12px; color:var(--text-muted);">Unit Commitment & Dispatch</div>
      </div>
      <div class="card" style="text-align:center;">
        <div style="font-size:28px; margin-bottom:8px;">🚢</div>
        <div style="font-weight:700; font-size:15px; margin-bottom:4px;">Logistics</div>
        <div style="font-size:12px; color:var(--text-muted);">Fleet Routing & Supply</div>
      </div>
    </div>
  </div>

  <div class="card" style="height:100%; display:flex; flex-direction:column; justify-content:center; align-items:center; position:relative; overflow:hidden; border:1px solid var(--accent);">
    <div style="position:absolute; width:400px; height:400px; background:radial-gradient(circle, rgba(2, 132, 199, 0.2) 0%, transparent 70%); border-radius:50%; animation:pulse-glow 3s infinite alternate;"></div>
    <div style="width:120px; height:120px; border-radius:24px; background:linear-gradient(135deg, #0284c7, #38bdf8); display:flex; align-items:center; justify-content:center; font-size:48px; font-weight:900; color:#07090e; box-shadow:0 0 50px rgba(56, 189, 248, 0.5); z-index:2; margin-bottom:20px;">
      NX
    </div>
    <div style="font-size:32px; font-weight:900; letter-spacing:2px; color:var(--text-primary); z-index:2;">NIYAM-X</div>
    <div style="font-size:15px; color:var(--accent-light); font-weight:600; letter-spacing:1px; z-index:2; margin-top:6px;">SOVEREIGN ADAPTIVE ENGINE</div>
    <div style="margin-top:24px; padding:8px 20px; background:rgba(31, 43, 66, 0.8); border-radius:20px; font-size:13px; font-family:monospace; color:var(--text-secondary); z-index:2;">
      COMPLIANT WITH SIH PROBLEM 26119
    </div>
  </div>
</div>
"""

# SCENE 2
s2_content = """
<div style="flex:1; display:flex; flex-direction:column; justify-content:center; gap:40px;">
  <!-- Old vs New Paradigm -->
  <div style="display:flex; align-items:center; justify-content:space-between; background:rgba(21, 29, 46, 0.5); border:1px solid var(--border); border-radius:12px; padding:20px 30px;">
    <div style="color:var(--text-muted); font-size:14px; font-weight:700; text-transform:uppercase;">Conventional Legacy Pipeline:</div>
    <div style="display:flex; align-items:center; gap:20px; font-family:monospace; font-size:16px;">
      <span style="padding:6px 14px; background:#1e293b; border-radius:6px; color:#cbd5e1;">RAW MODEL</span>
      <span style="color:var(--danger); font-size:20px;">&rarr;</span>
      <span style="padding:6px 14px; background:rgba(239, 68, 68, 0.15); border:1px solid var(--danger); border-radius:6px; color:var(--danger);">BLACK-BOX SOLVER</span>
      <span style="color:var(--danger); font-size:20px;">&rarr;</span>
      <span style="padding:6px 14px; background:#1e293b; border-radius:6px; color:#cbd5e1;">BLIND ANSWER</span>
    </div>
    <div style="color:var(--danger); font-size:13px; font-weight:600;">⚠ High Numerical Risk &bull; Zero Re-use</div>
  </div>

  <!-- The NIYAM-X 4 Pillars -->
  <div>
    <div style="font-size:16px; font-weight:700; color:var(--accent-light); text-transform:uppercase; letter-spacing:1px; margin-bottom:16px;">The NIYAM-X Paradigm:</div>
    <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:20px;">
      <div class="card" style="border-top:4px solid var(--accent); transition:transform 0.3s ease;">
        <div style="font-size:12px; font-family:monospace; color:var(--accent-light); margin-bottom:8px;">STAGE 01</div>
        <div style="font-size:22px; font-weight:800; margin-bottom:10px;">DIAGNOSE</div>
        <div style="font-size:14px; color:var(--text-secondary); line-height:1.5;">Model X-Ray detects conditioning, sparsity, bounds, and builds an explainable Fingerprint.</div>
      </div>
      <div class="card" style="border-top:4px solid #38bdf8;">
        <div style="font-size:12px; font-family:monospace; color:#38bdf8; margin-bottom:8px;">STAGE 02</div>
        <div style="font-size:22px; font-weight:800; margin-bottom:10px;">SOLVE</div>
        <div style="font-size:14px; color:var(--text-secondary); line-height:1.5;">NIYAM-X C++20 Core executes GPU-accelerated PDHG algorithm with robust CPU fallback.</div>
      </div>
      <div class="card" style="border-top:4px solid var(--warning);">
        <div style="font-size:12px; font-family:monospace; color:var(--warning); margin-bottom:8px;">STAGE 03</div>
        <div style="font-size:22px; font-weight:800; margin-bottom:10px;">ADAPT</div>
        <div style="font-size:14px; color:var(--text-secondary); line-height:1.5;">DeltaSolve and Scenario Swarm reuse previous states for instant warm-start re-optimization.</div>
      </div>
      <div class="card" style="border-top:4px solid var(--success);">
        <div style="font-size:12px; font-family:monospace; color:var(--success); margin-bottom:8px;">STAGE 04</div>
        <div style="font-size:22px; font-weight:800; margin-bottom:10px;">VERIFY</div>
        <div style="font-size:14px; color:var(--text-secondary); line-height:1.5;">Independent Verifier reconstructs residuals and constraints in an isolated mathematical sandbox.</div>
      </div>
    </div>
  </div>
</div>
"""

# SCENE 3
s3_content = """
<div style="flex:1; display:grid; grid-template-columns: 1fr 1.2fr; gap:30px; align-items:center;">
  <div style="display:flex; flex-direction:column; gap:20px;">
    <div class="card">
      <div class="metric-label">Ingested Optimization File</div>
      <div style="display:flex; align-items:center; gap:12px; margin-top:8px;">
        <span style="font-size:32px;">📄</span>
        <div>
          <div style="font-size:20px; font-weight:800; font-family:monospace; color:var(--accent-light);">refinery_demo.mps</div>
          <div style="font-size:13px; color:var(--text-muted);">Standard MPS Format &bull; Upload Validated</div>
        </div>
      </div>
    </div>

    <div class="card">
      <div style="display:grid; grid-template-columns: 1fr 1fr; gap:16px;">
        <div>
          <div class="metric-label">Decision Variables</div>
          <div class="metric-value">25,000</div>
        </div>
        <div>
          <div class="metric-label">Constraints</div>
          <div class="metric-value">18,000</div>
        </div>
        <div>
          <div class="metric-label">Non-Zero Entries</div>
          <div class="metric-value" style="color:var(--accent-light);">210,000</div>
        </div>
        <div>
          <div class="metric-label">Matrix Sparsity</div>
          <div class="metric-value" style="color:var(--success);">99.95%</div>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="metric-label">Supported IR Formats</div>
      <div style="display:flex; gap:12px; margin-top:10px;">
        <span style="padding:6px 16px; background:rgba(2, 132, 199, 0.2); border:1px solid var(--accent); border-radius:6px; font-weight:700; font-size:14px;">JSON IR</span>
        <span style="padding:6px 16px; background:rgba(2, 132, 199, 0.2); border:1px solid var(--accent); border-radius:6px; font-weight:700; font-size:14px;">LP FILE</span>
        <span style="padding:6px 16px; background:rgba(2, 132, 199, 0.2); border:1px solid var(--accent); border-radius:6px; font-weight:700; font-size:14px;">MPS BENCHMARK</span>
      </div>
    </div>
  </div>

  <div class="card" style="height:100%; display:flex; flex-direction:column;">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
      <div class="metric-label">Compressed Sparse Row (CSR) Coefficient View</div>
      <span style="font-family:monospace; font-size:12px; color:var(--accent-light);">NONZERO DENSITY: 0.046%</span>
    </div>
    <div style="flex:1; background:#07090e; border:1px solid var(--border); border-radius:8px; display:grid; grid-template-columns:repeat(16, 1fr); gap:4px; padding:12px; overflow:hidden;">
      <!-- Generate simulated sparse matrix dots -->
      """ + "".join([f'<div style="background:{"rgba(56, 189, 248, " + str(0.8 if (i*31)%7==0 else 0.05) + ")"}; border-radius:2px; height:18px;"></div>' for i in range(256)]) + """
    </div>
    <div style="margin-top:14px; font-family:monospace; font-size:13px; color:var(--text-secondary); display:flex; justify-content:space-between;">
      <span>Row Offsets: ptr[0..18001]</span>
      <span>Col Indices: ind[0..210000]</span>
      <span>Values: val[0..210000]</span>
    </div>
  </div>
</div>
"""

# SCENE 4
s4_content = """
<div style="flex:1; display:grid; grid-template-columns: 1.1fr 1fr; gap:30px;">
  <div style="display:flex; flex-direction:column; gap:20px;">
    <div class="card" style="border-left:4px solid var(--warning);">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
        <span style="font-size:18px; font-weight:700;">Mathematical Health & Diagnostic Report</span>
        <span style="background:rgba(245, 158, 11, 0.2); color:var(--warning); border:1px solid var(--warning); padding:4px 12px; border-radius:4px; font-weight:800; font-family:monospace; font-size:13px;">NUMERICAL RISK: HIGH</span>
      </div>
      <p style="font-size:15px; color:var(--text-secondary); line-height:1.5;">
        Model X-Ray probes the model before dispatching execution, exposing ill-conditioned rows, extreme coefficient spreads, and degenerate bounds.
      </p>
    </div>

    <div style="display:grid; grid-template-columns: repeat(2, 1fr); gap:16px;">
      <div class="card">
        <div class="metric-label">Coefficient Dynamic Range</div>
        <div style="font-size:22px; font-family:monospace; font-weight:800; color:var(--warning);">1.0e-8 &rarr; 1.0e+7</div>
        <div style="font-size:12px; color:var(--text-muted); margin-top:4px;">Span of 15 orders of magnitude</div>
      </div>
      <div class="card">
        <div class="metric-label">Poorly Scaled Rows</div>
        <div class="metric-value" style="color:var(--danger);">817</div>
        <div style="font-size:12px; color:var(--text-muted); margin-top:4px;">Requires equilibration</div>
      </div>
      <div class="card">
        <div class="metric-label">Fixed Variables Detected</div>
        <div class="metric-value">421</div>
        <div style="font-size:12px; color:var(--text-muted); margin-top:4px;">Eligible for presolve reduction</div>
      </div>
      <div class="card">
        <div class="metric-label">Equality Ratio</div>
        <div class="metric-value">42.4%</div>
        <div style="font-size:12px; color:var(--text-muted); margin-top:4px;">High structural tightness</div>
      </div>
    </div>
  </div>

  <div class="card" style="display:flex; flex-direction:column; align-items:center; justify-content:center;">
    <div style="font-size:14px; font-weight:700; color:var(--accent-light); text-transform:uppercase; letter-spacing:1px; margin-bottom:16px;">Model Structural Radar Assessment</div>
    <svg width="340" height="340" viewBox="0 0 340 340">
      <polygon points="170,30 290,100 290,240 170,310 50,240 50,100" fill="none" stroke="rgba(31, 43, 66, 0.8)" stroke-width="1.5" />
      <polygon points="170,70 250,120 250,220 170,270 90,220 90,120" fill="none" stroke="rgba(31, 43, 66, 0.5)" stroke-width="1" />
      <polygon points="170,110 210,140 210,200 170,230 130,200 130,140" fill="none" stroke="rgba(31, 43, 66, 0.3)" stroke-width="1" />
      <!-- Radar Area (Scaling, Sparsity, Structure, Risk, Redundancy, Bounds) -->
      <polygon points="170,45 280,110 240,230 170,290 80,210 70,115" fill="rgba(56, 189, 248, 0.25)" stroke="var(--accent-light)" stroke-width="2.5" />
      <!-- Labels -->
      <text x="170" y="20" fill="var(--text-primary)" font-size="12" text-anchor="middle" font-weight="700">SCALING (HIGH)</text>
      <text x="300" y="105" fill="var(--text-primary)" font-size="12" font-weight="700">SPARSITY (99.95%)</text>
      <text x="300" y="245" fill="var(--text-primary)" font-size="12" font-weight="700">STRUCTURE (BLOCK)</text>
      <text x="170" y="330" fill="var(--text-primary)" font-size="12" text-anchor="middle" font-weight="700">NUMERICAL RISK</text>
      <text x="35" y="245" fill="var(--text-primary)" font-size="12" text-anchor="end" font-weight="700">REDUNDANCY</text>
      <text x="35" y="105" fill="var(--text-primary)" font-size="12" text-anchor="end" font-weight="700">BOUNDS DENSITY</text>
    </svg>
  </div>
</div>
"""

# SCENE 5
s5_content = """
<div style="flex:1; display:grid; grid-template-columns: 1fr 1fr; gap:30px; align-items:center;">
  <div class="card" style="display:flex; flex-direction:column; gap:16px;">
    <div style="font-size:18px; font-weight:800; color:var(--text-primary); margin-bottom:4px;">1. Diagnostic Model Fingerprint</div>
    <div style="font-size:13px; color:var(--text-muted); margin-bottom:10px;">Deterministic 7-dimensional feature extraction vector</div>

    <div style="display:flex; flex-direction:column; gap:10px; font-family:monospace; font-size:13px;">
      <div style="display:flex; justify-content:space-between; padding:8px 12px; background:#07090e; border-radius:6px;">
        <span style="color:var(--text-secondary);">Density Factor</span>
        <span style="color:var(--accent-light);">0.046%</span>
      </div>
      <div style="display:flex; justify-content:space-between; padding:8px 12px; background:#07090e; border-radius:6px;">
        <span style="color:var(--text-secondary);">Integer Ratio</span>
        <span style="color:var(--accent-light);">0.000 (Pure Continuous LP)</span>
      </div>
      <div style="display:flex; justify-content:space-between; padding:8px 12px; background:#07090e; border-radius:6px;">
        <span style="color:var(--text-secondary);">Coefficient Spread</span>
        <span style="color:var(--warning);">1.0e15 (Extreme Dynamic Span)</span>
      </div>
      <div style="display:flex; justify-content:space-between; padding:8px 12px; background:#07090e; border-radius:6px;">
        <span style="color:var(--text-secondary);">Equality Ratio</span>
        <span style="color:var(--accent-light);">0.424</span>
      </div>
      <div style="display:flex; justify-content:space-between; padding:8px 12px; background:#07090e; border-radius:6px;">
        <span style="color:var(--text-secondary);">Block Structure</span>
        <span style="color:var(--success);">0.941 (Highly Parallelizable)</span>
      </div>
    </div>
  </div>

  <div class="card" style="border:1px solid var(--accent); background:rgba(18, 24, 36, 0.95); display:flex; flex-direction:column; gap:16px;">
    <div style="display:flex; justify-content:space-between; align-items:center;">
      <span style="font-size:18px; font-weight:800; color:var(--accent-light);">2. Solver Autopilot Configuration</span>
      <span style="background:var(--success); color:#07090e; font-weight:800; font-size:11px; padding:3px 8px; border-radius:4px;">RULE DETERMINISTIC</span>
    </div>
    
    <div style="display:flex; flex-direction:column; gap:12px; margin-top:8px;">
      <div style="padding:12px; background:rgba(2, 132, 199, 0.15); border:1px solid var(--border); border-radius:8px; display:flex; justify-content:space-between; align-items:center;">
        <div>
          <div style="font-size:11px; text-transform:uppercase; color:var(--text-muted);">Execution Backend</div>
          <div style="font-size:16px; font-weight:800; color:var(--text-primary);">NVIDIA CUDA GPU</div>
        </div>
        <span style="font-size:20px;">⚡</span>
      </div>

      <div style="padding:12px; background:rgba(2, 132, 199, 0.15); border:1px solid var(--border); border-radius:8px; display:flex; justify-content:space-between; align-items:center;">
        <div>
          <div style="font-size:11px; text-transform:uppercase; color:var(--text-muted);">Algorithm Selection</div>
          <div style="font-size:16px; font-weight:800; color:var(--text-primary);">Primal-Dual Hybrid Gradient (PDHG)</div>
        </div>
        <span style="font-size:20px;">📐</span>
      </div>

      <div style="padding:12px; background:rgba(2, 132, 199, 0.15); border:1px solid var(--border); border-radius:8px; display:flex; justify-content:space-between; align-items:center;">
        <div>
          <div style="font-size:11px; text-transform:uppercase; color:var(--text-muted);">Scaling Strategy</div>
          <div style="font-size:16px; font-weight:800; color:var(--text-primary);">Ruiz Equilibration (Robust Mode)</div>
        </div>
        <span style="font-size:20px;">⚖️</span>
      </div>

      <div style="padding:12px; background:rgba(2, 132, 199, 0.15); border:1px solid var(--border); border-radius:8px; display:flex; justify-content:space-between; align-items:center;">
        <div>
          <div style="font-size:11px; text-transform:uppercase; color:var(--text-muted);">Numerical Precision</div>
          <div style="font-size:16px; font-weight:800; color:var(--text-primary);">Mixed Precision (FP32/FP64)</div>
        </div>
        <span style="font-size:20px;">🔬</span>
      </div>
    </div>
  </div>
</div>
"""

# SCENE 6
s6_content = """
<div style="flex:1; display:flex; flex-direction:column; justify-content:center; gap:24px;">
  <div class="card" style="display:flex; justify-content:space-between; align-items:center; padding:20px 30px;">
    <div style="display:flex; align-items:center; gap:16px;">
      <div style="width:48px; height:48px; border-radius:10px; background:linear-gradient(135deg, #0284c7, #38bdf8); display:flex; align-items:center; justify-content:center; font-weight:900; color:#07090e; font-size:20px;">C++</div>
      <div>
        <div style="font-size:18px; font-weight:800;">NIYAM-X Core Optimization Architecture</div>
        <div style="font-size:13px; color:var(--text-muted);">High-throughput Sparse Kernel Implementation (C++20 & CUDA 12.8)</div>
      </div>
    </div>
    <div style="display:flex; gap:12px;">
      <span style="padding:6px 14px; background:rgba(16, 185, 129, 0.2); border:1px solid var(--success); border-radius:6px; color:var(--success); font-weight:700; font-size:12px;">CUDA ACCELERATED</span>
      <span style="padding:6px 14px; background:rgba(2, 132, 199, 0.2); border:1px solid var(--accent); border-radius:6px; color:var(--accent-light); font-weight:700; font-size:12px;">CPU FALLBACK READY</span>
    </div>
  </div>

  <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:20px;">
    <div class="card">
      <div style="font-size:14px; font-weight:700; color:var(--accent-light); margin-bottom:12px;">Sparse SpMV Kernels</div>
      <div style="font-family:monospace; font-size:13px; color:var(--text-secondary); line-height:1.6; background:#07090e; padding:12px; border-radius:6px;">
        y &larr; A &times; x &nbsp;(Forward CSR)<br>
        s &larr; A<sup>T</sup> &times; y (Adjoint CSC)<br>
        Coalesced GPU global memory reads with warp shuffle reductions
      </div>
    </div>

    <div class="card">
      <div style="font-size:14px; font-weight:700; color:var(--accent-light); margin-bottom:12px;">PDHG Iterate Step</div>
      <div style="font-family:monospace; font-size:13px; color:var(--text-secondary); line-height:1.6; background:#07090e; padding:12px; border-radius:6px;">
        x<sup>k+1</sup> = proj<sub>X</sub>(x<sup>k</sup> - &tau; A<sup>T</sup> y<sup>k</sup> - &tau; c)<br>
        x&#772;<sup>k+1</sup> = 2 x<sup>k+1</sup> - x<sup>k</sup><br>
        y<sup>k+1</sup> = proj<sub>Y</sub>(y<sup>k</sup> + &sigma; A x&#772;<sup>k+1</sup> - &sigma; b)
      </div>
    </div>

    <div class="card">
      <div style="font-size:14px; font-weight:700; color:var(--accent-light); margin-bottom:12px;">Memory & Zero-Copy Bridge</div>
      <div style="font-family:monospace; font-size:13px; color:var(--text-secondary); line-height:1.6; background:#07090e; padding:12px; border-radius:6px;">
        Pinned Host Memory staging<br>
        Unified Virtual Addressing<br>
        Asynchronous CUDA streams for overlapped I/O and telemetry logging
      </div>
    </div>
  </div>
</div>
"""

# SCENE 7
s7_content = """
<div style="flex:1; display:grid; grid-template-columns: 1fr 1.3fr; gap:30px;">
  <div style="display:flex; flex-direction:column; gap:20px;">
    <div class="card">
      <div class="metric-label">Active Iteration Counter</div>
      <div class="metric-value" style="font-size:42px; color:var(--accent-light);">1,420 <span style="font-size:16px; color:var(--text-muted); font-weight:500;">/ 5,000 max</span></div>
      <div style="margin-top:8px; height:6px; background:#1e293b; border-radius:3px; overflow:hidden;">
        <div style="width:28.4%; height:100%; background:var(--accent-light);"></div>
      </div>
    </div>

    <div class="card">
      <div style="display:grid; grid-template-columns: 1fr 1fr; gap:16px;">
        <div>
          <div class="metric-label">Objective Value</div>
          <div style="font-size:24px; font-weight:800; font-family:monospace; color:var(--text-primary);">₹ 31.82 Cr</div>
        </div>
        <div>
          <div class="metric-label">Convergence Rate</div>
          <div style="font-size:24px; font-weight:800; font-family:monospace; color:var(--success);">-8.4 dB/k</div>
        </div>
        <div>
          <div class="metric-label">Primal Infeasibility</div>
          <div style="font-size:20px; font-weight:800; font-family:monospace; color:var(--success);">2.41e-07</div>
        </div>
        <div>
          <div class="metric-label">Dual Infeasibility</div>
          <div style="font-size:20px; font-weight:800; font-family:monospace; color:var(--success);">6.18e-07</div>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="metric-label">Numerical Status</div>
      <div style="display:flex; align-items:center; gap:8px; margin-top:8px;">
        <span class="status-dot"></span>
        <span style="font-weight:700; color:var(--success); font-family:monospace;">STATUS: OPTIMAL_CONVERGED (tol &le; 1e-6)</span>
      </div>
    </div>
  </div>

  <div class="card" style="display:flex; flex-direction:column;">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
      <div class="metric-label">Live Residual Convergence Trajectory (Log Scale)</div>
      <span style="font-family:monospace; font-size:12px; color:var(--text-muted);">TOLERANCE THRESHOLD: 1.0e-6</span>
    </div>
    <div style="flex:1; background:#07090e; border:1px solid var(--border); border-radius:8px; position:relative; overflow:hidden; padding:20px;">
      <svg width="100%" height="100%" viewBox="0 0 500 240" preserveAspectRatio="none">
        <!-- Grid lines -->
        <line x1="0" y1="40" x2="500" y2="40" stroke="rgba(31, 43, 66, 0.4)" stroke-dasharray="4" />
        <line x1="0" y1="100" x2="500" y2="100" stroke="rgba(31, 43, 66, 0.4)" stroke-dasharray="4" />
        <line x1="0" y1="160" x2="500" y2="160" stroke="rgba(31, 43, 66, 0.4)" stroke-dasharray="4" />
        <line x1="0" y1="200" x2="500" y2="200" stroke="rgba(16, 185, 129, 0.5)" stroke-width="1.5" stroke-dasharray="6" />

        <!-- Primal Residual Curve (Blue) -->
        <path d="M 0,20 Q 80,60 180,120 T 360,180 T 500,215" fill="none" stroke="var(--accent-light)" stroke-width="3" />
        <!-- Dual Residual Curve (Green) -->
        <path d="M 0,35 Q 120,80 240,140 T 400,195 T 500,218" fill="none" stroke="var(--success)" stroke-width="3" />

        <circle cx="500" cy="215" r="5" fill="var(--accent-light)" />
        <circle cx="500" cy="218" r="5" fill="var(--success)" />
      </svg>
      <div style="position:absolute; bottom:12px; right:20px; font-family:monospace; font-size:12px; display:flex; gap:16px;">
        <span style="color:var(--accent-light);">&bull; Primal Residual</span>
        <span style="color:var(--success);">&bull; Dual Residual</span>
      </div>
    </div>
  </div>
</div>
"""

# SCENE 8
s8_content = """
<div style="flex:1; display:flex; flex-direction:column; gap:20px;">
  <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:16px;">
    <div class="card">
      <div class="metric-label">Optimized Net Profit</div>
      <div class="metric-value" style="color:var(--success);">₹ 31.82 Cr</div>
      <div style="font-size:12px; color:var(--text-muted); margin-top:4px;">Feasible Global Optimum</div>
    </div>
    <div class="card">
      <div class="metric-label">Total Crude Processed</div>
      <div class="metric-value">120,000 bpd</div>
      <div style="font-size:12px; color:var(--text-muted); margin-top:4px;">100% Capacity Utilized</div>
    </div>
    <div class="card">
      <div class="metric-label">Light / Heavy Blend</div>
      <div class="metric-value" style="color:var(--accent-light);">65% / 35%</div>
      <div style="font-size:12px; color:var(--text-muted); margin-top:4px;">Sweet / Sour Ratio</div>
    </div>
    <div class="card">
      <div class="metric-label">Solution Status</div>
      <div class="metric-value" style="color:var(--success); font-size:22px;">OPTIMAL & VALID</div>
      <div style="font-size:12px; color:var(--text-muted); margin-top:4px;">Zero Violations</div>
    </div>
  </div>

  <div style="flex:1; display:grid; grid-template-columns: 1fr 1fr; gap:20px;">
    <div class="card">
      <div class="metric-label" style="margin-bottom:16px;">Refinery Product Slate Yield Allocation</div>
      <div style="display:flex; flex-direction:column; gap:12px;">
        <div>
          <div style="display:flex; justify-content:space-between; font-size:14px; margin-bottom:4px;">
            <span>Ultra-Low Sulfur Diesel (Euro VI)</span>
            <span style="font-family:monospace; font-weight:700;">40,800 bpd (34%)</span>
          </div>
          <div style="height:8px; background:#1e293b; border-radius:4px; overflow:hidden;"><div style="width:34%; height:100%; background:var(--accent);"></div></div>
        </div>
        <div>
          <div style="display:flex; justify-content:space-between; font-size:14px; margin-bottom:4px;">
            <span>Motor Gasoline (RON 95)</span>
            <span style="font-family:monospace; font-weight:700;">45,600 bpd (38%)</span>
          </div>
          <div style="height:8px; background:#1e293b; border-radius:4px; overflow:hidden;"><div style="width:38%; height:100%; background:var(--accent-light);"></div></div>
        </div>
        <div>
          <div style="display:flex; justify-content:space-between; font-size:14px; margin-bottom:4px;">
            <span>Aviation Turbine Fuel (Jet-A1)</span>
            <span style="font-family:monospace; font-weight:700;">19,200 bpd (16%)</span>
          </div>
          <div style="height:8px; background:#1e293b; border-radius:4px; overflow:hidden;"><div style="width:16%; height:100%; background:var(--success);"></div></div>
        </div>
        <div>
          <div style="display:flex; justify-content:space-between; font-size:14px; margin-bottom:4px;">
            <span>Liquefied Petroleum Gas (LPG)</span>
            <span style="font-family:monospace; font-weight:700;">14,400 bpd (12%)</span>
          </div>
          <div style="height:8px; background:#1e293b; border-radius:4px; overflow:hidden;"><div style="width:12%; height:100%; background:var(--warning);"></div></div>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="metric-label" style="margin-bottom:16px;">Core Unit Constraints & Shadow Prices</div>
      <div style="display:flex; flex-direction:column; gap:10px; font-family:monospace; font-size:13px;">
        <div style="display:flex; justify-content:space-between; padding:10px 14px; background:#07090e; border-radius:6px;">
          <span>Atmospheric Distillation Unit</span>
          <span style="color:var(--warning);">BOTTLENECK (Dual: ₹420/bbl)</span>
        </div>
        <div style="display:flex; justify-content:space-between; padding:10px 14px; background:#07090e; border-radius:6px;">
          <span>Fluidized Catalytic Cracker (FCC)</span>
          <span style="color:var(--success);">94.2% (Dual: ₹0.00)</span>
        </div>
        <div style="display:flex; justify-content:space-between; padding:10px 14px; background:#07090e; border-radius:6px;">
          <span>Hydrocracker Unit (HCU)</span>
          <span style="color:var(--success);">88.7% (Dual: ₹0.00)</span>
        </div>
        <div style="display:flex; justify-content:space-between; padding:10px 14px; background:#07090e; border-radius:6px;">
          <span>Sulfur Recovery Unit</span>
          <span style="color:var(--success);">76.1% (Dual: ₹0.00)</span>
        </div>
      </div>
    </div>
  </div>
</div>
"""

# SCENE 9
s9_content = """
<div style="flex:1; display:grid; grid-template-columns: 1fr 1.2fr; gap:30px; align-items:center;">
  <div style="display:flex; flex-direction:column; gap:20px;">
    <div class="card" style="border-left:4px solid var(--danger);">
      <div style="display:flex; align-items:center; gap:10px; margin-bottom:12px;">
        <span style="font-size:24px;">🚨</span>
        <span style="font-size:20px; font-weight:800; color:var(--danger);">Operational Disruption Event</span>
      </div>
      <p style="font-size:15px; color:var(--text-secondary); line-height:1.6;">
        Real-world operations never stay static. Unforeseen market price shifts, demand spikes, or equipment derating instantly render prior optimization plans obsolete.
      </p>
    </div>

    <div class="card">
      <div class="metric-label" style="margin-bottom:12px;">Shifted Environmental Parameters</div>
      <div style="display:flex; flex-direction:column; gap:10px; font-family:monospace; font-size:14px;">
        <div style="display:flex; justify-content:space-between; padding:8px 12px; background:rgba(239, 68, 68, 0.15); border:1px solid var(--danger); border-radius:6px;">
          <span>Crude A Purchase Price</span>
          <span style="color:var(--danger); font-weight:700;">+8.0% SHOCK</span>
        </div>
        <div style="display:flex; justify-content:space-between; padding:8px 12px; background:rgba(245, 158, 11, 0.15); border:1px solid var(--warning); border-radius:6px;">
          <span>Export Gasoline Demand</span>
          <span style="color:var(--warning); font-weight:700;">+4.0% SURGE</span>
        </div>
        <div style="display:flex; justify-content:space-between; padding:8px 12px; background:#07090e; border-radius:6px;">
          <span>Distillation Capacity</span>
          <span style="color:var(--text-muted);">UNCHANGED (Constrained)</span>
        </div>
      </div>
    </div>
  </div>

  <div class="card" style="display:flex; flex-direction:column; align-items:center; justify-content:center; padding:40px; text-align:center;">
    <div style="font-size:48px; margin-bottom:16px;">⏱️</div>
    <div style="font-size:24px; font-weight:800; margin-bottom:12px;">The Cold-Start Dilemma</div>
    <p style="font-size:15px; color:var(--text-secondary); max-width:460px; line-height:1.6; margin-bottom:24px;">
      Conventional solvers re-solve from scratch: recalculating matrix orderings, scaling factors, and starting from zero, wasting critical minutes.
    </p>
    <div style="padding:16px 24px; background:rgba(2, 132, 199, 0.15); border:1px solid var(--accent); border-radius:8px; font-family:monospace; font-size:14px; color:var(--accent-light);">
      NIYAM-X DeltaSolve activates warm-start trajectory &rarr;
    </div>
  </div>
</div>
"""

# SCENE 10
s10_content = """
<div style="flex:1; display:grid; grid-template-columns: 1.1fr 1fr; gap:30px; align-items:center;">
  <div style="display:flex; flex-direction:column; gap:20px;">
    <div class="card" style="border-left:4px solid var(--accent-light);">
      <div style="font-size:20px; font-weight:800; color:var(--text-primary); margin-bottom:8px;">DeltaSolve: Warm Re-Optimization Core</div>
      <p style="font-size:15px; color:var(--text-secondary); line-height:1.5;">
        Instead of discarding previous numerical effort, DeltaSolve preserves the mathematical trajectory, warm-starting the primal-dual iterate directly inside the new feasible basin.
      </p>
    </div>

    <div class="card">
      <div class="metric-label" style="margin-bottom:12px;">Reused Solver State Vectors</div>
      <div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px; font-family:monospace; font-size:13px;">
        <div style="padding:10px; background:#07090e; border-radius:6px; border:1px solid var(--border);">
          <div style="color:var(--accent-light); font-weight:700;">x* Primal Solution</div>
          <div style="color:var(--text-muted); font-size:11px;">25,000 variables warm base</div>
        </div>
        <div style="padding:10px; background:#07090e; border-radius:6px; border:1px solid var(--border);">
          <div style="color:var(--accent-light); font-weight:700;">y* Dual Multipliers</div>
          <div style="color:var(--text-muted); font-size:11px;">18,000 shadow prices</div>
        </div>
        <div style="padding:10px; background:#07090e; border-radius:6px; border:1px solid var(--border);">
          <div style="color:var(--accent-light); font-weight:700;">Equilibration Scales</div>
          <div style="color:var(--text-muted); font-size:11px;">D_r and D_c preserved</div>
        </div>
        <div style="padding:10px; background:#07090e; border-radius:6px; border:1px solid var(--border);">
          <div style="color:var(--accent-light); font-weight:700;">Sparse Ordering</div>
          <div style="color:var(--text-muted); font-size:11px;">Zero re-symbolic cost</div>
        </div>
      </div>
    </div>
  </div>

  <div class="card" style="display:flex; flex-direction:column; justify-content:center; gap:20px;">
    <div style="font-size:16px; font-weight:700; color:var(--accent-light); text-transform:uppercase;">Performance Comparison (Re-Solve)</div>
    
    <div>
      <div style="display:flex; justify-content:space-between; font-size:14px; margin-bottom:6px;">
        <span>Cold Solve (From Scratch)</span>
        <span style="font-family:monospace; color:var(--text-muted);">1,420 iterations (100%)</span>
      </div>
      <div style="height:12px; background:#1e293b; border-radius:6px; overflow:hidden;">
        <div style="width:100%; height:100%; background:var(--text-muted);"></div>
      </div>
    </div>

    <div>
      <div style="display:flex; justify-content:space-between; font-size:14px; margin-bottom:6px;">
        <span style="color:var(--success); font-weight:700;">DeltaSolve Warm Start</span>
        <span style="font-family:monospace; color:var(--success); font-weight:800;">280 iterations (19.7%)</span>
      </div>
      <div style="height:12px; background:#1e293b; border-radius:6px; overflow:hidden;">
        <div style="width:19.7%; height:100%; background:var(--success);"></div>
      </div>
    </div>

    <div style="padding:16px; background:rgba(16, 185, 129, 0.15); border:1px solid var(--success); border-radius:8px; margin-top:10px;">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <div>
          <div style="font-size:12px; color:var(--text-secondary); text-transform:uppercase;">Updated Optimal Objective</div>
          <div style="font-size:24px; font-weight:800; font-family:monospace; color:var(--text-primary);">₹ 29.91 Cr</div>
        </div>
        <div style="text-align:right;">
          <div style="font-size:12px; color:var(--text-secondary); text-transform:uppercase;">Iteration Reduction</div>
          <div style="font-size:24px; font-weight:800; font-family:monospace; color:var(--success);">&sim; 5&times; Faster</div>
        </div>
      </div>
    </div>
  </div>
</div>
"""

# SCENE 11
s11_content = """
<div style="flex:1; display:flex; flex-direction:column; gap:20px;">
  <div class="card" style="display:flex; justify-content:space-between; align-items:center; padding:16px 24px;">
    <div>
      <div style="font-size:18px; font-weight:800;">Scenario Swarm Matrix Execution</div>
      <div style="font-size:13px; color:var(--text-muted);">Parallel Multi-Parametric Exploration over Price &times; Demand &times; Outage Assays</div>
    </div>
    <div style="display:flex; gap:10px;">
      <span style="padding:6px 12px; background:rgba(2, 132, 199, 0.2); border-radius:4px; font-family:monospace; font-size:12px; color:var(--accent-light);">8 SCENARIOS CONCURRENT</span>
      <span style="padding:6px 12px; background:rgba(16, 185, 129, 0.2); border-radius:4px; font-family:monospace; font-size:12px; color:var(--success);">WARM RE-USE ACTIVE</span>
    </div>
  </div>

  <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:16px;">
    <div class="card" style="border-top:3px solid var(--accent-light);">
      <div style="font-size:12px; font-family:monospace; color:var(--accent-light); margin-bottom:4px;">SCENARIO A</div>
      <div style="font-weight:700; font-size:16px; margin-bottom:8px;">Base + Crude +5%</div>
      <div style="font-family:monospace; font-size:20px; font-weight:800; color:var(--text-primary);">₹ 30.64 Cr</div>
      <div style="font-size:12px; color:var(--success); margin-top:4px;">Iter: 245 &bull; 0.21s</div>
    </div>

    <div class="card" style="border-top:3px solid var(--accent-light);">
      <div style="font-size:12px; font-family:monospace; color:var(--accent-light); margin-bottom:4px;">SCENARIO B</div>
      <div style="font-weight:700; font-size:16px; margin-bottom:8px;">Crude +10%, Dem +2%</div>
      <div style="font-family:monospace; font-size:20px; font-weight:800; color:var(--text-primary);">₹ 29.18 Cr</div>
      <div style="font-size:12px; color:var(--success); margin-top:4px;">Iter: 310 &bull; 0.27s</div>
    </div>

    <div class="card" style="border-top:3px solid var(--warning);">
      <div style="font-size:12px; font-family:monospace; color:var(--warning); margin-bottom:4px;">SCENARIO C</div>
      <div style="font-weight:700; font-size:16px; margin-bottom:8px;">FCC Capacity -15%</div>
      <div style="font-family:monospace; font-size:20px; font-weight:800; color:var(--warning);">₹ 26.85 Cr</div>
      <div style="font-size:12px; color:var(--success); margin-top:4px;">Iter: 420 &bull; 0.36s</div>
    </div>

    <div class="card" style="border-top:3px solid var(--accent-light);">
      <div style="font-size:12px; font-family:monospace; color:var(--accent-light); margin-bottom:4px;">SCENARIO D</div>
      <div style="font-weight:700; font-size:16px; margin-bottom:8px;">Diesel Export Surge +8%</div>
      <div style="font-family:monospace; font-size:20px; font-weight:800; color:var(--text-primary);">₹ 33.40 Cr</div>
      <div style="font-size:12px; color:var(--success); margin-top:4px;">Iter: 290 &bull; 0.25s</div>
    </div>
  </div>

  <div class="card" style="flex:1; display:flex; flex-direction:column; justify-content:center;">
    <div class="metric-label" style="margin-bottom:12px;">Decision Stability & Sensitivity Envelope Across Scenarios</div>
    <div style="display:flex; align-items:center; gap:20px; font-family:monospace; font-size:13px; color:var(--text-secondary);">
      <div style="flex:1; height:40px; background:#07090e; border:1px solid var(--border); border-radius:6px; display:flex; align-items:center; padding:0 20px; position:relative;">
        <span style="position:absolute; left:20px;">₹ 26.85 Cr (Min)</span>
        <div style="margin:0 auto; width:60%; height:12px; background:linear-gradient(90deg, #0284c7, #10b981); border-radius:6px;"></div>
        <span style="position:absolute; right:20px;">₹ 33.40 Cr (Max)</span>
      </div>
      <div style="width:260px; padding:10px; background:rgba(21, 29, 46, 0.8); border-radius:6px; text-align:center;">
        Decision Band: <strong style="color:var(--accent-light);">&plusmn; 11.2% Robustness</strong>
      </div>
    </div>
  </div>
</div>
"""

# SCENE 12
s12_content = """
<div style="flex:1; display:grid; grid-template-columns: 1fr 1.2fr; gap:30px;">
  <div style="display:flex; flex-direction:column; gap:20px;">
    <div class="card">
      <div class="metric-label">Anytime Solution Guarantee</div>
      <div style="display:flex; align-items:baseline; gap:10px; margin-top:8px;">
        <div class="metric-value" style="color:var(--success); font-size:36px;">&le; 0.48%</div>
        <span style="font-size:13px; color:var(--text-muted);">Duality Gap at Stop</span>
      </div>
      <p style="font-size:14px; color:var(--text-secondary); margin-top:8px; line-height:1.5;">
        Industrial control systems cannot afford unbounded execution. NIYAM-X tracks monotone feasibility bounds: guaranteed valid candidate solution available at any interruption moment.
      </p>
    </div>

    <div class="card">
      <div class="metric-label">Precision Escalator</div>
      <div style="display:flex; flex-direction:column; gap:8px; margin-top:10px; font-family:monospace; font-size:13px;">
        <div style="display:flex; justify-content:space-between; padding:8px 12px; background:#07090e; border-radius:6px;">
          <span>Stage 1: FP32 High-Throughput Preconditioning</span>
          <span style="color:var(--success);">PASS</span>
        </div>
        <div style="display:flex; justify-content:space-between; padding:8px 12px; background:#07090e; border-radius:6px;">
          <span>Stage 2: FP64 Accurate Residual Convergence</span>
          <span style="color:var(--success);">ACTIVE</span>
        </div>
        <div style="display:flex; justify-content:space-between; padding:8px 12px; background:#07090e; border-radius:6px;">
          <span>Stage 3: Iterative Refinement Polish</span>
          <span style="color:var(--accent-light);">READY</span>
        </div>
      </div>
    </div>
  </div>

  <div class="card" style="display:flex; flex-direction:column;">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
      <div class="metric-label">Flight Recorder Telemetry Stream (JSONL)</div>
      <span style="font-family:monospace; font-size:12px; color:var(--accent-light);">SSE LIVE REPLAY READY</span>
    </div>
    <div style="flex:1; background:#07090e; border:1px solid var(--border); border-radius:8px; padding:14px; font-family:monospace; font-size:12px; line-height:1.7; color:#94a3b8; overflow:hidden;">
      <div style="color:#64748b;">// JSONL Structured Flight Recorder Stream</div>
      <div>{"ts": "18:40:02.104", "event": "ITER_STEP", "iter": 200, "obj": 31.8492, "res_p": 4.12e-4, "res_d": 8.91e-4}</div>
      <div>{"ts": "18:40:02.321", "event": "ITER_STEP", "iter": 400, "obj": 31.8310, "res_p": 1.28e-5, "res_d": 2.45e-5}</div>
      <div>{"ts": "18:40:02.580", "event": "ITER_STEP", "iter": 800, "obj": 31.8241, "res_p": 3.82e-6, "res_d": 7.19e-6}</div>
      <div>{"ts": "18:40:02.844", "event": "ITER_STEP", "iter": 1200, "obj": 31.8209, "res_p": 8.91e-7, "res_d": 1.42e-6}</div>
      <div style="color:var(--success);">{"ts": "18:40:03.012", "event": "CONVERGENCE_MET", "iter": 1420, "final_obj": 31.8201, "res_p": 2.41e-7, "res_d": 6.18e-7}</div>
      <div style="color:var(--accent-light);">{"ts": "18:40:03.045", "event": "PROOF_PACK_EMITTED", "hash": "sha256:d8b2e1a49f..."}</div>
    </div>
  </div>
</div>
"""

# SCENE 13
s13_content = """
<div style="flex:1; display:grid; grid-template-columns: 1fr 1.2fr; gap:30px; align-items:center;">
  <div style="display:flex; flex-direction:column; gap:20px;">
    <div class="card" style="border-left:4px solid var(--success);">
      <div style="display:flex; align-items:center; gap:12px; margin-bottom:8px;">
        <span style="font-size:28px;">🛡️</span>
        <span style="font-size:22px; font-weight:800; color:var(--text-primary);">Independent Verifier</span>
      </div>
      <p style="font-size:15px; color:var(--text-secondary); line-height:1.6;">
        Trust in critical infrastructure requires mathematical verification. The Independent Verifier operates in a decoupled sandbox, checking mathematical invariants from scratch without trusting solver flags.
      </p>
    </div>

    <div class="card">
      <div class="metric-label">Proof Pack Digital Artifact</div>
      <div style="margin-top:10px; font-family:monospace; font-size:13px; color:var(--text-secondary); display:flex; flex-direction:column; gap:6px;">
        <div>&bull; SHA-256 Checksum: <span style="color:var(--accent-light);">9a8f...3e2b</span></div>
        <div>&bull; Primal Bounds: Validated [0.0 &le; x &le; u]</div>
        <div>&bull; Constraint Feasibility: Max viol &le; 1e-6</div>
        <div>&bull; Reconstructed Objective: Matches within 1e-9</div>
      </div>
    </div>
  </div>

  <div class="card" style="border:1px solid var(--success); background:rgba(18, 24, 36, 0.95); display:flex; flex-direction:column; gap:16px;">
    <div style="display:flex; justify-content:space-between; align-items:center;">
      <span style="font-size:18px; font-weight:800; color:var(--success);">NIYAM-X VERIFICATION AUDIT REPORT</span>
      <span style="padding:4px 10px; background:var(--success); color:#07090e; font-weight:900; border-radius:4px; font-size:12px;">PASSED</span>
    </div>

    <div style="display:flex; flex-direction:column; gap:10px; font-family:monospace; font-size:14px;">
      <div style="display:flex; justify-content:space-between; padding:10px 14px; background:#07090e; border-radius:6px;">
        <span>Primal Linear Constraints (Ax &le; b)</span>
        <span style="color:var(--success); font-weight:700;">&check; VERIFIED (&le; 2.4e-7)</span>
      </div>
      <div style="display:flex; justify-content:space-between; padding:10px 14px; background:#07090e; border-radius:6px;">
        <span>Variable Lower/Upper Bounds</span>
        <span style="color:var(--success); font-weight:700;">&check; ZERO VIOLATIONS</span>
      </div>
      <div style="display:flex; justify-content:space-between; padding:10px 14px; background:#07090e; border-radius:6px;">
        <span>Independent Objective Reconstruction</span>
        <span style="color:var(--success); font-weight:700;">&check; EXACT (₹ 31.8201 Cr)</span>
      </div>
      <div style="display:flex; justify-content:space-between; padding:10px 14px; background:#07090e; border-radius:6px;">
        <span>Dual Infeasibility Check (A<sup>T</sup>y + c)</span>
        <span style="color:var(--success); font-weight:700;">&check; WITHIN TOLERANCE</span>
      </div>
      <div style="display:flex; justify-content:space-between; padding:10px 14px; background:#07090e; border-radius:6px;">
        <span>Complementary Slackness</span>
        <span style="color:var(--success); font-weight:700;">&check; FEASIBLE</span>
      </div>
    </div>
  </div>
</div>
"""

# SCENE 14
s14_content = """
<div style="flex:1; display:flex; flex-direction:column; gap:20px;">
  <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px;">
    <div class="card">
      <div class="metric-label" style="margin-bottom:12px;">Benchmark & Validation Rig</div>
      <div style="display:flex; flex-direction:column; gap:10px; font-family:monospace; font-size:13px;">
        <div style="display:flex; justify-content:space-between; padding:10px; background:#07090e; border-radius:6px;">
          <span>Netlib LP Suite (Linear Programming)</span>
          <span style="color:var(--accent-light);">Continuous Test Rig</span>
        </div>
        <div style="display:flex; justify-content:space-between; padding:10px; background:#07090e; border-radius:6px;">
          <span>MIPLIB 2017 (Mixed-Integer Scale)</span>
          <span style="color:var(--accent-light);">Branch & Bound Roadmap</span>
        </div>
        <div style="display:flex; justify-content:space-between; padding:10px; background:#07090e; border-radius:6px;">
          <span>Industrial Refinery Models</span>
          <span style="color:var(--success);">End-to-End Operational</span>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="metric-label" style="margin-bottom:12px;">Full Production Tech Stack</div>
      <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px; font-size:13px;">
        <div style="padding:10px; background:#07090e; border-radius:6px;">
          <div style="font-weight:700; color:var(--accent-light);">Numerical Core</div>
          <div style="color:var(--text-muted); font-size:12px;">C++20, CUDA 12.8, Eigen/SpMV</div>
        </div>
        <div style="padding:10px; background:#07090e; border-radius:6px;">
          <div style="font-weight:700; color:var(--accent-light);">Orchestration</div>
          <div style="color:var(--text-muted); font-size:12px;">FastAPI, Uvicorn, Python 3.14</div>
        </div>
        <div style="padding:10px; background:#07090e; border-radius:6px;">
          <div style="font-weight:700; color:var(--accent-light);">Command Workbench</div>
          <div style="color:var(--text-muted); font-size:12px;">React 19, TypeScript, Vite, Tailwind</div>
        </div>
        <div style="padding:10px; background:#07090e; border-radius:6px;">
          <div style="font-weight:700; color:var(--accent-light);">State & Telemetry</div>
          <div style="color:var(--text-muted); font-size:12px;">SQLite, SQLAlchemy, SSE / JSONL</div>
        </div>
      </div>
    </div>
  </div>

  <div class="card" style="flex:1; display:flex; flex-direction:column; justify-content:center;">
    <div class="metric-label" style="margin-bottom:14px;">Development Roadmap & Phased Scaling</div>
    <div style="display:flex; align-items:center; justify-content:space-between; font-family:monospace; font-size:13px;">
      <div style="padding:14px; background:rgba(2, 132, 199, 0.2); border:1px solid var(--accent); border-radius:8px; text-align:center; width:22%;">
        <div style="color:var(--accent-light); font-weight:800;">PHASE 1 (Now)</div>
        <div style="font-size:12px; color:var(--text-secondary); margin-top:4px;">Verified LP Core & CUDA PDHG</div>
      </div>
      <span style="color:var(--accent); font-size:20px;">&rarr;</span>
      <div style="padding:14px; background:rgba(2, 132, 199, 0.2); border:1px solid var(--accent); border-radius:8px; text-align:center; width:22%;">
        <div style="color:var(--accent-light); font-weight:800;">PHASE 2</div>
        <div style="font-size:12px; color:var(--text-secondary); margin-top:4px;">Model X-Ray & Autopilot</div>
      </div>
      <span style="color:var(--accent); font-size:20px;">&rarr;</span>
      <div style="padding:14px; background:rgba(2, 132, 199, 0.2); border:1px solid var(--accent); border-radius:8px; text-align:center; width:22%;">
        <div style="color:var(--accent-light); font-weight:800;">PHASE 3</div>
        <div style="font-size:12px; color:var(--text-secondary); margin-top:4px;">DeltaSolve & Scenario Swarm</div>
      </div>
      <span style="color:var(--accent); font-size:20px;">&rarr;</span>
      <div style="padding:14px; background:rgba(16, 185, 129, 0.2); border:1px solid var(--success); border-radius:8px; text-align:center; width:22%;">
        <div style="color:var(--success); font-weight:800;">PHASE 4</div>
        <div style="font-size:12px; color:var(--text-secondary); margin-top:4px;">Full MILP & Distributed GPU</div>
      </div>
    </div>
  </div>
</div>
"""

# SCENE 15
s15_content = """
<div style="flex:1; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; gap:24px;">
  <div style="display:flex; align-items:center; gap:16px; margin-bottom:8px;">
    <div style="width:72px; height:72px; border-radius:18px; background:linear-gradient(135deg, #0284c7, #38bdf8); display:flex; align-items:center; justify-content:center; font-size:32px; font-weight:900; color:#07090e; box-shadow:0 0 40px rgba(56, 189, 248, 0.6);">
      NX
    </div>
    <div style="text-align:left;">
      <div style="font-size:42px; font-weight:900; letter-spacing:3px; color:var(--text-primary);">NIYAM-X</div>
      <div style="font-size:16px; font-weight:600; color:var(--accent-light); letter-spacing:1px;">SOVEREIGN ADAPTIVE OPTIMIZATION ENGINE</div>
    </div>
  </div>

  <div style="font-size:24px; font-weight:800; color:var(--text-primary); letter-spacing:1px; max-width:800px; line-height:1.5;">
    Diagnose the Model. Solve Intelligently. Adapt to Reality. Verify the Decision.
  </div>

  <div style="display:flex; gap:20px; margin-top:12px;">
    <span style="padding:10px 24px; background:rgba(21, 29, 46, 0.8); border:1px solid var(--border); border-radius:8px; font-weight:700; font-size:15px; color:var(--accent-light);">
      Smart India Hackathon 2026
    </span>
    <span style="padding:10px 24px; background:rgba(21, 29, 46, 0.8); border:1px solid var(--border); border-radius:8px; font-weight:700; font-size:15px; color:var(--success);">
      Problem Statement 26119
    </span>
    <span style="padding:10px 24px; background:rgba(21, 29, 46, 0.8); border:1px solid var(--border); border-radius:8px; font-weight:700; font-size:15px; color:var(--text-primary);">
      Team TRINETRA 05
    </span>
  </div>
</div>
"""

ALL_SCENES = [
    (1, "The Industrial Optimization Problem", "OVERVIEW", "FOUNDATION & CONTEXT", s1_content),
    (2, "The Core Problem & Our 4-Stage Approach", "ALL", "ARCHITECTURE & PARADIGM", s2_content),
    (3, "Model Ingestion & Representation", "DIAGNOSE", "DATA LAYER & IR", s3_content),
    (4, "Model X-Ray Diagnostic Engine", "DIAGNOSE", "MATHEMATICAL HEALTH CHECK", s4_content),
    (5, "Model Fingerprint & Solver Autopilot", "DIAGNOSE", "INTELLIGENT DISPATCH", s5_content),
    (6, "NIYAM-X C++20 / CUDA Solver Core", "SOLVE", "NUMERICAL KERNELS", s6_content),
    (7, "GPU Execution & Real-Time Convergence", "SOLVE", "RESIDUAL TELEMETRY", s7_content),
    (8, "Industrial Refinery Optimal Solution", "SOLVE", "DECISION SYNTHESIS", s8_content),
    (9, "Reality Changes: Parameter Shock Event", "ADAPT", "MARKET DISRUPTION", s9_content),
    (10, "DeltaSolve: Warm Re-Optimization", "ADAPT", "STATE PRESERVATION", s10_content),
    (11, "Scenario Analysis & Scenario Swarm", "ADAPT", "SENSITIVITY EXPLORATION", s11_content),
    (12, "Decision Stability, Anytime Mode & Flight Recorder", "ADAPT", "AUDIT & TELEMETRY", s12_content),
    (13, "Proof Pack & Independent Mathematical Verifier", "VERIFY", "INDEPENDENT TRUST LAYER", s13_content),
    (14, "Validation, Benchmarking & Tech Stack", "VERIFY", "SCALE & ROADMAP", s14_content),
    (15, "Sovereign Optimization for Modern Industry", "OVERVIEW", "SOVEREIGN SEAL & SIH 2026", s15_content),
]

for clip_id, title, pillar, tag, content in ALL_SCENES:
    file_path = os.path.join(SCENES_DIR, f"scene_{clip_id:02d}.html")
    html_code = make_html(clip_id, title, pillar, tag, content)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_code)
    print(f"Generated scene_{clip_id:02d}.html")

print("\nAll 15 scene templates generated in e:\\Niyan\\video_production\\scenes")
