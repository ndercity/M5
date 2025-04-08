document.addEventListener("DOMContentLoaded", function () {
    // DOM Elements
    const toggleCameraButton = document.getElementById("toggle-camera");
    const videoFeed = document.getElementById("video-feed");
    const previewButton = document.getElementById("preview-btn");
    const captureAgainButton = document.getElementById("capture-again-btn");
    const captureButton = document.getElementById("capture-btn");
    const showGridButton = document.getElementById("show-grid-btn");
    const saveButton = document.getElementById("save-photo");
    const captureSection = document.getElementById("capture-section");
    const previewSection = document.getElementById("preview-section");
    const mainPreview = document.getElementById("main-preview");
    const brightnessControl = document.getElementById("brightness");
    const contrastControl = document.getElementById("contrast");

    let cameraActive = false;
    let currentImageUrl = null;
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");

    // Initialize sections
    captureSection.classList.add("section-active");
    previewSection.classList.add("section-inactive");

    // Camera Control
    toggleCameraButton.addEventListener("click", toggleCamera);
    
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
        
        toggleCameraButton.textContent = "Close Camera";
        cameraActive = true;
    }

    function stopCamera() {
        videoFeed.onerror = null;
        videoFeed.src = "";
        toggleCameraButton.textContent = "Open Camera";
        cameraActive = false;
        fetch("/stop_camera");
    }

    // Capture Functionality
    captureButton.addEventListener("click", capturePhoto);
    
    function capturePhoto() {
        if (!cameraActive) {
            alert("Please enable the camera first");
            return;
        }

        captureButton.disabled = true;
        captureButton.textContent = "Capturing...";

        fetch("/capture_snapshot")
            .then(response => {
                if (!response.ok) throw new Error("Capture failed");
                return response.blob();
            })
            .then(imageBlob => {
                const newImageUrl = URL.createObjectURL(imageBlob);
                
                // Clear previous image URL if exists
                if (currentImageUrl) {
                    URL.revokeObjectURL(currentImageUrl);
                }
                
                currentImageUrl = newImageUrl;
                updateImageDisplay();
                showPreviewSection();
            })
            .catch(error => {
                console.error("Error capturing:", error);
                alert("Failed to capture photo. Please try again.");
            })
            .finally(() => {
                captureButton.disabled = false;
                captureButton.textContent = "Capture";
            });
    }

    function updateImageDisplay() {
        // Update main preview
        mainPreview.src = currentImageUrl;
        applyEditsToMainPreview();
        
        // Update grid if visible
        if (document.querySelector(".parent").classList.contains("active")) {
            updateGridWithCurrentImage();
        }
    }

    // Navigation
    previewButton.addEventListener("click", showPreviewSection);
    captureAgainButton.addEventListener("click", showCaptureSection);

    function showPreviewSection() {
        if (!currentImageUrl) {
            alert("Please capture a photo first");
            return;
        }
        captureSection.classList.remove("section-active");
        captureSection.classList.add("section-inactive");
        
        previewSection.classList.remove("section-inactive");
        previewSection.classList.add("section-active");
        
        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    }

    function showCaptureSection() {
        // Clear previous image
        if (currentImageUrl) {
            URL.revokeObjectURL(currentImageUrl);
            currentImageUrl = null;
        }
        
        previewSection.classList.remove("section-active");
        previewSection.classList.add("section-inactive");
        
        captureSection.classList.remove("section-inactive");
        captureSection.classList.add("section-active");
        
        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
        
        // Reset grid view
        document.querySelector(".parent").classList.remove("active");
        showGridButton.textContent = "Show Grid View";
        
        if (!cameraActive) startCamera();
    }

    // Grid Toggle
    showGridButton.addEventListener("click", toggleGrid);
    
    function toggleGrid() {
        const grid = document.querySelector(".parent");
        grid.classList.toggle("active");
        
        if (grid.classList.contains("active")) {
            updateGridWithCurrentImage();
            showGridButton.textContent = "Hide Grid View";
        } else {
            showGridButton.textContent = "Show Grid View";
        }
    }

    function updateGridWithCurrentImage() {
        if (!currentImageUrl) return;
        
        const divs = document.querySelectorAll(".parent div");
        divs.forEach(div => {
            div.style.backgroundImage = `url(${currentImageUrl})`;
            applyEditsToGrid(div);
        });
    }

    // Image Editing
    brightnessControl.addEventListener("input", applyEdits);
    contrastControl.addEventListener("input", applyEdits);

    function applyEdits() {
        applyEditsToMainPreview();
        
        // Apply to grid if visible
        if (document.querySelector(".parent").classList.contains("active")) {
            const divs = document.querySelectorAll(".parent div");
            divs.forEach(div => applyEditsToGrid(div));
        }
    }

    function applyEditsToMainPreview() {
        const brightness = brightnessControl.value;
        const contrast = contrastControl.value;
        mainPreview.style.filter = `brightness(${100 + parseInt(brightness)}%) contrast(${100 + parseInt(contrast)}%)`;
    }

    function applyEditsToGrid(element) {
        const brightness = brightnessControl.value;
        const contrast = contrastControl.value;
        element.style.filter = `brightness(${100 + parseInt(brightness)}%) contrast(${100 + parseInt(contrast)}%)`;
    }

    // Save Functionality
    saveButton.addEventListener("click", savePhoto);
    
    function savePhoto() {
        if (!currentImageUrl) {
            alert("No photo to save!");
            return;
        }
        // Implement your save logic here
        alert("Photo saved with current edits!");
    }

    // Clean up
    window.addEventListener("beforeunload", function() {
        if (currentImageUrl) {
            URL.revokeObjectURL(currentImageUrl);
        }
        stopCamera();
    });
});