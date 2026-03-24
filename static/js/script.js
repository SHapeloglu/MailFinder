// static/js/script.js

// Sayfa yüklendiğinde çalışacak fonksiyonlar
document.addEventListener('DOMContentLoaded', function() {
    initializeTooltips();
    initializeFileUpload();
    initializeMultiFileUpload();
    updateTimestamp();
    setupScrollButton();
    setupFormValidation();
    setupDragAndDrop();
});

// Tooltips başlatma
function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Tekli dosya yükleme
function initializeFileUpload() {
    const fileInputs = document.querySelectorAll('input[type="file"]:not([multiple])');
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const fileName = this.files.length > 0 ? this.files[0].name : 'Dosya seçilmedi';
            const fileLabel = this.nextElementSibling;
            if (fileLabel && fileLabel.classList.contains('file-name')) {
                fileLabel.textContent = fileName;
            }
        });
    });
}

// Çoklu dosya yükleme
function initializeMultiFileUpload() {
    const multiFileInputs = document.querySelectorAll('input[type="file"][multiple]');
    
    multiFileInputs.forEach(input => {
        const container = document.createElement('div');
        container.className = 'file-list mt-2';
        container.id = `file-list-${Math.random().toString(36).substr(2, 9)}`;
        input.parentNode.insertBefore(container, input.nextSibling);
        
        const counter = document.createElement('span');
        counter.className = 'multi-file-badge badge bg-success';
        counter.style.display = 'none';
        input.parentNode.insertBefore(counter, input.nextSibling);
        
        input.addEventListener('change', function(e) {
            updateFileList(this, container, counter);
        });
    });
}

function updateFileList(input, container, counter) {
    const files = Array.from(input.files);
    
    if (files.length === 0) {
        container.innerHTML = '';
        counter.style.display = 'none';
        return;
    }
    
    counter.textContent = `${files.length} dosya seçildi`;
    counter.style.display = 'inline-block';
    
    let html = '<div class="file-list-header d-flex justify-content-between align-items-center mb-2">';
    html += '<small class="text-muted">Seçilen dosyalar:</small>';
    html += '<button type="button" class="btn btn-sm btn-link text-danger clear-files">Temizle</button>';
    html += '</div>';
    
    files.forEach((file, index) => {
        const size = formatFileSize(file.size);
        html += `
            <div class="file-item" data-index="${index}">
                <i class="bi bi-file-earmark"></i>
                <span class="file-name">${file.name}</span>
                <span class="file-size">${size}</span>
                <i class="bi bi-x-circle remove-file" data-index="${index}"></i>
            </div>
        `;
    });
    
    container.innerHTML = html;
    
    container.querySelector('.clear-files')?.addEventListener('click', function() {
        input.value = '';
        container.innerHTML = '';
        counter.style.display = 'none';
    });
    
    container.querySelectorAll('.remove-file').forEach(btn => {
        btn.addEventListener('click', function() {
            const index = parseInt(this.dataset.index);
            removeFileFromInput(input, index, container, counter);
        });
    });
}

function removeFileFromInput(input, index, container, counter) {
    const dt = new DataTransfer();
    const files = Array.from(input.files);
    
    files.forEach((file, i) => {
        if (i !== index) {
            dt.items.add(file);
        }
    });
    
    input.files = dt.files;
    updateFileList(input, container, counter);
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function setupDragAndDrop() {
    const dropZones = document.querySelectorAll('.file-upload');
    
    dropZones.forEach(zone => {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            zone.addEventListener(eventName, preventDefaults, false);
        });
        
        ['dragenter', 'dragover'].forEach(eventName => {
            zone.addEventListener(eventName, highlight, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            zone.addEventListener(eventName, unhighlight, false);
        });
        
        zone.addEventListener('drop', handleDrop, false);
    });
}

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function highlight(e) {
    e.target.classList.add('dragover');
}

function unhighlight(e) {
    e.target.classList.remove('dragover');
}

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    const fileInput = e.target.closest('.file-upload')?.querySelector('input[type="file"]');
    
    if (fileInput) {
        if (fileInput.multiple) {
            const newDt = new DataTransfer();
            const existingFiles = Array.from(fileInput.files);
            existingFiles.forEach(file => newDt.items.add(file));
            Array.from(files).forEach(file => newDt.items.add(file));
            fileInput.files = newDt.files;
        } else {
            fileInput.files = files;
        }
        
        const event = new Event('change', { bubbles: true });
        fileInput.dispatchEvent(event);
    }
}

function updateTimestamp() {
    const timestampElements = document.querySelectorAll('[data-timestamp]');
    timestampElements.forEach(elem => {
        const now = new Date();
        const formatted = now.toLocaleString('tr-TR');
        elem.textContent = formatted;
    });
}

function setupScrollButton() {
    const scrollTopBtn = document.getElementById('scrollTopBtn');
    const scrollBottomBtn = document.getElementById('scrollBottomBtn');

    function updateButtons() {
        const scrolled = document.body.scrollTop > 300 || document.documentElement.scrollTop > 300;
        const atBottom = (window.innerHeight + window.scrollY) >= document.body.offsetHeight - 50;

        if (scrollTopBtn) scrollTopBtn.style.display = scrolled ? 'block' : 'none';
        if (scrollBottomBtn) scrollBottomBtn.style.display = atBottom ? 'none' : 'block';
    }

    window.addEventListener('scroll', updateButtons);
    updateButtons();
}

function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function scrollToBottom() {
    window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
}

function setupFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const fileInputs = this.querySelectorAll('input[type="file"]');
            let hasFile = false;
            
            fileInputs.forEach(input => {
                if (input.files.length > 0) hasFile = true;
            });
            
            if (this.querySelector('input[type="url"]')) {
                const urlInput = this.querySelector('input[type="url"]');
                if (urlInput && !urlInput.value) {
                    e.preventDefault();
                    showNotification('Lütfen bir URL girin!', 'warning');
                }
            }
            
            if (fileInputs.length > 0 && !hasFile) {
                e.preventDefault();
                showNotification('Lütfen en az bir dosya seçin!', 'warning');
            }
        });
    });
}

function showNotification(message, type = 'info') {
    const oldAlert = document.querySelector('.notification-alert');
    if (oldAlert) oldAlert.remove();
    
    const alert = document.createElement('div');
    alert.className = `notification-alert alert alert-${type} alert-dismissible fade show position-fixed top-0 end-0 m-3`;
    alert.style.zIndex = '9999';
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(alert);
    
    setTimeout(() => {
        if (alert && alert.parentNode) {
            alert.remove();
        }
    }, 3000);
}

function setExampleUrl(url) {
    const urlInput = document.getElementById('url_input');
    if (urlInput) {
        urlInput.value = url;
    }
}