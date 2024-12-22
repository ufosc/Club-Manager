
document.addEventListener('DOMContentLoaded', () => {
    const editButton = document.querySelector('.edit-button');
    const profileItems = document.querySelectorAll('.profile-item');
    const profileContainer = document.querySelector('.profile-container');


    editButton.addEventListener('click', () => {
        if (editButton.innerText == 'Edit') {

            // allow edit mode css changes
            profileContainer.classList.add('edit-mode');

            profileItems.forEach(item => {
                const label = item.querySelector('.field-label').innerText;
                const value = item.querySelector('.field-value').innerText;

                const input = document.createElement('input');
                input.type = 'text';
                input.value = value;
                input.setAttribute('data-label', label.toLowerCase());
                item.replaceChild(input, item.querySelector('.field-value'));
            });

            editButton.innerText = 'Save';
        }
        else if (editButton.innerText == 'Save') {
            // remove edit mode class
            profileContainer.classList.remove('edit-mode');

            const updatedData = {};
            profileItems.forEach(item => {
                const input = item.querySelector('input');
                updatedData[input.getAttribute('data-label')] = input.value;

                const span = document.createElement('span');
                span.className = 'field-value';
                span.innerText = input.value;
                item.replaceChild(span, input);
            });

            console.log('Updated Data:', updatedData);

            alert('Profile updated successfully!');

            editButton.innerText = 'Edit';
        }
    });
});