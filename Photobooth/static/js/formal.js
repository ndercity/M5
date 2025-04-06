document.addEventListener("DOMContentLoaded", function () {
    const toggleCameraButton = document.getElementById("toggle-camera");
    const videoFeed = document.getElementById("video-feed");
    const previewButton = document.getElementById("preview-btn");
    const captureAgainButton = document.getElementById("capture-again-btn");
    const captureButton = document.getElementById("capture-btn");
    const captureSection = document.getElementById("capture-section");
    const previewSection = document.getElementById("preview-section");

    let cameraActive = false;
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");

    // Initialize sections
    captureSection.classList.add("section-active");
    previewSection.classList.add("section-inactive");

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

    toggleCameraButton.addEventListener("click", function () {
        if (cameraActive) {
            stopCamera();
        } else {
            startCamera();
        }
    });

    // Navigation functions
    function showPreviewSection() {
        captureSection.classList.remove("section-active");
        captureSection.classList.add("section-inactive");
        
        previewSection.classList.remove("section-inactive");
        previewSection.classList.add("section-active");
        
        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
        
        // Focus for accessibility
        setTimeout(() => {
            previewSection.querySelector("h3").focus();
        }, 300);
    }

    function showCaptureSection() {
        previewSection.classList.remove("section-active");
        previewSection.classList.add("section-inactive");
        
        captureSection.classList.remove("section-inactive");
        captureSection.classList.add("section-active");
        
        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
        
        // Focus for accessibility
        setTimeout(() => {
            document.getElementById("toggle-camera").focus();
        }, 300);
    }

    previewButton.addEventListener("click", showPreviewSection);
    captureAgainButton.addEventListener("click", showCaptureSection);

    // Capture functionality
    captureButton.addEventListener("click", function () {
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
                const imageUrl = URL.createObjectURL(imageBlob);
                const divs = document.querySelectorAll(".parent div");
                divs.forEach(div => {
                    div.style.backgroundImage = `url(${imageUrl})`;
                    div.style.backgroundSize = "cover";
                    div.style.backgroundPosition = "center";
                });
                showPreviewSection();
            })
            .catch(error => {
                console.error("Error capturing snapshot:", error);
                alert("Failed to capture photo. Please try again.");
            })
            .finally(() => {
                captureButton.disabled = false;
                captureButton.textContent = "Capture";
            });
    });

    // Clean up camera when leaving page
    window.addEventListener("beforeunload", stopCamera);
});