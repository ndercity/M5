document.addEventListener("DOMContentLoaded", function () {
    const toggleCameraButton = document.getElementById("toggle-camera");
    const videoFeed = document.getElementById("video-feed");
    const captureAgainButton = document.getElementById("capture-again-btn");

    let cameraActive = false;

    function startCamera() {
        videoFeed.src = "/video_feed?" + new Date().getTime(); // Fresh feed
        toggleCameraButton.textContent = "Close Camera";
        cameraActive = true;
    }

    function stopCamera() {
        videoFeed.src = ""; // Clear feed
        toggleCameraButton.textContent = "Open Camera";
        cameraActive = false;
        fetch("/stop_camera"); // Tell the server to stop the camera
    }

    toggleCameraButton.addEventListener("click", function () {
        if (cameraActive) {
            stopCamera();
        } else {
            startCamera();
        }
    });

    // Scroll behavior without hiding sections
    captureAgainButton.addEventListener("click", function () {
        document.getElementById("capture-section").scrollIntoView({ behavior: "smooth", block: "center" });
    });

    // Stop camera when leaving the page
    window.addEventListener("beforeunload", function () {
        stopCamera();
    });
});