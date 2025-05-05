/**
 * PayRing - Admin Panel JavaScript
 * Contains functionality specific to the admin dashboard
 */

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize all tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    
    // Initialize date pickers if any exist
    const datepickerElements = document.querySelectorAll('input[type="date"]');
    datepickerElements.forEach(element => {
        // Set default date to today if not already set
        if (!element.value) {
            const today = new Date();
            const yyyy = today.getFullYear();
            let mm = today.getMonth() + 1;
            let dd = today.getDate();
            
            if (dd < 10) dd = '0' + dd;
            if (mm < 10) mm = '0' + mm;
            
            const formattedDate = yyyy + '-' + mm + '-' + dd;
            element.value = formattedDate;
        }
    });
    
    // Table search functionality
    const tableSearchInputs = document.querySelectorAll('.table-search-input');
    
    tableSearchInputs.forEach(input => {
        input.addEventListener('keyup', function() {
            const searchTerm = this.value.toLowerCase();
            const targetTableId = this.dataset.tableTarget;
            const table = document.getElementById(targetTableId);
            
            if (table) {
                const tableRows = table.querySelectorAll('tbody tr');
                
                tableRows.forEach(row => {
                    const text = row.textContent.toLowerCase();
                    if (text.includes(searchTerm)) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                });
            }
        });
    });
    
    // Sidebar toggle for mobile
    const sidebarToggle = document.getElementById('sidebarToggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            document.body.classList.toggle('sidebar-collapsed');
        });
    }
    
    // Admin panel image upload preview
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    
    imageInputs.forEach(input => {
        input.addEventListener('change', function() {
            const previewElement = document.getElementById(this.dataset.preview);
            
            if (previewElement && this.files && this.files[0]) {
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    previewElement.src = e.target.result;
                };
                
                reader.readAsDataURL(this.files[0]);
            }
        });
    });
    
    // Confirm delete actions
    const confirmDeleteBtns = document.querySelectorAll('.confirm-delete');
    
    confirmDeleteBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });
    
    // Initialize any charts if Chart.js is available
    if (typeof Chart !== 'undefined') {
        // Order status chart (example)
        const orderStatusChartEl = document.getElementById('orderStatusChart');
        if (orderStatusChartEl) {
            new Chart(orderStatusChartEl.getContext('2d'), {
                type: 'doughnut',
                data: orderStatusChartEl.dataset.chartData ? JSON.parse(orderStatusChartEl.dataset.chartData) : {},
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        }
        
        // Sales chart (example)
        const salesChartEl = document.getElementById('salesChart');
        if (salesChartEl) {
            new Chart(salesChartEl.getContext('2d'), {
                type: 'line',
                data: salesChartEl.dataset.chartData ? JSON.parse(salesChartEl.dataset.chartData) : {},
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        }
    }
    
    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
    
    // Auto-dismiss alerts after 5 seconds
    const autoCloseAlerts = document.querySelectorAll('.alert-dismissible.auto-close');
    
    autoCloseAlerts.forEach(alert => {
        setTimeout(() => {
            const closeButton = alert.querySelector('.btn-close');
            if (closeButton) {
                closeButton.click();
            }
        }, 5000);
    });
});