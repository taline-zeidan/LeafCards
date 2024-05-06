document.getElementById('addCardBtn').addEventListener('click', function() {
    const container = document.getElementById('flashcardsContainer');
    const index = container.children.length;
    
    const flashcardHTML = `
        <div class="key-value-pair-remove-btn" id="flashcard-${index}">
            <label for="key-${index}" class="key-title" >Key:</label>
            <input type="text" id="key-${index}" name="key-${index}" class="key-box" placeholder="Enter key">
            <label for="value-${index}" class="value-title" >Value:</label>
            <input type="text" id="value-${index}" name="value-${index}" class="value-box" placeholder="Enter value">
            <button type="button" onclick="removeCard(${index})"  class="remove-btn" >Remove</button>
        </div>
    `;
    
    container.insertAdjacentHTML('beforeend', flashcardHTML);
});

function removeCard(index) {
    const card = document.getElementById(`flashcard-${index}`);
    card.parentNode.removeChild(card);
}
