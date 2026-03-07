from fastapi import Request

def rate_limit_key(request : Request):
    payload = request.state.jwt_payload

    if payload and payload.get("type") == "access":
        return f"user:{payload['sub']}"

    return request.client.host