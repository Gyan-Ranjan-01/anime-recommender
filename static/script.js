document.getElementById("animeInput").addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        getRecommendations();
    }
});

async function getRecommendations() {
    const inputElement = document.getElementById("animeInput");
    const originalInput = inputElement.value.trim();
    const resultsDiv = document.getElementById("results");

    if (!originalInput) return;

    resultsDiv.innerHTML = '<div class="status-message">Fetching recommendations...</div>';

    try {
        const response = await fetch(`/recommend/${encodeURIComponent(originalInput)}`);

        if (!response.ok) {
            throw new Error("Could not find recommendations for that anime.");
        }

        const data = await response.json();
        
        if (!data.recommendations || data.recommendations.length === 0) {
            resultsDiv.innerHTML = '<div class="status-message">No recommendations found. Try another title.</div>';
            return;
        }

        let html = '<div class="header-container">';

        if (originalInput.toLowerCase() !== data.query.toLowerCase()) {
            html += `<p class="did-you-mean">Did you mean: <span class="corrected-query">${data.query}</span> ?</p>`;
        }

        html += `<h2>If you liked <b>${data.query}</b>, then you may like these!</h2></div>`;

        data.recommendations.forEach(item => {
            const alternateTitle = item.other_name ? item.other_name : "No alternate title";
            html += `
                <div class="card">
                    <h3>${item.title}</h3>
                    <p>${alternateTitle}</p>
                </div>
            `;
        });

        resultsDiv.innerHTML = html;

    } catch (error) {
        resultsDiv.innerHTML = `<div class="error-message">${error.message}</div>`;
    }
}