document.getElementById('predictionForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const variance = document.getElementById('variance').value;
    const skewness = document.getElementById('skewness').value;
    const curtosis = document.getElementById('curtosis').value;
    const entropy = document.getElementById('entropy').value;
    
    const form = document.getElementById('predictionForm');
    const result = document.getElementById('result');
    const loading = document.getElementById('loading');
    const resultContent = document.getElementById('resultContent');
    
    // Show loading state
    form.style.display = 'none';
    loading.classList.remove('hidden');
    
    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                variance: parseFloat(variance),
                skewness: parseFloat(skewness),
                curtosis: parseFloat(curtosis),
                entropy: parseFloat(entropy)
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            const isGenuine = data.result.includes('Genuine');
            const resultClass = isGenuine ? 'result-genuine' : 'result-forged';
            
            resultContent.innerHTML = `
                <div class="result-item">
                    <div class="result-label">Prediction Result</div>
                    <div class="result-value ${resultClass}">${data.result}</div>
                </div>
                <div class="result-item">
                    <div class="result-label">Confidence Level</div>
                    <div class="result-value">${data.confidence}%</div>
                </div>
                <div class="result-item">
                    <div class="result-label">Model Probability</div>
                    <div class="result-value">${data.probability}</div>
                </div>
                <hr style="margin: 15px 0; border: none; border-top: 1px solid #ddd;">
                <div style="font-size: 12px; color: #999;">
                    Input: Variance=${variance}, Skewness=${skewness}, 
                    Curtosis=${curtosis}, Entropy=${entropy}
                </div>
            `;
            
            result.classList.remove('hidden');
        } else {
            resultContent.innerHTML = `<p style="color: #e74c3c;">Error: ${data.error}</p>`;
            result.classList.remove('hidden');
        }
    } catch (error) {
        resultContent.innerHTML = `<p style="color: #e74c3c;">Error: ${error.message}</p>`;
        result.classList.remove('hidden');
    } finally {
        loading.classList.add('hidden');
    }
});

function resetForm() {
    document.getElementById('predictionForm').reset();
    document.getElementById('result').classList.add('hidden');
    document.getElementById('predictionForm').style.display = 'block';
    document.getElementById('variance').focus();
}
