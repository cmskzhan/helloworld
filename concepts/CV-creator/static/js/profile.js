function showToast(msg, type="info") {
    const toast = document.getElementById('toast');
    toast.textContent = msg;
    toast.style.borderColor = type === 'error' ? 'var(--danger-color)' : 'var(--accent-color)';
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 3000);
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

async function updateModelList() {
    const apiKey = document.getElementById('api-key').value;
    const select = document.getElementById('model-name');
    if (!apiKey || apiKey.length < 10) return;

    try {
        const res = await fetch('/api/models', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ api_key: apiKey })
        });
        if (res.ok) {
            const data = await res.json();
            const currentVal = select.value;
            select.innerHTML = '';
            data.models.forEach(m => {
                const opt = document.createElement('option');
                opt.value = m;
                opt.textContent = m;
                if (m === currentVal) opt.selected = true;
                select.appendChild(opt);
            });
        }
    } catch (e) {
        console.error("Failed to load models", e);
    }
}

let currentProfile = {};

async function loadProfile() {
    try {
        const res = await fetch('/api/profile');
        if(!res.ok) throw new Error("Failed to load");
        currentProfile = await res.json();
        
        const hasProfile = currentProfile.personal_info && currentProfile.personal_info.full_name;
        const summary = document.getElementById('profile-summary');
        
        if(hasProfile) {
            summary.innerHTML = `
                <p>✅ Profile loaded — <b>${currentProfile.personal_info.full_name}</b></p>
                <p>• ${currentProfile.work_experience.length} work entries</p>
                <p>• ${currentProfile.education.length} education entries</p>
            `;
            document.getElementById('reset-btn').classList.remove('hidden');
        } else {
            summary.innerHTML = `<p style="color:var(--text-secondary)">No profile found. Upload CV below.</p>`;
            document.getElementById('reset-btn').classList.add('hidden');
        }

        document.getElementById('profile-json-editor').value = JSON.stringify(currentProfile, null, 2);
    } catch(e) {
        showToast(e.message, "error");
    }
}

document.addEventListener('DOMContentLoaded', () => {
    loadProfile();
    document.getElementById('api-key').addEventListener('input', debounce(updateModelList, 1000));
});

document.getElementById('reset-btn').addEventListener('click', async () => {
    if(!confirm("Are you sure you want to reset your profile?")) return;
    try {
        await fetch('/api/profile', { method: 'DELETE' });
        loadProfile();
        showToast("Profile reset!");
    } catch(e) {
        showToast(e.message, "error");
    }
});

async function apiCall(endpoint, formData, btnId) {
    const btn = document.getElementById(btnId);
    const apiVal = document.getElementById('api-key').value;
    const model = document.getElementById('model-name').value;
    
    if(!apiVal) return showToast("API Key required", "error");

    if(formData instanceof FormData) {
        formData.append('api_key', apiVal);
        formData.append('model_name', model);
    } else {
        formData.api_key = apiVal;
        formData.model_name = model;
    }

    const txt = btn.querySelector('span');
    const loader = btn.querySelector('.loader');
    
    btn.disabled = true;
    txt.classList.add('hidden');
    loader.classList.remove('hidden');

    try {
        const isJson = !(formData instanceof FormData);
        const res = await fetch(endpoint, {
            method: 'POST',
            headers: isJson ? {'Content-Type': 'application/json'} : undefined,
            body: isJson ? JSON.stringify(formData) : formData
        });
        
        const data = await res.json();
        if(!res.ok) throw new Error(data.detail || "Error");
        
        await loadProfile();
        showToast("Success!");
    } catch(e) {
        showToast(e.message, "error");
    } finally {
        btn.disabled = false;
        txt.classList.remove('hidden');
        loader.classList.add('hidden');
    }
}

document.getElementById('scan-btn').addEventListener('click', () => {
    apiCall('/api/profile/scan', new FormData(), 'scan-btn');
});

document.getElementById('extract-btn').addEventListener('click', () => {
    const files = document.getElementById('manual-uploads').files;
    if(!files.length) return showToast("Upload at least one file", "error");
    
    const formData = new FormData();
    for(let f of files) formData.append('files', f);
    
    apiCall('/api/profile/extract', formData, 'extract-btn');
});

document.getElementById('dedup-btn').addEventListener('click', () => {
    apiCall('/api/profile/deduplicate', { profile: currentProfile }, 'dedup-btn');
});

document.getElementById('save-json-btn').addEventListener('click', async () => {
    try {
        const val = document.getElementById('profile-json-editor').value;
        const newProfile = JSON.parse(val);
        
        await fetch('/api/profile', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newProfile)
        });
        
        await loadProfile();
        showToast("Manual edits saved!");
    } catch(e) {
        showToast("Invalid JSON: " + e.message, "error");
    }
});
