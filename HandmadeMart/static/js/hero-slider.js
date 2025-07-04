document.addEventListener('DOMContentLoaded', function() {
    // Initialize variables
    const slides = document.querySelectorAll('.slide');
    const dots = document.querySelectorAll('.slider-dot');
    const prevArrow = document.querySelector('.slider-arrow.prev');
    const nextArrow = document.querySelector('.slider-arrow.next');
    let currentSlide = 0;
    let slideInterval;
    const slideDuration = 6000; // 6 seconds

    // Function to show a specific slide
    function showSlide(index) {
        // Hide all slides
        slides.forEach(slide => slide.classList.remove('active'));
        dots.forEach(dot => dot.classList.remove('active'));
        
        // Show the current slide
        slides[index].classList.add('active');
        dots[index].classList.add('active');
        currentSlide = index;
    }

    // Function to go to the next slide
    function nextSlide() {
        const nextIndex = (currentSlide + 1) % slides.length;
        showSlide(nextIndex);
    }

    // Function to go to the previous slide
    function prevSlide() {
        const prevIndex = (currentSlide - 1 + slides.length) % slides.length;
        showSlide(prevIndex);
    }

    // Start the slideshow
    function startSlideShow() {
        slideInterval = setInterval(nextSlide, slideDuration);
    }

    // Pause the slideshow when hovering over the slider
    function pauseSlideShow() {
        clearInterval(slideInterval);
    }

    // Resume the slideshow when mouse leaves the slider
    function resumeSlideShow() {
        startSlideShow();
    }

    // Add event listeners
    prevArrow.addEventListener('click', function() {
        pauseSlideShow();
        prevSlide();
        resumeSlideShow();
    });

    nextArrow.addEventListener('click', function() {
        pauseSlideShow();
        nextSlide();
        resumeSlideShow();
    });

    // Add click event to dots
    dots.forEach((dot, index) => {
        dot.addEventListener('click', function() {
            pauseSlideShow();
            showSlide(index);
            resumeSlideShow();
        });
    });

    // Pause on hover
    const slider = document.querySelector('.hero-slider');
    slider.addEventListener('mouseenter', pauseSlideShow);
    slider.addEventListener('mouseleave', resumeSlideShow);

    // Touch events for mobile
    let touchStartX = 0;
    let touchEndX = 0;

    slider.addEventListener('touchstart', function(e) {
        touchStartX = e.changedTouches[0].screenX;
        pauseSlideShow();
    }, false);

    slider.addEventListener('touchend', function(e) {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
        resumeSlideShow();
    }, false);

    function handleSwipe() {
        const swipeThreshold = 50; // Minimum swipe distance in pixels
        const swipeDiff = touchStartX - touchEndX;

        if (Math.abs(swipeDiff) > swipeThreshold) {
            if (swipeDiff > 0) {
                // Swipe left - next slide
                nextSlide();
            } else {
                // Swipe right - previous slide
                prevSlide();
            }
        }
    }

    // Start the slideshow
    startSlideShow();

    // Show the first slide initially
    showSlide(0);
});
