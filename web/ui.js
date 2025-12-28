import { state, elements } from './state.js';

export function setStatus(type, message) {
    elements.status.className = `status-bar ${type}`;
    elements.statusText.textContent = message;
}

export function showErrors(errors) {
    elements.errorList.innerHTML = errors.map(e => `<li>${e}</li>`).join('');
    elements.errorPanel.classList.add('show');
}

export function hideErrors() {
    elements.errorPanel.classList.remove('show');
}

export function checkParameterVisibility(param, currentParams) {
    if (!param.visible_when) return true;
    for (const [condParam, condValue] of Object.entries(param.visible_when)) {
        let actualValue = currentParams[condParam];
        if (actualValue === undefined && state.parameterDefinitions.parameters[condParam]) {
            actualValue = state.parameterDefinitions.parameters[condParam].default;
        }
        if (actualValue !== condValue) return false;
    }
    return true;
}

export function isParameterOutput(param, currentMode) {
    if (!param.is_output) return false;
    return param.is_output[currentMode] === true;
}

export function generateUI(callbacks) {
    const container = elements.parametersContainer;
    const currentParams = callbacks.collectParameters();
    const currentMode = currentParams.instrument_family || 'VIOLIN';

    container.innerHTML = '';
    const categories = state.parameterDefinitions.categories;
    const parameters = state.parameterDefinitions.parameters;

    for (const category of categories) {
        const section = document.createElement('div');
        section.className = 'category-section';

        const title = document.createElement('div');
        title.className = 'category-title';
        title.textContent = category;
        section.appendChild(title);

        for (const [name, param] of Object.entries(parameters)) {
            if (param.category === category) {
                const isVisible = checkParameterVisibility(param, currentParams);
                const isOutput = isParameterOutput(param, currentMode);
                const control = createParameterControl(name, param, isOutput, callbacks);

                if (!isVisible) control.style.display = 'none';
                section.appendChild(control);
            }
        }
        container.appendChild(section);
    }
}

export function createParameterControl(name, param, isOutput, callbacks) {
    const group = document.createElement('div');
    group.className = 'param-group';
    group.dataset.paramName = name;

    if (isOutput) group.classList.add('param-output');

    if (param.type === 'number') {
        const labelDiv = document.createElement('div');
        labelDiv.className = 'param-label';
        const label = document.createElement('label');
        label.textContent = param.label;
        label.htmlFor = name;

        if (isOutput) {
            const indicator = document.createElement('span');
            indicator.className = 'output-indicator';
            indicator.textContent = ' (calculated)';
            label.appendChild(indicator);
        }

        const unit = document.createElement('span');
        unit.className = 'param-unit';
        unit.textContent = param.unit;

        labelDiv.appendChild(label);
        labelDiv.appendChild(unit);
        group.appendChild(labelDiv);

        const input = document.createElement('input');
        input.type = 'number';
        input.id = name;
        input.name = name;
        input.value = param.default;
        input.min = param.min;
        input.max = param.max;
        input.step = param.step;

        if (isOutput) {
            input.readOnly = true;
            input.classList.add('readonly-output');
        } else {
            input.addEventListener('change', hideErrors);
            input.addEventListener('input', callbacks.onInputChange);
        }
        group.appendChild(input);

    } else if (param.type === 'enum') {
        const labelDiv = document.createElement('div');
        labelDiv.className = 'param-label';
        const label = document.createElement('label');
        label.textContent = param.label;
        label.htmlFor = name;
        labelDiv.appendChild(label);
        group.appendChild(labelDiv);

        const select = document.createElement('select');
        select.id = name;
        select.name = name;

        for (const option of param.options) {
            const opt = document.createElement('option');
            opt.value = option.value;
            opt.textContent = option.label;
            if (option.value === param.default) opt.selected = true;
            select.appendChild(opt);
        }

        select.addEventListener('change', hideErrors);
        select.addEventListener('change', callbacks.onEnumChange);
        if (name === 'instrument_family') {
            select.addEventListener('change', () => updateParameterVisibility(callbacks.collectParameters()));
        }
        group.appendChild(select);

    } else if (param.type === 'boolean') {
        const checkboxDiv = document.createElement('div');
        checkboxDiv.className = 'checkbox-group';
        const input = document.createElement('input');
        input.type = 'checkbox';
        input.id = name;
        input.name = name;
        input.checked = param.default;
        input.addEventListener('change', hideErrors);
        input.addEventListener('change', callbacks.onEnumChange);

        const label = document.createElement('label');
        label.textContent = param.label;
        label.htmlFor = name;

        checkboxDiv.appendChild(input);
        checkboxDiv.appendChild(label);
        group.appendChild(checkboxDiv);

    } else if (param.type === 'string') {
        const labelDiv = document.createElement('div');
        labelDiv.className = 'param-label';
        const label = document.createElement('label');
        label.textContent = param.label;
        label.htmlFor = name;
        labelDiv.appendChild(label);
        group.appendChild(labelDiv);

        const input = document.createElement('input');
        input.type = 'text';
        input.id = name;
        input.name = name;
        input.value = param.default;
        input.maxLength = param.max_length || 100;
        input.addEventListener('change', hideErrors);
        input.addEventListener('input', callbacks.onInputChange);
        group.appendChild(input);
    }

    if (param.description) {
        const desc = document.createElement('div');
        desc.className = 'param-description';
        desc.textContent = param.description;
        group.appendChild(desc);
    }

    return group;
}

