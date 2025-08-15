def get_options(
    host: str,
    port: int,
    workers: int,
    logconfig_dict: dict,
) -> dict:
    return {
        "logconfig_dict": logconfig_dict,
        "bind": f"{host}:{port}",
        "workers": workers,
        "worker_class": "uvicorn.workers.UvicornWorker",
    }
