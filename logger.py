from datetime import datetime, timezone

def Log(type: str, msg: str):
    now = datetime.now(timezone.utc)
    iso_time = now.isoformat()

    print(f"{iso_time}: {type.capitalize()} {msg}")
