from uuid import uuid4


def generate_request_id() -> str:
    return f"req-{uuid4().hex[:12]}"


def generate_ticket_id() -> str:
    return f"tkt-{uuid4().hex[:10]}"
