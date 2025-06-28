/**
 * Dashboard JavaScript for enhanced mobile responsiveness
 * Safari Desert Tours
 */

document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const sidebarToggle = document.getElementById('sidebarToggle');
    const dashboardSidebar = document.getElementById('dashboardSidebar');
    const dashboardWrapper = document.getElementById('dashboardWrapper');
    
    // Mobile detection
    const isMobile = window.innerWidth < 992;
    
    // Initialize sidebar state based on device
    function initSidebar() {
        if (isMobile) {
            // On mobile, sidebar is hidden by default
            dashboardWrapper.classList.add('sidebar-collapsed');
            dashboardSidebar.classList.remove('show');
        } else {
            // On desktop, check saved preference
            const sidebarCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
            if (sidebarCollapsed) {
                dashboardWrapper.classList.add('sidebar-collapsed');
            } else {
                dashboardWrapper.classList.remove('sidebar-collapsed');
            }
        }
    }
    
    // Toggle sidebar visibility
    function toggleSidebar() {
        if (isMobile) {
            dashboardSidebar.classList.toggle('show');
        } else {
            dashboardWrapper.classList.toggle('sidebar-collapsed');
            // Save state to localStorage
            localStorage.setItem('sidebarCollapsed', dashboardWrapper.classList.contains('sidebar-collapsed'));
        }
    }
    
    // Close sidebar when clicking outside on mobile
    function setupClickOutside() {
        if (isMobile) {
            document.addEventListener('click', function(event) {
                const isClickInside = dashboardSidebar.contains(event.target) || 
                                     sidebarToggle.contains(event.target);
                
                if (!isClickInside && dashboardSidebar.classList.contains('show')) {
                    dashboardSidebar.classList.remove('show');
                }
            });
        }
    }
    
    // Close sidebar when clicking on a nav link on mobile
    function setupNavLinkClose() {
        const navLinks = dashboardSidebar.querySelectorAll('.nav-link');
        
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                if (isMobile && dashboardSidebar.classList.contains('show')) {
                    dashboardSidebar.classList.remove('show');
                }
            });
        });
    }
    
    // Handle window resize
    function handleResize() {
        window.addEventListener('resize', function() {
            const wasMobile = isMobile;
            const newIsMobile = window.innerWidth < 992;
            
            // Only take action if device type changed
            if (wasMobile !== newIsMobile) {
                location.reload(); // Refresh to apply correct layout
            }
        });
    }
    
    // Add touch swipe support for mobile
    function setupTouchSwipe() {
        let touchStartX = 0;
        let touchEndX = 0;
        
        document.addEventListener('touchstart', function(e) {
            touchStartX = e.changedTouches[0].screenX;
        }, false);
        
        document.addEventListener('touchend', function(e) {
            touchEndX = e.changedTouches[0].screenX;
            handleSwipe();
        }, false);
        
        function handleSwipe() {
            const swipeDistance = touchEndX - touchStartX;
            
            // Right swipe (open sidebar)
            if (swipeDistance > 100 && !dashboardSidebar.classList.contains('show')) {
                dashboardSidebar.classList.add('show');
            }
            
            // Left swipe (close sidebar)
            if (swipeDistance < -100 && dashboardSidebar.classList.contains('show')) {
                dashboardSidebar.classList.remove('show');
            }
        }
    }
    
    // Make tables responsive
    function enhanceTableResponsiveness() {
        const tables = document.querySelectorAll('.table-dashboard, .booking-table');
        
        tables.forEach(table => {
            // Add responsive wrapper if not already present
            if (!table.parentElement.classList.contains('table-responsive')) {
                const wrapper = document.createElement('div');
                wrapper.className = 'table-responsive';
                table.parentNode.insertBefore(wrapper, table);
                wrapper.appendChild(table);
            }
            
            // Add data-title attributes for mobile view
            const headers = Array.from(table.querySelectorAll('thead th')).map(th => th.textContent.trim());
            
            table.querySelectorAll('tbody tr').forEach(row => {
                Array.from(row.cells).forEach((cell, index) => {
                    if (headers[index]) {
                        cell.setAttribute('data-title', headers[index]);
                    }
                });
            });
            
            // Add mobile-friendly classes
            if (window.innerWidth < 576) {
                // Mark less important columns to hide on mobile
                const lessImportantIndexes = [2, 4]; // Example: columns to hide (adjust as needed)
                
                lessImportantIndexes.forEach(index => {
                    if (table.rows[0] && table.rows[0].cells[index]) {
                        Array.from(table.querySelectorAll(`tr > *:nth-child(${index + 1})`)).forEach(cell => {
                            cell.classList.add('hide-on-mobile');
                        });
                    }
                });
            }
        });
    }
    
    // Initialize all functions
    if (sidebarToggle && dashboardSidebar) {
        // Set up sidebar toggle
        sidebarToggle.addEventListener('click', toggleSidebar);
        
        // Initialize sidebar
        initSidebar();
        
        // Setup mobile-specific behaviors
        setupClickOutside();
        setupNavLinkClose();
        setupTouchSwipe();
        
        // Handle window resize
        handleResize();
        
        // Enhance tables
        enhanceTableResponsiveness();
    }
    
    // Initialize any charts with responsive options
    function initResponsiveCharts() {
        // Check if Chart is available
        if (typeof Chart !== 'undefined') {
            Chart.defaults.responsive = true;
            Chart.defaults.maintainAspectRatio = false;
            
            // Add custom responsive behavior to existing charts
            const chartElements = document.querySelectorAll('canvas[id]');
            chartElements.forEach(canvas => {
                const chart = Chart.getChart(canvas);
                if (chart) {
                    // Adjust font sizes for mobile
                    if (window.innerWidth < 576) {
                        chart.options.plugins.legend.labels.font = { size: 10 };
                        chart.options.scales.x.ticks.font = { size: 9 };
                        chart.options.scales.y.ticks.font = { size: 9 };
                        chart.update();
                    }
                }
            });
        }
    }
    
    // Initialize responsive charts after a short delay to ensure they're created
    setTimeout(initResponsiveCharts, 500);
}); 