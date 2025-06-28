// Slideshow Background Script
document.addEventListener('DOMContentLoaded', function() {
    // Array of images for the slideshow
    const slideshowImages = [
        '/static/images/gallery/1.jpg',
        '/static/images/gallery/2.jpg',
        '/static/images/gallery/3.jpg',
        '/static/images/gallery/4.jpg',
        '/static/images/gallery/5.jpg',
        '/static/images/gallery/6.jpg'
    ];
    
    // Get the slideshow container
    const slideshowContainer = document.querySelector('.slideshow-background');
    
    // Create slides for each image
    slideshowImages.forEach((image, index) => {
        const slide = document.createElement('div');
        slide.classList.add('slide');
        slide.style.backgroundImage = `url('${image}')`;
        
        // Make the first slide active
        if (index === 0) {
            slide.classList.add('active');
        }
        
        slideshowContainer.appendChild(slide);
    });
    
    // Get all slides
    const slides = document.querySelectorAll('.slide');
    let currentSlide = 0;
    const slideCount = slides.length;
    
    // Function to change slides
    function nextSlide() {
        // Remove active class from current slide
        slides[currentSlide].classList.remove('active');
        
        // Move to next slide or back to first slide
        currentSlide = (currentSlide + 1) % slideCount;
        
        // Add active class to new current slide
        slides[currentSlide].classList.add('active');
    }
    
    // Change slide every 5 seconds
    setInterval(nextSlide, 5000);
}); 