document.addEventListener("DOMContentLoaded", function() {
    // =============================================
    // CONSTANTS AND CONFIGURATION
    // =============================================
    const TEMPLATE_CONFIG = {
        grid: {
            name: "Classic Grid",
            areas: [
                { x: 0, y: 0, width: 900, height: 600, color: '#FFDDC1' }, // Top-left
                { x: 900, y: 0, width: 900, height: 600, color: '#C1FFD7' }, // Top-right
                { x: 0, y: 600, width: 900, height: 600, color: '#C1D7FF' }, // Bottom-left
                { x: 900, y: 600, width: 900, height: 600, color: '#FFC1E3' } // Bottom-right
            ]
        },
        featured: {
            name: "Featured + 3",
            areas: [
                { x: 0, y: 0, width: 1200, height: 600, color: '#FFDDC1' }, // Main featured
                { x: 0, y: 600, width: 600, height: 600, color: '#C1FFD7' }, // Small 1
                { x: 600, y: 600, width: 600, height: 600, color: '#C1D7FF' }, // Small 2
                { x: 1200, y: 0, width: 600, height: 1200, color: '#FFC1E3' } // Small 3
            ]
        },
        vertical: {
            name: "Vertical Strip",
            areas: [
                { x: 0, y: 0, width: 450, height: 1200, color: '#FFDDC1' }, // Left
                { x: 450, y: 0, width: 450, height: 1200, color: '#C1FFD7' }, // Middle-left
                { x: 900, y: 0, width: 450, height: 1200, color: '#C1D7FF' }, // Middle-right
                { x: 1350, y: 0, width: 450, height: 1200, color: '#FFC1E3' } // Right
            ]
        },
        horizontal: {
            name: "Horizontal Strip",
            areas: [
                { x: 0, y: 0, width: 1800, height: 300, color: '#FFDDC1' }, // Left
                { x: 0, y: 300, width: 1800, height: 300, color: '#C1FFD7' }, // Middle-left
                { x: 0, y: 600, width: 1800, height: 300, color: '#C1D7FF' }, // Middle-right
                { x: 0, y: 900, width: 1800, height: 300, color: '#FFC1E3' } // Right
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
    
    // Capture Section Elements
    const captureSection = document.getElementById('capture-section');
    const videoFeed = document.getElementById('video-feed');
    const videoContainer = document.querySelector('.video-container');
    const toggleCameraBtn = document.getElementById('toggle-camera');
    const captureBtn = document.getElementById('capture-btn');
    const poseNumber = document.getElementById('pose-number');
    const confirmLayoutBtn = document.getElementById('confirm-layout');
    
    // Preview Section Elements
    const previewSection = document.getElementById('preview-section');
    const saveBtn = document.getElementById('save-layout');
    const startOverBtn = document.getElementById('start-over');
    const backToLayoutBtn = document.getElementById('back-to-layout');
    const imageSelectBtns = document.querySelectorAll('.image-select-btn');
    const selectedImagePreview = document.getElementById('selected-image-preview');
    const editBtn = document.getElementById('edit-btn');
    const retakeBtn = document.getElementById('retake-btn');
    
    // Canvas Elements
    const resultCanvas = document.getElementById('result-canvas');
    const ctx = resultCanvas.getContext('2d');
    
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
    const colorButtons = document.querySelectorAll('.circle-button-color')

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
    let filterButtonPressedAgain = false;

    // =============================================
    // INITIALIZATION
    // =============================================
    window.addEventListener('load', startCamera);
    window.addEventListener('beforeunload', stopCamera);
    
    function initialize() {
        resultCanvas.width = 1800;
        resultCanvas.height = 1200;
        
        setupEditMode();
        renderTemplates();
        setupEventListeners();
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
        container.style.position = 'relative';
        container.style.width = '100%';
        container.style.height = '100%';
        
        const originalWidth = Math.max(...template.areas.map(area => area.x + area.width));
        const originalHeight = Math.max(...template.areas.map(area => area.y + area.height));
        const previewWidth = 300;
        const previewHeight = 200;
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
        currentIndex = index;
    }

    function handleKeyboardNavigation(e) {
        if (layoutSelection.classList.contains('section-active')) {
            if (e.key === 'ArrowLeft') navigateCarousel(-1);
            if (e.key === 'ArrowRight') navigateCarousel(1);
        }
    }

    function updateVideoContainerLayout() {
        videoContainer.querySelectorAll('.layout-marker').forEach(marker => marker.remove());
        if (!currentTemplate) return;
        
        currentTemplate.areas.forEach((area, index) => {
            const marker = createLayoutMarker(area, index);
            videoContainer.appendChild(marker);
        });
    }

    function createLayoutMarker(area, index) {
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
    }

    // =============================================
    // CAMERA CONTROLS
    // =============================================
    function toggleCamera() {
        cameraActive ? stopCamera() : startCamera();
    }

    function startCamera() {
        videoFeed.onerror = handleCameraError;
        videoFeed.src = "/video_feed?" + new Date().getTime();
        toggleCameraBtn.textContent = "Close Camera";
        cameraActive = true;
        setTimeout(updateVideoContainerLayout, 100);
    }

    function stopCamera() {
        videoFeed.onerror = null;
        videoFeed.src = "";
        toggleCameraBtn.textContent = "Open Camera";
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
        enterEditMode(currentlySelectedImageIndex);
    }

    function retakeImage() {
        if (!capturedImages[currentlySelectedImageIndex]) {
            alert("No image to retake");
            return;
        }
    
        if (confirm("Are you sure you want to retake this photo?")) {
            setupRetakeState();
            switchToCaptureSection();
            prepareForRetake();
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
        // Draw colored background for each area
        currentTemplate.areas.forEach(area => {
            ctx.fillStyle = area.color + '80';
            ctx.fillRect(area.x, area.y, area.width, area.height);
        });
        
        // Draw the images
        currentTemplate.areas.forEach((area, index) => {
            if (capturedImages[index]) {
                drawImageInArea(area, index);
            }
        });
    }

    function drawImageInArea(area, index) {
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
        };
        img.src = capturedImages[index];
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
        setupStickerAndFilterButtons();
    }


    function activateMode(btn) {
        modeButtons.forEach(b => b.classList.remove('active'));  
        btn.classList.add('active'); 
        modeFilter.forEach(set => set.classList.remove('visible'));
        document.getElementById(btn.getAttribute('data-target')).classList.add('visible');
    }

    
    //ito yung pagpasok mo mismo ng edit part ng site. ito na din ang responsible para maibigay
    //ang image doon sa container

    function enterEditMode(index) {
        currentEditImageIndex = index;
        const img = new Image();
        
        img.onload = function() {
            editCanvas.width = img.width;
            editCanvas.height = img.height;
            editCtx.drawImage(img, 0, 0);
        };
        
        img.src = capturedImages[index];
        insertSelectedImageInEditMode(capturedImages[index])
        editControls.classList.remove('hidden');
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
            console.log("natawag ako")
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

    //kukunin nito yung index ng pinindot na button mula sa available na filters
    colorButtons.forEach((btn, index)=>{
        btn.addEventListener('click', () => {
            //console.log('Clicked button index: ', index)
            //currentButtonIndex = index;
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
            default:
                console.error("Invalid filter index:", index);
                return Promise.resolve(null);  // Dunno how it works pero hayaan lang ito
        }

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

    function exitEditMode() {
        editControls.classList.add('hidden');
    }

    function applyEdit() {
        const editedImageData = editCanvas.toDataURL('image/png');

        if (capturedImages[currentEditImageIndex]) {
            URL.revokeObjectURL(capturedImages[currentEditImageIndex]);
        }
        
        capturedImages[currentEditImageIndex] = editedImageData;
        selectedImagePreview.src = editedImageData;
        renderTemplate();
        exitEditMode();
    }

    function setupStickerAndFilterButtons() {
        document.querySelectorAll('#stickers .circle-button').forEach((btn, index) => {
            btn.addEventListener('click', () => addSticker(index));
        });

        document.querySelectorAll('#colors .circle-button').forEach((btn, index) => {
            btn.addEventListener('click', () => applyColorFilter(index));
        });
    }

    function addSticker(index) {
        editCtx.fillStyle = 'white';
        editCtx.font = '20px Arial';
        editCtx.fillText(`Sticker ${index + 1}`, 50, 50);
    }

    function applyColorFilter(index) {
        editCtx.fillStyle = `rgba(${index * 40}, ${index * 30}, ${index * 50}, 0.3)`;
        editCtx.fillRect(0, 0, editCanvas.width, editCanvas.height);
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
        
        layoutName.textContent = currentTemplate.name;
        updatePoseCounter();
    }

    function saveLayout() {
        renderTemplate();
        previewSection.classList.remove("section-active");
        previewSection.classList.add("section-inactive");
        finalResultSection.classList.remove("section-inactive");
        finalResultSection.classList.add("section-active");
    }

    function downloadResult() {
        const link = document.createElement('a');
        link.download = `photo-booth-${currentTemplate.name.toLowerCase().replace(/ /g, '-')}-${new Date().getTime()}.png`;
        link.href = resultCanvas.toDataURL('image/png');
        link.click();
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
        stopCamera();
    }

    function startOver() {
        if (confirm("Are you sure you want to retake all photos?")) {
            resetCaptureState();
            switchToCaptureSection();
            updatePoseCounter();
        }
    }

    // =============================================
    // EVENT LISTENERS SETUP
    // =============================================
    function setupEventListeners() {
        // Template selection
        templateContainer.addEventListener('click', handleTemplateClick);
        
        // Camera and capture
        toggleCameraBtn.addEventListener('click', toggleCamera);
        captureBtn.addEventListener('click', capturePose);
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
        window.addEventListener('resize', updateVideoContainerLayout);
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