"""
Django settings for Menulance Backend (Notebook).
"""
from menulance.settings_base import *

NOTEBOOK_ARGUMENTS = [
    "--ip",
    "0.0.0.0",
    "--port",
    env("NOTEBOOK_PORT", "8888"),
    "--no-browser",
    "--NotebookApp.allow_password_change=False",
]

if get_bool_env("ALLOW_ROOT", False):
    NOTEBOOK_ARGUMENTS.append("--allow-root")
if DEBUG:
    # 11
    NOTEBOOK_ARGUMENTS.append(
        "--NotebookApp.password='argon2:$argon2id$v=19$m=10240,t=10,p=8$jJ57sn8jo5JEmZPG2kCFow$dAmGRVOb80cJShCu43M0oA'"
    )
