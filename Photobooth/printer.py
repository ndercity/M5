import tempfile
import os

try:
    import cups
    cups_available = True
except ImportError:
    cups = None
    cups_available = False

def print_pdf(pdf_data, printer_name=None, job_name="Photo Session Print"):
    """
    Prints PDF binary data using CUPS
    
    Args:
        pdf_data (bytes): Binary PDF data
        printer_name (str): Optional specific printer name
        job_name (str): Name for the print job
        
    Returns:
        int: The print job ID
        
    Raises:
        TypeError: If input is not bytes
        RuntimeError: For any printing failure
        ValueError: For invalid PDF data
    """
    # 1. Input Validation
    if not isinstance(pdf_data, (bytes, bytearray, memoryview)):
        raise TypeError(f"PDF data must be bytes-like object, got {type(pdf_data)}")
    
    if len(pdf_data) < 8:
        raise ValueError("PDF data too small to be valid")
    
    if not pdf_data.startswith(b'%PDF-'):
        app.logger.warning("PDF header missing - may still print but could be corrupted")

    # 2. CUPS Availability Check
    if not cups_available:
        raise RuntimeError("Printing unavailable (CUPS not installed)")

    # 3. Temporary File Handling
    temp_file = None
    try:
        # Create secure temp file (automatically deleted when closed)
        with tempfile.NamedTemporaryFile(prefix='print_', suffix='.pdf', delete=True) as temp_file:
            # Write binary data
            temp_file.write(pdf_data)
            temp_file.flush()  # Ensure all data is on disk
            
            app.logger.debug(f"Temporary PDF created at {temp_file.name} ({len(pdf_data)} bytes)")

            # 4. Printer Setup
            conn = cups.Connection()
            printers = conn.getPrinters()
            
            if not printers:
                raise RuntimeError("No printers available")
                
            app.logger.debug(f"Available printers: {list(printers.keys())}")
            
            # Select printer (fallback logic)
            printer = printer_name or conn.getDefault()
            if not printer and printers:
                printer = list(printers.keys())[0]
                
            if not printer:
                raise RuntimeError("No printer specified and no default available")
            
            # 5. Print Options
            print_options = {
                'media': 'A4',
                'fit-to-page': 'True',
                'print-quality': 3,  # High quality
                'sides': 'one-sided',
                'orientation-requested': 3  # Portrait
            }
            
            # 6. Submit Print Job
            app.logger.info(f"Submitting print job to {printer}")
            job_id = conn.printFile(
                printer,
                temp_file.name,
                job_name,
                print_options
            )
            
            app.logger.info(f"Print job submitted (ID: {job_id})")
            return job_id
            
    except cups.IPPError as e:
        error_msg = f"Printer error ({e.status_code}): {e.message}"
        app.logger.error(error_msg)
        raise RuntimeError(error_msg) from e
    except IOError as e:
        error_msg = f"File system error: {str(e)}"
        app.logger.error(error_msg)
        raise RuntimeError(error_msg) from e
    except Exception as e:
        error_msg = f"Unexpected print error: {str(e)}"
        app.logger.error(error_msg, exc_info=True)
        raise RuntimeError(error_msg) from e
    finally:
        # Double-check cleanup if something went wrong mid-process
        if temp_file and os.path.exists(temp_file.name):
            try:
                os.unlink(temp_file.name)
            except Exception as cleanup_error:
                app.logger.warning(f"Temp file cleanup failed: {str(cleanup_error)}")