// ============================================================================
// VALIDADOR DE FORMULARIOS FRONTEND
// ============================================================================

/**
 * Validar email
 */
function validateEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

/**
 * Validar cédula (formato básico)
 */
function validateCedula(cedula) {
    return cedula && cedula.length >= 5 && cedula.length <= 20;
}

/**
 * Validar teléfono
 */
function validatePhone(phone) {
    const regex = /^\d{7,20}$/;
    return !phone || regex.test(phone);
}

/**
 * Validar fecha
 */
function validateDate(date) {
    const regex = /^\d{4}-\d{2}-\d{2}$/;
    return !date || regex.test(date);
}

/**
 * Validar número positivo
 */
function validatePositiveNumber(value) {
    return !isNaN(value) && parseFloat(value) >= 0;
}

/**
 * Validar campo requerido
 */
function validateRequired(value) {
    return value && value.trim().length > 0;
}

/**
 * Mostrar error en campo
 */
function showFieldError(fieldId, message) {
    const field = document.getElementById(fieldId);
    if (!field) return;
    
    field.classList.add('is-invalid');
    
    // Remover error anterior si existe
    const existingError = field.parentElement.querySelector('.form-error');
    if (existingError) {
        existingError.remove();
    }
    
    // Agregar nuevo error
    const errorElement = document.createElement('div');
    errorElement.className = 'form-error';
    errorElement.textContent = message;
    field.parentElement.appendChild(errorElement);
}

/**
 * Limpiar error en campo
 */
function clearFieldError(fieldId) {
    const field = document.getElementById(fieldId);
    if (!field) return;
    
    field.classList.remove('is-invalid');
    
    const errorElement = field.parentElement.querySelector('.form-error');
    if (errorElement) {
        errorElement.remove();
    }
}

/**
 * Limpiar todos los errores
 */
function clearAllErrors() {
    const fields = document.querySelectorAll('.is-invalid');
    fields.forEach(field => {
        field.classList.remove('is-invalid');
        const errorElement = field.parentElement.querySelector('.form-error');
        if (errorElement) {
            errorElement.remove();
        }
    });
}

/**
 * Validar formulario genérico
 * @param {string} formId - ID del formulario
 * @param {object} rules - Objeto con reglas: {fieldId: [validadores]}
 */
function validateForm(formId, rules) {
    clearAllErrors();
    
    let isValid = true;
    const form = document.getElementById(formId);
    
    for (const fieldId in rules) {
        const field = document.getElementById(fieldId);
        if (!field) continue;
        
        const value = field.value;
        const fieldRules = rules[fieldId];
        
        for (const rule of fieldRules) {
            let isFieldValid = true;
            let errorMessage = '';
            
            if (typeof rule === 'string') {
                // Validador predefinido
                switch (rule) {
                    case 'required':
                        isFieldValid = validateRequired(value);
                        errorMessage = 'Este campo es requerido';
                        break;
                    case 'email':
                        isFieldValid = !value || validateEmail(value);
                        errorMessage = 'Email inválido';
                        break;
                    case 'cedula':
                        isFieldValid = !value || validateCedula(value);
                        errorMessage = 'Cédula inválida';
                        break;
                    case 'phone':
                        isFieldValid = !value || validatePhone(value);
                        errorMessage = 'Teléfono inválido';
                        break;
                    case 'date':
                        isFieldValid = !value || validateDate(value);
                        errorMessage = 'Formato de fecha inválido (YYYY-MM-DD)';
                        break;
                    case 'positive':
                        isFieldValid = !value || validatePositiveNumber(value);
                        errorMessage = 'Debe ser un número positivo';
                        break;
                }
            } else if (typeof rule === 'object') {
                // Validador personalizado
                if (rule.test) {
                    isFieldValid = rule.test(value);
                    errorMessage = rule.message || 'Campo inválido';
                } else if (rule.minLength) {
                    isFieldValid = !value || value.length >= rule.minLength;
                    errorMessage = `Mínimo ${rule.minLength} caracteres`;
                } else if (rule.maxLength) {
                    isFieldValid = !value || value.length <= rule.maxLength;
                    errorMessage = `Máximo ${rule.maxLength} caracteres`;
                } else if (rule.min !== undefined) {
                    isFieldValid = !value || parseFloat(value) >= rule.min;
                    errorMessage = `Debe ser mayor o igual a ${rule.min}`;
                } else if (rule.max !== undefined) {
                    isFieldValid = !value || parseFloat(value) <= rule.max;
                    errorMessage = `Debe ser menor o igual a ${rule.max}`;
                }
            }
            
            if (!isFieldValid) {
                showFieldError(fieldId, errorMessage);
                isValid = false;
                break;
            }
        }
    }
    
    return isValid;
}

/**
 * Setup validación en tiempo real
 * @param {string} fieldId - ID del campo
 * @param {array} rules - Array de reglas de validación
 */
function setupFieldValidation(fieldId, rules) {
    const field = document.getElementById(fieldId);
    if (!field) return;
    
    field.addEventListener('blur', () => {
        const value = field.value;
        let isValid = true;
        let errorMessage = '';
        
        for (const rule of rules) {
            if (typeof rule === 'string') {
                switch (rule) {
                    case 'required':
                        isValid = validateRequired(value);
                        errorMessage = 'Este campo es requerido';
                        break;
                    case 'email':
                        isValid = !value || validateEmail(value);
                        errorMessage = 'Email inválido';
                        break;
                    case 'cedula':
                        isValid = !value || validateCedula(value);
                        errorMessage = 'Cédula inválida';
                        break;
                    case 'phone':
                        isValid = !value || validatePhone(value);
                        errorMessage = 'Teléfono inválido';
                        break;
                }
            }
            
            if (!isValid) break;
        }
        
        if (!isValid) {
            showFieldError(fieldId, errorMessage);
        } else {
            clearFieldError(fieldId);
        }
    });
}

/**
 * Setup validación en tiempo real para múltiples campos
 * @param {object} rules - Objeto: {fieldId: [validadores]}
 */
function setupFormValidation(rules) {
    for (const fieldId in rules) {
        setupFieldValidation(fieldId, rules[fieldId]);
    }
}

/**
 * Obtener errores del servidor (si existen)
 * @param {object} serverResponse - Respuesta del servidor
 */
function handleServerErrors(serverResponse) {
    if (serverResponse.detail) {
        if (typeof serverResponse.detail === 'string') {
            showError(serverResponse.detail);
        } else if (Array.isArray(serverResponse.detail)) {
            // Formato de Pydantic validation errors
            serverResponse.detail.forEach(error => {
                const fieldId = error.loc[error.loc.length - 1];
                showFieldError(fieldId, error.msg);
            });
        }
    }
}

// Agregar estilos para campos inválidos
const style = document.createElement('style');
style.textContent = `
    .is-invalid {
        border-color: var(--danger-color) !important;
        background: rgba(220, 53, 69, 0.05);
    }
    
    .is-invalid:focus {
        border-color: var(--danger-color) !important;
        box-shadow: 0 0 0 0.2rem rgba(220, 53, 69, 0.25) !important;
    }
    
    .form-error {
        color: var(--danger-color);
        font-size: 12px;
        margin-top: 5px;
        display: block;
    }
`;
document.head.appendChild(style);
