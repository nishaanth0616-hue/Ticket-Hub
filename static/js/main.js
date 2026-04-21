document.addEventListener('DOMContentLoaded', function() {
    // Interactive Seat Selection Logic
    const seatLayout = document.getElementById('dynamic-seat-layout');
    const selectedSeatsInput = document.getElementById('selected-seats');
    const totalAmountInput = document.getElementById('total-amount');
    const displaySelected = document.getElementById('display-selected');
    const displayTotal = document.getElementById('display-total');
    
    if (seatLayout) {
        const basePrice = parseFloat(seatLayout.dataset.price);
        let selectedSeats = [];

        seatLayout.addEventListener('click', function(e) {
            const seat = e.target.closest('.seat');
            if (!seat || seat.classList.contains('booked')) return;

            const seatId = seat.dataset.seatId;

            if (seat.classList.contains('selected')) {
                seat.classList.remove('selected');
                selectedSeats = selectedSeats.filter(id => id !== seatId);
            } else {
                seat.classList.add('selected');
                selectedSeats.push(seatId);
            }

            // Update UI & Hidden form inputs
            selectedSeatsInput.value = selectedSeats.join(', ');
            displaySelected.textContent = selectedSeats.length > 0 ? selectedSeats.join(', ') : 'None';
            
            const total = selectedSeats.length * basePrice;
            totalAmountInput.value = total;
            displayTotal.textContent = '₹' + total.toFixed(2);
            
            // Enable/disable proceed button
            const proceedBtn = document.getElementById('proceed-btn');
            if(proceedBtn) {
                proceedBtn.disabled = selectedSeats.length === 0;
            }
        });
    }

    // Payment Simulation Logic
    const paymentForm = document.getElementById('payment-form');
    if (paymentForm) {
        paymentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const btn = document.getElementById('pay-btn');
            const loader = document.getElementById('payment-loader-ui');
            
            // Show loader, hide button text
            btn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Verifying...';
            btn.disabled = true;
            if(loader) loader.classList.remove('d-none');
            
            // Simulate API call delay
            setTimeout(() => {
                this.submit();
            }, 2500);
        });
    }
});
