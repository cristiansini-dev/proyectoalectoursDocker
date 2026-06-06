// ============================================================================
// MANEJADOR UNIVERSAL DE CRUD CON FETCH API
// ============================================================================

/**
 * Realizar petición HTTP genérica
 * @param {string} method - Método HTTP (GET, POST, PUT, DELETE)
 * @param {string} url - URL del endpoint
 * @param {object} data - Datos a enviar (para POST/PUT)
 * @param {boolean} showLoading - Mostrar spinner
 */
async function fetchAPI(method, url, data = null, showLoading = true) {
    try {
        if (showLoading) showSpinner('Procesando...');
        
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            }
        };
        
        // Agregar body si es POST o PUT
        if (data && (method === 'POST' || method === 'PUT')) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(url, options);
        const result = await response.json();
        
        if (showLoading) hideSpinner();
        
        return {
            status: response.status,
            ok: response.ok,
            data: result
        };
    } catch (error) {
        if (showLoading) hideSpinner();
        console.error('Error en fetchAPI:', error);
        return {
            status: 0,
            ok: false,
            data: { detail: error.message }
        };
    }
}

/**
 * Obtener lista de registros
 * @param {string} endpoint - Endpoint API (ej: '/api/hoteles')
 * @param {number} page - Página (comienza en 0)
 * @param {number} limit - Límite de registros por página
 */
async function fetchList(endpoint, page = 0, limit = 10) {
    const url = `${endpoint}?skip=${page * limit}&limit=${limit}`;
    return await fetchAPI('GET', url);
}

/**
 * Obtener un registro por ID
 * @param {string} endpoint - Endpoint API
 * @param {number} id - ID del registro
 */
async function fetchById(endpoint, id) {
    return await fetchAPI('GET', `${endpoint}/${id}`);
}

/**
 * Crear nuevo registro
 * @param {string} endpoint - Endpoint API
 * @param {object} data - Datos del nuevo registro
 */
async function createRecord(endpoint, data) {
    const result = await fetchAPI('POST', endpoint, data);
    
    if (result.ok) {
        showSuccess('Registro creado exitosamente');
    } else {
        const message = result.data.detail || 'Error al crear el registro';
        showError(message);
    }
    
    return result;
}

/**
 * Actualizar registro
 * @param {string} endpoint - Endpoint API
 * @param {number} id - ID del registro
 * @param {object} data - Datos actualizados
 */
async function updateRecord(endpoint, id, data) {
    const result = await fetchAPI('PUT', `${endpoint}/${id}`, data);
    
    if (result.ok) {
        showSuccess('Registro actualizado exitosamente');
    } else {
        const message = result.data.detail || 'Error al actualizar el registro';
        showError(message);
    }
    
    return result;
}

/**
 * Eliminar registro
 * @param {string} endpoint - Endpoint API
 * @param {number} id - ID del registro
 */
async function deleteRecord(endpoint, id, onConfirm) {
    showConfirm(
        '¿Está seguro de que desea eliminar este registro?',
        async () => {
            const result = await fetchAPI('DELETE', `${endpoint}/${id}`);
            
            if (result.ok) {
                showSuccess('Registro eliminado exitosamente');
                if (typeof onConfirm === 'function') {
                    onConfirm();
                }
            } else {
                const message = result.data.detail || 'Error al eliminar el registro';
                showError(message);
            }
        }
    );
}

/**
 * Cargar tabla con registros
 * @param {string} endpoint - Endpoint API
 * @param {string} tableId - ID de la tabla HTML
 * @param {array} columns - Array con nombres de columnas
 * @param {function} renderRow - Función personalizada para renderizar filas
 * @param {number} page - Página actual
 * @param {number} limit - Límite por página
 */
