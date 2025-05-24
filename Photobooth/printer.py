import cups
import tempfile
import os

def print_pdf(pdf_data, printer_name=None):
    """
    Print a PDF document using CUPS.
    
    Args:
        pdf_data (bytes): The PDF data to print
        printer_name (str, optional): Name of the printer to use. If None, uses default printer.
        options (dict, optional): Printing options like {'media': 'A4', 'fit-to-page': 'True'}
    
    Returns:
        tuple: (success: bool, job_id: int/str, message: str)
    """
    try:
        # Create a temporary file to hold the PDF
        with tempfile.NamedTemporaryFile(prefix='print_', suffix='.pdf', delete=False) as tmp_file:
            tmp_file.write(pdf_data)
            tmp_path = tmp_file.name
        
        # Connect to CUPS
        conn = cups.Connection()
        
        # Get printer if not specified
        if not printer_name:
            printer_name = conn.getDefault()
            if not printer_name:
                raise Exception("No default printer available")
        
        # Set default options if none provided

        
        # Print the file
        job_id = conn.printFile(printer_name, tmp_path, "Python Print Job")
        
        # Clean up the temporary file
        os.unlink(tmp_path)
        
        # Get printer status
        printer_status = conn.getPrinterAttributes(printer_name).get('printer-state-message', '')
        
        return True, job_id, printer_status
    
    except cups.IPPError as e:
        error_msg = f"CUPS IPP Error: {e}"
        return False, -1, error_msg
    except Exception as e:
        error_msg = f"Printing error: {e}"
        return False, -1, error_msg