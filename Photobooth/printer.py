import cups
import tempfile

# Check CUPS availability at module load
try:
    conn = cups.Connection()
    cups_available = True
    print("Printer system ready")
except Exception as e:
    cups_available = False
    print(f"Printer system unavailable: {str(e)}")

def print_pdf(pdf_data, printer_name=None):
    """Print PDF document"""
    if not cups_available:
        raise RuntimeError("Printing system not available")

    try:
        printers = conn.getPrinters()
        if not printers:
            raise RuntimeError("No printers available")
            
        printer = printer_name or conn.getDefault() or list(printers.keys())[0]
        print(f"Using printer: {printer}")
        
        with tempfile.NamedTemporaryFile(suffix='.pdf') as tmp:
            tmp.write(pdf_data)
            tmp.flush()
            print(f"Printing temporary file: {tmp.name}")
            
            job_id = conn.printFile(printer, tmp.name, "PDF Print Job", {})
            print(f"Print job ID: {job_id}")
            return job_id
            
    except Exception as e:
        print(f"Print error occurred: {str(e)}")
        raise