async function loadTable(endpoint, tableId, columns, renderRow = null, page = 0, limit = 10) {
    const result = await fetchList(endpoint, page, limit);
    
    if (!result.ok) {
        showError('Error al cargar los datos');
        return;
    }
    
    const tbody = document.querySelector(`#${tableId} tbody`);
    tbody.innerHTML = '';
    
    const records = result.data;
    
    if (records.length === 0) {
        tbody.innerHTML = `<tr><td colspan="${columns.length}" class="text-center text-muted">No hay registros</td></tr>`;
        return;
    }
    
    records.forEach(record => {
        const tr = document.createElement('tr');
        
        if (typeof renderRow === 'function') {
            tr.innerHTML = renderRow(record);
        } else {
            // Renderizado por defecto
            columns.forEach(col => {
                const td = document.createElement('td');
                const value = getNestedValue(record, col);
                td.textContent = value || '-';
                tr.appendChild(td);
            });
        }
        
        tbody.appendChild(tr);
    });
}

/**
 * Obtener valor anidado de objeto (ej: 'hotel.nombre_hotel')
 */
function getNestedValue(obj, path) {
    return path.split('.').reduce((current, prop) => current?.[prop], obj);
}

/**
 * Llenar select dinámicamente
 * @param {string} endpoint - Endpoint API
 * @param {string} selectId - ID del select
 * @param {string} valueKey - Clave del valor
 * @param {string} labelKey - Clave de la etiqueta
 * @param {string} placeholder - Placeholder opcional
 */
async function populateSelect(endpoint, selectId, valueKey, labelKey, placeholder = null) {
    const result = await fetchList(endpoint, 0, 1000);
    
    const select = document.getElementById(selectId);
    select.innerHTML = '';
    
    if (placeholder) {
        const option = document.createElement('option');
        option.value = '';
        option.textContent = placeholder;
        select.appendChild(option);
    }
    
    if (result.ok && result.data) {
        result.data.forEach(item => {
            const option = document.createElement('option');
            option.value = getNestedValue(item, valueKey);
            option.textContent = getNestedValue(item, labelKey);
            select.appendChild(option);
        });
    }
}

/**
 * Buscar en tabla localmente (sin API)
 * @param {string} inputId - ID del input de búsqueda
 * @param {string} tableId - ID de la tabla
 */
function setupTableSearch(inputId, tableId) {
    const input = document.getElementById(inputId);
    const table = document.getElementById(tableId);
    const rows = table.querySelectorAll('tbody tr');
    
    input.addEventListener('keyup', function() {
        const searchTerm = this.value.toLowerCase();
        
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchTerm) ? '' : 'none';
        });
    });
}

/**
 * Setup de paginación
 * @param {string} endpoint - Endpoint API
 * @param {string} tableId - ID de la tabla
 * @param {array} columns - Columnas de la tabla
 * @param {function} renderRow - Función para renderizar filas
 * @param {number} limit - Registros por página
 */
function setupPagination(endpoint, tableId, columns, renderRow, limit = 10) {
    let currentPage = 0;
    
    const pagination = document.querySelector('.pagination');
    
    window.goToPage = async function(page) {
        if (page < 0) return;
        
        await loadTable(endpoint, tableId, columns, renderRow, page, limit);
        currentPage = page;
        
        // Actualizar botones de paginación
        const items = pagination.querySelectorAll('.pagination-item');
        items.forEach((item, index) => {
            item.classList.remove('active');
            if (index === page) {
                item.classList.add('active');
            }
        });
    };
    
    // Cargar primera página
    goToPage(0);
}

/**
 * Validar y enviar formulario
 * @param {string} formId - ID del formulario
 * @param {string} endpoint - Endpoint API
 * @param {string} method - Método HTTP
 * @param {function} onSuccess - Callback si es exitoso
 */
async function submitForm(formId, endpoint, method = 'POST', onSuccess = null) {
    const form = document.getElementById(formId);
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);
    
    // Convertir valores numéricos
    for (const key in data) {
        if (data[key] === '' || data[key] === null) {
            data[key] = null;
        } else if (!isNaN(data[key]) && data[key] !== '') {
            data[key] = Number(data[key]);
        }
    }
    
    const url = method === 'PUT' ? `${endpoint}/${data.id}` : endpoint;
    const result = await fetchAPI(method, url, data);
    
    if (result.ok) {
        showSuccess(method === 'POST' ? 'Registro creado' : 'Registro actualizado');
        if (typeof onSuccess === 'function') {
            onSuccess();
        }
    } else {
        const message = result.data.detail || 'Error en la operación';
        showError(message);
    }
    
    return result;
}
