// Enhanced JavaScript for Desert Safari Dubai Website

document.addEventListener('DOMContentLoaded', function() {
    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }
    
    // Initialize AOS animation library
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-in-out',
            once: true
        });
    }
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Parallax effect for hero section
    const hero = document.querySelector('.hero');
    if (hero) {
        window.addEventListener('scroll', function() {
            const scrollPosition = window.scrollY;
            hero.style.backgroundPositionY = scrollPosition * 0.5 + 'px';
        });
    }
    
    // Feature cards hover effect
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.classList.add('animated');
        });
        
        card.addEventListener('mouseleave', function() {
            this.classList.remove('animated');
        });
    });
    
    // Package cards image zoom effect
    const packageCards = document.querySelectorAll('.package-card');
    packageCards.forEach(card => {
        const img = card.querySelector('.package-img img');
        if (img) {
            card.addEventListener('mouseenter', function() {
                img.style.transform = 'scale(1.1)';
            });
            
            card.addEventListener('mouseleave', function() {
                img.style.transform = 'scale(1)';
            });
        }
    });
    
    // Testimonial carousel
    const testimonialCarousel = document.querySelector('#testimonialCarousel');
    if (testimonialCarousel && typeof bootstrap !== 'undefined') {
        new bootstrap.Carousel(testimonialCarousel, {
            interval: 5000,
            wrap: true
        });
    }
    
    // Counter animation for stats
    const counters = document.querySelectorAll('.counter');
    const speed = 200;
    
    counters.forEach(counter => {
        const updateCount = () => {
            const target = +counter.getAttribute('data-target');
            const count = +counter.innerText.replace(/,/g, '');
            const increment = target / speed;
            
            if (count < target) {
                counter.innerText = Math.ceil(count + increment).toLocaleString();
                setTimeout(updateCount, 1);
            } else {
                counter.innerText = target.toLocaleString();
            }
        };
        
        // Only start counting when element is in viewport
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    updateCount();
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        
        observer.observe(counter);
    });
    
    // Dashboard sidebar toggle
    const sidebarToggle = document.querySelector('#sidebarToggle');
    const dashboardSidebar = document.querySelector('.dashboard-sidebar');
    const dashboardMain = document.querySelector('.dashboard-main');
    
    if (sidebarToggle && dashboardSidebar && dashboardMain) {
        sidebarToggle.addEventListener('click', function() {
            dashboardSidebar.classList.toggle('show');
            
            if (window.innerWidth > 992) {
                if (dashboardSidebar.classList.contains('show')) {
                    dashboardMain.style.marginLeft = '280px';
                } else {
                    dashboardMain.style.marginLeft = '0';
                }
            }
        });
        
        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', function(e) {
            if (window.innerWidth <= 992 && 
                !dashboardSidebar.contains(e.target) && 
                !sidebarToggle.contains(e.target) && 
                dashboardSidebar.classList.contains('show')) {
                dashboardSidebar.classList.remove('show');
            }
        });
    }
    
    // Tooltip initialization
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    if (tooltipTriggerList.length && typeof bootstrap !== 'undefined') {
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Dashboard charts initialization
    initDashboardCharts();
});

