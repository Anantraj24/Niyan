import asyncio
import os
import json
import subprocess
import edge_tts

CLIPS = [
    {
        "id": 1,
        "title": "The Industrial Optimization Problem",
        "target_sec": 25,
        "text": "Modern industries constantly make complex optimization decisions: how much raw material to buy, how to allocate limited resources, how to schedule production, and how to react when prices, demand, or capacity change. These decisions can involve large mathematical models with thousands of variables and constraints. Reliable optimization is critical to industrial planning. NIYAM-X is our proposed sovereign optimization engine for this challenge."
    },
    {
        "id": 2,
        "title": "The Core Problem and Our Approach",
        "target_sec": 25,
        "text": "NIYAM-X is designed around a complete optimization workflow, not a simple black-box solver. Instead of only receiving a model and returning an answer, the system first diagnoses its mathematical structure, builds a Model Fingerprint, selects an appropriate solving configuration, and solves using its own optimization core. When conditions change, it can adapt the solution, compare scenarios, and independently verify the result."
    },
    {
        "id": 3,
        "title": "Model Input",
        "target_sec": 25,
        "text": "The process begins with the optimization model. NIYAM-X is designed to accept standard representations including JSON, LP, and MPS. For our industrial demonstration, we use a refinery-style model containing variables, constraints, and a large sparse coefficient structure. Before optimization begins, the model is validated and converted into an internal representation, giving the rest of the system a consistent foundation for analysis, solving, and verification."
    },
    {
        "id": 4,
        "title": "Model X-Ray",
        "target_sec": 25,
        "text": "NIYAM-X does not immediately start solving. Model X-Ray first examines the mathematical model. It measures properties such as sparsity, coefficient range, fixed variables, poorly scaled rows, bounds, structure, and numerical risk. This analysis exposes characteristics that can affect numerical behavior before an algorithm is selected. The result is a detailed diagnostic view that helps the system understand what it is about to solve."
    },
    {
        "id": 5,
        "title": "Model Fingerprint and Autopilot",
        "target_sec": 25,
        "text": "These diagnostics become the Model Fingerprint: a compact description of the model's structure, density, integer ratio, coefficient spread, equality ratio, bounds, block structure, and potential degeneracy. Solver Autopilot uses this fingerprint to select an appropriate configuration, including algorithm, scaling, execution backend, precision, and warm-start behavior. In the prototype, this selection is deterministic and rule-based, making the decision explainable and reproducible."
    },
    {
        "id": 6,
        "title": "NIYAM-X Solver Core",
        "target_sec": 25,
        "text": "At the center is the NIYAM-X solver core. The prototype begins with Linear Programming and sparse CSR and CSC matrix operations. The initial LP method uses Primal-Dual Hybrid Gradient, or PDHG. Its main operations, including matrix-vector multiplication, transpose multiplication, vector updates, projections, and reductions, map naturally to accelerated computation. The architecture supports a CUDA GPU backend while keeping CPU execution available as a fallback."
    },
    {
        "id": 7,
        "title": "GPU Execution and Live Solving",
        "target_sec": 25,
        "text": "During optimization, NIYAM-X continuously tracks the solver state instead of hiding the computation behind a single progress bar. The live dashboard exposes iterations, objective value, primal residual, dual residual, and convergence behavior. These signals help show whether the numerical process is progressing toward a feasible solution. GPU execution accelerates sparse computation, while the same solver architecture can fall back to the CPU when required."
    },
    {
        "id": 8,
        "title": "Industrial Solution",
        "target_sec": 25,
        "text": "Once the solver reaches its stopping conditions, NIYAM-X produces optimized decision variables, the objective value, solver statistics, and exportable artifacts. In the refinery scenario, those decisions can represent an optimized production or blending plan while respecting the model's constraints. The result is not the end of the workflow, because industrial planning is dynamic. The next question is what happens when market conditions change."
    },
    {
        "id": 9,
        "title": "Reality Changes",
        "target_sec": 25,
        "text": "Now we introduce a realistic scenario change. Crude A price increases by eight percent and demand increases by four percent, while capacity remains unchanged. A conventional static workflow could require the modified problem to be solved again from scratch. NIYAM-X is designed for this situation through DeltaSolve, which carries useful information from the previous optimization state into the updated problem instead of discarding the work already performed."
    },
    {
        "id": 10,
        "title": "DeltaSolve",
        "target_sec": 25,
        "text": "DeltaSolve is NIYAM-X's warm re-optimization layer. It can reuse the previous primal and dual states, scaling information, model structure, and other relevant solver state. The changed parameters are incorporated into the updated scenario, and the solver starts from an informed state. This design is intended for changing prices, demand, capacity, availability, and other operational parameters that can alter an existing optimization plan."
    },
    {
        "id": 11,
        "title": "Scenario Analysis",
        "target_sec": 25,
        "text": "The same warm-state approach can be extended into scenario analysis and Scenario Swarm. Instead of evaluating only one future condition, NIYAM-X can explore multiple combinations of price, demand, capacity, outages, and operational assumptions. Shared model structure and solver state can support these comparisons. Planners can examine different objectives, convergence behavior, and decision stability to understand how sensitive a proposed operating plan is to future changes."
    },
    {
        "id": 12,
        "title": "Decision Stability, Anytime Mode and Telemetry",
        "target_sec": 25,
        "text": "Around the solver, NIYAM-X provides telemetry and decision-analysis capabilities. Scenario results can be compared for objective stability and operational sensitivity. The Flight Recorder captures solver history and structured telemetry for replay, debugging, and analysis. An Anytime-style workflow can expose the best validated solution available so far if computation is interrupted. Precision escalation and numerical monitoring provide additional safeguards when difficult models require greater numerical care."
    },
    {
        "id": 13,
        "title": "Proof Pack and Independent Verification",
        "target_sec": 25,
        "text": "Trust is a separate layer in NIYAM-X. After solving, the system generates a Proof Pack containing solution evidence and numerical checks. An Independent Verifier then checks feasibility, variable bounds, objective reconstruction, primal residuals, dual residuals, and other consistency information without simply trusting the optimizer's status flag. This separation is designed to make optimization results more auditable, reproducible, and easier to validate before they influence an industrial decision."
    },
    {
        "id": 14,
        "title": "Validation, Feasibility, Technology and Scale",
        "target_sec": 25,
        "text": "NIYAM-X is designed for incremental validation and scale. The roadmap starts with a verified LP core, sparse computation, and basic verification, then adds CUDA acceleration, Model X-Ray and Autopilot, DeltaSolve and scenarios, and broader MILP support with benchmarking. Validation can include Netlib, MIPLIB, Mittelmann, and industrial-style models. The stack combines C++20 and CUDA for computation, FastAPI for orchestration, and React with TypeScript for visualization."
    },
    {
        "id": 15,
        "title": "Final Message & Sovereign Core",
        "target_sec": 10,
        "text": "NIYAM-X diagnoses the model, solves it intelligently, adapts as reality changes, and independently verifies the decision — a sovereign optimization engine for modern industry."
    }
]

