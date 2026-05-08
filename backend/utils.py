"""
Utility functions shared across the application.
"""

import os
from pathlib import Path
from datetime import datetime


def ensure_directories():
    """Create all required directories if they don't exist."""
    # ✅ Use /tmp for HuggingFace Spaces writable storage
    dirs = ["/tmp/uploaded_docs", "/tmp/chroma_db", "assets"]
    for d in dirs:
        Path(d).mkdir(exist_ok=True)


def get_file_size_str(size_bytes: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def get_uploaded_files_info() -> list:
    # ✅ Use /tmp for HuggingFace Spaces writable storage
    upload_dir = Path("/tmp/uploaded_docs")
    if not upload_dir.exists():
        return []

    files = []
    for f in upload_dir.glob("*.pdf"):
        stat = f.stat()
        files.append({
            "name": f.name,
            "path": str(f),
            "size_bytes": stat.st_size,
            "size_str": get_file_size_str(stat.st_size),
            "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%b %d, %Y %H:%M"),
        })

    return sorted(files, key=lambda x: x["modified"], reverse=True)


def sanitize_filename(filename: str) -> str:
    keepchars = (" ", ".", "_", "-")
    return "".join(c for c in filename if c.isalnum() or c in keepchars).rstrip()
