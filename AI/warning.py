# warning.py

def get_warning_level(count):
    if count == 0:
        return 0, "SAFE", (0, 255, 0)
    elif count <= 2:
        return 1, "WARNING", (0, 255, 255)
    elif count <= 5:
        return 2, "DANGER", (0, 165, 255)
    else:
        return 3, "CRITICAL", (0, 0, 255)