// Dashboard charts
function initDashboardCharts() {
    // Check if Chart.js is available
    if (typeof Chart === 'undefined') return;
    
    // Booking trends chart
    const bookingTrendsChart = document.getElementById('bookingTrendsChart');
    if (bookingTrendsChart) {
        new Chart(bookingTrendsChart, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                datasets: [{
                    label: 'Bookings',
                    data: [65, 59, 80, 81, 56, 55, 40, 60, 75, 85, 90, 100],
                    fill: true,
                    backgroundColor: 'rgba(230, 126, 34, 0.1)',
                    borderColor: '#e67e22',
                    tension: 0.4,
                    pointBackgroundColor: '#e67e22',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        backgroundColor: '#2c3e50',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        borderColor: '#e67e22',
                        borderWidth: 1,
                        padding: 10,
                        displayColors: false
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        beginAtZero: true,
                        grid: {
                            borderDash: [2, 4],
                            color: '#e9ecef'
                        }
                    }
                }
            }
        });
    }
    
    // Revenue chart
    const revenueChart = document.getElementById('revenueChart');
    if (revenueChart) {
        new Chart(revenueChart, {
            type: 'bar',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                datasets: [{
                    label: 'Revenue',
                    data: [12500, 19000, 15000, 17000, 22000, 24000, 19000, 21000, 25000, 23000, 26000, 30000],
                    backgroundColor: '#e67e22',
                    borderRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        backgroundColor: '#2c3e50',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        callbacks: {
                            label: function(context) {
                                let label = context.dataset.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                if (context.parsed.y !== null) {
                                    label += new Intl.NumberFormat('en-US', {
                                        style: 'currency',
                                        currency: 'USD'
                                    }).format(context.parsed.y);
                                }
                                return label;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        beginAtZero: true,
                        grid: {
                            borderDash: [2, 4],
                            color: '#e9ecef'
                        },
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toLocaleString();
                            }
                        }
                    }
                }
            }
        });
    }
    
    // Booking status chart
    const bookingStatusChart = document.getElementById('bookingStatusChart');
    if (bookingStatusChart) {
        new Chart(bookingStatusChart, {
            type: 'doughnut',
            data: {
                labels: ['Pending', 'Confirmed', 'Paid', 'Completed', 'Cancelled'],
                datasets: [{
                    data: [15, 25, 20, 30, 10],
                    backgroundColor: ['#f39c12', '#3498db', '#27ae60', '#9b59b6', '#e74c3c'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            boxWidth: 12,
                            usePointStyle: true,
                            pointStyle: 'circle'
                        }
                    },
                    tooltip: {
                        backgroundColor: '#2c3e50',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        displayColors: false,
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.formattedValue;
                                const dataset = context.dataset;
                                const total = dataset.data.reduce((acc, data) => acc + data, 0);
                                const percentage = Math.round((context.raw / total) * 100);
                                return `${label}: ${value} (${percentage}%)`;
                            }
                        }
                    }
                },
                cutout: '70%'
            }
        });
    }
    
    // Package popularity chart
    const packagePopularityChart = document.getElementById('packagePopularityChart');
    if (packagePopularityChart) {
        new Chart(packagePopularityChart, {
            type: 'polarArea',
            data: {
                labels: ['Evening Safari', 'Morning Safari', 'Overnight Safari', 'Dune Buggy', 'Camel Trekking'],
                datasets: [{
                    data: [35, 20, 15, 18, 12],
                    backgroundColor: ['#e67e22', '#3498db', '#27ae60', '#9b59b6', '#f39c12'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            boxWidth: 12,
                            usePointStyle: true,
                            pointStyle: 'circle'
                        }
                    },
                    tooltip: {
                        backgroundColor: '#2c3e50',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        displayColors: false
                    }
                },
                scales: {
                    r: {
                        ticks: {
                            display: false
                        },
                        grid: {
                            color: '#e9ecef'
                        }
                    }
                }
            }
        });
    }
}

// Add animation classes to elements when they come into view
function animateOnScroll() {
    const elements = document.querySelectorAll('.animate-on-scroll');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const animation = entry.target.dataset.animation || 'fadeIn';
                entry.target.classList.add(animation);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
    
    elements.forEach(element => {
        observer.observe(element);
    });
}

// Call animation function
window.addEventListener('load', animateOnScroll);

// Image gallery lightbox
function initLightbox() {
    const galleryItems = document.querySelectorAll('.gallery-item');
    
    galleryItems.forEach(item => {
        item.addEventListener('click', function() {
            const imgSrc = this.querySelector('img').getAttribute('src');
            const lightbox = document.createElement('div');
            lightbox.className = 'lightbox';
            lightbox.innerHTML = `
                <div class="lightbox-content">
                    <span class="lightbox-close">&times;</span>
                    <img src="${imgSrc}" class="lightbox-img">
                </div>
            `;
            
            document.body.appendChild(lightbox);
            document.body.style.overflow = 'hidden';
            
            setTimeout(() => {
                lightbox.style.opacity = '1';
            }, 10);
            
            const close = lightbox.querySelector('.lightbox-close');
            close.addEventListener('click', function() {
                lightbox.style.opacity = '0';
                setTimeout(() => {
                    document.body.removeChild(lightbox);
                    document.body.style.overflow = '';
                }, 300);
            });
            
            lightbox.addEventListener('click', function(e) {
                if (e.target === lightbox) {
                    lightbox.style.opacity = '0';
                    setTimeout(() => {
                        document.body.removeChild(lightbox);
                        document.body.style.overflow = '';
                    }, 300);
                }
            });
        });
    });
}

// Call lightbox function if gallery exists
document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('.gallery-item')) {
        initLightbox();
    }
});
