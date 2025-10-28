import logging
import os
import azure.functions as func

# Directory where text/html files are stored (relative to function folder)
TEXT_FILES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "textfiles"))

ALLOWED_EXT = {".txt", ".html"}

def _is_safe_path(base_dir: str, target_path: str) -> bool:
    """Ensure the requested file path is within the allowed directory."""
    try:
        base = os.path.abspath(base_dir)
        target = os.path.abspath(target_path)
        return os.path.commonpath([base]) == os.path.commonpath([base, target])
    except Exception:
        return False

def main(req: func.HttpRequest) -> func.HttpResponse:
    client_ip = req.headers.get("X-Forwarded-For", req.headers.get("X-Client-IP", "Unknown IP"))
    filename = req.params.get("filename")

    # Log the incoming request details
    logging.info(f"Request received from {client_ip} | URL: {req.url} | Filename: {filename}")

    if not filename:
        return func.HttpResponse("Missing filename parameter.", status_code=400)

    _, ext = os.path.splitext(filename)
    ext = ext.lower()
    if ext not in ALLOWED_EXT:
        logging.warning(f"Invalid file extension attempt from {client_ip}: {filename}")
        return func.HttpResponse("Invalid file extension; only .txt and .html are allowed.", status_code=400)

    # Compute full file path
    file_path = os.path.abspath(os.path.join(TEXT_FILES_DIR, filename))

    # Prevent directory traversal
    if not _is_safe_path(TEXT_FILES_DIR, file_path):
        logging.warning(f"Directory traversal attempt blocked from {client_ip}: {filename}")
        return func.HttpResponse("Access denied.", status_code=403)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        mimetype = "text/html" if ext == ".html" else "text/plain"
        logging.info(f"Successfully served {filename} to {client_ip}")
        return func.HttpResponse(content, mimetype=mimetype, status_code=200)

    except FileNotFoundError:
        logging.warning(f"File not found: {filename} requested by {client_ip}")
        return func.HttpResponse("File not found in directory.", status_code=404)
    except Exception as e:
        logging.error(f"Error reading file {filename} requested by {client_ip}: {e}")
        return func.HttpResponse("Internal server error.", status_code=500)