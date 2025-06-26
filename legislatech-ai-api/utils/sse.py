# utils/sse.py
import json

def make_sse_event(event_name: str, data_payload: dict | str) -> str:
    """Formata dados para o padrão Server-Sent Event (SSE)."""
    if isinstance(data_payload, dict):
        data_str = json.dumps(data_payload, ensure_ascii=False)
    else:
        data_str = data_payload
    return f"event: {event_name}\ndata: {data_str}\n\n"