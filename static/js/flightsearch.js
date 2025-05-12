
//Flight Search Page JS

// Initialize flight search page elements
function initFlightSearch() {
    setupDatePicker();
    setupDestinationFiltering();
}

// Set up date picker with minimum date constraints
function setupDatePicker() {
    const departureDateInput = document.getElementById('departure_date');
    if (!departureDateInput) return;
    
    // Set minimum date to today
    const today = new Date().toISOString().split('T')[0];
    departureDateInput.min = today;
    
    // Default to today if no date is selected
    if (!departureDateInput.value) {
        departureDateInput.value = today;
    }
}

// Set up event listeners for origin/destination selects
function setupDestinationFiltering() {
    const originSelect = document.getElementById('origin');
    if (!originSelect) return;
    
    // Add change event listener
    originSelect.addEventListener('change', updateDestinationOptions);
    
    // Initialize on page load
    updateDestinationOptions();
}

/**
 * Update destination options based on selected origin
 * Rules:
 * 1. Can't select same airport for origin and destination
 * 2. If origin is not Dairy Flat, destination must be Dairy Flat
 */
function updateDestinationOptions() {
    const originValue = document.getElementById('origin').value;
    const destinationSelect = document.getElementById('destination');
    
    if (!destinationSelect) return;
    
    // First, enable all options
    for (let i = 0; i < destinationSelect.options.length; i++) {
        destinationSelect.options[i].disabled = false;
    }
    
    // Rule 1: Can't select same origin/destination
    for (let i = 0; i < destinationSelect.options.length; i++) {
        if (destinationSelect.options[i].value === originValue) {
            destinationSelect.options[i].disabled = true;
        }
    }
    
    // Rule 2: If origin is not Dairy Flat (NZNE), then destination must be Dairy Flat
    if (originValue !== 'NZNE') {
        for (let i = 0; i < destinationSelect.options.length; i++) {
            // Disable all options except Dairy Flat
            if (destinationSelect.options[i].value !== 'NZNE' && destinationSelect.options[i].value !== '') {
                destinationSelect.options[i].disabled = true;
            }
        }
        
        // If current selection is now disabled, set to Dairy Flat
        if (destinationSelect.value !== 'NZNE' && destinationSelect.value !== '') {
            destinationSelect.value = 'NZNE';
        }
    }
    
    // If current selection is disabled for any reason, reset it
    const selectedOption = destinationSelect.options[destinationSelect.selectedIndex];
    if (selectedOption && selectedOption.disabled) {
        destinationSelect.value = '';
    }
}

function showAllFlights() {
    // Get the search form
    const searchForm = document.getElementById('flight-search-form');
    
    if (!searchForm) return;
    
    // Reset all form elements to default values
    // Origin - set to Dairy Flat (NZNE)
    const originSelect = document.getElementById('origin');
    if (originSelect) {
        originSelect.value = 'NZNE';
    }
    
    // Destination - clear selection
    const destinationSelect = document.getElementById('destination');
    if (destinationSelect) {
        destinationSelect.value = '';
        
        // Enable all destination options
        for (let i = 0; i < destinationSelect.options.length; i++) {
            destinationSelect.options[i].disabled = false;
            
            // Disable only the NZNE option (same as origin)
            if (destinationSelect.options[i].value === 'NZNE') {
                destinationSelect.options[i].disabled = true;
            }
        }
    }
    
    // Set departure date to null or today
    const departureDateInput = document.getElementById('departure_date');
    if (departureDateInput) {
        const today = new Date().toISOString().split('T')[0];
        departureDateInput.value = today;
    }
    
    // Set passengers to 1 (or leave as is)
    const passengersSelect = document.getElementById('passengers');
    if (passengersSelect) {
        passengersSelect.value = '1';
    }
    
    // Submit the form to show all flights
    searchForm.submit();
}
// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initFlightSearch);