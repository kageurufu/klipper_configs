from kalico import Kalico, gcode_macro


@gcode_macro
def push_notification(k: Kalico, body: str, title: str = None):
    if title:
        k.respond_info(f"MR_NOTIFY:{title}|{body}")
    else:
        k.respond_info(f"MR_NOTIFY:{body}")
