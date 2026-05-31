// Auto-dismiss flash alerts after 4 seconds
document.addEventListener('DOMContentLoaded', function () {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 4000);
    });

    // Image fallback for broken images
    document.querySelectorAll('img').forEach(function(img) {
        img.addEventListener('error', function() {
            this.src = 'https://via.placeholder.com/300x200?text=🌿+Organic';
        });
    });
});
