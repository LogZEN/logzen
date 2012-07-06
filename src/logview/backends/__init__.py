from logview.backends.postgres.backend import PostgresBackend


def __init_backend():
    return PostgresBackend()

backend = __init_backend()
