document.addEventListener('DOMContentLoaded', function() {
    const passwordInput = document.getElementById('studentPassword');
    const confirmPasswordInput = document.getElementById('confirmPassword');
    const submitButton = document.querySelector('input[type="submit"]');
    const messageContainer = document.getElementById('doesPasswordMatch');
    const passwordLength = document.getElementById('correctPasswordLength');
    const charactors = document.getElementById('correctCharacters');

    // Function to check if passwords match
    function validatePasswords() {
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;

        if (password === confirmPassword && password !== '') {
            messageContainer.textContent = 'Passwords match!';
            messageContainer.style.color = 'green';
            submitButton.disabled = false;
        } else {
            messageContainer.textContent = 'Passwords do not match';
            messageContainer.style.color = 'red';
            submitButton.disabled = true;
            
            const isLengthValid = password.length >= 12;

            passwordLength.textContent = isLengthValid ? 'Password length is valid' : 'Password must be at least 12 characters';
            passwordLength.style.color = isLengthValid ? 'green' : 'red';

            const hasCapital = /[A-Z]/.test(password);
            const hasSpecialChar = /[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]/.test(password);

            const isCriteriaValid = hasCapital && hasSpecialChar;
            charactors.textContent = isCriteriaValid ? 'Password criteria are met' : 'Password must contain at least one capital letter and one special character';
            charactors.style.color = isCriteriaValid ? 'green' : 'red';

            submitButton.disabled = !(isLengthValid && isCriteriaValid);
        }
    }

    // Add event listeners to password and confirm password fields
    passwordInput.addEventListener('input', validatePasswords);
    confirmPasswordInput.addEventListener('input', validatePasswords);
});
