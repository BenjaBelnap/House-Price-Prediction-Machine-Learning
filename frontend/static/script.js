// Configuration
const API_BASE_URL = 'http://localhost:8000';

// Global variables
let featuresData = null;
let currentPrediction = null;

// DOM elements
const loadingEl = document.getElementById('loading');
const mainContentEl = document.getElementById('mainContent');
const formEl = document.getElementById('predictionForm');
const submitBtnEl = document.getElementById('submitBtn');
const resultContainerEl = document.getElementById('resultContainer');
const detailsModalEl = document.getElementById('detailsModal');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    loadFeatures();
});

// Load features from API
async function loadFeatures() {
    try {
        const response = await fetch(`${API_BASE_URL}/features`);
        if (!response.ok) {
            throw new Error('Failed to load features');
        }
        
        featuresData = await response.json();
        renderForm();
        hideLoading();
    } catch (error) {
        console.error('Error loading features:', error);
        showError('Failed to load application. Please ensure the API server is running.');
    }
}

// Hide loading screen and show main content
function hideLoading() {
    loadingEl.style.display = 'none';
    mainContentEl.style.display = 'block';
}

// Show error message
function showError(message) {
    loadingEl.innerHTML = `
        <div style="color: white; text-align: center;">
            <h3>⚠️ Error</h3>
            <p>${message}</p>
            <button onclick="location.reload()" style="margin-top: 1rem; padding: 0.5rem 1rem; background: white; color: #333; border: none; border-radius: 4px; cursor: pointer;">
                Retry
            </button>
        </div>
    `;
}

// Render the form with features
function renderForm() {
    const essentialContainer = document.getElementById('essentialFeatures');
    const additionalContainer = document.getElementById('additionalFeatures');
    
    // Clear containers
    essentialContainer.innerHTML = '';
    additionalContainer.innerHTML = '';
    
    // Get top features (most important)
    const topFeatures = featuresData.top_features || [];
    const allFeatures = Object.keys(featuresData.feature_defaults);
    
    // Render essential features (top 15 most important)
    topFeatures.slice(0, 15).forEach(feature => {
        const formGroup = createFormGroup(feature, true);
        essentialContainer.appendChild(formGroup);
    });
    
    // Render additional features (remaining features, show more for completeness)
    const additionalFeatures = allFeatures
        .filter(feature => !topFeatures.slice(0, 15).includes(feature))
        // .filter(feature => !feature.includes('_')) // Commented out to show dummy variables too
        .slice(0, 200); // Show up to 100 additional features
    
    additionalFeatures.forEach(feature => {
        const formGroup = createFormGroup(feature, false);
        additionalContainer.appendChild(formGroup);
    });
}

// Create a form group for a feature
function createFormGroup(feature, isImportant = false) {
    const formGroup = document.createElement('div');
    formGroup.className = `form-group ${isImportant ? 'important' : ''}`;
    
    const defaultValue = featuresData.feature_defaults[feature];
    const isNumerical = typeof defaultValue === 'number';
    
    // Clean up feature name for display
    const displayName = formatFeatureName(feature);
    
    formGroup.innerHTML = `
        <label class="form-label" for="${feature}">
            ${displayName}
            ${isImportant ? '<span style="color: #ff6b6b;">*</span>' : ''}
        </label>
        <input 
            type="${isNumerical ? 'number' : 'text'}" 
            id="${feature}" 
            name="${feature}" 
            class="form-input"
            placeholder="${isImportant ? 'Required' : 'Optional (default: ' + defaultValue + ')'}"
            ${isNumerical ? 'step="any"' : ''}
        >
    `;
    
    return formGroup;
}

// Format feature name for display
function formatFeatureName(feature) {
    return feature
        .replace(/([A-Z])/g, ' $1') // Add space before capital letters
        .replace(/^./, str => str.toUpperCase()) // Capitalize first letter
        .replace(/\b\w/g, str => str.toUpperCase()) // Capitalize each word
        .replace(/sf/gi, 'SF') // Fix SF abbreviation
        .replace(/1st/g, '1st')
        .replace(/2nd/g, '2nd')
        .replace(/3rd/g, '3rd');
}

