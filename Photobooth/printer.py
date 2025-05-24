import cups
import tempfile
import time
import os

def print_pdf(pdf_data, printer_name=None):
    try:
        conn = cups.Connection()

        printers = conn.getPrinters()
        if not printers:
            return False, None, "No printers available"

        printer = printer_name or conn.getDefault() or list(printers.keys())[0]

        # Save to disk properly
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(pdf_data)
            tmp.flush()
            pdf_path = tmp.name

        # Submit job after file is fully closed
        job_id = conn.printFile(printer, pdf_path, "PDF Print", {})

        # Monitor job
        for _ in range(10):
            time.sleep(1)
            job_info = conn.getJobAttributes(job_id)
            state = job_info.get("job-state")
            if state == 9:  # Completed
                return True, job_id, "Print successful"
            elif state in (5, 6, 7):
                return False, job_id, f"Print failed - state {state}"

        return False, job_id, "Print timed out"

    except cups.IPPError as e:
        return False, None, f"Printer error: {e.message}"
    except Exception as e:
        return False, None, f"Print failed: {str(e)}"
    finally:
        try:
            if pdf_path and os.path.exists(pdf_path):
                os.remove(pdf_path)
        except Exception:
            pass
