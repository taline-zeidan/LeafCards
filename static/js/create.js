document.getElementById('addCardBtn').addEventListener('click', function() {
    const container = document.getElementById('flashcardsContainer');
    const index = container.children.length;
    
    const flashcardHTML = `
        <div class="key-value-pair-remove-btn" id="flashcard-${index}">
            <label for="key-${index}" class="key-title">Key (Question):</label>
            <input type="text" id="key-${index}" name="questions[]" class="key-box" placeholder="Enter key (question)" required>
            <label for="value-${index}" class="value-title">Value (Answer):</label>
            <input type="text" id="value-${index}" name="answers[]" class="value-box" placeholder="Enter value (answer)" required>
            <button type="button" onclick="removeCard(${index})" class="remove-btn">Remove</button>
        </div>
    `;
    
    container.insertAdjacentHTML('beforeend', flashcardHTML);
});

function removeCard(index) {
    const card = document.getElementById(`flashcard-${index}`);
    card.parentNode.removeChild(card);
}
