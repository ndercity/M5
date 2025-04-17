document.addEventListener("DOMContentLoaded", function () {
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
        // Camera controls
        toggleCameraBtn: document.getElementById("toggle-camera"),
        videoFeed: document.getElementById("video-feed"),
        captureBtn: document.getElementById("capture-btn"),
        previewBtn: document.getElementById("preview-btn"),
        
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
        elements.toggleCameraBtn.addEventListener("click", toggleCamera);
        elements.captureBtn.addEventListener("click", capturePhoto);
        elements.previewBtn.addEventListener("click", showPreviewSection);
        
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
        
        elements.toggleCameraBtn.textContent = "Close Camera";
        state.cameraActive = true;
    }

    function stopCamera() {
        elements.videoFeed.onerror = null;
        elements.videoFeed.src = "";
        elements.toggleCameraBtn.textContent = "Open Camera";
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

    function disableCaptureButton(disabled) {
        elements.captureBtn.disabled = disabled;
        elements.captureBtn.textContent = disabled ? "Capturing..." : "Capture";
    }

    function handleCaptureResponse(response) {
        if (!response.ok) throw new Error("Capture failed");
        return response.blob();
    }

    function handleCaptureSuccess(imageBlob) {
        // Clear previous image if exists
        if (state.currentImageUrl) {
            URL.revokeObjectURL(state.currentImageUrl);
        }
        
        state.currentImageUrl = URL.createObjectURL(imageBlob);
        updateMainPreview();
        showPreviewSection();
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
        if (!state.currentImageUrl) {
            alert("No photo to save!");
            return;
        }
        
        // Create temporary link to download canvas as PNG
        const link = document.createElement('a');
        link.download = '4R-formal-template.png';
        link.href = elements.resultCanvas.toDataURL('image/png');
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        // Show download confirmation
        showDownloadConfirmation();
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