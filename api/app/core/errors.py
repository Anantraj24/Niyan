from typing import Any
from fastapi import HTTPException, status

class NiyamException(HTTPException):
    def __init__(self, status_code: int, code: str, message: str, details: Any = None):
        super().__init__(status_code=status_code, detail={"code": code, "message": message, "details": details})
        self.code = code
        self.message = message
        self.details = details

class NotFoundException(NiyamException):
    def __init__(self, resource: str, resource_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code="NOT_FOUND",
            message=f"{resource} '{resource_id}' was not found"
        )

class ValidationException(NiyamException):
    def __init__(self, message: str, details: Any = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            code="VALIDATION_ERROR",
            message=message,
            details=details
        )

class ConflictException(NiyamException):
    def __init__(self, message: str, details: Any = None):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            code="CONFLICT",
            message=message,
            details=details
        )

class SolverProcessException(NiyamException):
    def __init__(self, message: str, details: Any = None):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="SOLVER_PROCESS_ERROR",
            message=message,
            details=details
        )
