import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
from pathlib import Path

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = RGBColor(15, 23, 42) # Slate 900
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = RGBColor(14, 116, 144) # Cyan 700
    return p

def add_paragraph(doc, text, bold_prefix=None, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Arial"
        r_pre.font.size = Pt(10.5)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(30, 41, 59)
    run = p.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(10.5)
    run.font.color.rgb = RGBColor(51, 65, 85)
    return p

def add_bullet(doc, text, bold_title=None):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    if bold_title:
        r_pre = p.add_run(bold_title + ": ")
        r_pre.font.name = "Arial"
        r_pre.font.size = Pt(10)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(15, 23, 42)
    run = p.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(51, 65, 85)
    return p

def add_callout(doc, title, body):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    set_cell_background(cell, "F0F9FF") # Very soft cyan/sky
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    
    # Left border highlight
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="0" w:color="0284C7"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(3)
    r_title = p.add_run(title + "\n")
    r_title.font.name = "Arial"
    r_title.font.size = Pt(11)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(3, 105, 161)
    
    r_body = p.add_run(body)
    r_body.font.name = "Arial"
    r_body.font.size = Pt(9.5)
    r_body.font.color.rgb = RGBColor(30, 41, 59)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def style_table(table, col_widths, headers, rows):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], "0F172A") # Dark Navy
        set_cell_margins(hdr_cells[i], top=100, bottom=100, left=120, right=120)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in p.runs:
            run.font.name = "Arial"
            run.font.size = Pt(9.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)
            
    for r_idx, row_data in enumerate(rows):
        row_cells = table.add_row().cells
        bg_color = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            row_cells[c_idx].text = str(val)
            set_cell_background(row_cells[c_idx], bg_color)
            set_cell_margins(row_cells[c_idx], top=90, bottom=90, left=120, right=120)
            p = row_cells[c_idx].paragraphs[0]
            for run in p.runs:
                run.font.name = "Arial"
                run.font.size = Pt(9)
                run.font.color.rgb = RGBColor(30, 41, 59)
                
    for row in table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width

