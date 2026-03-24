// B2Builder Frontend JavaScript

// Global variables
let currentTemplate = 'invoice';

// DOM elements
const templates = {
    invoice: document.getElementById('invoice-template'),
    certificate: document.getElementById('certificate-template'),
    report: document.getElementById('report-template')
};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    setupNavigation();
    setupForms();
    setupItemManagement();
    showTemplate('invoice');
});

// Navigation setup
function setupNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');

    navButtons.forEach(button => {
        button.addEventListener('click', function() {
            const templateType = this.getAttribute('onclick').match(/'(\w+)'/)[1];
            showTemplate(templateType);
        });
    });
}

// Show selected template
function showTemplate(templateType) {
    // Hide all templates
    Object.values(templates).forEach(template => {
        template.classList.remove('active');
    });

    // Show selected template
    templates[templateType].classList.add('active');
    currentTemplate = templateType;

    // Update navigation
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    document.querySelector(`[onclick="showTemplate('${templateType}')"]`).classList.add('active');
}

// Form setup
function setupForms() {
    // Invoice form
    document.getElementById('invoice-form').addEventListener('submit', function(e) {
        e.preventDefault();
        generateInvoice();
    });

    // Certificate form
    document.getElementById('certificate-form').addEventListener('submit', function(e) {
        e.preventDefault();
        generateCertificate();
    });

    // Report form
    document.getElementById('report-form').addEventListener('submit', function(e) {
        e.preventDefault();
        generateReport();
    });
}

// Item management for invoice
function setupItemManagement() {
    // Auto-calculate totals
    document.addEventListener('input', function(e) {
        if (e.target.classList.contains('item-quantity') || e.target.classList.contains('item-price')) {
            calculateItemTotal(e.target.closest('.item-row'));
        }
    });
}

function addItem() {
    const container = document.getElementById('items-container');
    const itemRow = document.createElement('div');
    itemRow.className = 'item-row';
    itemRow.innerHTML = `
        <div class="form-row">
            <div class="form-group large">
                <label>Opis</label>
                <input type="text" class="item-description" placeholder="Usługa/produkt" required>
            </div>
            <div class="form-group small">
                <label>Ilość</label>
                <input type="number" class="item-quantity" placeholder="1" min="1" required>
            </div>
            <div class="form-group small">
                <label>Cena jedn.</label>
                <input type="number" class="item-price" placeholder="100.00" step="0.01" min="0" required>
            </div>
            <div class="form-group small">
                <label>Wartość</label>
                <input type="number" class="item-total" placeholder="100.00" step="0.01" readonly>
            </div>
            <div class="form-group action">
                <button type="button" class="btn-remove" onclick="removeItem(this)">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `;
    container.appendChild(itemRow);
}

function removeItem(button) {
    const itemRow = button.closest('.item-row');
    if (document.querySelectorAll('.item-row').length > 1) {
        itemRow.remove();
    } else {
        showMessage('Musi pozostać przynajmniej jedna pozycja', 'error');
    }
}

function calculateItemTotal(itemRow) {
    const quantity = parseFloat(itemRow.querySelector('.item-quantity').value) || 0;
    const price = parseFloat(itemRow.querySelector('.item-price').value) || 0;
    const total = quantity * price;
    itemRow.querySelector('.item-total').value = total.toFixed(2);
}

// Generate functions
async function generateInvoice() {
    const formData = {
        template_id: 'invoice_standard',
        data: {
            invoice_number: document.getElementById('invoice-number').value,
            customer: {
                name: document.getElementById('customer-name').value,
                address: document.getElementById('customer-address').value
            },
            items: []
        }
    };

    // Collect items
    document.querySelectorAll('.item-row').forEach(row => {
        const description = row.querySelector('.item-description').value;
        const quantity = parseFloat(row.querySelector('.item-quantity').value);
        const unit_price = parseFloat(row.querySelector('.item-price').value);
        const total_price = parseFloat(row.querySelector('.item-total').value);

        if (description && quantity && unit_price) {
            formData.data.items.push({
                description: description,
                quantity: quantity,
                unit_price: unit_price,
                total_price: total_price
            });
        }
    });

    await generatePDF(formData);
}

async function generateCertificate() {
    const formData = {
        template_id: 'certificate_custom',
        data: {
            recipient_name: document.getElementById('recipient-name').value,
            course_title: document.getElementById('course-title').value,
            completion_date: document.getElementById('completion-date').value,
            issuer_name: document.getElementById('issuer-name').value,
            certificate_number: document.getElementById('certificate-number').value
        }
    };

    await generatePDF(formData);
}

async function generateReport() {
    const formData = {
        template_id: 'report_monthly',
        data: {
            report_title: document.getElementById('report-title').value,
            report_month: document.getElementById('report-month').value,
            summary: document.getElementById('summary').value,
            metrics: {
                revenue: parseFloat(document.getElementById('revenue').value),
                expenses: parseFloat(document.getElementById('expenses').value),
                profit: parseFloat(document.getElementById('profit').value)
            }
        }
    };

    await generatePDF(formData);
}

// Generic PDF generation function
async function generatePDF(formData) {
    const apiKey = document.getElementById('api-key').value;

    if (!apiKey) {
        showMessage('Wprowadź API key przed generowaniem PDF', 'error');
        return;
    }

    showLoading(true);

    try {
        const response = await fetch('/v1/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-API-Key': apiKey
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Create download link
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'generated-document.pdf';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        showMessage('PDF został wygenerowany pomyślnie!', 'success');
    } catch (error) {
        console.error('Error generating PDF:', error);
        showMessage('Wystąpił błąd podczas generowania PDF. Sprawdź dane i API key.', 'error');
    } finally {
        showLoading(false);
    }
}

// UI helper functions
function showLoading(show) {
    let overlay = document.querySelector('.loading-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.className = 'loading-overlay';
        overlay.innerHTML = `
            <div class="loading-content">
                <div class="spinner"></div>
                <p>Generowanie PDF...</p>
            </div>
        `;
        document.body.appendChild(overlay);
    }

    overlay.style.display = show ? 'flex' : 'none';
}

function showMessage(text, type) {
    // Remove existing messages
    document.querySelectorAll('.message').forEach(msg => msg.remove());

    const message = document.createElement('div');
    message.className = `message ${type}`;
    message.textContent = text;

    const form = document.querySelector('.template.active .form');
    form.insertBefore(message, form.firstChild);

    message.style.display = 'block';

    // Auto-hide after 5 seconds
    setTimeout(() => {
        message.style.display = 'none';
    }, 5000);
}

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('pl-PL', {
        style: 'currency',
        currency: 'PLN'
    }).format(amount);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('pl-PL');
}