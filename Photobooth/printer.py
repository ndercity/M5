# printer.py
import cups
import tempfile
import os
import subprocess

def is_printer_online(printer_name="test_printer"):
    try:
        result = subprocess.run(["lpstat", "-p", printer_name], capture_output=True, text=True)
        output = result.stdout.strip()
        print("[DEBUG] lpstat output:", output)
        if "disabled" in output or "not connected" in output:
            return False
        return True
    except Exception as e:
        print(f"[Error] Could not check printer status: {e}")
        return False

def print_pdf(pdf_bytes, printer_name="test_printer"):
    
    """
    Print a PDF using CUPS
    Args:
        pdf_bytes: PDF content as bytes
        printer_name: Optional specific printer name. If None, uses default printer.
    Returns:
        bool: True if printing was successful
    """
    try:
        # Create a temporary PDF file
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_pdf:
            tmp_pdf.write(pdf_bytes)
            tmp_path = tmp_pdf.name
        
        # Connect to CUPS
        conn = cups.Connection()
        
        # Get default printer if none specified
        if not printer_name:
            printer_name = conn.getDefault()
            if not printer_name:
                print("[PRINT ERROR] No default printer found")
                return False
        
        # Print the file
        print_job_id = conn.printFile(printer_name, tmp_path, "Photo Booth Print", {})
        
        # Clean up
        os.remove(tmp_path)
        
        if print_job_id > 0:
            print(f"[PRINT] Successfully sent to printer {printer_name} (Job ID: {print_job_id})")
            return True
        else:
            print("[PRINT ERROR] Failed to send print job")
            return False
            
    except Exception as e:
        print(f"[PRINT ERROR] Printing failed: {e}")
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.remove(tmp_path)
        return False