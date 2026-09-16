import uuid

def generate_id(prefix: str) -> str:
    """Generate a prefixed unique ID, e.g. mod_a1b2c3d4e5f6."""
    raw = uuid.uuid4().hex[:12]
    return f"{prefix}_{raw}"

def model_id() -> str:
    return generate_id("mod")

def version_id() -> str:
    return generate_id("ver")

def analysis_id() -> str:
    return generate_id("ana")

def solve_id() -> str:
    return generate_id("slv")

def verification_id() -> str:
    return generate_id("vrf")

def benchmark_id() -> str:
    return generate_id("bnk")

def scenario_schema_id() -> str:
    return generate_id("sch")
