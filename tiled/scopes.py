SCOPES = {
    "inherit": {
        "description": "Default scope for API keys. Inherit scopes of Principal, resolved at access time."
    },
    "read:metadata": {"description": "Read metadata."},
    "read:data": {"description": "Read data."},
    "write:metadata": {"description": "Write metadata."},
    "write:data": {"description": "Write data."},
    "metrics": {"description": "Access (Prometheus) metrics."},
    "apikeys": {
        "description": "Create and revoke API keys as the currently-authenticated user or service."
    },
    "admin:apikeys": {
        "description": "Create and revoke API keys on behalf of any user or service."
    },
    "read:principals": {
        "description": "Read list of all users and services and their attributes."
    },
}
