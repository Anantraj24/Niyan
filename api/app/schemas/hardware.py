from pydantic import BaseModel

class CPUInfo(BaseModel):
    name: str
    logical_cores: int
    system_ram_bytes: int

class GPUInfo(BaseModel):
    cuda_available: bool
    name: str
    vram_bytes: int

class HardwareResponse(BaseModel):
    cpu: CPUInfo
    gpu: GPUInfo