VOICE = "en-US-ChristopherNeural"
OUTPUT_DIR = r"E:\Niyan\video_production\audio"

def get_audio_duration(file_path):
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        file_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(res.stdout.strip())

async def generate_speech():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    results = []
    
    for clip in CLIPS:
        clip_id = clip["id"]
        raw_path = os.path.join(OUTPUT_DIR, f"clip_{clip_id:02d}_raw.mp3")
        fitted_path = os.path.join(OUTPUT_DIR, f"clip_{clip_id:02d}_fitted.mp3")
        padded_path = os.path.join(OUTPUT_DIR, f"clip_{clip_id:02d}_voiced.mp3")
        
        target_sec = clip["target_sec"]
        max_speech_sec = target_sec - 1.5 if target_sec > 12 else target_sec - 0.8
        
        print(f"Generating narration for Clip {clip_id:02d}: {clip['title']}...")
        communicate = edge_tts.Communicate(clip["text"], VOICE, rate="+16%")
        await communicate.save(raw_path)
        
        raw_duration = get_audio_duration(raw_path)
        
        # If speech exceeds max_speech_sec, adjust tempo cleanly
        if raw_duration > max_speech_sec:
            speed_factor = raw_duration / max_speech_sec
            tempo_cmd = [
                "ffmpeg", "-y",
                "-i", raw_path,
                "-af", f"atempo={speed_factor:.3f}",
                fitted_path
            ]
            subprocess.run(tempo_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            speech_file = fitted_path
        else:
            speech_file = raw_path
            
        speech_dur = get_audio_duration(speech_file)
        
        # Pad with silence to exact target_sec
        pad_cmd = [
            "ffmpeg", "-y",
            "-i", speech_file,
            "-af", f"apad=whole_dur={target_sec}",
            "-t", str(target_sec),
            padded_path
        ]
        subprocess.run(pad_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        final_dur = get_audio_duration(padded_path)
        
        print(f"  Clip {clip_id:02d}: Raw {raw_duration:.2f}s -> Fitted {speech_dur:.2f}s -> Padded {final_dur:.2f}s (Target: {target_sec}s)")
        results.append({
            "id": clip_id,
            "title": clip["title"],
            "raw_duration": raw_duration,
            "speech_duration": speech_dur,
            "final_duration": final_dur,
            "audio_file": padded_path
        })
        
    with open(os.path.join(OUTPUT_DIR, "audio_manifest.json"), "w") as f:
        json.dump(results, f, indent=2)
        
    total_time = sum(r["final_duration"] for r in results)
    print(f"\nAll 15 clips successfully synthesized! Total runtime: {total_time:.2f} seconds ({total_time/60:.2f} minutes)")

if __name__ == "__main__":
    asyncio.run(generate_speech())
