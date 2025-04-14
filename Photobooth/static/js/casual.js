document.addEventListener("DOMContentLoaded", function() {
    // State management
    const state = {
        selectedLayout: null,
        layoutName: "",
        capturedImages: Array(4).fill(null),
        currentPose: 1,
        cameraActive: false
    };

    // DOM elements
    const layoutSelection = document.getElementById('layout-selection');
    const captureSection = document.getElementById('capture-section');
    const previewSection = document.getElementById('preview-section');
    const videoFeed = document.getElementById('video-feed');
    const toggleCameraBtn = document.getElementById('toggle-camera');
    const captureBtn = document.getElementById('capture-btn');
    const retakeBtn = document.getElementById('retake-btn');
    const poseNumber = document.getElementById('pose-number');
    const layoutName = document.getElementById('layout-name');
    const saveBtn = document.getElementById('save-layout');
    const startOverBtn = document.getElementById('start-over');
    const layoutContainer = document.querySelector('.layout-container');

    //Event Listeners

    document.querySelectorAll('.layout-option').forEach(option => {
        option.addEventListener('click', () => {
            // Update UI
            document.querySelectorAll('.layout-option').forEach(opt => {
                opt.classList.remove('selected');
            });
            option.classList.add('selected');
            
            // Store selection
            state.selectedLayout = option.dataset.layout;
            state.layoutName = option.querySelector('span').textContent;
            
            // Proceed to capture
            layoutSelection.classList.add('hidden');
            captureSection.classList.remove('hidden');
            updateCaptureUI();
        });
    });

    toggleCameraBtn.addEventListener('click', toggleCamera);
    captureBtn.addEventListener('click', capturePose);
    retakeBtn.addEventListener('click', retakePose);
    saveBtn.addEventListener('click', saveLayout);
    startOverBtn.addEventListener('click', startOver);
    
    function toggleCamera() {
        if (state.cameraActive) {
            stopCamera();
        } else {
            startCamera();
        }
    }

    function startCamera() {
        videoFeed.src = "/video_feed?" + new Date().getTime();
        videoFeed.onerror = () => {
            if (state.cameraActive) {
                alert("Could not access camera. Please check permissions.");
                stopCamera();
            }
        };
        toggleCameraBtn.textContent = "Close Camera";
        state.cameraActive = true;
    }

    function stopCamera() {
        videoFeed.onerror = null;
        videoFeed.src = "";
        toggleCameraBtn.textContent = "Open Camera";
        state.cameraActive = false;
        fetch("/stop_camera");
    }

    function capturePose() {
        if (!state.cameraActive) {
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
                const imageUrl = URL.createObjectURL(imageBlob);
                state.capturedImages[state.currentPose - 1] = imageUrl;
                
                if (state.currentPose < 4) {
                    state.currentPose++;
                    updateCaptureUI();
                } else {
                    showPreview();
                }
            })
            .catch(error => {
                console.error("Error capturing:", error);
                alert("Failed to capture. Please try again.");
            })
            .finally(() => {
                captureBtn.disabled = false;
                captureBtn.textContent = "Capture Pose";
            });
    }

    function retakePose() {
        state.capturedImages[state.currentPose - 1] = null;
        updateCaptureUI();
    }

    function showPreview() {
        layoutName.textContent = state.layoutName;
        captureSection.classList.add('hidden');
        previewSection.classList.remove('hidden');
        renderLayoutPreview();
    }

    function renderLayoutPreview() {
        layoutContainer.innerHTML = '';
        
        const layoutDiv = document.createElement('div');
        layoutDiv.className = `final-layout ${state.selectedLayout}`;
        
        switch(state.selectedLayout) {
            case 'grid':
                layoutDiv.innerHTML = `
                    <div class="slot"><img src="${state.capturedImages[0] || ''}" alt="Pose 1"></div>
                    <div class="slot"><img src="${state.capturedImages[1] || ''}" alt="Pose 2"></div>
                    <div class="slot"><img src="${state.capturedImages[2] || ''}" alt="Pose 3"></div>
                    <div class="slot"><img src="${state.capturedImages[3] || ''}" alt="Pose 4"></div>
                `;
                break;
                
            case 'vertical':
                layoutDiv.innerHTML = `
                    <div class="slot"><img src="${state.capturedImages[0] || ''}" alt="Pose 1"></div>
                    <div class="slot"><img src="${state.capturedImages[1] || ''}" alt="Pose 2"></div>
                    <div class="slot"><img src="${state.capturedImages[2] || ''}" alt="Pose 3"></div>
                    <div class="slot"><img src="${state.capturedImages[3] || ''}" alt="Pose 4"></div>
                `;
                break;
                
            case 'horizontal':
                layoutDiv.innerHTML = `
                    <div class="slot"><img src="${state.capturedImages[0] || ''}" alt="Pose 1"></div>
                    <div class="slot"><img src="${state.capturedImages[1] || ''}" alt="Pose 2"></div>
                    <div class="slot"><img src="${state.capturedImages[2] || ''}" alt="Pose 3"></div>
                    <div class="slot"><img src="${state.capturedImages[3] || ''}" alt="Pose 4"></div>
                `;
                break;
        }
        
        const slots = layoutDiv.querySelectorAll('.slot');
        slots.forEach((slot, index) => {
            if (state.capturedImages[index]) {
                const retakeBtn = document.createElement('button');
                retakeBtn.className = 'retake-single';
                retakeBtn.textContent = 'Retake';
                retakeBtn.dataset.index = index;
                retakeBtn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    retakeSpecificPose(index);
                });
                slot.appendChild(retakeBtn);
            }
        });
        
        layoutContainer.appendChild(layoutDiv);
    }

    function retakeSpecificPose(index) {
        state.currentPose = index + 1;
        state.capturedImages[index] = null;
        previewSection.classList.add('hidden');
        captureSection.classList.remove('hidden');
        updateCaptureUI();
        if (!state.cameraActive) startCamera();
    }

    function updateCaptureUI() {
        poseNumber.textContent = state.currentPose;
        retakeBtn.classList.toggle('hidden', !state.capturedImages[state.currentPose - 1]);
    }

    function saveLayout() {
        // Here you would implement actual saving logic
        alert("All 4 photos saved successfully!");
    }

    function startOver() {
        if (confirm("Are you sure you want to start over? All captured photos will be lost.")) {
            state.capturedImages = Array(4).fill(null);
            state.currentPose = 1;
            previewSection.classList.add('hidden');
            layoutSelection.classList.remove('hidden');
            updateCaptureUI();
            stopCamera();
        }
    }

    // Clean up
    window.addEventListener('beforeunload', stopCamera);
});