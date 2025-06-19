import discoverTopics from './topics.js';

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
    const suggestedTopics = document.getElementById('suggestedTopics');
    const topicButtons = document.querySelectorAll('.topic-button');
    const shuffleButton = document.getElementById('shuffleButton');

    // All available categories
    const allCategories = [
        { name: 'Technology', topics: discoverTopics.slice(0, 10) },
        { name: 'Science', topics: discoverTopics.slice(10, 20) },
        { name: 'Health', topics: discoverTopics.slice(20, 30) },
        { name: 'Culture', topics: discoverTopics.slice(30, 40) },
        { name: 'Emerging', topics: discoverTopics.slice(40, 50) }
    ];

    // Randomly select 3 categories
    const selectedCategories = [...allCategories]
        .sort(() => Math.random() - 0.5)
        .slice(0, 3);

    // Create category buttons dynamically
    const topicRow = document.querySelector('.topic-row');
    topicRow.innerHTML = selectedCategories
        .map(category => `
            <button class="topic-button" data-category="${category.name.toLowerCase()}">
                ${category.name}
            </button>
        `).join('');

    // Update topic categories object
    const topicCategories = {};
    selectedCategories.forEach(category => {
        topicCategories[category.name.toLowerCase()] = category.topics;
    });

    let currentCategory = null;

    // Function to get 5 random items from an array
    function getRandomItems(array, count) {
        const shuffled = [...array].sort(() => Math.random() - 0.5);
        return shuffled.slice(0, count);
    }

    // Function to display topics for a category
    function displayTopics(category) {
        if (currentCategory === category) {
            suggestedTopics.innerHTML = '';
            suggestedTopics.classList.remove('visible');
            currentCategory = null;
            document.querySelectorAll('.topic-button').forEach(btn => btn.classList.remove('active'));
            return;
        }

        currentCategory = category;
        const allTopics = topicCategories[category];
        const selectedTopics = getRandomItems(allTopics, 5);
        
        suggestedTopics.innerHTML = selectedTopics
            .map(topic => `
                <button class="suggested-topic" data-topic="${topic}">
                    ${topic}
                </button>
            `).join('');

        // Show the suggestions with animation
        setTimeout(() => {
            suggestedTopics.classList.add('visible');
        }, 50);

        // Update active state of category buttons
        document.querySelectorAll('.topic-button').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.category === category);
        });
    }

    // Function to hide topic suggestions
    function hideTopicSuggestions() {
        const topicSuggestions = document.querySelector('.topic-suggestions');
        topicSuggestions.classList.add('hidden');
        suggestedTopics.classList.remove('visible');
        currentCategory = null;
        document.querySelectorAll('.topic-button').forEach(btn => btn.classList.remove('active'));
    }

    // Function to show topic suggestions
    function showTopicSuggestions() {
        const topicSuggestions = document.querySelector('.topic-suggestions');
        topicSuggestions.classList.remove('hidden');
    }

    // Handle category button clicks
    topicRow.addEventListener('click', (e) => {
        const button = e.target.closest('.topic-button');
        if (button) {
            const category = button.dataset.category;
            displayTopics(category);
        }
    });

    // Handle topic selection
    suggestedTopics.addEventListener('click', (e) => {
        const topicButton = e.target.closest('.suggested-topic');
        if (topicButton) {
            const topic = topicButton.dataset.topic;
            queryInput.value = topic;
            queryInput.focus();
        }
    });

    // Handle shuffle button
    shuffleButton.addEventListener('click', () => {
        if (currentCategory) {
            const topics = topicCategories[currentCategory];
            const randomTopic = topics[Math.floor(Math.random() * topics.length)];
            queryInput.value = randomTopic;
            queryInput.focus();
        }
    });

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
        
        // Hide topic suggestions before search
        hideTopicSuggestions();
        
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
            
            // Show topic suggestions again in case of error
            showTopicSuggestions();
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