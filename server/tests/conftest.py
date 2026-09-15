import os

os.environ.setdefault("database_url", "postgresql://postgres:postgres@localhost:5432/eigent")
os.environ.setdefault("secret_key", "test-secret-key")
