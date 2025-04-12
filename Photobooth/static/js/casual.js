document.addEventListener("DOMContentLoaded", function () {
    const toggleCameraButton = document.getElementById("toggle-camera");
    const videoFeed = document.getElementById("video-feed");
    const captureButton = document.getElementById("capture-btn");
    const recaptureButton = document.getElementById("recapture-btn");
    const confirmButton = document.getElementById("confirm-btn");
    const currentPath = window.location.pathname;
    
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

    function hideButtons(hasCaptured){
        console.log(hasCaptured)
        if(!hasCaptured){
            captureButton.style.display = 'inline-block'
            recaptureButton.style.display = 'none'
            confirmButton.style.display = 'none'
        }
        else{
            captureButton.style.display = 'none'
            recaptureButton.style.display = 'inline-block'
            confirmButton.style.display = 'inline-block'
        }
    }

    document.addEventListener("visibilitychange", function(){
        if(document.visibilityState === "visible"){
            console.log("Hello user")
            hideButtons(false);
            startCamera();
        }
    });

    toggleCameraButton.addEventListener("click", function () {
        if (cameraActive) {
            stopCamera();
        } else {
            startCamera();
        }
    });

    captureButton.addEventListener("click", function() {
        if (!cameraActive){
            startCamera()
        }
        fetch("/capture_image") //test method only
        hideButtons(true);
        console.log("Image captured");
    });

    recaptureButton.addEventListener("click", function() {
        hideButtons(false);
        fetch("/remove_image")
        console.log("Image Removed");

    });

    confirmButton.addEventListener("click", function() {
        hideButtons(false);
        console.log("Image Confirmed");
    });

    //para magopen agad on transition
    window.addEventListener("load", function(){
        console.log("Hello user")
        hideButtons(false);
        startCamera();
    });

    // Stop camera when leaving the page
    window.addEventListener("beforeunload", function () {
        stopCamera();
    });
});