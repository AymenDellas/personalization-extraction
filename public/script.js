async function scrapeProfile() {
    const urlInput = document.getElementById('urlInput');
    const url = urlInput.value.trim();

    if (!url) {
        showError("Please enter a LinkedIn URL");
        return;
    }

    // Reset UI
    showError(null); // Hide error
    document.getElementById('resultsArea').classList.add('hidden');

    // Show Loading
    const btn = document.getElementById('scrapeBtn');
    const btnText = document.getElementById('btnText');
    const btnLoader = document.getElementById('btnLoader');

    btn.disabled = true;
    btnText.textContent = "Scraping...";
    btnLoader.classList.remove('hidden');

    try {
        console.log("Sending request to server for:", url);

        const response = await fetch('/api/scrape', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: url })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Failed to scrape profile");
        }

        displayResults(data);

    } catch (error) {
        console.error("Scrape error:", error);
        showError(error.message);
    } finally {
        // Reset Button
        btn.disabled = false;
        btnText.textContent = "Scrape Profile";
        btnLoader.classList.add('hidden');
    }
}

function displayResults(data) {
    const resultsArea = document.getElementById('resultsArea');

    // Set JSON
    document.getElementById('jsonOutput').textContent = JSON.stringify(data, null, 2);

    resultsArea.classList.remove('hidden');

    if (data.website_url) {
        document.getElementById('websiteInput').value = data.website_url;
    }
}

async function scrapeWebsite() {
    const urlInput = document.getElementById('websiteInput');
    const url = urlInput.value.trim();

    if (!url) {
        showError("Please enter a Website URL");
        return;
    }

    // UI State
    const btn = document.getElementById('websiteBtn');
    const btnText = document.getElementById('webBtnText');
    const btnLoader = document.getElementById('webBtnLoader');

    btn.disabled = true;
    btnText.textContent = "Analyzing...";
    btnLoader.classList.remove('hidden');
    document.getElementById('webResults').classList.add('hidden');

    try {
        const response = await fetch('/api/scrape-website', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: url })
        });

        const data = await response.json();

        if (!response.ok) throw new Error(data.error || "Failed to scrape website");

        // Show Results
        document.getElementById('directGoalVal').textContent = data.direct_goal || "Unknown";
        document.getElementById('primaryCtaVal').textContent = data.primary_cta_text || "None found";
        document.getElementById('ctaDestVal').textContent = data.cta_destination ? `➞ ${data.cta_destination}` : "";

        // Show all CTAs found
        const allCtas = data.all_ctas_found || [];
        document.getElementById('allCtasVal').textContent = allCtas.length > 0 ? allCtas.join(', ') : "None else detected";

        document.getElementById('roadblockVal').textContent = data.roadblock || "None detected";
        document.getElementById('audienceVal').textContent = data.audience || "Not specified";

        document.getElementById('webJsonOutput').textContent = JSON.stringify(data, null, 2);
        document.getElementById('webResults').classList.remove('hidden');

    } catch (error) {
        showError(error.message);
    } finally {
        btn.disabled = false;
        btnText.textContent = "Analyze Site";
        btnLoader.classList.add('hidden');
    }
}

function showError(msg) {
    const errorArea = document.getElementById('errorArea');
    const msgEl = document.getElementById('errorMessage');

    if (msg) {
        msgEl.textContent = msg;
        errorArea.classList.remove('hidden');
    } else {
        errorArea.classList.add('hidden');
    }
}

function toggleJson() {
    const pre = document.getElementById('jsonOutput');
    pre.classList.toggle('hidden');
}

function toggleWebJson() {
    const pre = document.getElementById('webJsonOutput');
    pre.classList.toggle('hidden');
}

// Allow Enter key to submit
document.getElementById('urlInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        scrapeProfile();
    }
});

document.getElementById('websiteInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        scrapeWebsite();
    }
});