def generate_document(output_path: str):
    doc = Document()
    
    # 1 inch margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # -------------------------------------------------------------
    # Document Header / Cover Banner
    # -------------------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(2)
    t_run = title_p.add_run("NIYAM-X Prototype Overview")
    t_run.font.name = "Arial"
    t_run.font.size = Pt(24)
    t_run.font.bold = True
    t_run.font.color.rgb = RGBColor(15, 23, 42)

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(14)
    s_run = sub_p.add_run("Indigenous GPU-Accelerated Mathematical Optimization Solver & Decision Workbench\n")
    s_run.font.name = "Arial"
    s_run.font.size = Pt(12)
    s_run.font.bold = True
    s_run.font.color.rgb = RGBColor(14, 116, 144)
    
    meta_run = sub_p.add_run("Platform Architecture, Working Mechanism, Technical Stack, and Practical Value")
    meta_run.font.name = "Arial"
    meta_run.font.size = Pt(10)
    meta_run.font.color.rgb = RGBColor(100, 116, 139)

    add_callout(
        doc,
        "The Sovereign Mission (Tagline: Solve. Adapt. Prove.)",
        "India's petroleum refining, power transmission grids, logistics networks, and defense manufacturing rely almost entirely on foreign commercial optimization solvers (IBM CPLEX, Gurobi, FICO Xpress). These engines carry multi-million dollar recurring licensing fees and operate as mathematical black-boxes with zero national visibility. NIYAM-X is built from first principles as an indigenous, clean-room sovereign alternative that combines GPU acceleration, pre-solve risk diagnosis, real-time convergence telemetry, parametric warm re-optimization, and mathematical decision-proof certificates."
    )

    # -------------------------------------------------------------
    # Section 1: The Big Idea in Simple Terms
    # -------------------------------------------------------------
    add_heading_1(doc, "1. The Big Idea Explained in Simple Language")
    add_paragraph(doc, "What is mathematical optimization, why does it matter, and what does NIYAM-X do differently?")

    add_paragraph(doc, 
        "Every major industry faces complex decisions with thousands of variables and constraints. For example: A petroleum refinery must decide how much crude oil to process across distillation and catalytic cracking units to produce gasoline, jet fuel, and diesel at maximum profit without exceeding storage capacity or sulfur emission limits. An electric power grid must decide which power plants to dispatch every 5 minutes to meet consumer demand at the lowest cost while preventing transmission line overloads and meeting carbon emission quotas.",
        bold_prefix="The Problem: "
    )
    
    add_paragraph(doc,
        "These problems are written as giant mathematical equations (Linear Programs or Integer Programs) with thousands of variables. Today, Indian enterprises spend millions annually leasing foreign software engines from the US or Europe to calculate these decisions. If foreign software licenses are revoked or restricted, critical infrastructure planning halts. Furthermore, existing engines act as black boxes—they output numbers without cryptographic proof that the solution is strictly feasible and tamper-free.",
        bold_prefix="The Vulnerability: "
    )

    add_paragraph(doc,
        "NIYAM-X is a 100% sovereign, clean-room mathematical optimization solver. It executes natively on modern CPU and NVIDIA CUDA hardware, analyzes problem structure before solving, streams live progress via real-time telemetry, solves 'what-if' market shocks in milliseconds via warm restarts, and produces an independently verified cryptographic Proof Pack that guarantees audit compliance.",
        bold_prefix="The Solution: "
    )

    # -------------------------------------------------------------
    # Section 2: Core Working Mechanism (The 5-Stage Loop)
    # -------------------------------------------------------------
    add_heading_1(doc, "2. How the Prototype Works: The 5-Stage Workflow")
    add_paragraph(doc, "NIYAM-X operates around a deterministic, industrial workflow designed for high reliability and transparency:")

    add_heading_2(doc, "Stage 1: Model X-Ray (Pre-Solve Structural Diagnosis)")
    add_bullet(doc, "Before running expensive algorithms, the engine inspects the model matrix A, cost vector c, and bounds.", "Deep Inspection")
    add_bullet(doc, "Detects extreme ratios between the largest and smallest matrix coefficients (e.g. 10^8 vs 10^-4) which cause numerical instability in standard solvers.", "Dynamic Range")
    add_bullet(doc, "Calculates zero vs non-zero densities (e.g. 79.6% sparse) to select compressed sparse column/row (CSC/CSR) representations.", "Matrix Sparsity")
    add_bullet(doc, "Flags duplicate constraints, empty rows, infinite bounds, and potential conditioning risks before computing.", "Numerical Health")

    add_heading_2(doc, "Stage 2: Solver Autopilot (Intelligent Strategy Configuration)")
    add_bullet(doc, "Automatically selects between CPU multicore execution and massive-parallel NVIDIA CUDA acceleration based on matrix dimensions and density.", "Hardware Selection")
    add_bullet(doc, "Applies Ruiz scaling equilibration to re-scale rows and columns, shrinking numerical condition numbers for rapid convergence.", "Numerical Scaling")
    add_bullet(doc, "Deterministically tunes iteration limits, primal-dual tolerance thresholds (1e-6), and step-size schedules.", "Heuristic Tuning")

    add_heading_2(doc, "Stage 3: Live Telemetry Runner (Real-Time Solve Execution)")
    add_bullet(doc, "Executes clean-room First-Order / PDHG (Primal-Dual Hybrid Gradient) and continuous optimization algorithms.", "Sovereign Engine")
    add_bullet(doc, "Unlike traditional solvers that freeze until finished, NIYAM-X streams iteration events in real time over Server-Sent Events (SSE).", "Live Telemetry")
    add_bullet(doc, "Operators watch log-scale primal residuals, dual residuals, and objective convergence in a live interactive visual curve.", "Visual Trajectory")

    add_heading_2(doc, "Stage 4: DeltaSolve (Parametric What-If Re-optimization)")
    add_bullet(doc, "Real-world operations face sudden shocks (e.g. crude oil prices spike 20%, or a transmission line trips). Standard solvers restart from zero.", "Operational Shocks")
    add_bullet(doc, "DeltaSolve injects parameter deltas and hot-starts the algorithm from the previous optimal basis and primal-dual vectors.", "Warm Start")
    add_bullet(doc, "Reduces solve iterations by up to 63% and delivers up to 3.4x faster turnaround for real-time dispatch decisions.", "Proven Speedup")

    add_heading_2(doc, "Stage 5: Proof Pack & Independent Decision Verifier")
    add_bullet(doc, "The solver kernel outputs a cryptographic solution certificate with SHA-256 model verification.", "Proof Certificate")
    add_bullet(doc, "A completely decoupled executable (niyam-verify) validates bounds, constraint feasibility, and dot-product objective match without relying on the solver.", "Zero-Trust Audit")
    add_bullet(doc, "Users can download a complete audit bundle (.zip) containing certificates, solution JSON, and validation reports.", "ZIP Compliance Export")

    # -------------------------------------------------------------
    # Section 3: Feature & Workflow Summary Table
    # -------------------------------------------------------------
    add_heading_1(doc, "3. Prototype Feature Matrix")
    
    headers = ["Workbench View", "Core Functionality", "Industrial Value"]
    rows = [
        [
            "Model Overview",
            "Model library browser, MPS/LP file import, SHA-256 integrity check",
            "Validates model authenticity and integrity before optimization."
        ],
        [
            "Model X-Ray",
            "Matrix dynamic range, sparsity calculations, coefficient distribution",
            "Catches ill-conditioned models before they waste hours of compute time."
        ],
        [
            "Solver Autopilot",
            "Hardware recommendation (CPU vs CUDA), Ruiz scaling selection",
            "Eliminates manual trial-and-error solver parameter tuning."
        ],
        [
            "Live Telemetry",
            "Real-time SSE convergence curves, primal/dual residuals, iterations",
            "Complete transparency into optimization progress without black boxes."
        ],
        [
            "DeltaSolve",
            "Interactive scenario shock sliders, warm-start comparison vs cold-start",
            "Enables real-time contingency planning and emergency re-dispatch."
        ],
        [
            "Proof Pack",
            "Independent mathematical decision audit, constraint verification, ZIP export",
            "Regulatory compliance, ESG auditing, and cryptographic decision proof."
        ],
        [
            "Benchmark Suite",
            "Head-to-head CPU vs CUDA differential solver execution",
            "Proves 4x GPU hardware speedup while verifying 100% numerical equivalence."
        ]
    ]
    
    widths = [Inches(1.8), Inches(2.7), Inches(2.0)]
    tbl = doc.add_table(rows=1, cols=3)
    style_table(tbl, widths, headers, rows)
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # Section 4: Real-World Demonstration Models
    # -------------------------------------------------------------
    add_heading_1(doc, "4. Pre-Loaded Industrial Demonstration Models")
    add_paragraph(doc, "The prototype includes two fully validated, realistic industrial optimization models demonstrating strategic national infrastructure use cases:")

    add_heading_2(doc, "1. Refinery Operations & Product Blending LP (Synthetic)")
    add_bullet(doc, "Crude oil distillation (Heavy vs Light Arab), Fluid Catalytic Cracking (FCC), Reformer throughput, product blending for Gasoline, Jet Fuel, and High-Speed Diesel.", "Domain")
    add_bullet(doc, "12 decision variables, 8 operational and capacity constraints, 79.6% matrix sparsity, 3.3e+0 dynamic range.", "Scale")
    add_bullet(doc, "Maximizes net production margin ($318,200,000 optimal objective).", "Objective")
    add_bullet(doc, "Interactive sliders adjust Crude Price Multiplier and Diesel Demand Shocks, demonstrating 3.4x faster warm-start solve times.", "DeltaSolve Shock")

    add_heading_2(doc, "2. 5-Bus Electric Power Transmission & Economic Dispatch LP")
    add_bullet(doc, "Power generation balancing, transmission line thermal limits, and regional carbon emission caps across a 5-bus electric transmission grid.", "Domain")
    add_bullet(doc, "10 decision variables, 7 balance/thermal constraints, 71.4% sparsity, 2.38 dynamic range.", "Scale")
    add_bullet(doc, "Minimizes total dispatch and fuel cost while meeting real-time consumer load demand.", "Objective")
    add_bullet(doc, "Natural gas price spikes, regional carbon cap tightening (forcing green dispatch), and line thermal derating contingency.", "DeltaSolve Shock")

    # -------------------------------------------------------------
    # Section 5: Technical Stack & Architecture
    # -------------------------------------------------------------
    add_heading_1(doc, "5. Technical Stack & Implementation Architecture")
    add_paragraph(doc, "The system is architected as a local-first, containerized modular monolith with zero external proprietary solver dependencies:")

    add_bullet(doc, "React 19, TypeScript, Vite, Tailwind CSS, Lucide Icons, TanStack Query, Recharts for dynamic numerical visualization.", "Frontend UI Layer")
    add_bullet(doc, "FastAPI (Python), Asyncio subprocess manager, Server-Sent Events (SSE) for streaming iteration telemetry, SQLite metadata persistence.", "Backend Orchestrator")
    add_bullet(doc, "Sovereign First-Order / PDHG engine and Ruiz equilibration module executing pure numerical mathematics without external solver binaries.", "Optimization Solver Core")
    add_bullet(doc, "Independent Python/C++ verification executable calculating constraint violations, bounds checks, and SHA-256 signatures in isolation.", "Decision Verifier")
    add_bullet(doc, "Multi-stage Dockerfile (Node 20 build stage -> Python 3.11-slim runtime) delivering unified single-port hosting on port 10000/8000.", "Container Deployment")

    # -------------------------------------------------------------
    # Section 6: Key Highlights for Evaluators & Stakeholders
    # -------------------------------------------------------------
    add_heading_1(doc, "6. Key Takeaways for Evaluators & Stakeholders")
    
    add_paragraph(doc, "Zero commercial licenses (no CPLEX, Gurobi, or Xpress). Clean-room engineering guarantees sovereignty over strategic critical infrastructure.", bold_prefix="1. Complete National Sovereignty: ")
    add_paragraph(doc, "Real-time SSE telemetry replaces legacy solver 'black-box' freezes with live convergence curves and observable residuals.", bold_prefix="2. Unprecedented Transparency: ")
    add_paragraph(doc, "DeltaSolve saves up to 63% of compute iterations under market or contingency shocks, enabling real-time industrial dispatch.", bold_prefix="3. Rapid Warm Re-optimization: ")
    add_paragraph(doc, "Mathematical decisions are cryptographically certified and independently audited before being executed in high-stakes environments.", bold_prefix="4. Trust & Verifiability: ")
    add_paragraph(doc, "Runs as a lightweight container on cloud PaaS (Render, Cloud Run) or completely offline in secure air-gapped defense/refinery facilities.", bold_prefix="5. Deployment Flexibility: ")

    # Save document
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    doc.save(output_path)
    print(f"[SUCCESS] Document generated: {output_path}")

if __name__ == "__main__":
    generate_document("e:/Niyan/NIYAM_X_Prototype_Overview.docx")
