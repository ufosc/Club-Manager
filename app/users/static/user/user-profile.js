document.addEventListener('DOMContentLoaded', () => {
    const editButton = document.querySelector('.edit-button');
    const profileItems = document.querySelectorAll('.profile-item');
    const profileContainer = document.querySelector('.profile-container');

    editButton.addEventListener('click', () => {
        if (editButton.innerText === 'Edit') {
            // Enter edit mode: Replace each span.field-value with an input.
            profileItems.forEach(item => {
                const span = item.querySelector('.field-value');
                if (span) {
                    const label = item.querySelector('.field-label').innerText;
                    const value = span.innerText;
                    const input = document.createElement('input');
                    
                    // If the label includes "birthday", use input type "date"
                    if (label.toLowerCase().includes('birthday')) {
                        input.type = 'date';
                        // Make sure the value is in YYYY-MM-DD format.
                        input.value = value;
                    } else {
                        input.type = 'text';
                        input.value = value;
                    }
                    // Store the label (or field key) for later use
                    input.setAttribute('data-label', label.toLowerCase());
                    
                    // Replace the span with the input
                    item.replaceChild(input, span);
                }
            });
            editButton.innerText = 'Save';
        } else if (editButton.innerText === 'Save') {
            // Save mode: Replace each input with a new span.
            const updatedData = {};
            profileItems.forEach(item => {
                const input = item.querySelector('input');
                if (input) {
                    const key = input.getAttribute('data-label') || input.id;
                    updatedData[key] = input.value;
                    
                    const span = document.createElement('span');
                    span.className = 'field-value';
                    span.innerText = input.value;
                    
                    // Replace the input with the new span
                    item.replaceChild(span, input);
                }
            });
            console.log('Updated Data:', updatedData);
            alert('Profile updated successfully!');
            editButton.innerText = 'Edit';
        }
    });
});
