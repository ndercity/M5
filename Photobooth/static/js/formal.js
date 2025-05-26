document.addEventListener("DOMContentLoaded", function () {
    //START COUNTDOWN
    let endTime = localStorage.getItem('countdownEnd')
	if (!endTime) {
		endTime = Date.now() + 10 * 60 * 1000;
		localStorage.setItem('countdownEnd', endTime);
	}

    // =====================
    // Configuration
    // =====================
    const CONFIG = {
        template: {
            width: 1800,
            height: 1200,
            areas: [
                // 4 Large (2×2) Photos - Each 600×600
                { x: 0, y: 0, width: 600, height: 600 },
                { x: 600, y: 0, width: 600, height: 600 },
                { x: 0, y: 600, width: 600, height: 600 },
                { x: 600, y: 600, width: 600, height: 600 },
                
                // 8 Small (1×1) Photos - Each 300×300
                { x: 1200, y: 0, width: 300, height: 300 },
                { x: 1500, y: 0, width: 300, height: 300 },
                { x: 1200, y: 300, width: 300, height: 300 },
                { x: 1500, y: 300, width: 300, height: 300 },
                { x: 1200, y: 600, width: 300, height: 300 },
                { x: 1500, y: 600, width: 300, height: 300 },
                { x: 1200, y: 900, width: 300, height: 300 },
                { x: 1500, y: 900, width: 300, height: 300 }
            ]
        },
        canvasStyle: {
            borderColor: '#333',
            borderWidth: 3,
            backgroundColor: 'white'
        }
    };

    // =====================
    // DOM Elements
    // =====================
    const elements = {
        //Universal Control
        goBackBtn: document.getElementById('back-content'),

        // Camera controls
        countdownDisplay: document.getElementById('countdown-display'),
        flashOverlay: document.getElementById('flash-overlay'),
        videoFeed: document.getElementById("video-feed"),
        captureBtn: document.getElementById("capture-btn"),
        
        // Preview controls
        mainPreview: document.getElementById("main-preview"),
        brightnessControl: document.getElementById("brightness"),
        contrastControl: document.getElementById("contrast"),
        finalizeBtn: document.getElementById("finalize-btn"),
        captureAgainBtn: document.getElementById("capture-again-btn"),
        
        // Results controls
        resultsSection: document.getElementById("results-section"),
        downloadBtn: document.getElementById("download-btn"),
        backToPreviewBtn: document.getElementById("back-to-preview-btn"),
        resultCanvas: document.getElementById("result-canvas"),
        
        // Sections
        captureSection: document.getElementById("capture-section"),
        previewSection: document.getElementById("preview-section")
    };

    // Canvas context
    const ctx = elements.resultCanvas.getContext("2d");

    // =====================
    // State Management
    // =====================
    const state = {
        cameraActive: false,
        currentImageUrl: null
    };

    // =====================
    // Initialization
    // =====================
    function initialize() {
        // Set up canvas
        setupCanvas();
        if (!state.cameraActive) startCamera();
        
        // Initialize sections
        elements.captureSection.classList.add("section-active");
        elements.previewSection.classList.add("section-inactive");
        elements.resultsSection.classList.add("section-inactive");
        
        // Set up event listeners
        setupEventListeners();
    }

    function setupCanvas() {
        elements.resultCanvas.width = CONFIG.template.width;
        elements.resultCanvas.height = CONFIG.template.height;
        clearCanvas();
    }

    function clearCanvas() {
        ctx.fillStyle = CONFIG.canvasStyle.backgroundColor;
        ctx.fillRect(0, 0, CONFIG.template.width, CONFIG.template.height);
    }

    function setupEventListeners() {
        // Camera controls
        elements.captureBtn.addEventListener('click', async () => {
            elements.captureBtn.classList.add("section-inactive");
            elements.goBackBtn.classList.add("section-inactive");
            await startCountdown(3);
            triggerFlash();
            
            setTimeout(() => {
                capturePhoto();
            }, 150);
        });
        
        // Preview controls
        elements.finalizeBtn.addEventListener("click", showResultsSection);
        elements.captureAgainBtn.addEventListener("click", showCaptureSection);
        elements.brightnessControl.addEventListener("input", applyEdits);
        elements.contrastControl.addEventListener("input", applyEdits);
        
        // Results controls
        elements.downloadBtn.addEventListener("click", savePhoto);
        elements.backToPreviewBtn.addEventListener("click", showPreviewSection);
        
        // Clean up on page unload
        window.addEventListener("beforeunload", cleanup);


    }

    // =====================
    // Camera Functions
    // =====================
    function toggleCamera() {
        state.cameraActive ? stopCamera() : startCamera();
    }

    function startCamera() {
        elements.videoFeed.onerror = null;
        elements.videoFeed.src = "/video_feed?" + new Date().getTime();
        
        elements.videoFeed.onerror = () => {
            if (state.cameraActive) {
                alert("Could not access camera. Please check permissions.");
                stopCamera();
            }
        };
        
        state.cameraActive = true;
    }

    function stopCamera() {
        elements.videoFeed.onerror = null;
        elements.videoFeed.src = "";
        state.cameraActive = false;
        fetch("/stop_camera");
    }

    // =====================
    // Capture Functions
    // =====================
    function capturePhoto() {
        if (!state.cameraActive) {
            alert("Please enable the camera first");
            return;
        }

        disableCaptureButton(true);

        fetch("/capture_snapshot")
            .then(handleCaptureResponse)
            .then(handleCaptureSuccess)
            .catch(handleCaptureError)
            .finally(() => disableCaptureButton(false));
    }

    function startCountdown(seconds) {
        return new Promise((resolve) => {
            elements.countdownDisplay.style.display = 'block';
            let count = seconds;

            const interval = setInterval(() => {
                elements.countdownDisplay.textContent = '';
                elements.countdownDisplay.textContent = count;
                count--;

                if (count < 0) {
                    clearInterval(interval);
                    elements.countdownDisplay.style.display = 'none';
                    elements.countdownDisplay.textContent = '';
                    elements.captureBtn.classList.remove("section-inactive");
                    elements.goBackBtn.classList.remove("section-inactive");
                    resolve();
                }
            }, 1000);
        });
    }

    function triggerFlash() {
        elements.flashOverlay.style.opacity = '1';
        setTimeout(() => {
            elements.flashOverlay.style.opacity = '0';
        }, 100);
    }

    function disableCaptureButton(disabled) {
        elements.captureBtn.disabled = disabled;
        elements.captureBtn.textContent = disabled ? "Capturing..." : "Capture";
    }

    function handleCaptureResponse(response) {
        if (!response.ok) throw new Error("Capture failed");
        return response.blob();
    }

    function handleCaptureSuccess(imageBlob) {
        if (state.currentImageUrl) {
            URL.revokeObjectURL(state.currentImageUrl);
        }
    
        const img = new Image();
        img.onload = function () {
            // Crop to square (smallest side)
            const size = Math.min(img.width, img.height);
            const tempCanvas = document.createElement('canvas');
            tempCanvas.width = size;
            tempCanvas.height = size;
            const tempCtx = tempCanvas.getContext('2d');
            
            // Draw centered crop
            const offsetX = (img.width - size) / 2;
            const offsetY = (img.height - size) / 2;
            tempCtx.drawImage(img, offsetX, offsetY, size, size, 0, 0, size, size);
    
            // Save the cropped image
            tempCanvas.toBlob(blob => {
                state.currentImageUrl = URL.createObjectURL(blob);
                updateMainPreview();
                showPreviewSection();
            }, 'image/png');
        };
        img.src = URL.createObjectURL(imageBlob);
    }
    

    function handleCaptureError(error) {
        console.error("Error capturing:", error);
        alert("Failed to capture photo. Please try again.");
    }

    // =====================
    // Preview Functions
    // =====================
    function updateMainPreview() {
        elements.mainPreview.src = state.currentImageUrl;
        applyEditsToMainPreview();
    }

    // =====================
    // Template Functions
    // =====================
    function renderTemplate() {
        if (!state.currentImageUrl) return;
        
        clearCanvas();
        
        const img = new Image();
        img.onload = function() {
            drawTemplateImages(img);
        };
        img.src = state.currentImageUrl;
        elements.goBackBtn.classList.add("section-inactive");
    }

    function drawTemplateImages(img) {
        const brightness = elements.brightnessControl.value;
        const contrast = elements.contrastControl.value;
        const filter = `brightness(${100 + parseInt(brightness)}%) contrast(${100 + parseInt(contrast)}%)`;
        
        CONFIG.template.areas.forEach(area => {
            // Draw image with filters
            drawImageWithFilter(img, area, filter);
            
            // Draw border
            drawBorder(area);
        });
    }

    function drawImageWithFilter(img, area, filter) {
        const tempCanvas = document.createElement('canvas');
        tempCanvas.width = area.width;
        tempCanvas.height = area.height;
        const tempCtx = tempCanvas.getContext('2d');
        
        tempCtx.filter = filter;
        tempCtx.drawImage(img, 0, 0, area.width, area.height);
        ctx.drawImage(tempCanvas, area.x, area.y, area.width, area.height);
    }

    function drawBorder(area) {
        ctx.strokeStyle = CONFIG.canvasStyle.borderColor;
        ctx.lineWidth = CONFIG.canvasStyle.borderWidth;
        ctx.strokeRect(area.x, area.y, area.width, area.height);
    }

    // =====================
    // Editing Functions
    // =====================
    function applyEdits() {
        applyEditsToMainPreview();
    }

    function applyEditsToMainPreview() {
        const brightness = elements.brightnessControl.value;
        const contrast = elements.contrastControl.value;
        elements.mainPreview.style.filter = 
            `brightness(${100 + parseInt(brightness)}%) contrast(${100 + parseInt(contrast)}%)`;
    }

    // =====================
    // Navigation Functions
    // =====================
    function showPreviewSection() {
        if (!state.currentImageUrl) {
            alert("Please capture a photo first");
            return;
        }
        
        toggleSection(elements.captureSection, false);
        toggleSection(elements.resultsSection, false);
        toggleSection(elements.previewSection, true);
        scrollToTop();
        elements.goBackBtn.classList.remove("section-inactive");
    }

    function showResultsSection() {
        if (!state.currentImageUrl) {
            alert("Please capture and finalize a photo first");
            return;
        }
        
        // Render template for final output
        renderTemplate();
        
        toggleSection(elements.captureSection, false);
        toggleSection(elements.previewSection, false);
        toggleSection(elements.resultsSection, true);
        scrollToTop();
    }

    function showCaptureSection() {
        // Clear previous image
        if (state.currentImageUrl) {
            URL.revokeObjectURL(state.currentImageUrl);
            state.currentImageUrl = null;
        }

        // Reset sliders
        elements.brightnessControl.value = 0;
        elements.contrastControl.value = 0;
        applyEdits();
        
        toggleSection(elements.previewSection, false);
        toggleSection(elements.resultsSection, false);
        toggleSection(elements.captureSection, true);
        scrollToTop();
        
        if (!state.cameraActive) startCamera();
    }

    function toggleSection(section, show) {
        section.classList.toggle("section-active", show);
        section.classList.toggle("section-inactive", !show);
    }

    function scrollToTop() {
        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    }

    // =====================
    // Save Functions
    // =====================
    function savePhoto() {
        localStorage.removeItem('countdownEnd');    //RESET TIMER
	    stopCamera();
        if (!state.currentImageUrl) {
            alert("No photo to save!");
            return;
        }
    
        const session_id = localStorage.getItem('session_id');
        console.log(session_id);
    
        elements.resultCanvas.toBlob(blob => {
            if (!blob) {
                alert("Failed to get image blob!");
                return;
            }
    
            const formData = new FormData();
            formData.append('photo', blob, 'photo.png');
            formData.append('session_id', session_id);
    
            fetch('/upload_photo', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
            })
            .then(data => {
                if (data.message === "Photo saved successfully") {
                    document.getElementById("sendingOverlay").classList.remove("section-inactive");
    
                    // Directly call finalize_session with session_id only
                    const finalizeForm = new FormData();
                    finalizeForm.append('session_id', session_id);
    
                    return fetch('/finalize_session', {
                        method: 'POST',
                        body: finalizeForm
                    })
                } else {
                    throw new Error(data.error || 'Failed to save photo');
                }
            })
            .then(response => {
                if (!response.ok) throw new Error('Failed to finalize session');
                return response.json();
            })
            .then(finalizeData => {
                if (finalizeData.print_message) {
                    alert(finalizeData.print_message);  // <-- show the print status
                }

                if (finalizeData.status === 'completed' || finalizeData.status === 'partial') {
                    alert("Email sent! Redirecting to home...");
                } else {
                    alert("Failed to complete session. Redirecting to home...");
                }

                document.getElementById("sendingOverlay").classList.add("section-inactive");
                window.location.href = "/";
            })

            .catch(error => {
                console.error(error);
                alert('Error during photo save or email sending: ' + error.message + ' Redirecting to home...');
                window.location.href = "/";
            })
             .finally(() => {
                document.getElementById("sendingOverlay").classList.add("section-inactive");
                window.location.href = "/";
                stopRFIDSession(session_id);  
            });
    
        }, 'image/png');
    }    

    function stopRFIDSession(sessionID) {
        fetch('/end_rfid_access', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ session_id: sessionID })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to end session');
            }
            return response.json();
        })
        .then(data => {
            console.log('RFID session ended:', data);
            alert('RFID session has been successfully ended.');
            // Optionally clear session from localStorage
            localStorage.removeItem('session_id');
        })
        .catch(error => {
            console.error('Error ending session:', error);
            alert('There was an error ending the session.');
        });
    }


    function showDownloadConfirmation() {
        const confirmation = document.createElement('div');
        confirmation.textContent = 'Download started!';
        confirmation.className = 'download-confirmation';
        elements.resultsSection.appendChild(confirmation);
        
        setTimeout(() => {
            confirmation.remove();
        }, 2000);
    }

    //
    function finalizeAndSendPdf(pdfBlob) {
        const session_id = localStorage.getItem('session_id');
        const formData = new FormData();
        formData.append('pdf', pdfBlob, 'session.pdf');
        formData.append('session_id', session_id);
    
        return fetch('/finalize_session', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        });
    }
    

    // =====================
    // Cleanup
    // =====================
    function cleanup() {
        if (state.currentImageUrl) {
            URL.revokeObjectURL(state.currentImageUrl);
        }
        stopCamera();
    }

    // Initialize the application
    initialize();
});