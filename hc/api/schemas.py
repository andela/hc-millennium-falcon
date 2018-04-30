check = {
    "properties": {
        "name": {"type": "string"},
        "tags": {"type": "string"},
        "timeout": {"type": "number", "minimum": 60, "maximum": 31104000},
        "grace": {"type": "number", "minimum": 60, "maximum": 31104000},
        "channels": {"type": "string"}
    }
}
