document.addEventListener('DOMContentLoaded', function() {
    const createWebhookBtn = document.getElementById('createWebhookBtn');
    const editWebhookBtn = document.getElementById('editWebhookBtn');
    const deleteWebhookBtn = document.getElementById('deleteWebhookBtn');
    const webhookModal = document.getElementById('webhookModal');
    const webhookForm = document.getElementById('webhookForm');
    const cancelWebhookBtn = document.getElementById('cancelWebhookBtn');
    const webhookList = document.getElementById('webhook-list');

    let selectedWebhook = null;

    function showWebhookModal(isEdit = false) {
        webhookModal.style.display = 'block';
        document.getElementById('webhookModalTitle').textContent = isEdit ? 'Edit Webhook' : 'Create Webhook';
        document.getElementById('saveWebhookBtn').textContent = isEdit ? 'Update' : 'Save';
        
        if (!isEdit) {
            webhookForm.reset();
        }
    }

    function hideWebhookModal() {
        webhookModal.style.display = 'none';
        selectedWebhook = null;
    }

    function updateWebhookList() {
        fetch('/get_webhooks')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    webhookList.innerHTML = '';
                    data.webhooks.forEach(webhook => {
                        const webhookElement = document.createElement('div');
                        webhookElement.className = 'webhook-item mb-4 p-2 border rounded cursor-pointer';
                        webhookElement.innerHTML = `
                            <h3 class="font-semibold text-gray-800">Webhook for ${webhook.assistant_id}</h3>
                            <p>WhatsApp Number: ${webhook.whatsapp_number}</p>
                            <p>URL: ${webhook.webhook_url}</p>
                            <p class="text-sm text-gray-600">Enabled: ${webhook.enabled ? 'Yes' : 'No'}</p>
                        `;
                        webhookElement.addEventListener('click', () => selectWebhook(webhook, webhookElement));
                        webhookList.appendChild(webhookElement);
                    });
                } else {
                    console.error('Failed to fetch webhooks:', data.message);
                }
            })
            .catch(error => console.error('Error:', error));
    }

    function selectWebhook(webhook, element) {
        const webhookItems = webhookList.querySelectorAll('.webhook-item');
        webhookItems.forEach(item => item.classList.remove('bg-blue-100', 'border-blue-500'));
        element.classList.add('bg-blue-100', 'border-blue-500');
        selectedWebhook = webhook;
    }

    createWebhookBtn.addEventListener('click', () => showWebhookModal(false));

    editWebhookBtn.addEventListener('click', function() {
        if (selectedWebhook) {
            document.getElementById('webhookAssistant').value = selectedWebhook.assistant_id;
            document.getElementById('whatsappNumber').value = selectedWebhook.whatsapp_number;
            document.getElementById('webhookUrl').value = selectedWebhook.webhook_url;
            document.getElementById('webhookEnabled').checked = selectedWebhook.enabled;
            showWebhookModal(true);
        } else {
            alert("Please select a webhook to edit.");
        }
    });

    deleteWebhookBtn.addEventListener('click', function() {
        if (selectedWebhook) {
            if (confirm(`Are you sure you want to delete the webhook for ${selectedWebhook.assistant_id}?`)) {
                fetch('/delete_webhook', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({webhook_id: selectedWebhook.webhook_id}),
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        updateWebhookList();
                        selectedWebhook = null;
                    } else {
                        alert('Failed to delete webhook: ' + data.message);
                    }
                })
                .catch(error => console.error('Error:', error));
            }
        } else {
            alert("Please select a webhook to delete.");
        }
    });

    cancelWebhookBtn.addEventListener('click', hideWebhookModal);

    webhookForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = {
            assistant_id: document.getElementById('webhookAssistant').value,
            whatsapp_number: document.getElementById('whatsappNumber').value,
            webhook_url: document.getElementById('webhookUrl').value,
            enabled: document.getElementById('webhookEnabled').checked
        };
        
        const url = selectedWebhook ? '/edit_webhook' : '/create_webhook';
        const method = 'POST';
        if (selectedWebhook) {
            formData.webhook_id = selectedWebhook.webhook_id;
        }

        fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                hideWebhookModal();
                updateWebhookList();
            } else {
                alert(data.message);
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    });

    // Initialize webhook list
    updateWebhookList();
});