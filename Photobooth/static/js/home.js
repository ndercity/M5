document.addEventListener('DOMContentLoaded', function() {
    const carousel = document.querySelector('.carousel');
    const items = document.querySelectorAll('.carousel-item');
    const prevBtn = document.querySelector('.carousel-control.prev');
    const nextBtn = document.querySelector('.carousel-control.next');
    const indicatorsContainer = document.querySelector('.carousel-indicators');
    const scan = document.querySelector('.scan');
    const emailForm = document.querySelector('.email-form');
    const carouselProMax = document.querySelector('.carouselProMax');
    let currentIndex = 0;

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
        toggleSection(scan,false);
        toggleSection(emailForm, true);
        document.getElementById("email-form").scrollIntoView({behavior:'smooth' , block: 'center'});
    }

    function displayCarousel(){
        toggleSection(emailForm, false);
        toggleSection(carouselProMax, true);
        document.getElementById("carouselProMax").scrollIntoView({behavior:'smooth' , block: 'center'});
    }

    function initialize() {
        //Page Initialization
    scan.classList.add("section-active");
    emailForm.classList.add("section-inactive");
    carouselProMax.classList.add("section-inactive");
    }

    function toggleSection(section, show) {
        section.classList.toggle("section-active", show);
        section.classList.toggle("section-inactive", !show);
    }
    
    // Event listeners
    nextBtn.addEventListener('click', nextSlide);
    prevBtn.addEventListener('click', prevSlide);
    scan.addEventListener('click', displayEmail)
    
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
    
        try {
            const response = await fetch('/start_session', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email })
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