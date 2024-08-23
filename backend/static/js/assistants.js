document.addEventListener('DOMContentLoaded', function() {
    const assistantList = document.getElementById('assistant-list');
    const chatTitle = document.getElementById('chat-title');
    const createAssistantBtn = document.getElementById('createAssistantBtn');
    const editAssistantBtn = document.getElementById('editAssistantBtn');
    const deleteAssistantBtn = document.getElementById('deleteAssistantBtn');

    const assistantEditorModal = document.getElementById('assistantEditorModal');
    const deleteConfirmationModal = document.getElementById('deleteConfirmationModal');
    const deleteConfirmationMessage = document.getElementById('deleteConfirmationMessage');
    const cancelBtn = document.getElementById('cancelBtn');
    const cancelDeleteBtn = document.getElementById('cancelDeleteBtn');
    const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
    const assistantForm = document.getElementById('assistantForm');
    const modalTitle = document.getElementById('modalTitle');
    const submitBtn = document.getElementById('submitBtn');

    let selectedAssistant = null;
    let isEditMode = false;

    function attachAssistantButtonListeners() {
        const assistantButtons = assistantList.querySelectorAll('.assistant-button');
        assistantButtons.forEach(button => {
            button.addEventListener('click', function() {
                selectAssistant(this);
            });
        });

        // Select the first assistant by default
        if (assistantButtons.length > 0) {
            selectAssistant(assistantButtons[0]);
        }
    }

    function selectAssistant(assistantElement) {
        const assistantButtons = assistantList.querySelectorAll('.assistant-button');
        assistantButtons.forEach(btn => btn.classList.remove('bg-blue-100', 'border-blue-500'));
        assistantElement.classList.add('bg-blue-100', 'border-blue-500');
        selectedAssistant = assistantElement;
    }

    function openAssistantEditor(isEdit = false) {
        modalTitle.textContent = isEdit ? "Edit Assistant" : "Create Assistant";
        submitBtn.textContent = isEdit ? "Update" : "Save";
        isEditMode = isEdit;
        if (isEdit && selectedAssistant) {
            assistantForm.assistantName.value = selectedAssistant.getAttribute('data-assistant-name');
            assistantForm.assistantRole.value = selectedAssistant.getAttribute('data-assistant-role');
            assistantForm.systemPrompt.value = selectedAssistant.getAttribute('data-assistant-prompt');
        } else {
            assistantForm.reset();
        }