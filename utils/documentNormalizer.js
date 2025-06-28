/**
 * Utilidades para normalizar números de documento
 */

/**
 * Normaliza un número de documento removiendo guiones, espacios y puntos
 * @param {string} documentNumber - Número de documento a normalizar
 * @returns {string} - Número de documento normalizado
 */
export function normalizeDocumentNumber(documentNumber) {
    if (!documentNumber) return "";
    
    // Remover guiones, espacios, puntos y otros caracteres especiales
    return documentNumber.replace(/[^a-zA-Z0-9]/g, '');
}

/**
 * Formatea un número de documento para mostrar (agrega guiones)
 * @param {string} documentNumber - Número de documento normalizado
 * @param {string} format - Formato deseado ('dashed', 'dotted', 'none')
 * @returns {string} - Número de documento formateado
 */
export function formatDocumentNumber(documentNumber, format = 'dashed') {
    if (!documentNumber) return "";
    
    const normalized = normalizeDocumentNumber(documentNumber);
    
    switch (format) {
        case 'dashed':
            // Formato: XX-XXX-XXX-X para cédulas de 10 dígitos
            if (normalized.length === 10) {
                return `${normalized.slice(0, 2)}-${normalized.slice(2, 5)}-${normalized.slice(5, 8)}-${normalized.slice(8)}`;
            }
            // Formato: XX-XXX-XXX para cédulas de 8 dígitos
            else if (normalized.length === 8) {
                return `${normalized.slice(0, 2)}-${normalized.slice(2, 5)}-${normalized.slice(5)}`;
            }
            return normalized;
            
        case 'dotted':
            // Formato: XX.XXX.XXX-X para cédulas de 10 dígitos
            if (normalized.length === 10) {
                return `${normalized.slice(0, 2)}.${normalized.slice(2, 5)}.${normalized.slice(5, 8)}-${normalized.slice(8)}`;
            }
            // Formato: XX.XXX.XXX para cédulas de 8 dígitos
            else if (normalized.length === 8) {
                return `${normalized.slice(0, 2)}.${normalized.slice(2, 5)}.${normalized.slice(5)}`;
            }
            return normalized;
            
        case 'none':
        default:
            return normalized;
    }
}

/**
 * Valida si un número de documento tiene el formato correcto
 * @param {string} documentNumber - Número de documento a validar
 * @returns {boolean} - True si es válido
 */
export function isValidDocumentNumber(documentNumber) {
    if (!documentNumber) return false;
    
    const normalized = normalizeDocumentNumber(documentNumber);
    
    // Validar que solo contenga números y tenga longitud válida
    return /^\d{8,10}$/.test(normalized);
}

/**
 * Hook de React para manejar documentos en formularios
 */
export function useDocumentNumber() {
    const [value, setValue] = useState('');
    const [displayValue, setDisplayValue] = useState('');
    
    const handleChange = (newValue) => {
        const normalized = normalizeDocumentNumber(newValue);
        setValue(normalized);
        setDisplayValue(formatDocumentNumber(normalized, 'dashed'));
    };
    
    const handleBlur = () => {
        // Al perder el foco, mostrar formato con guiones
        setDisplayValue(formatDocumentNumber(value, 'dashed'));
    };
    
    const handleFocus = () => {
        // Al ganar el foco, mostrar sin formato para facilitar edición
        setDisplayValue(value);
    };
    
    return {
        value,
        displayValue,
        handleChange,
        handleBlur,
        handleFocus,
        isValid: isValidDocumentNumber(value)
    };
} 