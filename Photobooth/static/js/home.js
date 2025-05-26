document.addEventListener('DOMContentLoaded', function() {
    const carousel = document.querySelector('.carousel');
    const items = document.querySelectorAll('.carousel-item');
    const prevBtn = document.querySelector('.carousel-control.prev');
    const nextBtn = document.querySelector('.carousel-control.next');
    const indicatorsContainer = document.querySelector('.carousel-indicators');
    const start = document.querySelector('.start-section');
    const emailForm = document.querySelector('.email-form');
    const carouselProMax = document.querySelector('.carouselProMax');
    const ocean = document.querySelector('.ocean');
    const wave = document.querySelector('.wave');
    let currentIndex = 0;
    let rfidInterval;
    let rfidID; //dapat blanko ito kapag gagamitin
    let customerId;
    let cust;
    
    console.log("KioskBoard:", window.KioskBoard);
    
    KioskBoard.init({

        keysJsonUrl: '/static/kioskboard/kioskboard-keys-english.json', // Make sure this file exists
        language: 'en',
        theme: 'light',

        keysSpecialCharsArrayOfStrings: [
            "@", ".", "_", "-", "+", "!", "#", "$", "%", "&", "'", "*", "=", "^",
            "`", "{", "}", "|", "~", "(", ")", "[", "]", "\\", "/", ":", ";", "\""
        ],
        allowedSpecialCharacters: true,
        specialCharactersButtonText: "&?123",

        keysNumpadArrayOfNumbers: [1, 2, 3, 0, 4, 5, 6, 7, 8, 9],
        autoScroll: false,
        capsLockActive: false,
        allowRealKeyboard: true,
        allowMobileKeyboard: true,
        cssAnimations: true,
        cssAnimationsDuration: 360,
        cssAnimationsStyle: 'slide',
        keysAllowSpacebar: true,
        keysSpacebarText: 'Space',
        keysFontFamily: 'sans-serif',
        keysFontSize: '14px', // Slightly smaller font
        keysFontWeight: 'normal',
        keysIconSize: '18px',
        keysEnterText: 'Enter',
        keysEnterCanClose: true,
    });
    

    // Create indicators (remove if mas better)
    items.forEach((_, index) => {
        const indicator = document.createElement('div');
        indicator.classList.add('carousel-indicator');
        if (index === 0) indicator.classList.add('active');
        indicator.addEventListener('click', () => goToSlide(index));
        indicatorsContainer.appendChild(indicator);
    });
    
    const indicators = document.querySelectorAll('.carousel-indicator');
    
    function updateCarousel() {
        items.forEach((item, index) => {
            item.classList.toggle('active', index === currentIndex);
        });
        
        indicators.forEach((indicator, index) => {
            indicator.classList.toggle('active', index === currentIndex);
        });
    }
    
    function goToSlide(index) {
        currentIndex = index;
        updateCarousel();
    }
    
    function nextSlide() {
        currentIndex = (currentIndex + 1) % items.length;
        updateCarousel();
    }
    
    function prevSlide() {
        currentIndex = (currentIndex - 1 + items.length) % items.length;
        updateCarousel();
    }

    function displayEmail(){
        toggleSection(emailForm, true);
        toggleSection(start, false);
        KioskBoard.run('.js-kioskboard-input');
    }

    function displayCarousel(){
        /*toggleWaveOrOcean(ocean);*/
        toggleSection(emailForm, false);
        toggleSection(carouselProMax, true);
        document.getElementById("carouselProMax").scrollIntoView({behavior:'smooth' , block: 'center'});
    }

    
    //RFID utils. uncommetn to make it work

    function getRFIDKey(){
        fetch("/rfid_scan")
        .then(response => response.json())
        .then(data => {
            if (data.scanned_id) {
                console.log("RFID Key:", data.scanned_id);
                clearInterval(rfidInterval);
                verifyRFID(data.scanned_id)
            } else {
                console.log("No RFID key scanned yet.");
            }
        })
        .catch(error => {
            console.error("Error fetching RFID key:", error);
        });    
    }

    function verifyRFID(rfidKey){
        fetch('/allow_access', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({
                rfid_key: rfidKey
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.key_status === "YES") {
                console.log("Access granted!");
                localStorage.setItem('rfidKey', rfidID);
                rfidID = rfidKey



                get_customer_if(rfidID).then(cust_Id => {
                    if (cust_Id) {
                        customerId = cust_Id;
                        // Use customerId here
                        console.log("Customer ID:", customerId);
                    } else {
                        console.error("Customer ID fetch failed");
                    }
                });





                displayEmail(); 
            } else {
                console.log("Access denied.");
                rfidInterval = setInterval(getRFIDKey, 1000); //reinitilize para pwede ulit magscan

                cleanRFID();
            }
        })
        .catch(error => {
            console.error("Error checking RFID access:", error);
        });
    }

    function cleanRFID(){
        fetch("/clear_scan")
        .then(response => response.json())
         .then(data => {
            console.log("RFID cleared:", data);
        })
        .catch(error => {
            console.error("Error Clearing:", error);
        });    
    }

    function turnRFIDOn(){
        fetch("/turn_on_rfid")
        .then(response => response.json())
         .then(data => {
            console.log("RFID is now on:", data);
        })
        .catch(error => {
            console.error("Error turning on:", error);
        });    

    }

    function initialize() {
        //Page Initialization
        cleanRFID();
        emailForm.style.display = "none";
        carouselProMax.style.display = "none";
        start.classList.add("section-active");
        turnRFIDOn();
        rfidInterval = setInterval(getRFIDKey, 1000);
    }

    function toggleSection(section, show) {
        section.classList.toggle("section-inactive", !show);
        section.classList.toggle("section-active", show);
        if (show){
            setTimeout(() => {
                section.style.display = "block";
            }, 900);
        }
        if (!show){
            setTimeout(() => {
                section.style.display = "none";
            }, 900);
        }
    }

    /* function toggleWaveOrOcean(activeElement) {
        if (activeElement === wave) {
            wave.classList.add("wave-active");
            wave.classList.remove("wave-inactive");

            ocean.classList.add("ocean-inactive");
            ocean.classList.remove("ocean-active");
        } else if (activeElement === ocean) {
            ocean.classList.add("ocean-active");
            ocean.classList.remove("ocean-inactive");

            wave.classList.add("wave-inactive");
            wave.classList.remove("wave-active");
            setTimeout(() => {
                wave.style.display = "none";
            }, 0);
        }
    }*/
    
    // Event listeners
    nextBtn.addEventListener('click', nextSlide);
    prevBtn.addEventListener('click', prevSlide);


    function get_customer_if(rfid_key) {
        return fetch('/get_cust_id', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ rfidKey: rfid_key })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                console.log("Customer ID:", data.id);
                return data.id;
            } else {
                console.error("Error:", data.message || "Unknown error");
                return null;
            }
        })
        .catch(error => {
            console.error("Fetch error:", error);
            return null;
        });
    }

    
    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight') {
            nextSlide();
        } else if (e.key === 'ArrowLeft') {
            prevSlide();
        }
    });
    
    // setInterval(nextSlide, 5000);


    //HOLDS EMAIL VALUE
    document.querySelector('.email-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        const emailInput = document.getElementById('email');
        const email = emailInput.value.trim();
    
        if (!email) {
            alert('Please enter a valid email');
            return;
        }


        get_customer_if(rfidID).then(cust_Id => {
            if (cust_Id) {
                customerId = cust_Id;
                // Use customerId here
                console.log("Customer ID:", customerId);
            } else {
                console.error("Customer ID fetch failed");
            }
        });

        
        try {
            const response = await fetch('/start_session', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    email: email,
                    rfidKey: rfidID, 
                    cust_id: customerId})
            });
            const data = await response.json();
    
            if (data.session_id) {
                localStorage.setItem('session_id', data.session_id);
                localStorage.setItem('email', email);
                //check kung present yung 2 data
                console.log('Session started with ID:', data.session_id);
                console.log('Session started with email:', email);
                displayCarousel();
    
                // OPTIONAL: Redirect to mode selection if needed
                // window.location.href = "/mode";
            } else {
                alert('Failed to start session');
            }
        } catch (err) {
            console.error('Error starting session:', err);
            alert('Server error');
        }
    });
    initialize();
    console.log("nagana lods")

});