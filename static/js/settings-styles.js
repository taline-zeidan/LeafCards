document.getElementById('changeUsernameBtn').addEventListener('click', function() {
    toggleVisibility('usernameChangeContainer');
});

document.getElementById('changePasswordBtn').addEventListener('click', function() {
    toggleVisibility('passwordChangeContainer');
});

document.getElementById('changeEmailBtn').addEventListener('click', function() {
    toggleVisibility('emailChangeContainer');
});

document.getElementById('logOutBtn').addEventListener('click', function() {
    logOut();
});

document.getElementById('deleteAccountBtn').addEventListener('click', function() {
    deleteAccount();
});

function toggleVisibility(id) {
    const container = document.getElementById(id);
    container.style.display = container.style.display === 'none' ? 'block' : 'none';
    ensureSubmitButton(id);
}

function logOut() {
    alert('Log out functionality not implemented yet');
}

function deleteAccount() {
    alert('Delete account functionality not implemented yet');
}

function ensureSubmitButton(containerId) {
    const container = document.getElementById(containerId);
    if (container.getElementsByClassName('submit-btn').length === 0) {  // Check if the submit button already exists
        const button = document.createElement('button');
        button.type = 'submit';
        button.textContent = 'Submit';
        button.className = 'submit-btn';
        container.appendChild(button);
    }
}
