class FileManager {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.fileList = this.container.querySelector('#file-list');
        this.noFilesMessage = this.container.querySelector('#no-files-message');
        this.deleteFileBtn = this.container.querySelector('#deleteFileBtn');
        this.fileInput = this.container.querySelector('#fileInput');
        this.dropArea = this.container.querySelector('#dropArea');
        this.deleteFileConfirmationModal = document.getElementById('deleteFileConfirmationModal');
        this.deleteFileConfirmationMessage = document.getElementById('deleteFileConfirmationMessage');
        this.cancelDeleteFileBtn = document.getElementById('cancelDeleteFileBtn');
        this.confirmDeleteFileBtn = document.getElementById('confirmDeleteFileBtn');

        this.currentFile = null;
        this.onFileSelected = options.onFileSelected || (() => {});
        this.onFileAdded = options.onFileAdded || (() => {});
        this.onFileDeleted = options.onFileDeleted || (() => {});

        this.initEventListeners();
    }

    initEventListeners() {
        this.deleteFileBtn.addEventListener('click', () => this.handleDeleteFile());
        this.cancelDeleteFileBtn.addEventListener('click', () => this.closeDeleteConfirmationModal());
        this.confirmDeleteFileBtn.addEventListener('click', () => this.deleteFile());
        this.fileInput.addEventListener('change', (e) => this.handleFileSelection(e.target.files));
        
        this.dropArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.dropArea.classList.add('bg-blue-100');
        });
        
        this.dropArea.addEventListener('dragleave', () => {
            this.dropArea.classList.remove('bg-blue-100');
        });
        
        this.dropArea.addEventListener('drop', (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.dropArea.classList.remove('bg-blue-100');
            this.handleFileSelection(e.dataTransfer.files);
        });
    }

    updateFileList(files) {
        this.fileList.innerHTML = '';
        if (files.length > 0) {
            this.noFilesMessage.style.display = 'none';
            files.forEach(file => {
                const fileElement = document.createElement('div');
                fileElement.className = 'file-item mb-2 p-2 border rounded cursor-pointer hover:bg-blue-50 transition-colors duration-200';
                fileElement.textContent = file;
                fileElement.addEventListener('click', () => this.selectFile(fileElement));
                this.fileList.appendChild(fileElement);
            });
        } else {
            this.noFilesMessage.style.display = 'block';
        }
    }

    selectFile(fileElement) {
        const fileItems = this.fileList.querySelectorAll('.file-item');
        fileItems.forEach(item => item.classList.remove('bg-blue-100', 'border-blue-500'));
        fileElement.classList.add('bg-blue-100', 'border-blue-500');
        this.currentFile = fileElement.textContent;
        this.onFileSelected(this.currentFile);
    }

    handleDeleteFile() {
        if (this.currentFile) {
            this.deleteFileConfirmationMessage.textContent = `Are you sure you want to delete the file "${this.currentFile}"?`;
            this.deleteFileConfirmationModal.style.display = 'block';
        } else {
            alert("Please select a file to delete.");
        }
    }

    closeDeleteConfirmationModal() {
        this.deleteFileConfirmationModal.style.display = 'none';
    }

    deleteFile() {
        if (this.currentFile) {
            this.onFileDeleted(this.currentFile);
            this.currentFile = null;
            this.closeDeleteConfirmationModal();
        }
    }

    handleFileSelection(files) {
        Array.from(files).forEach(file => {
            this.onFileAdded(file);
        });
        this.fileInput.value = ''; // Reset file input
    }
}
