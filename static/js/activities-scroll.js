// Activities Infinite Scroll Animation
document.addEventListener('DOMContentLoaded', function() {
    // Get the container element
    const container = document.getElementById('activitiesScrollContainer');
    if (!container) return;

    // Add click event to make activities interactive
    container.addEventListener('click', function(e) {
        const activityItem = e.target.closest('.activity-scroll-item');
        if (activityItem) {
            // Toggle a 'selected' class for visual feedback
            const allItems = document.querySelectorAll('.activity-scroll-item');
            allItems.forEach(item => {
                if (item !== activityItem) {
                    item.classList.remove('selected');
                }
            });
            activityItem.classList.toggle('selected');
            
            // Optional: Scroll to packages section when an activity is clicked
            // This creates a nice user flow from activities to booking
            const packagesSection = document.getElementById('packages');
            if (packagesSection) {
                setTimeout(() => {
                    packagesSection.scrollIntoView({ behavior: 'smooth' });
                }, 500);
            }
        }
    });

    // Adjust animation speed based on screen width for better mobile experience
    function adjustAnimationSpeed() {
        if (window.innerWidth < 768) {
            container.style.animationDuration = '20s'; // Faster on mobile
        } else {
            container.style.animationDuration = '30s'; // Normal speed on desktop
        }
    }

    // Call once on load
    adjustAnimationSpeed();
    
    // Update on window resize
    window.addEventListener('resize', adjustAnimationSpeed);
});
