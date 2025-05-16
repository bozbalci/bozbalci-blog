from ninja import Schema


class HealthResponse(Schema):
    motd: str