export function updateParameterVisibility(currentParams) {
    const currentMode = currentParams.instrument_family;

    for (const [name, param] of Object.entries(state.parameterDefinitions.parameters)) {
        const group = document.querySelector(`.param-group[data-param-name="${name}"]`);
        if (!group) continue;

        const isVisible = checkParameterVisibility(param, currentParams);
        group.style.display = isVisible ? '' : 'none';

        if (isVisible) {
            const isOutput = isParameterOutput(param, currentMode);
            const input = document.getElementById(name);
            if (input) {
                input.readOnly = isOutput;
                input.classList.toggle('readonly-output', isOutput);
                group.classList.toggle('param-output', isOutput);

                const label = group.querySelector('label');
                if (label) {
                    const baseText = param.label;
                    label.textContent = isOutput ? `${baseText} (calculated)` : baseText;
                }
            }
        }
    }
}

export function populatePresets() {
    const select = elements.presetSelect;
    select.innerHTML = '<option value="">-- Custom --</option>';
    for (const [id, preset] of Object.entries(state.presets)) {
        const option = document.createElement('option');
        option.value = id;
        option.textContent = preset.name || id.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        select.appendChild(option);
    }
}

export function displayCurrentView() {
    if (!state.views || !state.views[state.currentView]) return;

    if (state.svgCanvas) {
        state.svgCanvas.clear();
        state.svgCanvas.remove();
        state.svgCanvas = null;
    }

    elements.preview.innerHTML = '';

    if (state.currentView === 'dimensions') {
        document.querySelectorAll('.zoom-btn').forEach(btn => {
            btn.disabled = true;
            btn.style.opacity = '0.3';
        });
        elements.preview.innerHTML = state.views[state.currentView];
    } else {
        document.querySelectorAll('.zoom-btn').forEach(btn => {
            btn.disabled = false;
            btn.style.opacity = '1';
        });

        state.svgCanvas = SVG().addTo('#preview-container');
        state.svgCanvas.svg(state.views[state.currentView]);

        const bbox = state.svgCanvas.bbox();
        const containerRect = elements.preview.getBoundingClientRect();
        const padding = Math.min(containerRect.width, containerRect.height) * 0.05;

        const viewBoxConfig = {
            x: bbox.x - padding,
            y: bbox.y - padding,
            width: bbox.width + padding * 2,
            height: bbox.height + padding * 2
        };

        state.svgCanvas.viewbox(viewBoxConfig.x, viewBoxConfig.y, viewBoxConfig.width, viewBoxConfig.height);
        state.initialViewBox = viewBoxConfig;
        state.svgCanvas.panZoom({ zoomMin: 0.1, zoomMax: 20, zoomFactor: 0.3 });
    }

    document.querySelectorAll('.view-tab').forEach(tab => {
        tab.classList.toggle('active', tab.dataset.view === state.currentView);
    });
}

export function generateDimensionsTableHTML(params, derivedValues, derivedFormatted = {}) {
    const categories = state.parameterDefinitions.categories || [];
    const paramDefs = state.parameterDefinitions.parameters || {};

    let html = '<div class="dimensions-table-container"><table class="dimensions-table">';
    html += '<thead><tr><th>Parameter</th><th>Value</th></tr></thead><tbody>';

    for (const category of categories) {
        if (category === 'Display Options') continue;
        html += `<tr><td colspan="2" class="category-header">${category}</td></tr>`;
        for (const [name, param] of Object.entries(paramDefs)) {
            if (param.category !== category) continue;
            const value = params[name];
            let displayValue = value;
            if (param.type === 'number') {
                if (value == null || isNaN(value)) {
                    displayValue = '<span class="param-unit">—</span>';
                } else {
                    let decimals = 1;
                    if (param.step !== undefined) {
                        const stepStr = param.step.toString();
                        const decimalIndex = stepStr.indexOf('.');
                        decimals = decimalIndex !== -1 ? stepStr.length - decimalIndex - 1 : 0;
                    }
                    displayValue = `${value.toFixed(decimals)} <span class="param-unit">${param.unit}</span>`;
                }
            } else if (param.type === 'boolean') {
                displayValue = value ? 'Yes' : 'No';
            } else if (param.type === 'enum') {
                const option = param.options.find(opt => opt.value === value);
                displayValue = option ? option.label : value;
            }
            html += `<tr><td class="param-name">${param.label}</td><td class="param-value">${displayValue}</td></tr>`;
        }
    }

    if (derivedValues && Object.keys(derivedValues).length > 0) {
        const dCategories = new Map();
        for (const [label, value] of Object.entries(derivedValues)) {
            const meta = state.derivedMetadata && state.derivedMetadata[label];
            if (meta && !meta.visible) continue;
            const category = meta ? meta.category : 'Calculated Values';
            if (!dCategories.has(category)) dCategories.set(category, []);
            dCategories.get(category).push({ label, value, meta });
        }
        for (const [category, items] of dCategories) {
            html += `<tr><td colspan="2" class="category-header">${category}</td></tr>`;
            items.sort((a, b) => (a.meta?.order || 999) - (b.meta?.order || 999));
            for (const { label, value, meta } of items) {
                const displayName = meta ? meta.display_name : label;
                let formattedValue;
                if (value == null || isNaN(value)) {
                    formattedValue = '<span class="param-unit">—</span>';
                } else if (derivedFormatted[label]) {
                    const parts = derivedFormatted[label].split(' ');
                    formattedValue = `${parts[0]} <span class="param-unit">${parts.slice(1).join(' ')}</span>`;
                } else if (meta) {
                    formattedValue = `${value.toFixed(meta.decimals)} <span class="param-unit">${meta.unit}</span>`;
                } else {
                    formattedValue = `${value} <span class="param-unit">mm</span>`;
                }
                html += `<tr><td class="param-name">${displayName}</td><td class="param-value">${formattedValue}</td></tr>`;
            }
        }
    }
    return html + '</tbody></table></div>';
}
