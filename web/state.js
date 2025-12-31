// Global state management
export const state = {
    pyodide: null,
    isGenerating: false,
    views: null,              // Stores all 3 SVG views + dimensions table
    currentView: 'side',      // Currently displayed view (default to side)
    svgCanvas: null,          // SVG.js canvas for zoom/pan
    initialViewBox: null,     // Initial viewBox for zoom reset
    parameterDefinitions: null,
    presets: null,
    derivedValues: null,      // Stores calculated derived values
    derivedMetadata: null,    // Stores metadata for derived values
    derivedFormatted: null    // Stores formatted derived values from backend
};

// Make state available globally for libraries like pdf-export that might still need it in transition
window.state = state;

export const elements = {
    status: document.getElementById('status'),
    statusText: document.getElementById('status-text'),
    genBtn: document.getElementById('gen-btn'),
    preview: document.getElementById('preview-container'),
    errorPanel: document.getElementById('error-panel'),
    errorList: document.getElementById('error-list'),
    parametersContainer: document.getElementById('parameters-container'),
    presetSelect: document.getElementById('preset'),
    viewTabs: document.getElementById('view-tabs'),
    zoomControls: document.getElementById('zoom-controls'),
    dlSvg: document.getElementById('dl-svg'),
    dlPdf: document.getElementById('dl-pdf'),
    calculatedFields: document.getElementById('calculated-fields'),
    saveParamsBtn: document.getElementById('save-params-btn'),
    loadParamsBtn: document.getElementById('load-params-btn'),
    loadParamsInput: document.getElementById('load-params-input'),
    zoomInBtn: document.getElementById('zoom-in'),
    zoomOutBtn: document.getElementById('zoom-out'),
    zoomResetBtn: document.getElementById('zoom-reset')
};
