import base64


def encode64(message: str) -> bytes:
    token = base64.b64encode(message.encode()).decode("ascii")
    return token


def decode64(token: bytes) -> str:
    message: bytes = base64.b64decode(token)
    return message.decode()
