import discoverTopics from './topics.js';

document.addEventListener('DOMContentLoaded', () => {
    const topicsGrid = document.getElementById('topicsGrid');

    // Populate topics
    discoverTopics.forEach(topic => {
        const topicCard = document.createElement('div');
        topicCard.className = 'topic-card';
        topicCard.innerHTML = `<h3>${topic}</h3>`;
        
        // Add click handler
        topicCard.addEventListener('click', () => {
            // Redirect to search with the topic
            window.location.href = `/?query=${encodeURIComponent(topic)}`;
        });

        topicsGrid.appendChild(topicCard);
    });
}); 