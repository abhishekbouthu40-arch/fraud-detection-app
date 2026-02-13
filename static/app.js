document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('fraudForm');
    const submitBtn = document.getElementById('submitBtn');
    const resultDiv = document.getElementById('result');
    const resultCard = document.getElementById('resultCard');
    const resultIcon = document.getElementById('resultIcon');
    const resultLabel = document.getElementById('resultLabel');
    const confidenceEl = document.getElementById('confidence');
    const errorDiv = document.getElementById('error');
    const errorMessage = document.getElementById('errorMessage');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Hide previous result and error
        resultDiv.classList.add('hidden');
        errorDiv.classList.add('hidden');
        
        const payload = {
            amount: parseFloat(document.getElementById('amount').value),
            type: document.getElementById('type').value,
            old_balance: parseFloat(document.getElementById('old_balance').value),
            new_balance: parseFloat(document.getElementById('new_balance').value),
            step: parseInt(document.getElementById('step').value, 10)
        };

        submitBtn.disabled = true;
        submitBtn.textContent = 'Checking...';

        try {
            const baseUrl = window.location.origin;
            const res = await fetch(`${baseUrl}/api/predict`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await res.json();

            if (!res.ok) {
                throw new Error(data.detail || 'Prediction failed');
            }

            resultCard.classList.remove('safe', 'fraud');
            resultCard.classList.add(data.is_fraud ? 'fraud' : 'safe');
            
            resultIcon.textContent = data.is_fraud ? '⚠' : '✓';
            resultLabel.textContent = data.prediction;
            confidenceEl.textContent = `Confidence: ${(data.confidence * 100).toFixed(1)}%`;
            
            resultDiv.classList.remove('hidden');
        } catch (err) {
            errorMessage.textContent = err.message || 'An error occurred';
            errorDiv.classList.remove('hidden');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Check for Fraud';
        }
    });
});
