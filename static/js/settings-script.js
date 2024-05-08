document.getElementById('changePasswordBtn').addEventListener('click', function() {
    toggleVisibility('passwordChangeContainer');
});

document.getElementById('oldPassword').addEventListener('input', function() {
    const newPasswordInput = document.getElementById('newPassword');
    // Enable new password field only if there is some text in the old password field
    newPasswordInput.disabled = !this.value;
});

function toggleVisibility(id) {
    const container = document.getElementById(id);
    container.style.display = container.style.display === 'none' ? 'block' : 'none';
}
