/**
 * Constants used across the web application.
 *
 * Centralizes magic numbers and configuration values for easier maintenance
 * and consistent behavior across the application.
 */

// Debounce timing (milliseconds)
export const DEBOUNCE_GENERATE = 500;  // Delay before auto-generating on input change
export const DEBOUNCE_INPUT = 300;    // Delay for input field changes

// Responsive breakpoints (pixels)
export const MOBILE_BREAKPOINT = 1024;  // Width below which mobile layout applies

// Zoom configuration
export const ZOOM_CONFIG = {
    min: 0.1,      // Minimum zoom level
    max: 20,       // Maximum zoom level
    factor: 1.3    // Multiplier for zoom in/out operations
};

// View names mapping
export const VIEW_NAMES = {
    side: 'Side View',
    top: 'Top View',
    cross_section: 'Cross-Section',
    dimensions: 'Dimensions',
    fret_positions: 'Fret Positions',
    radius_template: 'Radius Template'
};

// File download MIME types
export const MIME_TYPES = {
    svg: 'image/svg+xml',
    json: 'application/json',
    pdf: 'application/pdf'
};

// UI timing
export const AUTO_GENERATE_DELAY = 500;  // ms before auto-generating after input

// PDF export formats
export const PDF_FORMATS = {
    a4: { name: 'a4', width: 210, height: 297 },
    letter: { name: 'letter', width: 215.9, height: 279.4 },
    a3: { name: 'a3', width: 297, height: 420 }
};

// Button states
export const BUTTON_OPACITY = {
    enabled: '1',
    disabled: '0.3'
};
