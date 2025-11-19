import os

# ensure these are set before pytest imports any test modules that import the app
os.environ.setdefault("MODE", "test")