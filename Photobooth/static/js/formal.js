document.addEventListener("DOMContentLoaded", function () {
    // 4R Layout Template (1800×1200)
    const template = {
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
    };

    // DOM Elements
    const captureSection = document.getElementById('capture-section');
    const previewSection = document.getElementById('preview-section');
    const toggleCameraBtn = document.getElementById('toggle-camera');
    const videoFeed = document.getElementById('video-feed');
    const captureBtn = document.getElementById('capture-btn');
    const saveBtn = document.getElementById('save-photo');
    const captureAgainBtn = document.getElementById('capture-again-btn');
    const resultCanvas = document.getElementById('result-canvas');
    const ctx = resultCanvas.getContext('2d');

    // State
    let cameraActive = false;
    let capturedImageUrl = null;

    // Initialize Canvas
    resultCanvas.width = template.width;
    resultCanvas.height = template.height;
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, template.width, template.height);

    // Camera Control
    toggleCameraBtn.addEventListener('click', toggleCamera);
    
    function toggleCamera() {
        if (cameraActive) {
            stopCamera();
        } else {
            startCamera();
        }
    }

    function startCamera() {
        videoFeed.onerror = null;
        videoFeed.src = "/video_feed?" + new Date().getTime();
        videoFeed.onerror = () => {
            if (cameraActive) {
                alert("Could not access camera. Please check permissions.");
                stopCamera();
            }
        };
        toggleCameraBtn.textContent = "Close Camera";
        cameraActive = true;
    }

    function stopCamera() {
        videoFeed.onerror = null;
        videoFeed.src = "";
        toggleCameraBtn.textContent = "Open Camera";
        cameraActive = false;
        fetch("/stop_camera");
    }

    // Capture Functionality - Single Capture
    captureBtn.addEventListener('click', capturePhoto);
    
    function capturePhoto() {
        if (!cameraActive) {
            alert("Please enable the camera first");
            return;
        }

        captureBtn.disabled = true;
        captureBtn.textContent = "Capturing...";

        fetch("/capture_snapshot")
            .then(response => {
                if (!response.ok) throw new Error("Capture failed");
                return response.blob();
            })
            .then(imageBlob => {
                // Release previous image if exists
                if (capturedImageUrl) URL.revokeObjectURL(capturedImageUrl);
                
                capturedImageUrl = URL.createObjectURL(imageBlob);
                renderTemplate();
                showPreviewSection();
            })
            .catch(error => {
                console.error("Error capturing:", error);
                alert("Failed to capture photo. Please try again.");
            })
            .finally(() => {
                captureBtn.disabled = false;
                captureBtn.textContent = "Capture";
            });
    }

    // Render Template with Single Image
    function renderTemplate() {
        // Clear canvas
        ctx.fillStyle = 'white';
        ctx.fillRect(0, 0, template.width, template.height);
        
        if (!capturedImageUrl) return;
        
        const img = new Image();
        img.onload = function() {
            // Draw the same image in all slots
            template.areas.forEach(area => {
                ctx.drawImage(img, area.x, area.y, area.width, area.height);
                
                // Draw border
                ctx.strokeStyle = '#333';
                ctx.lineWidth = 3;
                ctx.strokeRect(area.x, area.y, area.width, area.height);
            });
        };
        img.src = capturedImageUrl;
    }

    // Navigation
    function showPreviewSection() {
        captureSection.classList.remove("section-active");
        captureSection.classList.add("section-inactive");
        previewSection.classList.remove("section-inactive");
        previewSection.classList.add("section-active");
    }

    captureAgainBtn.addEventListener('click', function() {
        // Clear captured image
        if (capturedImageUrl) URL.revokeObjectURL(capturedImageUrl);
        capturedImageUrl = null;
        
        // Reset UI
        previewSection.classList.remove("section-active");
        previewSection.classList.add("section-inactive");
        captureSection.classList.remove("section-inactive");
        captureSection.classList.add("section-active");
        
        if (!cameraActive) startCamera();
    });

    // Save/Print Functionality
    saveBtn.addEventListener('click', function() {
        if (!capturedImageUrl) {
            alert("No photo captured yet!");
            return;
        }
        
        const link = document.createElement('a');
        link.download = '4R-formal-layout.png';
        link.href = resultCanvas.toDataURL('image/png');
        link.click();
    });

    // Clean up
    window.addEventListener("beforeunload", function() {
        if (capturedImageUrl) URL.revokeObjectURL(capturedImageUrl);
        stopCamera();
    });
});