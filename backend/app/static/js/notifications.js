// ============================================================================
// SISTEMA DE NOTIFICACIONES
// ============================================================================

/**
 * Mostrar notificación en la UI
 * @param {string} message - Mensaje de la notificación
 * @param {string} type - Tipo: 'success', 'error', 'warning', 'info'
 * @param {string} title - Título de la notificación (opcional)
 * @param {number} duration - Duración en ms (0 = sin auto-dismiss)
 */
function showNotification(message, type = 'info', title = null, duration = 5000) {
    const container = document.getElementById('alerts-container');
    
    // Definir iconos y colores según tipo
    const config = {
        success: {
            icon: 'bi-check-circle-fill',
            title: title || 'Éxito',
            class: 'alert-success'
        },
        error: {
            icon: 'bi-exclamation-circle-fill',
            title: title || 'Error',
            class: 'alert-error'
        },
        warning: {
            icon: 'bi-exclamation-triangle-fill',
            title: title || 'Advertencia',
            class: 'alert-warning'
        },
        info: {
            icon: 'bi-info-circle-fill',
            title: title || 'Información',
            class: 'alert-info'
        }
    };
    
    const cfg = config[type] || config.info;
    
    // Crear elemento de alerta
    const alertElement = document.createElement('div');
    alertElement.className = `alert ${cfg.class}`;
    alertElement.innerHTML = `
        <i class="bi ${cfg.icon}"></i>
        <div class="alert-content">
            <div class="alert-title">${cfg.title}</div>
            <div class="alert-message">${message}</div>
        </div>
        <button type="button" class="alert-close" onclick="this.parentElement.remove()">
            <i class="bi bi-x"></i>
        </button>
    `;
    
    container.appendChild(alertElement);
    
    // Auto-dismiss después del tiempo especificado
    if (duration > 0) {
        setTimeout(() => {
            alertElement.classList.add('removing');
            setTimeout(() => alertElement.remove(), 300);
        }, duration);
    }
    
    // Scroll a la notificación
    alertElement.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Mostrar notificación de éxito
 */
function showSuccess(message, title = 'Éxito', duration = 5000) {
    showNotification(message, 'success', title, duration);
}

/**
 * Mostrar notificación de error
 */
function showError(message, title = 'Error', duration = 5000) {
    showNotification(message, 'error', title, duration);
}

/**
 * Mostrar notificación de advertencia
 */
function showWarning(message, title = 'Advertencia', duration = 5000) {
    showNotification(message, 'warning', title, duration);
}

/**
 * Mostrar notificación de información
 */
function showInfo(message, title = 'Información', duration = 5000) {
    showNotification(message, 'info', title, duration);
}

/**
 * Mostrar spinner/loader
 * @param {string} message - Mensaje opcional
 */
function showSpinner(message = 'Cargando...') {
    // Crear overlay con spinner
    const overlay = document.createElement('div');
    overlay.className = 'spinner-overlay';
    overlay.id = 'loadingSpinner';
    overlay.innerHTML = `
        <div>
            <div class="loader"></div>
            <p style="color: white; margin-top: 20px; text-align: center;">${message}</p>
        </div>
    `;
    
    document.body.appendChild(overlay);
}

/**
 * Ocultar spinner/loader
 */
function hideSpinner() {
    const spinner = document.getElementById('loadingSpinner');
    if (spinner) {
        spinner.remove();
    }
}

/**
 * Mostrar confirmación modal
 * @param {string} message - Mensaje de confirmación
 * @param {function} onConfirm - Callback si confirma
 * @param {function} onCancel - Callback si cancela
 */
function showConfirm(message, onConfirm, onCancel = null) {
    const html = `
        <p style="margin-bottom: 20px;">${message}</p>
        <div style="display: flex; gap: 10px; justify-content: flex-end;">
            <button type="button" class="btn btn-secondary" onclick="closeModal(); ${onCancel ? 'onCancel()' : ''}">
                Cancelar
            </button>
            <button type="button" class="btn btn-danger" onclick="closeModal(); onConfirm()">
                Confirmar
            </button>
        </div>
    `;
    
    window.onConfirm = onConfirm;
    window.onCancel = onCancel;
    
    openModal('Confirmar Acción', html, 'Aceptar', null);
}
