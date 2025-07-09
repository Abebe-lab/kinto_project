// Initialize tooltips
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
})

// Contact form subject preset from URL
document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const subject = urlParams.get('subject');
    if (subject && document.getElementById('id_subject')) {
        document.getElementById('id_subject').value = subject;
    }
});

// Golden opportunities
document.addEventListener('DOMContentLoaded', function() {
    // Set the date we're counting down to (6 months from now)
    const countDownDate = new Date();
    countDownDate.setMonth(countDownDate.getMonth() + 6);

    // Update the countdown every 1 second
    const x = setInterval(function() {
        const now = new Date().getTime();
        const distance = countDownDate - now;

        // Time calculations
        const months = Math.floor(distance / (1000 * 60 * 60 * 24 * 30));
        const days = Math.floor((distance % (1000 * 60 * 60 * 24 * 30)) / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));

        // Display the result
        document.getElementById("countdown").innerHTML = `
            <div class="countdown-item">
                <div class="display-4">${months}</div>
                <div class="small">Months</div>
            </div>
            <div class="countdown-item">
                <div class="display-4">${days}</div>
                <div class="small">Days</div>
            </div>
            <div class="countdown-item">
                <div class="display-4">${hours}</div>
                <div class="small">Hours</div>
            </div>
        `;

        // If the countdown is finished
        if (distance < 0) {
            clearInterval(x);
            document.getElementById("countdown").innerHTML = "OFFER EXPIRED";
        }
    }, 1000);
});

// Highlight golden opportunity selection
document.addEventListener('DOMContentLoaded', function() {
    const subjectField = document.getElementById('contact-subject');

    // Check for golden opportunity in URL
    const urlParams = new URLSearchParams(window.location.search);
    if(urlParams.get('subject') === 'GOLDEN_OPPORTUNITY') {
        subjectField.value = 'GOLDEN_OPPORTUNITY';
        subjectField.classList.add('golden-opportunity-field');
    }

    // Visual feedback when golden opportunity is selected
    subjectField.addEventListener('change', function() {
        if(this.value === 'GOLDEN_OPPORTUNITY') {
            this.classList.add('golden-opportunity-field');
        } else {
            this.classList.remove('golden-opportunity-field');
        }
    });
});