import tempfile

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

        conn = cups.Connection()
        printer = printer_name or conn.getDefault()
        conn.printFile(printer, temp.name, "Flask Job", {})