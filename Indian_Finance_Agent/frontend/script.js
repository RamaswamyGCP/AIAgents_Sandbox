document.addEventListener('DOMContentLoaded', () => {
    const companyInput = document.getElementById('companyInput');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const resultArea = document.getElementById('resultArea');
    const markdownContent = document.getElementById('markdownContent');
    const copyBtn = document.getElementById('copyBtn');

    analyzeBtn.addEventListener('click', async () => {
        const company = companyInput.value.trim();
        if (!company) return;

        // UI State: Loading
        analyzeBtn.classList.add('loading');
        analyzeBtn.disabled = true;
        resultArea.classList.add('hidden');
        markdownContent.innerHTML = '';

        try {
            const response = await fetch('http://localhost:8000/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ company }),
            });

            if (!response.ok) {
                throw new Error(`Error: ${response.statusText}`);
            }

            const data = await response.json();
            
            // Render Markdown
            // Accessing the 'result' field from the API response
            // CrewAI result object might need to be converted to string or accessed properly
            let resultText = data.result;
            if (typeof resultText === 'object') {
                 // If it's a CrewOutput object, try to get the raw string or tasks_output
                 resultText = resultText.raw || resultText.result || JSON.stringify(resultText);
            }

            markdownContent.innerHTML = marked.parse(resultText);
            resultArea.classList.remove('hidden');

        } catch (error) {
            alert('Failed to fetch analysis: ' + error.message);
        } finally {
            // UI State: Reset
            analyzeBtn.classList.remove('loading');
            analyzeBtn.disabled = false;
        }
    });

    // Allow Enter key to submit
    companyInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            analyzeBtn.click();
        }
    });

    // Copy to clipboard
    copyBtn.addEventListener('click', () => {
        const text = markdownContent.innerText;
        navigator.clipboard.writeText(text).then(() => {
            const originalIcon = copyBtn.innerHTML;
            copyBtn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#4ade80" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>';
            setTimeout(() => {
                copyBtn.innerHTML = originalIcon;
            }, 2000);
        });
    });
});
