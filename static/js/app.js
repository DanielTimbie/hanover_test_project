document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('searchForm');
    const queryInput = document.getElementById('queryInput');
    const searchButton = document.getElementById('searchButton');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const queryDisplay = document.getElementById('queryDisplay');
    const answer = document.getElementById('answer');
    const sourcesList = document.getElementById('sourcesList');

    // Function to perform search
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
            
            // Display results
            queryDisplay.textContent = `"${data.query}"`;
            answer.textContent = data.answer;
            
            // Display sources
            sourcesList.innerHTML = '';
            data.sources.forEach((source, index) => {
                const sourceDiv = document.createElement('div');
                sourceDiv.className = 'source-item';
                sourceDiv.innerHTML = `
                    <div class="source-title">${source.title}</div>
                    <div class="source-snippet">${source.snippet}</div>
                    <a href="${source.link}" target="_blank" class="source-link">${source.link}</a>
                `;
                sourcesList.appendChild(sourceDiv);
            });
            
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

    // Handle form submission
    searchForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const query = queryInput.value.trim();
        await performSearch(query);
    });

    // Check for query parameter on page load
    const urlParams = new URLSearchParams(window.location.search);
    const queryParam = urlParams.get('query');
    if (queryParam) {
        queryInput.value = queryParam;
        performSearch(queryParam);
    }
}); 