
// Global variables
let isRecording = false;
let detectionChart;

// DOM Elements
const recordBtn = document.getElementById('recordBtn');
const captureBtn = document.getElementById('captureBtn');
const settingsBtn = document.getElementById('settingsBtn');
const settingsModal = document.getElementById('settingsModal');
const closeModal = document.querySelector('.close-modal');
const confidenceThreshold = document.getElementById('confidenceThreshold');
const confidenceValue = document.getElementById('confidenceValue');
const toast = document.getElementById('toast');
const recordingStatus = document.getElementById('recordingStatus');

// Initialize Chart
function initChart() {
    const ctx = document.getElementById('detectionChart').getContext('2d');
    detectionChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Detections per Minute',
                data: [],
                borderColor: '#2ecc71',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Update Statistics
function updateStats() {
    fetch('/get_stats')
        .then(response => response.json())
        .then(data => {
            document.getElementById('totalDetections').textContent = data.total_detections;
            document.getElementById('avgConfidence').textContent = `${data.avg_confidence}%`;
            
            // Update detection history
            const historyHTML = data.detection_history.map(detection => `
                <div class="detection-item">
                    <span>${detection.class}</span>
                    <span>${(detection.confidence * 100).toFixed(1)}%</span>
                </div>
            `).join('');
            document.getElementById('detectionHistory').innerHTML = historyHTML;

            // Update chart
            if (detectionChart.data.labels.length > 10) {
                detectionChart.data.labels.shift();
                detectionChart.data.datasets[0].data.shift();
            }
            detectionChart.data.labels.push(new Date().toLocaleTimeString());
            detectionChart.data.datasets[0].data.push(data.total_detections);
            detectionChart.update();
        });
}

// Show Toast Message
function showToast(message, duration = 3000) {
    toast.textContent = message;
    toast.style.display = 'block';
    setTimeout(() => {
        toast.style.display = 'none';
    }, duration);
}

// Event Listeners
captureBtn.addEventListener('click', () => {
    fetch('/capture_screenshot', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showToast('Screenshot captured successfully!');
            }
        });
});

recordBtn.addEventListener('click', () => {
    fetch('/toggle_recording', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            isRecording = data.action === 'started';
            recordBtn.innerHTML = `
                <i class="fas fa-video"></i>
                ${isRecording ? 'Stop Recording' : 'Start Recording'}
            `;
            recordingStatus.style.display = isRecording ? 'flex' : 'none';
            showToast(`Recording ${data.action}!`);
        });
});

settingsBtn.addEventListener('click', () => {
    settingsModal.style.display = 'flex';
});

closeModal.addEventListener('click', () => {
    settingsModal.style.display = 'none';
});

confidenceThreshold.addEventListener('input', (e) => {
    confidenceValue.textContent = `${e.target.value}%`;
});
// Continue from the previous JavaScript...

// Settings form submission
document.getElementById('settingsForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const settings = {
        confidence_threshold: confidenceThreshold.value / 100,
        target_classes: Array.from(document.querySelectorAll('[name="targetClass"]:checked'))
            .map(cb => cb.value)
    };

    fetch('/update_settings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(settings)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast('Settings updated successfully!');
            settingsModal.style.display = 'none';
        }
    });
});

// Close modal when clicking outside
window.addEventListener('click', (e) => {
    if (e.target === settingsModal) {
        settingsModal.style.display = 'none';
    }
});

// Initialize target classes checkboxes
const targetClasses = ["garbage", "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe"];
const targetClassesContainer = document.getElementById('targetClassesContainer');
targetClasses.forEach(className => {
    const div = document.createElement('div');
    div.innerHTML = `
        <label>
            <input type="checkbox" name="targetClass" value="${className}" checked>
            ${className.charAt(0).toUpperCase() + className.slice(1)}
        </label>
    `;
    targetClassesContainer.appendChild(div);
});

// Initialize chart and start updates
document.addEventListener('DOMContentLoaded', () => {
    initChart();
    // Update stats every second
    setInterval(updateStats, 1000);
});

