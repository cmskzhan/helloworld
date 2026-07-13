function showToast(msg, type="info") {
    const toast = document.getElementById('toast');
    toast.textContent = msg;
    toast.style.borderColor = type === "error" ? 'var(--danger-color)' : 'var(--accent-color)';
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

function renderPreview() {
    const mdText = document.getElementById('cv-md').value;
    const previewEl = document.getElementById('cv-preview');
    if (!mdText.trim()) {
        previewEl.innerHTML = '<p class="preview-empty">Edit the markdown to see a live preview…</p>';
        return;
    }
    try {
        const rawHtml = marked.parse(mdText);
        previewEl.innerHTML = DOMPurify.sanitize(rawHtml);
    } catch (e) {
        previewEl.innerHTML = '<p class="preview-empty">Preview rendering failed. Ensure CDN scripts (marked, DOMPurify) are accessible.</p>';
        console.error("Preview render error:", e);
    }
}

function setView(mode) {
    try {
        const container = document.getElementById('editor-preview-container');
        const editorPane = document.getElementById('editor-pane');
        const previewPane = document.getElementById('preview-pane');
        const buttons = document.querySelectorAll('.view-toggle .toggle-btn');
        buttons.forEach(b => b.classList.remove('active'));

        container.classList.remove('view-split', 'view-editor', 'view-preview');

        if (mode === 'split') {
            container.classList.add('view-split');
            editorPane.classList.remove('hidden');
            previewPane.classList.remove('hidden');
            document.getElementById('view-split').classList.add('active');
        } else if (mode === 'editor') {
            container.classList.add('view-editor');
            editorPane.classList.remove('hidden');
            previewPane.classList.add('hidden');
            document.getElementById('view-editor').classList.add('active');
        } else if (mode === 'preview') {
            container.classList.add('view-preview');
            editorPane.classList.add('hidden');
            previewPane.classList.remove('hidden');
            document.getElementById('view-preview').classList.add('active');
        }
        if (mode !== 'editor') renderPreview();
    } catch (e) {
        console.error("setView error:", e);
    }
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

async function downloadExport(format) {
    const markdown = document.getElementById('cv-md').value;
    if(!markdown) return;

    try {
        const res = await fetch(`/api/cv/${format}`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ markdown })
        });
        if(!res.ok) throw new Error("Download failed");
        
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `Tailored_CV.${format}`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        showToast(`${format.toUpperCase()} downloaded`);
    } catch(e) {
        showToast(e.message, "error");
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    // ── API key → model list ──────────────────────────────────────────────────
    document.getElementById('api-key').addEventListener('input', debounce(updateModelList, 1000));

    // ── View-toggle buttons ───────────────────────────────────────────────────
    document.getElementById('view-split').addEventListener('click', () => setView('split'));
    document.getElementById('view-editor').addEventListener('click', () => setView('editor'));
    document.getElementById('view-preview').addEventListener('click', () => setView('preview'));

    // ── Live markdown → preview ───────────────────────────────────────────────
    document.getElementById('cv-md').addEventListener('input', debounce(renderPreview, 200));

    // ── Download buttons ──────────────────────────────────────────────────────
    document.getElementById('download-pdf').addEventListener('click', () => downloadExport('pdf'));
    document.getElementById('download-docx').addEventListener('click', () => downloadExport('docx'));

    // ── Generate button ───────────────────────────────────────────────────────
    document.getElementById('generate-btn').addEventListener('click', async () => {
        const apiKey = document.getElementById('api-key').value;
        const jd = document.getElementById('jd').value;
        const focus = document.getElementById('focus').value;
        const modelName = document.getElementById('model-name').value;
        const useProfile = document.getElementById('use-profile') ? document.getElementById('use-profile').checked : false;
        const files = document.getElementById('cv-uploads').files;

        if (!apiKey) return showToast("API Key is required", "error");
        if (!jd) return showToast("Job description is required", "error");
        if (!useProfile && files.length === 0) return showToast("Provide at least one CV or enable saved profile", "error");

        const formData = new FormData();
        formData.append('api_key', apiKey);
        formData.append('jd', jd);
        formData.append('focus', focus);
        formData.append('model_name', modelName);
        formData.append('use_profile', useProfile);

        for (let i = 0; i < files.length; i++) {
            formData.append('files', files[i]);
        }

        const btn = document.getElementById('generate-btn');
        const txt = document.getElementById('gen-btn-text');
        const loader = document.getElementById('gen-loader');

        btn.disabled = true;
        txt.classList.add('hidden');
        loader.classList.remove('hidden');

        try {
            const res = await fetch('/api/cv/generate', {
                method: 'POST',
                body: formData
            });
            const data = await res.json();
            if (!res.ok) throw new Error(data.detail || "Failed to generate");

            document.getElementById('results-panel').classList.remove('hidden');
            document.getElementById('cv-md').value = data.markdown;
            setView('split');
            showToast("CV generated successfully!");
        } catch (e) {
            showToast(e.message, "error");
        } finally {
            btn.disabled = false;
            txt.classList.remove('hidden');
            loader.classList.add('hidden');
        }
    });

    // ── Check if a saved profile exists ───────────────────────────────────────
    try {
        const res = await fetch('/api/profile');
        if (res.ok) {
            const profile = await res.json();
            const hasProfile = profile.personal_info && profile.personal_info.full_name;
            if (hasProfile) {
                document.getElementById('profile-status').style.display = 'block';
                document.getElementById('use-profile-wrapper').style.display = 'block';
                document.getElementById('profile-status-text').textContent =
                    `✅ ${profile.personal_info.full_name} profile found (${profile.work_experience.length} jobs).`;
            }
        }
    } catch (e) {
        console.error(e);
    }
});