// Handle form submission
formEl.addEventListener('submit', async function(e) {
    e.preventDefault();
    await makePrediction();
});

// Make prediction
async function makePrediction() {
    const formData = new FormData(formEl);
    const features = {};
    
    // Collect form data
    for (let [key, value] of formData.entries()) {
        if (value.trim() !== '') {
            // Convert to number if it's a numerical feature
            const defaultValue = featuresData.feature_defaults[key];
            if (typeof defaultValue === 'number') {
                features[key] = parseFloat(value);
            } else {
                features[key] = value;
            }
        }
    }
    
    // Show loading state
    setLoadingState(true);
    
    try {
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ features })
        });
        
        if (!response.ok) {
            throw new Error('Prediction failed');
        }
        
        currentPrediction = await response.json();
        showResults();
        
    } catch (error) {
        console.error('Error making prediction:', error);
        alert('Failed to get prediction. Please try again.');
    } finally {
        setLoadingState(false);
    }
}

// Set loading state for submit button
function setLoadingState(isLoading) {
    const btnTexts = document.querySelectorAll('.btn-text');
    const btnSpinners = document.querySelectorAll('.btn-spinner');
    const submitBtns = document.querySelectorAll('[type="submit"]');
    
    if (isLoading) {
        btnTexts.forEach(text => text.style.display = 'none');
        btnSpinners.forEach(spinner => spinner.style.display = 'inline');
        submitBtns.forEach(btn => btn.disabled = true);
    } else {
        btnTexts.forEach(text => text.style.display = 'inline');
        btnSpinners.forEach(spinner => spinner.style.display = 'none');
        submitBtns.forEach(btn => btn.disabled = false);
    }
}

// Show results
function showResults() {
    // Hide form and show results
    document.querySelector('.form-container').style.display = 'none';
    resultContainerEl.style.display = 'block';
    
    // Update result display
    document.getElementById('predictedPrice').textContent = 
        Math.round(currentPrediction.predicted_price).toLocaleString();
    
    document.getElementById('modelUsed').textContent = 
        currentPrediction.model_used.replace('_', ' ').toUpperCase();
    
    // Get confidence from metrics
    const metrics = currentPrediction.confidence_metrics;
    const r2 = metrics.test?.r2 || metrics.r2 || 0;
    document.getElementById('confidence').textContent = 
        `${(r2 * 100).toFixed(1)}%`;
    
    const totalFeatures = Object.keys(featuresData.feature_defaults).length;
    const missingCount = currentPrediction.missing_features.length;
    const providedCount = totalFeatures - missingCount;
    
    document.getElementById('featuresProvided').textContent = 
        `${providedCount} / ${totalFeatures}`;
    
    // Scroll to results
    resultContainerEl.scrollIntoView({ behavior: 'smooth' });
}

// Reset form
function resetForm() {
    formEl.reset();
    document.querySelector('.form-container').style.display = 'block';
    resultContainerEl.style.display = 'none';
    currentPrediction = null;
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Show details modal
function showDetails() {
    if (!currentPrediction) return;
    
    const breakdown = document.getElementById('featureBreakdown');
    breakdown.innerHTML = '';
    
    // Create feature breakdown
    const featuresUsed = currentPrediction.features_used;
    const missingFeatures = new Set(currentPrediction.missing_features);
    
    Object.entries(featuresUsed).forEach(([feature, value]) => {
        const isProvided = !missingFeatures.has(feature);
        const featureItem = document.createElement('div');
        featureItem.className = `feature-item ${isProvided ? 'provided' : 'default'}`;
        
        featureItem.innerHTML = `
            <span class="feature-name">${formatFeatureName(feature)}</span>
            <span class="feature-value">
                ${value} ${isProvided ? '✓' : '(default)'}
            </span>
        `;
        
        breakdown.appendChild(featureItem);
    });
    
    detailsModalEl.style.display = 'flex';
}

// Close details modal
function closeDetails() {
    detailsModalEl.style.display = 'none';
}

// Close modal when clicking outside
detailsModalEl.addEventListener('click', function(e) {
    if (e.target === detailsModalEl) {
        closeDetails();
    }
});

// Handle escape key for modal
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && detailsModalEl.style.display === 'flex') {
        closeDetails();
    }
});
