document.addEventListener("DOMContentLoaded", function() {
    // Layout Templates (4R size - 1800×1200)
    const templates = {
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
        },
    };

    // DOM Elements
    const templateContainer = document.getElementById('template-container');
    const layoutSelection = document.getElementById('layout-selection');
    const captureSection = document.getElementById('capture-section');
    const previewSection = document.getElementById('preview-section');
    const confirmLayoutBtn = document.getElementById('confirm-layout');
    const toggleCameraBtn = document.getElementById('toggle-camera');
    const videoFeed = document.getElementById('video-feed');
    const captureBtn = document.getElementById('capture-btn');
    const poseNumber = document.getElementById('pose-number');
    const layoutName = document.getElementById('layout-name');
    const saveBtn = document.getElementById('save-layout');
    const startOverBtn = document.getElementById('start-over');
    const resultCanvas = document.getElementById('result-canvas');
    const ctx = resultCanvas.getContext('2d');
    const videoContainer = document.querySelector('.video-container');

    // State
    let currentTemplate = null;
    let cameraActive = false;
    let capturedImages = Array(4).fill(null);
    let currentPose = 1;

    // Initialize
    resultCanvas.width = 1800;
    resultCanvas.height = 1200;

    // Template Selection
    document.querySelectorAll('.template-option').forEach(option => {
        option.addEventListener('click', function() {
            document.querySelectorAll('.template-option').forEach(opt => {
                opt.classList.remove('selected');
            });
            this.classList.add('selected');
            currentTemplate = templates[this.dataset.layout];
            updateVideoContainerLayout();
        });
    });

    function updateVideoContainerLayout() {
        // Clear previous layout markers
        videoContainer.querySelectorAll('.layout-marker').forEach(marker => {
            marker.remove();
        });

        if (!currentTemplate) return;

        // Create new layout markers
        currentTemplate.areas.forEach((area, index) => {
            const marker = document.createElement('div');
            marker.className = 'layout-marker';
            marker.style.position = 'absolute';
            marker.style.border = '2px dashed rgba(255,255,255,0.7)';
            marker.style.boxSizing = 'border-box';
            marker.style.pointerEvents = 'none';
            
            // Scale the template area to fit the video container
            const scaleX = videoContainer.offsetWidth / 1800;
            const scaleY = videoContainer.offsetHeight / 1200;
            
            marker.style.left = `${area.x * scaleX}px`;
            marker.style.top = `${area.y * scaleY}px`;
            marker.style.width = `${area.width * scaleX}px`;
            marker.style.height = `${area.height * scaleY}px`;
            
            // Add pose number indicator
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
            videoContainer.appendChild(marker);
        });
    }

    // Handle window resize
    window.addEventListener('resize', updateVideoContainerLayout);

    confirmLayoutBtn.addEventListener('click', function() {
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
    });

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
        
        // Update layout markers when camera starts
        setTimeout(updateVideoContainerLayout, 100);
    }

    function stopCamera() {
        videoFeed.onerror = null;
        videoFeed.src = "";
        toggleCameraBtn.textContent = "Open Camera";
        cameraActive = false;
        fetch("/stop_camera");
    }

    // Capture Functionality
    captureBtn.addEventListener('click', capturePose);
    
    function capturePose() {
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
                const imageUrl = URL.createObjectURL(imageBlob);
                capturedImages[currentPose - 1] = imageUrl;
                
                if (currentPose < 4) {
                    currentPose++;
                    updatePoseCounter();
                } else {
                    renderTemplate();
                    showPreview();
                }
            })
            .catch(error => {
                console.error("Error capturing:", error);
                alert("Failed to capture photo. Please try again.");
            })
            .finally(() => {
                captureBtn.disabled = false;
                captureBtn.textContent = "Capture Pose";
            });
    }

    function updatePoseCounter() {
        poseNumber.textContent = currentPose;
        
        // Highlight the current pose in the layout markers
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

    // Initialize
    resultCanvas.width = 1800;
    resultCanvas.height = 1200;
    
    // Render all templates dynamically
    let carousel;
    let carouselItems = [];
    let currentIndex = 0;
    renderTemplates();
    
    function renderTemplates() {
        carousel = document.querySelector('.template-carousel');
        
        // Clear existing items
        carousel.innerHTML = '';
        carouselItems = [];
        
        // Create template options
        for (const [key, template] of Object.entries(templates)) {
            const templateOption = document.createElement('div');
            templateOption.className = 'template-option';
            templateOption.dataset.layout = key;
            
            const preview = document.createElement('div');
            preview.className = 'template-preview';
            
            const templateAreasContainer = document.createElement('div');
            templateAreasContainer.style.position = 'relative';
            templateAreasContainer.style.width = '100%';
            templateAreasContainer.style.height = '100%';
            
            // Calculate the original template dimensions
            const originalWidth = Math.max(...template.areas.map(area => area.x + area.width));
            const originalHeight = Math.max(...template.areas.map(area => area.y + area.height));
            
            // Calculate scale factors to fit the preview while maintaining aspect ratio
            const previewWidth = 300; // matches CSS width
            const previewHeight = 200; // matches CSS height
            const scaleX = previewWidth / originalWidth;
            const scaleY = previewHeight / originalHeight;
            const scale = Math.min(scaleX, scaleY);
            
            // Center the template in the preview
            const scaledWidth = originalWidth * scale;
            const scaledHeight = originalHeight * scale;
            const offsetX = (previewWidth - scaledWidth) / 2;
            const offsetY = (previewHeight - scaledHeight) / 2;
            
            // Create each area of the template
            template.areas.forEach((area, index) => {
                const areaDiv = document.createElement('div');
                areaDiv.className = 'template-area';
                areaDiv.style.left = `${offsetX + (area.x * scale)}px`;
                areaDiv.style.top = `${offsetY + (area.y * scale)}px`;
                areaDiv.style.width = `${area.width * scale}px`;
                areaDiv.style.height = `${area.height * scale}px`;
                areaDiv.style.backgroundColor = area.color;
                
                // Add number indicator
                const number = document.createElement('div');
                number.className = 'template-area-number';
                number.textContent = index + 1;
                areaDiv.appendChild(number);
                
                templateAreasContainer.appendChild(areaDiv);
            });
            
            preview.appendChild(templateAreasContainer);
            templateOption.appendChild(preview);
            
            const label = document.createElement('span');
            label.className = 'template-label';
            label.textContent = template.name;
            templateOption.appendChild(label);
            
            carousel.appendChild(templateOption);
            carouselItems.push(templateOption);
        }
        
        // Set up carousel navigation
        setupCarouselNavigation();
        
        // Select first template by default
        if (carouselItems.length > 0) {
            currentTemplate = templates[Object.keys(templates)[0]];
            carouselItems[0].classList.add('selected');
        }
    }

    function setupCarouselNavigation() {
        const prevBtn = document.querySelector('.carousel-button.prev');
        const nextBtn = document.querySelector('.carousel-button.next');
        
        prevBtn.addEventListener('click', () => {
            currentIndex = (currentIndex - 1 + carouselItems.length) % carouselItems.length;
            scrollToItem(currentIndex);
        });
        
        nextBtn.addEventListener('click', () => {
            currentIndex = (currentIndex + 1) % carouselItems.length;
            scrollToItem(currentIndex);
        });
        
        // Handle template selection
        carouselItems.forEach((item, index) => {
            item.addEventListener('click', () => {
                currentIndex = index;
                selectItem(index);
            });
        });
        
        // Handle keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (layoutSelection.classList.contains('section-active')) {
                if (e.key === 'ArrowLeft') {
                    currentIndex = (currentIndex - 1 + carouselItems.length) % carouselItems.length;
                    scrollToItem(currentIndex);
                } else if (e.key === 'ArrowRight') {
                    currentIndex = (currentIndex + 1) % carouselItems.length;
                    scrollToItem(currentIndex);
                }
            }
        });
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
        // Update selection
        carouselItems.forEach(item => item.classList.remove('selected'));
        carouselItems[index].classList.add('selected');
        
        // Update current template
        currentTemplate = templates[carouselItems[index].dataset.layout];
        currentIndex = index;
    }
    
    templateContainer.addEventListener('click', function(e) {
        const option = e.target.closest('.template-option');
        if (!option) return;
        
        const index = carouselItems.indexOf(option);
        if (index !== -1) {
            selectItem(index);
        }
    });

    // Render Template
    function renderTemplate() {
        // Draw colored background for each area first
        currentTemplate.areas.forEach(area => {
            ctx.fillStyle = area.color + '80'; // Add transparency
            ctx.fillRect(area.x, area.y, area.width, area.height);
        });
        
        // Then draw the images
        currentTemplate.areas.forEach((area, index) => {
            if (capturedImages[index]) {
                const img = new Image();
                img.onload = function() {
                    // Calculate scale to fill area (cover effect)
                    const scale = Math.max(
                        area.width / img.width,
                        area.height / img.height
                    );
        
                    const scaledWidth = img.width * scale;
                    const scaledHeight = img.height * scale;
        
                    // Center the image
                    const sx = (scaledWidth - area.width) / 2;
                    const sy = (scaledHeight - area.height) / 2;
        
                    // Create an offscreen canvas to crop and scale the image correctly
                    const offCanvas = document.createElement('canvas');
                    offCanvas.width = area.width;
                    offCanvas.height = area.height;
                    const offCtx = offCanvas.getContext('2d');
        
                    offCtx.drawImage(
                        img,
                        -sx,
                        -sy,
                        scaledWidth,
                        scaledHeight
                    );
        
                    // Draw the cropped result to the main canvas
                    ctx.drawImage(offCanvas, area.x, area.y);
        
                    // Optional border
                    ctx.strokeStyle = 'rgba(0,0,0,0.3)';
                    ctx.lineWidth = 4;
                    ctx.strokeRect(area.x, area.y, area.width, area.height);
                };
                img.src = capturedImages[index];
            }
        });
    }

    // Navigation
    function showPreview() {
        captureSection.classList.remove("section-active");
        captureSection.classList.add("section-inactive");
        previewSection.classList.remove("section-inactive");
        previewSection.classList.add("section-active");
    }

    startOverBtn.addEventListener('click', function() {
        if (confirm("Are you sure you want to start over?")) {
            // Clear images
            capturedImages.forEach(img => {
                if (img) URL.revokeObjectURL(img);
            });
            capturedImages = Array(4).fill(null);
            currentPose = 1;
            
            // Reset UI
            previewSection.classList.remove("section-active");
            previewSection.classList.add("section-inactive");
            layoutSelection.classList.remove("section-inactive");
            layoutSelection.classList.add("section-active");
            
            updatePoseCounter();
            stopCamera();
        }
    });

    // Save Functionality
    saveBtn.addEventListener('click', function() {
        const link = document.createElement('a');
        link.download = `casual-${currentTemplate.name.toLowerCase().replace(/ /g, '-')}-${new Date().getTime()}.png`;
        link.href = resultCanvas.toDataURL('image/png');
        link.click();
    });

    // Clean up
    window.addEventListener("beforeunload", function() {
        capturedImages.forEach(img => {
            if (img) URL.revokeObjectURL(img);
        });
        stopCamera();
    });
});