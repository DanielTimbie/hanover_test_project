document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('searchForm');
    const queryInput = document.getElementById('queryInput');
    const searchButton = document.getElementById('searchButton');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const conversationHistory = document.getElementById('conversationHistory');
    const followupContainer = document.getElementById('followupContainer');
    const followupForm = document.getElementById('followupForm');
    const followupInput = document.getElementById('followupInput');
    const followupButton = document.getElementById('followupButton');
    const followupLoading = document.getElementById('followupLoading');

    // Function to display a conversation message
    function displayMessage(query, answer, sources, isFollowup = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'conversation-message';
        if (isFollowup) {
            messageDiv.className += ' followup-message';
        }
        
        messageDiv.innerHTML = `
            <div class="query-display">"${query}"</div>
            <div class="answer">${answer}</div>
            <div class="sources">
                <h3>Sources</h3>
                <div class="sources-list">
                    ${sources.map((source, index) => `
                        <div class="source-item">
                            <div class="source-title">${source.title}</div>
                            <div class="source-snippet">${source.snippet}</div>
                            <a href="${source.link}" target="_blank" class="source-link">${source.link}</a>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
        
        conversationHistory.appendChild(messageDiv);
        messageDiv.scrollIntoView({ behavior: 'smooth' });
    }

    // Function to perform initial search
    async function performSearch(query) {
        if (!query) return;
        
        // Show loading state
        searchButton.disabled = true;
        loading.style.display = 'block';
        results.style.display = 'none';
        
        try {
            const formData = new FormData();
            formData.append('query', query);
            
            const response = await fetch('/search', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            // Clear previous conversation
            conversationHistory.innerHTML = '';
            
            // Display results
            displayMessage(data.query, data.answer, data.sources);
            
            // Show follow-up form
            followupContainer.style.display = 'block';
            results.style.display = 'block';
        } catch (error) {
            console.error('Error:', error);
            results.innerHTML = '<div class="error">An error occurred while processing your request. Please try again.</div>';
            results.style.display = 'block';
        } finally {
            // Hide loading state
            searchButton.disabled = false;
            loading.style.display = 'none';
        }
    }

    // Function to perform follow-up search
    async function performFollowup(query) {
        if (!query) return;
        
        // Show loading state
        followupButton.disabled = true;
        followupLoading.style.display = 'block';
        
        try {
            const formData = new FormData();
            formData.append('query', query);
            
            const response = await fetch('/followup', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            // Display follow-up results
            displayMessage(data.query, data.answer, data.sources, true);
            
            // Clear follow-up input
            followupInput.value = '';
        } catch (error) {
            console.error('Error:', error);
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error';
            errorDiv.textContent = 'An error occurred while processing your follow-up question. Please try again.';
            conversationHistory.appendChild(errorDiv);
        } finally {
            // Hide loading state
            followupButton.disabled = false;
            followupLoading.style.display = 'none';
        }
    }

    // Handle main search form submission
    searchForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const query = queryInput.value.trim();
        await performSearch(query);
    });

    // Handle follow-up form submission
    followupForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const query = followupInput.value.trim();
        await performFollowup(query);
    });

    // Check for query parameter on page load
    const urlParams = new URLSearchParams(window.location.search);
    const queryParam = urlParams.get('query');
    if (queryParam) {
        queryInput.value = queryParam;
        performSearch(queryParam);
    }
}); 