import platform
import subprocess
import psutil
from fastapi import APIRouter
from api.app.schemas.hardware import HardwareResponse, CPUInfo, GPUInfo

router = APIRouter(tags=["Hardware"])

@router.get("/hardware", response_model=HardwareResponse)
def get_hardware():
    cpu_name = platform.processor() or "Modern x86_64 CPU"
    cores = psutil.cpu_count(logical=True) or 8
    ram = psutil.virtual_memory().total

    cuda_available = False
    gpu_name = "CPU Only"
    vram = 0

    try:
        res = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"],
            capture_output=True,
            text=True,
            timeout=3
        )
        if res.returncode == 0 and res.stdout.strip():
            lines = res.stdout.strip().split("\n")
            first_gpu = lines[0].split(",")
            gpu_name = first_gpu[0].strip()
            vram_mb = int(first_gpu[1].strip())
            vram = vram_mb * 1024 * 1024
            cuda_available = True
    except Exception:
        pass

    return HardwareResponse(
        cpu=CPUInfo(
            name=cpu_name,
            logical_cores=cores,
            system_ram_bytes=ram
        ),
        gpu=GPUInfo(
            cuda_available=cuda_available,
            name=gpu_name,
            vram_bytes=vram
        )
    )
