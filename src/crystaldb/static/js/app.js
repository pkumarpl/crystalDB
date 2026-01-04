// API Base URL
const API_BASE = '/api/v1';

// Pagination state
let currentMaterialPage = 0;
let currentSolventPage = 0;
const PAGE_SIZE = 20;

// Tab switching
document.querySelectorAll('.tab-button').forEach(button => {
    button.addEventListener('click', () => {
        // Remove active class from all tabs
        document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));

        // Add active class to clicked tab
        button.classList.add('active');
        const tabId = button.getAttribute('data-tab');
        document.getElementById(tabId).classList.add('active');

        // Load data for the tab
        if (tabId === 'materials') loadMaterials();
        else if (tabId === 'solvents') loadSolvents();
        else if (tabId === 'experiments') loadExperiments();
        else if (tabId === 'stats') loadStatistics();
    });
});

// Load materials
async function loadMaterials() {
    try {
        const response = await fetch(`${API_BASE}/materials?limit=${PAGE_SIZE}&skip=${currentMaterialPage * PAGE_SIZE}`);
        const materials = await response.json();
        displayMaterials(materials);
        updatePagination('material', materials.length);
    } catch (error) {
        console.error('Error loading materials:', error);
        document.getElementById('materialsBody').innerHTML = `<tr><td colspan="6" class="loading">Error loading materials</td></tr>`;
    }
}

function displayMaterials(materials) {
    const tbody = document.getElementById('materialsBody');
    if (materials.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" class="loading">No materials found</td></tr>`;
        return;
    }

    tbody.innerHTML = materials.map(m => `
        <tr>
            <td>${m.material_id}</td>
            <td>${m.compound_name}</td>
            <td>${m.chemical_formula}</td>
            <td>${m.type}</td>
            <td>${m.cas_number}</td>
            <td>${m.supplier}</td>
        </tr>
    `).join('');
}

async function searchMaterials() {
    const query = document.getElementById('materialSearch').value.trim();
    if (!query) {
        loadMaterials();
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/materials/search/by-name/${encodeURIComponent(query)}`);
        const materials = await response.json();
        displayMaterials(materials);
        document.getElementById('materialPageInfo').textContent = `Search: "${query}"`;
    } catch (error) {
        console.error('Error searching materials:', error);
    }
}

function nextPageMaterials() {
    currentMaterialPage++;
    loadMaterials();
}

function prevPageMaterials() {
    if (currentMaterialPage > 0) {
        currentMaterialPage--;
        loadMaterials();
    }
}

function updatePagination(type, itemCount) {
    if (type === 'material') {
        document.getElementById('materialPageInfo').textContent = `Page ${currentMaterialPage + 1}`;
        document.getElementById('prevMaterials').disabled = currentMaterialPage === 0;
        document.getElementById('nextMaterials').disabled = itemCount < PAGE_SIZE;
    } else if (type === 'solvent') {
        document.getElementById('solventPageInfo').textContent = `Page ${currentSolventPage + 1}`;
        document.getElementById('prevSolvents').disabled = currentSolventPage === 0;
        document.getElementById('nextSolvents').disabled = itemCount < PAGE_SIZE;
    }
}

// Load solvents
async function loadSolvents() {
    try {
        const response = await fetch(`${API_BASE}/solvents?limit=${PAGE_SIZE}&skip=${currentSolventPage * PAGE_SIZE}`);
        const solvents = await response.json();
        displaySolvents(solvents);
        updatePagination('solvent', solvents.length);
    } catch (error) {
        console.error('Error loading solvents:', error);
        document.getElementById('solventsBody').innerHTML = `<tr><td colspan="6" class="loading">Error loading solvents</td></tr>`;
    }
}

function displaySolvents(solvents) {
    const tbody = document.getElementById('solventsBody');
    if (solvents.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" class="loading">No solvents found</td></tr>`;
        return;
    }

    tbody.innerHTML = solvents.map(s => `
        <tr>
            <td>${s.solvent_id}</td>
            <td>${s.solvent_name}</td>
            <td>${s.chemical_formula}</td>
            <td>${s.cas_number}</td>
            <td>${s.product_number}</td>
            <td>${s.supplier}</td>
        </tr>
    `).join('');
}

async function searchSolvents() {
    const query = document.getElementById('solventSearch').value.trim();
    if (!query) {
        loadSolvents();
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/solvents/search/by-name/${encodeURIComponent(query)}`);
        const solvents = await response.json();
        displaySolvents(solvents);
        document.getElementById('solventPageInfo').textContent = `Search: "${query}"`;
    } catch (error) {
        console.error('Error searching solvents:', error);
    }
}

function nextPageSolvents() {
    currentSolventPage++;
    loadSolvents();
}

function prevPageSolvents() {
    if (currentSolventPage > 0) {
        currentSolventPage--;
        loadSolvents();
    }
}

// Load experiments
async function loadExperiments() {
    try {
        const response = await fetch(`${API_BASE}/experiments`);
        const experiments = await response.json();
        document.getElementById('experimentCount').textContent = experiments.length;
    } catch (error) {
        console.error('Error loading experiments:', error);
    }
}

// Load statistics
async function loadStatistics() {
    try {
        // Load counts
        const [materials, solvents, experiments, health] = await Promise.all([
            fetch(`${API_BASE}/materials`).then(r => r.json()),
            fetch(`${API_BASE}/solvents`).then(r => r.json()),
            fetch(`${API_BASE}/experiments`).then(r => r.json()),
            fetch('/health').then(r => r.json())
        ]);

        document.getElementById('totalMaterials').textContent = materials.length;
        document.getElementById('totalSolvents').textContent = solvents.length;
        document.getElementById('totalExperiments').textContent = experiments.length;
        document.getElementById('apiStatus').textContent = health.status === 'healthy' ? '✓' : '✗';

        // Count material types
        const typeCounts = {};
        materials.forEach(m => {
            typeCounts[m.type] = (typeCounts[m.type] || 0) + 1;
        });

        // Display bar chart
        displayBarChart(typeCounts);
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

function displayBarChart(data) {
    const maxCount = Math.max(...Object.values(data));
    const chartHtml = Object.entries(data).map(([type, count]) => {
        const percentage = (count / maxCount) * 100;
        return `
            <div class="bar">
                <div class="bar-label">${type}</div>
                <div class="bar-fill" style="width: ${percentage}%">${count}</div>
            </div>
        `;
    }).join('');

    document.getElementById('barChart').innerHTML = chartHtml;
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadMaterials();
    loadStatistics();
});

// Handle enter key in search boxes
document.getElementById('materialSearch').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') searchMaterials();
});

document.getElementById('solventSearch').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') searchSolvents();
});
