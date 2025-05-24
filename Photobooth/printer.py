import tempfile
import os

try:
    import cups
    cups_available = True
except ImportError:
    cups = None
    cups_available = False

def print_pdf(binary_data, printer_name=None):
    if not cups_available:
        raise RuntimeError("CUPS/pycups not available on this platform")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
        temp.write(binary_data)
        temp.flush()
        temp_path = temp.name

    try:
        print(f"[DEBUG] Binary type: {type(binary_data)}")
        print(f"[DEBUG] Temp path: {temp_path}")

        conn = cups.Connection()
        printer = printer_name or conn.getDefault()
        if not printer:
            raise RuntimeError("No default printer found and none specified.")
        print(f"[DEBUG] Using printer: {printer}")

        job_id = conn.printFile(printer, temp_path, "Flask Job", {})
        print(f"[DEBUG] Job sent, ID: {job_id}")
    except Exception as e:
        print(f"[ERROR] Print failed: {e}")
        raise
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)