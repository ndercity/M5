import cups
import tempfile
import time

def print_pdf(pdf_data, printer_name=None):
    """
    Print PDF with job verification
    Returns: (success: bool, job_id: int, message: str)
    """
    try:
        # 1. Connect to CUPS
        conn = cups.Connection()
        
        # 2. Select printer
        printers = conn.getPrinters()
        if not printers:
            return False, None, "No printers available"
            
        printer = printer_name or conn.getDefault() or list(printers.keys())[0]
        
        # 3. Create temp file
        with tempfile.NamedTemporaryFile(suffix='.pdf') as tmp:
            tmp.write(pdf_data)
            tmp.flush()
            
            # 4. Submit job
            job_id = conn.printFile(printer, tmp.name, "PDF Print", {})
            
            # 5. Verify job completion
            for _ in range(10):  # Check for 10 seconds
                time.sleep(1)
                job_info = conn.getJobAttributes(job_id)
                if job_info['job-state'] == 9:  # 9 = completed
                    return True, job_id, "Print successful"
                elif job_info['job-state'] in (5, 6, 7):  # 5=held, 6=stopped, 7=canceled
                    return False, job_id, f"Print failed - state {job_info['job-state']}"
            
            return False, job_id, "Print timed out"
            
    except cups.IPPError as e:
        return False, None, f"Printer error: {e.message}"
    except Exception as e:
        return False, None, f"Print failed: {str(e)}"