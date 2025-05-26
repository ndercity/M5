document.addEventListener("DOMContentLoaded", function() {
    //START COUNTDOWN
    let endTime = localStorage.getItem('countdownEnd')
	if (!endTime) {
		endTime = Date.now() + 10 * 60 * 1000;
		localStorage.setItem('countdownEnd', endTime);
	}

    // =============================================
    // CONSTANTS AND CONFIGURATION
    // =============================================
    const TEMPLATE_CONFIG = {
        one: {
            name: "Pic-a-Pi",
            background: "/static/others/frame1.png",
            areas: [
                { x: 69.8, y: 56.2, width: 814.2, height: 458, color: '#FFDDC1' },
                { x: 916, y: 56.2, width: 814.2, height: 458, color: '#C1FFD7' },
                { x: 69.8, y: 548.9, width: 814.2, height: 458, color: '#C1D7FF' },
                { x: 916, y: 548.9, width: 814.2, height: 458, color: '#FFC1E3' }
            ]
        },
        two: {
            name: "Adventure RPG",
            background: "/static/others/frame2.png",
            areas: [
                { x: 180.4, y: 167.6, width: 696.1, height: 391.5, color: '#FFDDC1' }, 
                { x: 913.1, y: 167.6, width: 696.1, height: 391.5, color: '#C1FFD7' },
                { x: 266.1, y: 579.1, width: 505.2, height: 284.2, color: '#C1D7FF' }, 
                { x: 1012, y: 579.1, width: 505.2, height: 284.2, color: '#FFC1E3' } 
            ]
        },
        three: {
            name: "Meeting",
            background: "/static/others/frame3.png",
            areas: [
                { x: 120, y: 155, width: 1027.5, height: 578, color: '#FFDDC1' }, 
                { x: 1206.9, y: 155, width: 473.1, height: 266.1, color: '#C1FFD7' },
                { x: 1206.9, y: 466.8, width: 473.1, height: 266.1, color: '#C1D7FF' },
                { x: 1206.9, y: 778.9, width: 473.1, height: 266.1, color: '#FFC1E3' } 
            ]
        },
        four: {
            name: "Summer",
            background: "/static/others/frame4.png",
            areas: [
                { x: 123.2, y: 218.9, width: 724.8, height: 407.7, color: '#FFDDC1' }, 
                { x: 123.2, y: 714.7, width: 505.2, height: 284.2, color: '#C1FFD7' }, 
                { x: 675.6, y: 714.7, width: 505.2, height: 284.2, color: '#C1D7FF' }, 
                { x: 1228, y: 714.7, width: 505.2, height: 284.2, color: '#FFC1E3' } 
            ]
        },
        five: {
            name: "Neon",
            background: "/static/others/frame5.png",
            areas: [
                { x: 153.5, y: 167.6, width: 696.1, height: 391.5, color: '#FFDDC1' }, 
                { x: 880.8, y: 167.6, width: 696.1, height: 391.5, color: '#C1FFD7' }, 
                { x: 153.5, y: 600, width: 696.1, height: 391.5, color: '#C1D7FF' }, 
                { x: 880.8, y: 600, width: 696.1, height: 391.5, color: '#FFC1E3' } 
            ]
        },
        six: {
            name: "Birthday",
            background: "/static/others/frame6.png",
            areas: [
                { x: 123.2, y: 242.4, width: 724.8, height: 407.7, color: '#FFDDC1' },
                { x: 123.2, y: 722.7, width: 505.2, height: 284.2, color: '#C1FFD7' },
                { x: 688.9, y: 722.7, width: 505.2, height: 284.2, color: '#C1D7FF' },
                { x: 1228, y: 722.7, width: 505.2, height: 284.2, color: '#FFC1E3' }
            ]
        },
        seven: {
            name: "Kill Feed",
            background: "/static/others/frame7.png",
            areas: [
                { x: 64.2, y: 295.9, width: 426.5, height: 239.9, color: '#FFDDC1' }, 
                { x: 1298.1, y: 295.9, width: 426.5, height: 239.9, color: '#C1FFD7' },
                { x: 64.2, y: 662.5, width: 426.5, height: 239.9, color: '#C1D7FF' },
                { x: 1298.1, y: 662.5, width: 426.5, height: 239.9, color: '#FFC1E3' } 
            ]
        },
        eight: {
            name: "Doodle",
            background: "/static/others/frame8.png",
            areas: [
                { x: 190.3, y: 170.2, width: 696.1, height: 391.5, color: '#FFDDC1' }, 
                { x: 913.7, y: 170.2, width: 696.1, height: 391.5, color: '#C1FFD7' },
                { x: 190.3, y: 591.3, width: 696.1, height: 391.5, color: '#C1D7FF' },
                { x: 913.7, y: 591.3, width: 696.1, height: 412.2, color: '#FFC1E3' } 
            ]
        },
        nine: {
            name: "Chicken Jockey",
            background: "/static/others/frame9.png",
            areas: [
                { x: 839.5, y: 319.7, width: 323.1, height: 181.7, color: '#FFDDC1' }, 
                { x: 497.7, y: 527.5, width: 323.1, height: 181.7, color: '#C1FFD7' },
                { x: 156, y: 735.5, width: 323.1, height: 181.7, color: '#C1D7FF' },
                { x: 1331.3, y: 473.6, width: 449.4, height: 252.8, color: '#FFC1E3' } 
            ]
        },
        ten: {
            name: "Racer",
            background: "/static/others/frame10.png",
            areas: [
                { x: 95, y: 217.8, width: 724.8, height: 407.7, color: '#FFDDC1' }, 
                { x: 95, y: 731.1, width: 505.2, height: 284.2, color: '#C1FFD7' },
                { x: 647.4, y: 731.1, width: 505.2, height: 284.2, color: '#C1D7FF' },
                { x: 1199.6, y: 731.1, width: 505.2, height: 284.2, color: '#FFC1E3' } 
            ]
        },
        eleven: {
            name: "Outer Space",
            background: "/static/others/frame11.png",
            areas: [
                { x: 95, y: 217.8, width: 724.8, height: 407.7, color: '#FFDDC1' }, 
                { x: 95, y: 698, width: 505.2, height: 284.2, color: '#C1FFD7' },
                { x: 647.4, y: 698, width: 505.2, height: 284.2, color: '#C1D7FF' },
                { x: 1199.8, y: 698, width: 505.2, height: 284.2, color: '#FFC1E3' } 
            ]
        },
        twelve: {
            name: "Apt.",
            background: "/static/others/frame12.png",
            areas: [
                { x: 190.3, y: 170.2, width: 696.1, height: 391.5, color: '#FFDDC1' }, 
                { x: 913.7, y: 170.2, width: 696.1, height: 391.5, color: '#C1FFD7' },
                { x: 190.3, y: 591.3, width: 696.1, height: 391.5, color: '#C1D7FF' },
                { x: 913.7, y: 591.3, width: 696.1, height: 391.5, color: '#FFC1E3' }  
            ]
        },
        thirteen: {
            name: "Pormula 1",
            background: "/static/others/frame13.png",
            areas: [
                { x: 332.9, y: 236, width: 486.3, height: 273.5, color: '#FFDDC1' },
                { x: 943.2, y: 372.7, width: 486.3, height: 273.5, color: '#C1FFD7' },
                { x: 335.8, y: 646.2, width: 486.3, height: 273.5, color: '#C1D7FF' },
                { x: 943.2, y: 783, width: 486.3, height: 273.5, color: '#FFC1E3' }
            ]
        },
        fourteen: {
            name: "Halloween",
            background: "/static/others/frame14.png",
            areas: [
                { x: 101, y: 157.7, width: 724.8, height: 407.7, color: '#FFDDC1' }, 
                { x: 101, y: 629.3, width: 505.2, height: 284.2, color: '#C1FFD7' },
                { x: 647.4, y: 629.3, width: 505.2, height: 284.2, color: '#C1D7FF' },
                { x: 1193.6, y: 629.3, width: 505.2, height: 284.2, color: '#FFC1E3' } 
            ]
        },
        fifteen: {
            name: "Sunrise",
            background: "/static/others/frame15.png",
            areas: [
                { x: 61.5, y: 120, width: 822.3, height: 462.5, color: '#FFDDC1' },
                { x: 916.2, y: 120, width: 822.3, height: 462.5, color: '#C1FFD7' },
                { x: 61.5, y: 617.5, width: 822.3, height: 462.5, color: '#C1D7FF' },
                { x: 916.2, y: 617.5, width: 822.3, height: 462.5, color: '#FFC1E3' }
            ]
        },
        sixteen: {
            name: "Sunset",
            background: "/static/others/frame16.png",
            areas: [
                { x: 61.5, y: 120, width: 822.3, height: 462.5, color: '#FFDDC1' },
                { x: 916.2, y: 120, width: 822.3, height: 462.5, color: '#C1FFD7' },
                { x: 61.5, y: 617.5, width: 822.3, height: 462.5, color: '#C1D7FF' },
                { x: 916.2, y: 617.5, width: 822.3, height: 462.5, color: '#FFC1E3' }
            ]
        },
        seventeen: {
            name: "Clear Sky",
            background: "/static/others/frame17.png",
            areas: [
                { x: 61.5, y: 120, width: 822.3, height: 462.5, color: '#FFDDC1' },
                { x: 916.2, y: 120, width: 822.3, height: 462.5, color: '#C1FFD7' },
                { x: 61.5, y: 617.5, width: 822.3, height: 462.5, color: '#C1D7FF' },
                { x: 916.2, y: 617.5, width: 822.3, height: 462.5, color: '#FFC1E3' }
            ]
        }
    };

    // =============================================
    // DOM ELEMENTS
    // =============================================
    // Layout Selection Elements
    const templateContainer = document.getElementById('template-container');
    const layoutSelection = document.getElementById('layout-selection');
    const layoutName = document.getElementById('layout-name');
    const backToModeBtn = document.getElementById('back-card');
    
    
    // Capture Section Elements
    const captureSection = document.getElementById('capture-section');
    const videoFeed = document.getElementById('video-feed');
    const videoContainer = document.querySelector('.video-container');
    const countdownDisplay = document.getElementById('countdown-display');
    const flashOverlay = document.getElementById('flash-overlay');
    const captureBtn = document.getElementById('capture-btn');
    const poseNumber = document.getElementById('pose-number');
    const confirmLayoutBtn = document.getElementById('confirm-layout');
    
    // Preview Section Elements
    const previewSection = document.getElementById('preview-section');
    const preview = document.getElementById('preview');
    const saveBtn = document.getElementById('save-layout');
    const startOverBtn = document.getElementById('start-over');
    const shutter = document.getElementById('capture-btn');
    const backToLayoutBtn = document.getElementById('back-to-layout');
    const imageSelectBtns = document.querySelectorAll('.image-select-btn');
    const selectedImagePreview = document.getElementById('selected-image-preview');
    const editBtn = document.getElementById('edit-btn');
    const retakeBtn = document.getElementById('retake-btn');
    
    // Canvas Elements
    const resultCanvas = document.getElementById('result-canvas');
    const ctx = resultCanvas.getContext('2d');
    let selectedBG = '';
    
    // Final Result Elements
    const finalResultSection = document.getElementById('final-result-section');
    const downloadBtn = document.getElementById('download-btn');
    const backToPreviewBtn = document.getElementById('back-to-preview');
    
    // Edit Mode Elements
    const editControls = document.getElementById('edit-controls');
    const editCanvas = document.getElementById('edit-canvas'); //ito ang container ng image sa editing
    const editCtx = editCanvas.getContext('2d');
    const backFromEditBtn = document.getElementById('back-from-edit');
    const applyEditBtn = document.getElementById('apply-edit');
    const modeButtons = document.querySelectorAll('.mode-selection-buttons');
    const modeFilter = document.querySelectorAll('.mode-set');
    const colorButtons = document.querySelectorAll('.circle-button-color');

    // Sticker Variables (dont delete anything pls)
    let stickerImages = [];
    const stickerTracker = {};
    const stickerMetaData = {};
    let picEditState = [false, false, false, false]; //ito ang magiindicate kung naedit na ba yung pic or hindi
    let isImageRaw = true; //titignan neto kung raw pa ba ang image or hindi na

    // =============================================
    // STATE VARIABLES
    // =============================================
    let currentTemplate = null;
    let cameraActive = false;
    let capturedImages = Array(4).fill(null);
    let currentPose = 1;
    let isRetaking = false;
    let retakeIndex = -1;
    let currentlySelectedImageIndex = 0;
    let currentEditImageIndex = 0;
    let carousel;
    let carouselItems = [];
    let currentIndex = 0;
    let currentButtonIndex = -1; //negative 1 ang default value para walang ibalik
    let retakeChances = 3;

    // =============================================
    // VARIABLES
    // =============================================
    let sticker_alt = ""


    // =============================================
    // INITIALIZATION
    // =============================================
    function initialize() {
        resultCanvas.width = 1800;
        resultCanvas.height = 1200;
        resultCanvas.background = selectedBG;
        setupEditMode();
        renderTemplates();
        setupEventListeners();
        //
        loadStickersDynamically();
        groupColorButtonsIntoSlides();
        setupColorCarousel();

        selectItem(currentIndex);
        console.log(currentIndex);

        if (videoFeed) {
            startCamera(); //START AGAD 
        }
    }

    // =============================================
    // TEMPLATE SELECTION AND RENDERING
    // =============================================
    function renderTemplates() {
        carousel = document.querySelector('.template-carousel');
        carousel.innerHTML = '';
        carouselItems = [];
        
        for (const [key, template] of Object.entries(TEMPLATE_CONFIG)) {
            const templateOption = createTemplateOption(key, template);
            carousel.appendChild(templateOption);
            carouselItems.push(templateOption);
        }
        
        setupCarouselNavigation();
        
        if (carouselItems.length > 0) {
            currentTemplate = TEMPLATE_CONFIG[Object.keys(TEMPLATE_CONFIG)[0]];
            carouselItems[0].classList.add('selected');
        }
    }

    function createTemplateOption(key, template) {
        const templateOption = document.createElement('div');
        templateOption.className = 'template-option';
        templateOption.dataset.layout = key;
        
        const preview = document.createElement('div');
        preview.className = 'template-preview';

        if (template.background) {
            preview.style.backgroundImage = `url('${template.background}')`;
        }
        
        const templateAreasContainer = createTemplateAreasContainer(template);
        preview.appendChild(templateAreasContainer);
        templateOption.appendChild(preview);
        
        const label = document.createElement('span');
        label.className = 'template-label';
        label.textContent = template.name;
        templateOption.appendChild(label);

        return templateOption;
    }

    function createTemplateAreasContainer(template) {
        const container = document.createElement('div');
        container.className = 'AreaForTemplate'
        container.style.position = 'absolute'; // absolute inside preview
        container.style.width = '300px';
        container.style.height = '200px';
        container.style.left = '0';
        container.style.top = '0';
        container.style.pointerEvents = 'none'; 
        
        const originalWidth = 1800;
        const originalHeight = 1200;
        const previewWidth = parseFloat(container.style.width);
        const previewHeight = parseFloat(container.style.height);
        const scaleX = previewWidth / originalWidth;
        const scaleY = previewHeight / originalHeight;
        const scale = Math.min(scaleX, scaleY);
        const scaledWidth = originalWidth * scale;
        const scaledHeight = originalHeight * scale;
        const offsetX = (previewWidth - scaledWidth) / 2;
        const offsetY = (previewHeight - scaledHeight) / 2;
        
        template.areas.forEach((area, index) => {
            const areaDiv = document.createElement('div');
            areaDiv.className = 'template-area';
            areaDiv.style.left = `${offsetX + (area.x * scale)}px`;
            areaDiv.style.top = `${offsetY + (area.y * scale)}px`;
            areaDiv.style.width = `${area.width * scale}px`;
            areaDiv.style.height = `${area.height * scale}px`;
            areaDiv.style.backgroundColor = area.color;
            
            const number = document.createElement('div');
            number.className = 'template-area-number';
            number.textContent = index + 1;
            areaDiv.appendChild(number);
            
            container.appendChild(areaDiv);
        });

        return container;
    }

    function setupCarouselNavigation() {
        const prevBtn = document.querySelector('.carousel-button.prev');
        const nextBtn = document.querySelector('.carousel-button.next');
        
        prevBtn.addEventListener('click', () => navigateCarousel(-1));
        nextBtn.addEventListener('click', () => navigateCarousel(1));
        
        carouselItems.forEach((item, index) => {
            item.addEventListener('click', () => selectItem(index));
        });
        
        document.addEventListener('keydown', handleKeyboardNavigation);
    }

    function navigateCarousel(direction) {
        currentIndex = (currentIndex + direction + carouselItems.length) % carouselItems.length;
        scrollToItem(currentIndex);
        selectItem(currentIndex);
    }

    function scrollToItem(index) {
        const item = carouselItems[index];
        item.scrollIntoView({
            behavior: 'smooth',
            block: 'nearest',
            inline: 'center'
        });
        selectItem(index);
    }

    function selectItem(index) {
        carouselItems.forEach(item => item.classList.remove('selected'));
        carouselItems[index].classList.add('selected');
        currentTemplate = TEMPLATE_CONFIG[carouselItems[index].dataset.layout];
        selectedBG = currentTemplate.background;
        currentIndex = index;
        console.log("Current Layout: ", currentIndex)
    }

    function handleKeyboardNavigation(e) {
        if (layoutSelection.classList.contains('section-active')) {
            if (e.key === 'ArrowLeft') navigateCarousel(-1);
            if (e.key === 'ArrowRight') navigateCarousel(1);
        }
    }

    /* function updateVideoContainerLayout() {
        videoContainer.querySelectorAll('.layout-marker').forEach(marker => marker.remove());
        if (!currentTemplate) return;
        
        currentTemplate.areas.forEach((area, index) => {
            const marker = createLayoutMarker(area, index);
            videoContainer.appendChild(marker);
        });
    } */

    /* function createLayoutMarker(area, index) {
        const marker = document.createElement('div');
        marker.className = 'layout-marker';
        
        const scaleX = videoContainer.offsetWidth / 1800;
        const scaleY = videoContainer.offsetHeight / 1200;
        
        marker.style.position = 'absolute';
        marker.style.border = '2px dashed rgba(255,255,255,0.7)';
        marker.style.boxSizing = 'border-box';
        marker.style.pointerEvents = 'none';
        marker.style.left = `${area.x * scaleX}px`;
        marker.style.top = `${area.y * scaleY}px`;
        marker.style.width = `${area.width * scaleX}px`;
        marker.style.height = `${area.height * scaleY}px`;
        
        const number = document.createElement('div');
        number.textContent = index + 1;
        number.style.position = 'absolute';
        number.style.top = '5px';
        number.style.left = '5px';
        number.style.backgroundColor = 'rgba(0,0,0,0.5)';
        number.style.color = 'white';
        number.style.borderRadius = '50%';
        number.style.width = '20px';
        number.style.height = '20px';
        number.style.display = 'flex';
        number.style.alignItems = 'center';
        number.style.justifyContent = 'center';
        number.style.fontSize = '12px';
        
        marker.appendChild(number);
        return marker;
    } */

    // =============================================
    // CAMERA CONTROLS
    // =============================================
    function toggleCamera() {
        cameraActive ? stopCamera() : startCamera();
    }

    function startCamera() {
        videoFeed.onerror = handleCameraError;
        videoFeed.src = "/video_feed?" + new Date().getTime();
        cameraActive = true;
        //setTimeout(updateVideoContainerLayout, 3000);
    }

    function stopCamera() {
        videoFeed.onerror = null;
        videoFeed.src = "";
        cameraActive = false;
        fetch("/stop_camera");
    }

    function handleCameraError() {
        if (cameraActive) {
            alert("Could not access camera. Please check permissions.");
            stopCamera();
        }
    }

    // =============================================
    // CAPTURE FUNCTIONALITY
    // =============================================
    function capturePose() {
        if (!cameraActive) {
            alert("Please enable the camera first");
            return;
        }
    
        captureBtn.disabled = true;
        captureBtn.textContent = "Capturing...";
    
        fetch("/capture_snapshot")

            .then(handleCaptureResponse)
            .then(handleCaptureSuccess)
            .catch(handleCaptureError)
            .finally(resetCaptureButton);
    }

    function startCountdown(seconds) {
        return new Promise((resolve) => {
            countdownDisplay.style.display = 'block';
            let count = seconds;

            const interval = setInterval(() => {
                countdownDisplay.textContent = '';
                countdownDisplay.textContent = count;
                count--;

                if (count < 0) {
                    clearInterval(interval);
                    countdownDisplay.style.display = 'none';
                    countdownDisplay.textContent = '';
                    shutter.classList.remove("section-inactive")
                    backToLayoutBtn.classList.remove("section-inactive");
                    resolve();
                }
            }, 1000);
        });
    }

    function triggerFlash() {
        flashOverlay.style.opacity = '1';
        setTimeout(() => {
            flashOverlay.style.opacity = '0';
        }, 100);
    }

    function handleCaptureResponse(response) {
        if (!response.ok) throw new Error("Capture failed");
        return response.blob();
    }

    function handleCaptureSuccess(imageBlob) {
        const imageUrl = URL.createObjectURL(imageBlob);
        
        if (isRetaking) {
            updateRetakenImage(imageUrl);
            showPreview();
            selectImage(currentPose - 1);
        } else {
            updateCapturedImage(imageUrl);
            advanceCaptureFlow();
        }
    }

    function updateRetakenImage(imageUrl) {
        if (capturedImages[retakeIndex]) {
            URL.revokeObjectURL(capturedImages[retakeIndex]);
        }
        capturedImages[retakeIndex] = imageUrl;
        isRetaking = false;
        retakeIndex = -1;
    }

    function updateCapturedImage(imageUrl) {
        if (capturedImages[currentPose - 1]) {
            URL.revokeObjectURL(capturedImages[currentPose - 1]);
        }
        capturedImages[currentPose - 1] = imageUrl;
    }

    function advanceCaptureFlow() {
        if (currentPose < 4) {
            currentPose++;
            updatePoseCounter();
        } else {
            renderTemplate();
            showPreview();
        }
    }

    function handleCaptureError(error) {
        console.error("Error capturing:", error);
        alert("Failed to capture photo. Please try again.");
    }

    function resetCaptureButton() {
        captureBtn.disabled = false;
        captureBtn.textContent = "Capture Pose";
    }

    function updatePoseCounter() {
        poseNumber.textContent = currentPose;
        
        if (videoContainer) {
            videoContainer.querySelectorAll('.layout-marker').forEach((marker, index) => {
                if (index === currentPose - 1) {
                    marker.style.border = '2px solid #4CAF50';
                    marker.style.boxShadow = '0 0 10px rgba(76, 175, 80, 0.8)';
                } else {
                    marker.style.border = '2px dashed rgba(255,255,255,0.7)';
                    marker.style.boxShadow = 'none';
                }
            });
        }

    }

    // =============================================
    // IMAGE PREVIEW AND SELECTION
    // =============================================
    function setupImagePreview() {
        imageSelectBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                selectImage(parseInt(this.dataset.index));
            });
        });
    
        editBtn.addEventListener('click', editImage);
        retakeBtn.addEventListener('click', retakeImage);
    
        if (capturedImages[0]) {
            selectImage(0);
        }
    }

    function selectImage(index) {
        currentlySelectedImageIndex = index;
        console.log("current index is: ", currentlySelectedImageIndex)
        imageSelectBtns.forEach(btn => {
            btn.classList.toggle('active', parseInt(btn.dataset.index) === index);
        });
        
        if (capturedImages[index]) {
            selectedImagePreview.src = capturedImages[index];
        } else {
            selectedImagePreview.src = '';
        }
    }
    
    //ito yung taga display???????
    function editImage() {
        if (!capturedImages[currentlySelectedImageIndex]) return;

        if(picEditState[currentlySelectedImageIndex] == false){
            enterEditMode(currentlySelectedImageIndex);
        }
        else{
            alert("The image has already been edited")
        }
    }

    function retakeImage() {
        if (!capturedImages[currentlySelectedImageIndex]) {
            alert("No image to retake");
            return;
        }

        if(retakeChances <= 0){
            alert("Retake chances has been used");
            return;
        }
    
        if (confirm("Are you sure you want to retake this photo?")) {
            setupRetakeState();
            switchToCaptureSection();
            prepareForRetake();
            picEditState[currentlySelectedImageIndex] = false; //para pwede na siyang maedit ulit
            isImageRaw = true;
            retakeChances -= 1;
        }
    }

    function setupRetakeState() {
        isRetaking = true;
        retakeIndex = currentlySelectedImageIndex;
    }

    function switchToCaptureSection() {
        previewSection.classList.remove("section-active");
        previewSection.classList.add("section-inactive");
        captureSection.classList.remove("section-inactive");
        captureSection.classList.add("section-active");
    }

    function prepareForRetake() {
        currentPose = currentlySelectedImageIndex + 1;
        updatePoseCounter();
        
        if (!cameraActive) {
            startCamera();
        }
    }

    // =============================================
    // TEMPLATE RENDERING
    // =============================================
    function renderTemplate() {
        ctx.clearRect(0, 0, resultCanvas.width, resultCanvas.height);

        // 1. First draw the colored template areas
        currentTemplate.areas.forEach(area => {
            ctx.fillStyle = area.color + '80'; // Semi-transparent
            ctx.fillRect(area.x, area.y, area.width, area.height);
        });

        // 2. Then draw the captured images
        const imagePromises = currentTemplate.areas.map((area, index) => {
            if (!capturedImages[index]) return Promise.resolve();
            
            return new Promise((resolve) => {
                const img = new Image();
                img.onload = function() {
                    const scale = Math.max(
                        area.width / img.width,
                        area.height / img.height
                    );

                    const scaledWidth = img.width * scale;
                    const scaledHeight = img.height * scale;
                    const sx = (scaledWidth - area.width) / 2;
                    const sy = (scaledHeight - area.height) / 2;

                    const offCanvas = document.createElement('canvas');
                    offCanvas.width = area.width;
                    offCanvas.height = area.height;
                    const offCtx = offCanvas.getContext('2d');

                    offCtx.drawImage(img, -sx, -sy, scaledWidth, scaledHeight);
                    ctx.drawImage(offCanvas, area.x, area.y);

                    // Optional border
                    ctx.strokeStyle = 'rgba(0,0,0,0.3)';
                    ctx.lineWidth = 4;
                    ctx.strokeRect(area.x, area.y, area.width, area.height);
                    resolve();
                };
                img.src = capturedImages[index];
            });
        });

        // 3. After all images are drawn, add the frame overlay
        return Promise.all(imagePromises).then(() => {
            if (selectedBG) {
                return new Promise((resolve) => {
                    const frameImg = new Image();
                    frameImg.onload = function() {
                        ctx.drawImage(frameImg, 0, 0, resultCanvas.width, resultCanvas.height);
                        resolve();
                    };
                    frameImg.src = selectedBG;
                });
            }
            return Promise.resolve();
        });
    }

    // =============================================
    // EDIT MODE FUNCTIONALITY
    // =============================================
    function setupEditMode() {
        modeButtons.forEach(btn => {

            btn.addEventListener('click', () => activateMode(btn));
        });
    
        backFromEditBtn.addEventListener('click', exitEditMode);
        applyEditBtn.addEventListener('click', applyEdit);

        //Event listener for color filter buttons. possible malipat somewhere if ginawang dynamic si color filter
        document.querySelectorAll('#colors .circle-button').forEach((btn, index) => {
            btn.addEventListener('click', () => applyColorFilter(index));
        });
        editControls.classList.add('section-inactive');
        preview.classList.add('section-active');
    }

    //ito yung pagpasok mo mismo ng edit part ng site. ito na din ang responsible para maibigay
    //ang image doon sa container

    function enterEditMode(index) {
        monitorEditSection();
        currentEditImageIndex = index;
        const img = new Image();
        
        img.onload = function() {
            console.log("Image width:", img.width);
            console.log("Image height:", img.height);
            editCanvas.width = img.width;
            editCanvas.height = img.height;
            editCtx.drawImage(img, 0, 0);
        };
        img.src = capturedImages[index];
        insertSelectedImageInEditMode(capturedImages[index])
        getImageForSticker(capturedImages[index])

        preview.classList.remove("section-active");
        preview.classList.add("section-inactive");
        editControls.classList.remove('section-inactive');
        editControls.classList.add('section-active');
    }

    //saves sends the image to python for color manipulation
    //magsesend ito ng blob image na dapat irereceive in flask
    //optimize this
    function insertSelectedImageInEditMode(urlBlob){
        fetch(urlBlob)
        .then(response=>response.blob())
        .then(blob => {
            const formData = new FormData();
            formData.append("image", blob)
            //console.log("natawag ako")
            fetch('get_image_edit', {
                method: 'POST', 
                body: formData,
            })
            .then(res => res.json())
            .then(data => console.log("Response from Flask:", data))
            .catch(err => console.error("Error:", err));
        })
        .catch(err => console.error("Error fetching blob:", err));
    }

    function activateMode(btn) {
        modeButtons.forEach(b => b.classList.remove('active'));  
        btn.classList.add('active'); 
        modeFilter.forEach(set => set.classList.remove('visible'));
        document.getElementById(btn.getAttribute('data-target')).classList.add('visible');
    }

    // --- Sticker functions
    
    //binabasa yung sticker folder then render the buttons. also gumagawa ng slide for sticker carousel.
    function loadStickersDynamically() {
        fetch('/api/stickers')
            .then(res => {
                if (!res.ok) throw new Error("Failed to fetch stickers");
                return res.json();
            })
            .then(files => {
                const stickerContainer = document.getElementById("stickers");
                stickerContainer.style.alignItems = 'center';
                stickerContainer.style.justifyContent = 'center';
                stickerContainer.innerHTML = `
                <button class="sticker-nav-button prev" aria-label="Previous stickers">&#10094;</button>
                    <div class="sticker-carousel-container">
                        <div class="sticker-carousel-track"></div>
                    </div>
                <button class="sticker-nav-button next" aria-label="Next stickers">&#10095;</button>
                `;
                
                const track = stickerContainer.querySelector('.sticker-carousel-track');
                let currentPage = 0;
                const stickersPerPage = 6;
                const totalPages = Math.ceil(files.length / stickersPerPage);
    
                // Create all sticker slides
                for (let i = 0; i < totalPages; i++) {
                    const slide = document.createElement('div');
                    slide.className = 'sticker-slide';
                    slide.dataset.page = i;
                    
                    // Add stickers for this page (slides)
                    const startIdx = i * stickersPerPage;
                    const endIdx = startIdx + stickersPerPage;
                    const pageFiles = files.slice(startIdx, endIdx);
                    
                    pageFiles.forEach(file => {
                        const baseName = file.split('.')[0];
                        const id = `${baseName}-sticker`;
                        const src = `/static/stickers/${file}`;
                        const alt = baseName.replace(/-/g, ' ');
    
                        const button = document.createElement("button");
                        button.className = "circle-button-sticker";
                        button.title = alt;
                        button.dataset.stickerId = id;
    
                        const img = document.createElement("img");
                        img.src = src;
                        img.alt = alt;
                        img.draggable = true;
                        img.classList.add("sticker-img");
                        img.dataset.stickerType = alt;
    
                        button.appendChild(img);
                        slide.appendChild(button);
                    });
                    
                    track.appendChild(slide);
                }
    
                stickerImages = Array.from(document.querySelectorAll('.sticker-img'));
                addStickerEventListener();
                
                setupStickerCarousel(stickerContainer, totalPages);
            })
            .catch(err => {
                console.error("Failed to load stickers:", err);
            });
    }
    //sticker carousel
    function setupStickerCarousel(container, totalPages) {
        const track = container.querySelector('.sticker-carousel-track');
        const prevBtn = container.querySelector('.sticker-nav-button.prev');
        const nextBtn = container.querySelector('.sticker-nav-button.next');
        let currentPage = 0;
    
        function updateCarousel() {
            track.style.transform = `translateX(-${currentPage * 100}%)`;
            prevBtn.disabled = currentPage === 0;
            nextBtn.disabled = currentPage === totalPages - 1;
        }
    
        prevBtn.addEventListener('click', () => {
            if (currentPage > 0) {
                currentPage--;
                updateCarousel();
            }
        });
    
        nextBtn.addEventListener('click', () => {
            if (currentPage < totalPages - 1) {
                currentPage++;
                updateCarousel();
            }
        });
    
        updateCarousel();
    }

    // --- Color Filter Functions
    
    //gumagawa ng slide for carousel function
    function groupColorButtonsIntoSlides() {
        const track = document.querySelector('.color-carousel-track');
        const buttons = Array.from(track.querySelectorAll('.circle-button-color'));
    
        const buttonsPerSlide = 6;
    
        // Clear existing slides
        track.innerHTML = '';
    
        for (let i = 0; i < buttons.length; i += buttonsPerSlide) {
            const slide = document.createElement('div');
            slide.className = 'color-slide';
    
            const group = buttons.slice(i, i + buttonsPerSlide);
            group.forEach(btn => slide.appendChild(btn));
            track.appendChild(slide);
        }
    }
    //color carousel
    function setupColorCarousel() {
        const colorsCont = document.querySelector('#colors');
        const container = document.querySelector('#colors .color-carousel-container');
        const track = container.querySelector('.color-carousel-track');
        const prevBtn = colorsCont.querySelector('.color-nav-button.prev');
        const nextBtn = colorsCont.querySelector('.color-nav-button.next');
        const slides = container.querySelectorAll('.color-slide');
        let currentPage = 0;
        const totalPages = slides.length;
    
        function updateCarousel() {
            track.style.transform = `translateX(-${currentPage * 100}%)`;
            
            // Disable buttons when at boundaries
            prevBtn.disabled = currentPage === 0;
            nextBtn.disabled = currentPage === totalPages - 1;
        }
    
        prevBtn.addEventListener('click', () => {
            if (currentPage > 0) {
                currentPage--;
                updateCarousel();
            }
        });
    
        nextBtn.addEventListener('click', () => {
            if (currentPage < totalPages - 1) {
                currentPage++;
                updateCarousel();
            }
        });
    
        // Initialize
        updateCarousel();
    }

    //kukunin nito yung index ng pinindot na button mula sa available na filters
    colorButtons.forEach((btn, index)=>{
        btn.addEventListener('click', () => {
            displayFilterImage(index);
        })
    })

    //convert blob to image url para madisplay
    function getFilteredImage(index) {
        let routeString;
        console.log("Index received: ", index)
        switch(index){
            case -1:
                routeString = '/get_raw';
                isImageRaw = true;
                break
            case 0:
                routeString = '/get_grayscaled';
                break;
            case 1:
                routeString = '/get_sepia';
                break;
            case 2:
                routeString = '/get_inverted';
                break;
            case 3:
                routeString = '/get_sketched';
                break;
            case 4:
                routeString = '/get_warm';
                break;
            case 5:
                routeString = '/get_blue';
                break;
            case 6:
                routeString = '/get_bright';
                break;
            case 7:
                routeString = '/get_cartoon';
                break;
            case 8:
                routeString = '/get_green';
                break;
            default:
                console.error("Invalid filter index:", index); //how the fuck did you get in here
                return Promise.resolve(null);  // Dunno how it works pero hayaan lang ito
        }
        //console.log("route string: ", routeString);
        if(routeString == '/get_raw'){ isImageRaw = true;}
        else{ isImageRaw = false; }

        console.log("isImageRaw value: ", isImageRaw);

        return fetch(routeString)
        .then(response =>{
            if (!response .ok){
                throw new Error('failed to fetch filtered image')
            }
            return response.blob(); 
        })
        .then(imageBlob=>{
            const imageUrl = URL.createObjectURL(imageBlob);
            return imageUrl;
        })
        .catch(error => {
            console.error("Error fetching filtered image:", error);
            return null;  // Return null if there's an error
        });
    }

    // dinidisplay lang nito yung image na makukuha nya
    function displayFilterImage(buttonIndex) {
        if (currentButtonIndex === buttonIndex) {
            currentButtonIndex = -1; //para makuha yung raw image ulit kailangan ito
        } else {
            currentButtonIndex = buttonIndex;
        }
        
        //does the convertion of the blob to image url
        getFilteredImage(currentButtonIndex).then(imageUrl => {
            if (imageUrl) {
                const img = new Image();
                img.onload = function() {
                    editCanvas.width = img.width;
                    editCanvas.height = img.height;
                    editCtx.drawImage(img, 0, 0);
                };
                img.src = imageUrl;
            }
            else {
                console.warn("No image URL returned.");
            }
        });
    }

    function getImageForSticker(urlBlob){
        fetch(urlBlob)
        .then(response=>response.blob())
        .then(blob => {
            const formData = new FormData();
            formData.append("image", blob)
            fetch('/get_image_sticker', {
                method: 'POST', 
                body: formData,
            })
            .then(res => res.json())
            .then(data => console.log("Response from Flask:", data))
            .catch(err => console.error("Error:", err));
        })
        .catch(err => console.error("Error fetching blob:", err));
    }


    function exitEditMode() {
        preview.classList.remove("section-inactive");
        preview.classList.add("section-active");
        editControls.classList.remove('section-active');
        editControls.classList.add('section-inactive');
        isImageRaw = true;
        clearBoundingBoxes();
        removeExistingStickers();
    }

    function applyEdit() {
        const editCanvas = document.getElementById('edit-canvas');
        const mergedCanvas = document.createElement('canvas');
        mergedCanvas.width = 640;  // base resolution
        mergedCanvas.height = 360;
        const ctx = mergedCanvas.getContext('2d');
        ctx.drawImage(editCanvas, 0, 0, 640, 360);  //copy here


        if(!isObjectEmpty(stickerMetaData)){
            /*
            const editCanvas = document.getElementById('edit-canvas');
            const mergedCanvas = document.createElement('canvas');
            mergedCanvas.width = 640;  // base resolution
            mergedCanvas.height = 480;
            const ctx = mergedCanvas.getContext('2d');

            ctx.drawImage(editCanvas, 0, 0, 640, 480);
            */

            // redraw all stickers now with its original values
            for (const data of Object.values(stickerMetaData)) {
                const stickerImg = new Image();
                stickerImg.src = data.imgSrc;

                if (stickerImg.complete) {
                    ctx.drawImage(stickerImg, data.x, data.y, data.width, data.height);
                } else {
                    stickerImg.onload = () => {
                        ctx.drawImage(stickerImg, data.x, data.y, data.width, data.height);
                    };
                }
            }
            picEditState[currentEditImageIndex] = true;

        }
        else{
            picEditState[currentEditImageIndex] = false;
        }

        const editedImageData = mergedCanvas.toDataURL('image/png');
        capturedImages[currentEditImageIndex] = editedImageData;
        selectedImagePreview.src = editedImageData;

        if(isImageRaw == false) {picEditState[currentEditImageIndex] = true;} //crucial placement ito kaya ito nandito kasi masisira yung overlay for some reason

        renderTemplate();
        exitEditMode();
        removeExistingStickers();
        clearBoundingBoxes();
    }

    const isObjectEmpty = (objectName =>{
        return(
            objectName && Object.keys(objectName).length === 0 && objectName.constructor === Object
        );
    });

    function applyColorFilter(index) {
        editCtx.fillStyle = `rgba(${index * 40}, ${index * 30}, ${index * 50}, 0.3)`;
        editCtx.fillRect(0, 0, editCanvas.width, editCanvas.height);
    }

    /*
    ================================================
    DRAG-DROP SECTION AND STICKER CONTROL
    ================================================
    */ 

    //para malaman kung edit na ba talaga
    function monitorEditSection() {
        const observer = new MutationObserver(() => {
            const isVisible = !editControls.classList.contains('section-inactive');
            
            if (isVisible) {
                //console.log('edit loaded');
    
                setTimeout(() => {
                    addStickerEventListener();
                    addEditCanvaEventListener();
                    addDoubleClickForSticker();
                }, 50);
    
                observer.disconnect();
            }
        });
    
        observer.observe(editControls, {
            attributes: true,
            attributeFilter: ['class'],
        });
    
        if (!editControls.classList.contains('section-inactive')) {
            setTimeout(() => {
                console.log('edit visible');
                addStickerEventListener();
            }, 50);
        }
    }

    //grrreeeeennnnnnnnn
    function drawBoundingBoxes(boxes) {

        if (boxes == null){ return;} //incase na walang mukhang nakita

        const ctx = createOverlayCanvas();
        const overlay = document.getElementById('overlay-canvas');
    
        ctx.clearRect(0, 0, overlay.width, overlay.height);
        ctx.strokeStyle = 'lime';
        ctx.lineWidth = 2;
        
        boxes.forEach(box => {
            ctx.beginPath(); 
            ctx.rect(box.x, box.y, box.w, box.h);  
            ctx.stroke();  
        });
    }
    
        
    //lahat ng exsisting stickers ay lalagyan ng draggable
    function addStickerEventListener(){
        if (stickerImages.length === 0) {
            console.log("No draggable stickers found.");
            return;
        }
        stickerImages.forEach((sticker) => {
            sticker.addEventListener('dragstart', (event) => {
                event.dataTransfer.setData('text/plain', sticker.src);
                sticker_alt = sticker.alt;

                fetch('/set_face_boxes')
                .then(res => res.json())
                .then(data => {
                    console.log("bounding boxes", data.boxes)
                    drawBoundingBoxes(data.boxes)
                })
                .catch(err => console.error("Failed to fetch face boxes", err));
            });
            sticker.addEventListener('dragend', ()=>{
                removeOverlayCanvas();
            })
        });
    }

    //for special scenario na may overlap ng bounding boxes
    async function getFaceIndex(x, y) {
        const res = await fetch('/set_face_boxes');
        const data = await res.json();
        const boxes = data.boxes;

        let closestIndex = null;
        let minDistance = Infinity;

        boxes.forEach((box, index) => {
            if (
                x >= box.x &&
                x <= box.x + box.w &&
                y >= box.y &&
                y <= box.y + box.h
            ) {
                const centerX = box.x + box.w / 2;
                const centerY = box.y + box.h / 2;
                const dx = x - centerX;
                const dy = y - centerY;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < minDistance) {
                    minDistance = distance;
                    closestIndex = index;
                }
            }
        });

        return closestIndex; // returns null if no box contains the point
    }

    //sticker snap occurs here
    function addEditCanvaEventListener(){
        let faceIndex = -1;

        if(editCanvas){
            editCanvas.addEventListener('dragover', function(event){
                event.preventDefault();
            });

            editCanvas.addEventListener('drop', async function(event){
                event.preventDefault();
                const rect = editCanvas.getBoundingClientRect();
                const scaleX = editCanvas.width / editCanvas.offsetWidth;
                const scaleY = editCanvas.height / editCanvas.offsetHeight;

                const dropX = (event.clientX - rect.left) * scaleX;
                const dropY = (event.clientY - rect.top) * scaleY;

                faceIndex = await getFaceIndex(dropX, dropY);
                console.log("the index is: ", faceIndex);

                if(faceIndex == null){return;} //kapag walang mukhang nadetect ay ito ang sasalo

                if (faceIndex !== -1) {
                    console.log("inside a face");

                    let formData = new FormData();
                    formData.append('faceIndex', faceIndex);
                    formData.append('stickerType', sticker_alt);
                
                    fetch('/set_face_index', {
                        method: 'POST',
                        body: formData
                    })
                    .then(res => res.json())
                    .then(data => {
                        console.log('Data sent, response:', data);
                        fetch("/get_warped_sticker")
                        .then(res => res.json())
                        .then(data => {
                            const img = new Image();
                            img.onload = function() {
                                setStickertoExistingSticker(faceIndex); //umayos kang method ka hayp ka
                                //store values for saving purposes
                                stickerMetaData[faceIndex] = {
                                    imgSrc: "data:image/png;base64," + data.sticker,   
                                    //original position nila sa 640x480 na scaling
                                    x: data.x,              
                                    y: data.y,
                                    width: data.width,
                                    height: data.height
                                }
                                drawStickers(img, data.x, data.y, data.width, data.height, faceIndex);
                                //console.log("image data: ", data.x, data.y, data.width, data.height);
                            };
                            img.src = "data:image/png;base64," + data.sticker;
                        });
                    })
                    .catch(error => {
                        console.error('Request failed', error);
                    });

                    //need to make a canvas para mailagay yung mismong sticker
                } else {
                    console.log("outside face");
                }
            });
        }
    }
    
    function addDoubleClickForSticker() {
        let faceIndex = -1
        editCanvas.addEventListener('dblclick', async function(event) { 

            event.preventDefault();
            const rect = editCanvas.getBoundingClientRect();
            const scaleX = editCanvas.width / editCanvas.offsetWidth;
            const scaleY = editCanvas.height / editCanvas.offsetHeight;

            const dropX = (event.clientX - rect.left) * scaleX;
            const dropY = (event.clientY - rect.top) * scaleY;

            faceIndex = await getFaceIndex(dropX, dropY);

            if (faceIndex !== -1){
                if(stickerTracker[faceIndex]){
                        stickerTracker[faceIndex].remove();
                        delete stickerMetaData[faceIndex];
                        //stickerTracker.delete('value');
                        console.log("selected sticker deleted")
                    }                    
                }
        }); 
    }
       
    //gagawa ito ng maliliit na overlays depending doon sa size na ibibigay ni flask
    function createStickerOverlayCanvas(x, y, width, height){
        const parent = document.getElementById('edit-canvas');
        let stickerGroup = document.getElementById('sticker-group');

        if (!stickerGroup) {
            stickerGroup = document.createElement('div');
            stickerGroup.id = 'sticker-group';
            stickerGroup.style.position = 'absolute';
            stickerGroup.style.top = '0';
            stickerGroup.style.left = '0';
            stickerGroup.style.width = '100%';
            stickerGroup.style.height = '100%';
            stickerGroup.style.pointerEvents = 'none'; 
            parent.parentElement.appendChild(stickerGroup);
        }
    
        const overlay = document.createElement('canvas');
        overlay.className = 'sticker-canvas'; 
        overlay.style.position = 'absolute';
        overlay.style.pointerEvents = 'none'; 
        overlay.style.zIndex = '999';
    
        //parent.parentElement.style.position = 'relative';
    
        overlay.width = width;
        overlay.height = height;
        overlay.style.width = width + 'px';
        overlay.style.height = height + 'px';
        overlay.style.left = x + 'px';
        overlay.style.top = y + 'px';
    
        stickerGroup.appendChild(overlay);
    
        return overlay.getContext('2d');
    }

    function drawStickers(img, x, y, width, height, faceIndex) {
        const newImg = new Image();
        newImg.onload = function () {
            const editCanvas = document.getElementById('edit-canvas');
    
            // scaling down ng mga sticekrs
            const scaleX = editCanvas.offsetWidth / editCanvas.width;
            const scaleY = editCanvas.offsetHeight / editCanvas.height;
            const scaledX = x * scaleX;
            const scaledY = y * scaleY;
            const scaledWidth = width * scaleX;
            const scaledHeight = height * scaleY;
    
            const ctx = createStickerOverlayCanvas(scaledX, scaledY, scaledWidth, scaledHeight);
            ctx.drawImage(newImg, 0, 0, scaledWidth, scaledHeight);
            stickerTracker[faceIndex] = ctx.canvas
        };
        newImg.src = img.src;
    }
    
    function createOverlayCanvas(parentId = 'edit-canvas') {
        const parent = document.getElementById(parentId);
        let overlay = document.getElementById('overlay-canvas');
    
        if (!overlay) {
            overlay = document.createElement('canvas');
            overlay.id = 'overlay-canvas';
            overlay.style.position = 'absolute';
            overlay.style.pointerEvents = 'none'; 
            overlay.style.zIndex = '999';
    
            parent.parentElement.style.position = 'relative';
        }
    
        overlay.width = parent.width;
        overlay.height = parent.height;
        overlay.style.width = parent.offsetWidth + 'px';
        overlay.style.height = parent.offsetHeight + 'px';
        overlay.style.left = parent.offsetLeft + 'px';
        overlay.style.top = parent.offsetTop + 'px';
        parent.parentElement.appendChild(overlay);

        return overlay.getContext('2d');
    }
    
    
    function removeOverlayCanvas() {
        const overlay = document.getElementById('overlay-canvas');
        if (overlay) {
            console.log("removed");
            overlay.remove();
        }
    }

    function removeExistingStickers(){
        const stickerGroup = document.getElementById('sticker-group');
        if (stickerGroup) {
            stickerGroup.remove();
            
            for (let key in stickerMetaData) {
                delete stickerMetaData[key];
            }
            console.log("All stickers removed");
        }
    }

    function setStickertoExistingSticker(index){
       
        if(stickerTracker[index]){
            stickerTracker[index].remove();
            delete stickerMetaData[index];
            console.log("sticker replaced")
        }

    }

    function clearBoundingBoxes(){
        console.log("boxes cleared")
        fetch('/clear_boxes')
        .then(response => response.json())
        .then(data=>{
            console.log(data.message);
        })
        .catch(err=>console.error("Error:", err));
    }

    // =============================================
    // NAVIGATION AND FLOW CONTROL
    // =============================================
    function showPreview() {
        captureSection.classList.remove("section-active");
        captureSection.classList.add("section-inactive");
        previewSection.classList.remove("section-inactive");
        previewSection.classList.add("section-active");
        
        setupImagePreview();
        
        if (isRetaking) {
            selectImage(retakeIndex);
            isRetaking = false;
            retakeIndex = -1;
        } else if (capturedImages[0]) {
            selectImage(0);
        }
        
        renderTemplate();
    }

    function confirmLayout() {
        if (!currentTemplate) {
            alert('Please select a layout first');
            return;
        }
        
        layoutSelection.classList.remove('section-active');
        layoutSelection.classList.add('section-inactive');
        captureSection.classList.remove('section-inactive');
        captureSection.classList.add('section-active');
        backToModeBtn.classList.add('section-inactive');
        
        layoutName.textContent = currentTemplate.name;
        updatePoseCounter();
    }

    async function saveLayout() {
        await renderTemplate();
        previewSection.classList.remove("section-active");
        previewSection.classList.add("section-inactive");
        finalResultSection.classList.remove("section-inactive");
        finalResultSection.classList.add("section-active");
    }

    function downloadResult() {
        localStorage.removeItem('countdownEnd');    //RESET TIMER
        stopCamera();

        
        /*
        const link = document.createElement('a');
        link.download = `photo-booth-${currentTemplate.name.toLowerCase().replace(/ /g, '-')}-${new Date().getTime()}.png`;
        link.href = resultCanvas.toDataURL('image/png');
        link.click();
        */
        if(capturedImages.length === 0){
            console.log("nothing so download");
            return;
        }

        const session_id = localStorage.getItem('session_id');
        console.log(session_id);
        

        resultCanvas.toBlob(blob => {
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

                   /* fetch(`/print/${session_id}`, {
        method: "POST"
    })
    .then(res => res.json())
    .then(data => alert(data.status || data.error))
    .catch(err => alert("Network error: " + err));
    */
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
    function returnToLayout() {
        if (confirm("Are you sure you want to go back to layout selection? All captured images will be lost.")) {
            resetCaptureState();
            switchToLayoutSelection();
        }
    }

    function resetCaptureState() {
        capturedImages.forEach(img => {
            if (img) URL.revokeObjectURL(img);
        });
        
        capturedImages = Array(4).fill(null);
        currentPose = 1;
        isRetaking = false;
        retakeIndex = -1;
    }

    function switchToLayoutSelection() {
        captureSection.classList.remove("section-active");
        captureSection.classList.add("section-inactive");
        layoutSelection.classList.remove("section-inactive");
        layoutSelection.classList.add("section-active");
        backToModeBtn.classList.remove("section-inactive");
        //stopCamera();
        //startCamera();
    }

    function startOver() {
        if (confirm("Are you sure you want to retake all photos?")) {
            resetCaptureState();
            switchToCaptureSection();
            updatePoseCounter();
	    picEditState = [false, false, false, false];

        }
    }

    // =============================================
    // EVENT LISTENERS SETUP
    // =============================================
    function setupEventListeners() {

        
        
        // Template selection
        templateContainer.addEventListener('click', handleTemplateClick);
        
        // Camera and capture
        captureBtn.addEventListener('click', async () => {
            shutter.classList.add("section-inactive");
            backToLayoutBtn.classList.add("section-inactive");
            await startCountdown(3);
            triggerFlash();
            
            setTimeout(() => {
                capturePose();
            }, 150);
        });
        confirmLayoutBtn.addEventListener('click', confirmLayout);
        
        // Navigation
        backToLayoutBtn.addEventListener('click', returnToLayout);
        saveBtn.addEventListener('click', saveLayout);
        downloadBtn.addEventListener('click', downloadResult);
        backToPreviewBtn.addEventListener('click', () => {
            finalResultSection.classList.remove("section-active");
            finalResultSection.classList.add("section-inactive");
            previewSection.classList.remove("section-inactive");
            previewSection.classList.add("section-active");
        });
        
        startOverBtn.addEventListener('click', startOver);
        
        // Window events
        //window.addEventListener('resize', updateVideoContainerLayout);
        window.addEventListener("beforeunload", cleanupBeforeUnload);
    }

    function handleTemplateClick(e) {
        const option = e.target.closest('.template-option');
        if (!option) return;
        
        const index = carouselItems.indexOf(option);
        if (index !== -1) selectItem(index);
    }

    function cleanupBeforeUnload() {
        capturedImages.forEach(img => {
            if (img) URL.revokeObjectURL(img);
        });
        stopCamera();
    }

    // =============================================
    // INITIALIZE THE APPLICATION
    // =============================================
    initialize();
    //111111
});