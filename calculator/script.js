let currentInput = '0';
let previousInput = '';
let operation = undefined;
let shouldResetScreen = false;
let memory = []; // Changed to array
let historyList = []; // Array to store history objects { expression: string, result: string }
let historyText = '';
let currentMode = 'standard'; // standard | scientific

const currentElement = document.getElementById('current');
const historyElement = document.getElementById('history');
const mcBtn = document.getElementById('mc-btn');
const mrBtn = document.getElementById('mr-btn');
const mListBtn = document.getElementById('m-list-btn');

function updateDisplay() {
    // Format number with commas
    const numberPart = currentInput.split('.')[0];
    const decimalPart = currentInput.includes('.') ? '.' + currentInput.split('.')[1] : '';
    
    // Handle huge numbers or infinity
    if (Math.abs(parseFloat(currentInput)) > 1e16) {
        currentElement.innerText = parseFloat(currentInput).toExponential(10);
    } else {
        const formattedInteger = parseFloat(numberPart).toLocaleString('en-US');
        currentElement.innerText = (numberPart === '' && decimalPart ? '0' : formattedInteger) + decimalPart;
        if (currentInput === '') currentElement.innerText = '0';
        if (isNaN(parseFloat(currentInput)) && currentInput !== '') currentElement.innerText = 'Error';
    }

    historyElement.innerText = historyText;
    
    // Scale font size based on length
    const len = currentElement.innerText.length;
    if (len > 10) {
        currentElement.style.fontSize = '36px'; // Increased
    } else if (len > 14) {
        currentElement.style.fontSize = '28px'; // Increased
    } else {
        currentElement.style.fontSize = '56px'; // Increased match CSS
    }
}

function toggleMemoryList() {
    const overlay = document.getElementById('memory-overlay');
    if (overlay.style.display === 'none') {
        renderMemoryList();
        overlay.style.display = 'flex';
    } else {
        overlay.style.display = 'none';
    }
}

function renderMemoryList() {
    const content = document.getElementById('memory-content');
    content.innerHTML = '';
    
    if (memory.length === 0) {
        const msg = document.createElement('div');
        msg.innerText = 'Memory is empty';
        msg.style.padding = '20px';
        msg.style.textAlign = 'center';
        msg.style.fontSize = '14px';
        msg.style.color = '#a8a8a8';
        content.appendChild(msg);
        return;
    }

    memory.forEach((val, index) => {
        const item = document.createElement('div');
        item.className = 'memory-item';
        
        // Value Display
        const valDiv = document.createElement('div');
        valDiv.className = 'memory-val';
        valDiv.innerText = Number(val).toLocaleString('en-US');
        valDiv.onclick = () => {
            currentInput = String(val);
            shouldResetScreen = true;
            updateDisplay();
        };

        // Actions Container
        const actionsDiv = document.createElement('div');
        actionsDiv.className = 'memory-actions';

        // M+ Button
        const btnPlus = document.createElement('button');
        btnPlus.className = 'memory-action-btn';
        btnPlus.innerText = 'M+';
        btnPlus.onclick = (e) => {
            e.stopPropagation();
            const curr = parseFloat(currentInput || 0);
            memory[index] += curr;
            renderMemoryList(); 
        };

        // M- Button
        const btnMinus = document.createElement('button');
        btnMinus.className = 'memory-action-btn';
        btnMinus.innerText = 'M-';
        btnMinus.onclick = (e) => {
            e.stopPropagation();
            const curr = parseFloat(currentInput || 0);
            memory[index] -= curr;
            renderMemoryList(); 
        };

        // MC (Delete) Button
        const btnMC = document.createElement('button');
        btnMC.className = 'memory-action-btn';
        btnMC.innerHTML = '&#128465;'; // Trash can icon
        btnMC.onclick = (e) => {
            e.stopPropagation();
            memory.splice(index, 1);
            renderMemoryList();
            updateMemoryButtons(); // Handle empty state if needed
        };

        actionsDiv.appendChild(btnPlus);
        actionsDiv.appendChild(btnMinus);
        actionsDiv.appendChild(btnMC);

        item.appendChild(valDiv);
        item.appendChild(actionsDiv);
        
        content.appendChild(item);
    });
}

function updateMemoryButtons() {
    const hasMemory = memory.length > 0;
    mcBtn.disabled = !hasMemory;
    mrBtn.disabled = !hasMemory;
    mListBtn.disabled = !hasMemory;
    
    if (!hasMemory) {
        document.getElementById('memory-overlay').style.display = 'none';
    } else {
        if (document.getElementById('memory-overlay').style.display === 'flex') {
            renderMemoryList();
        }
    }
}



function appendNumber(number) {
    if (shouldResetScreen) {
        resetScreen();
    }
    if (number === '.' && currentInput.includes('.')) return;
    if (currentInput === '0' && number !== '.') {
        currentInput = number;
    } else {
        currentInput += number;
    }
    updateDisplay();
}

function resetScreen() {
    currentInput = '';
    shouldResetScreen = false;
    // Clear history if we are starting a new calculation chain (not just entering 2nd operand)
    if (operation === undefined) {
        historyText = '';
    }
}

function clearAll() {
    currentInput = '0';
    previousInput = '';
    operation = undefined;
    historyText = '';
    updateDisplay();
}

function clearEntry() {
    currentInput = '0';
    updateDisplay();
}

function backspace() {
    if (shouldResetScreen) {
        historyText = ''; 
        updateDisplay(); 
        return;
    }
    if (currentInput.length === 1 || currentInput === 'Error') {
        currentInput = '0';
    } else {
        currentInput = currentInput.slice(0, -1);
    }
    updateDisplay();
}

function toggleSign() {
    if (currentInput === '0') return;
    currentInput = String(parseFloat(currentInput) * -1);
    updateDisplay();
}

function oneOverX() {
    const current = parseFloat(currentInput);
    if (current === 0) {
        currentInput = 'Cannot divide by zero';
    } else {
        historyText = `1/(${current})`;
        currentInput = String(1 / current);
        shouldResetScreen = true;
    }
    updateDisplay();
}

function square() {
    const current = parseFloat(currentInput);
    historyText = `sqr(${current})`;
    currentInput = String(current * current);
    shouldResetScreen = true;
    updateDisplay();
}

function squareRoot() {
    const current = parseFloat(currentInput);
    if (current < 0) {
        currentInput = 'Invalid Input';
    } else {
        historyText = `√(${current})`;
        currentInput = String(Math.sqrt(current));
    }
    shouldResetScreen = true;
    updateDisplay();
}

function appendOperator(op) {
    if (operation !== undefined && !shouldResetScreen) {
        calculate();
    }
    
    // Case where we just calculated, but now use result as prev
    operation = op;
    previousInput = currentInput;
    
    const symbol = op === '*' ? '×' : op === '/' ? '÷' : op === '-' ? '−' : '+';
    historyText = `${parseFloat(previousInput)} ${symbol}`;
    
    shouldResetScreen = true;
    updateDisplay();
}

function calculate() {
    if (operation === undefined) return;
    
    const prev = parseFloat(previousInput);
    const current = parseFloat(currentInput);
    
    if (isNaN(prev) || isNaN(current)) return;
    
    let computation;
    switch (operation) {
        case '+': computation = prev + current; break;
        case '-': computation = prev - current; break;
        case '*': computation = prev * current; break;
        case '/': computation = prev / current; break;
        case 'pow': computation = Math.pow(prev, current); break;
        case 'mod': computation = prev % current; break;
        case 'exp': computation = prev * Math.pow(10, current); break; // Scientific notation logic
        default: return;
    }
    
    let symbol = operation;
    if (operation === '*') symbol = '×';
    else if (operation === '/') symbol = '÷';
    else if (operation === '-') symbol = '−';
    else if (operation === 'pow') symbol = '^';
    else if (operation === 'mod') symbol = 'mod';
    else if (operation === 'exp') symbol = 'e';
    
    // History update
    historyText = `${prev} ${symbol} ${current} =`;
    
    // Add to history list
    addToHistory(`${prev} ${symbol} ${current}`, computation);

    currentInput = String(computation);
    operation = undefined;
    shouldResetScreen = true;
    updateDisplay();
}

// Replaces the first weak definition of mathFunc to avoid conflict
// The actual robust definition is at the bottom of the file


function addToHistory(expression, result) {
    historyList.unshift({ expression: expression, result: result });
    // If history is open, refresh it? Or just let it update next time.
    // Let's render if open?
    if (document.getElementById('history-overlay').style.display === 'flex') {
        renderHistoryList();
    }
}

function toggleHistoryList() {
    const overlay = document.getElementById('history-overlay');
    const memOverlay = document.getElementById('memory-overlay');
    
    // Close memory if open
    if (memOverlay.style.display === 'flex') memOverlay.style.display = 'none';

    if (overlay.style.display === 'none') {
        renderHistoryList();
        overlay.style.display = 'flex';
    } else {
        overlay.style.display = 'none';
    }
}

function clearHistory() {
    historyList = [];
    renderHistoryList();
}

function renderHistoryList() {
    const content = document.getElementById('history-content');
    content.innerHTML = '';
    
    if (historyList.length === 0) {
        const msg = document.createElement('div');
        msg.innerText = 'There\'s no history yet';
        msg.style.padding = '20px';
        msg.style.textAlign = 'center';
        msg.style.fontSize = '14px';
        msg.style.color = '#a8a8a8';
        content.appendChild(msg);
        return;
    }

    historyList.forEach((item) => {
        const historyItem = document.createElement('div');
        historyItem.className = 'history-item';
        
        const exprDiv = document.createElement('div');
        exprDiv.className = 'history-expression';
        exprDiv.innerText = item.expression + ' =';
        
        const resDiv = document.createElement('div');
        resDiv.className = 'history-result';
        resDiv.innerText = Number(item.result).toLocaleString('en-US');

        historyItem.onclick = () => {
            currentInput = String(item.result);
            historyText = ''; 
            shouldResetScreen = true;
            updateDisplay();
            document.getElementById('history-overlay').style.display = 'none';
        };

        historyItem.appendChild(exprDiv);
        historyItem.appendChild(resDiv);
        content.appendChild(historyItem);
    });
}

// Memory Functions
function memoryClear() { 
    memory = []; 
    updateMemoryButtons(); 
}

function memoryRecall() { 
    if (memory.length > 0) {
        currentInput = String(memory[0]); 
        shouldResetScreen = true; 
        updateDisplay(); 
    }
}

function memoryAdd() { 
    if (memory.length === 0) {
        memory.unshift(parseFloat(currentInput || 0));
    } else {
        memory[0] += parseFloat(currentInput || 0); 
    }
    shouldResetScreen = true; 
    updateMemoryButtons(); 
}

function memorySubtract() { 
    if (memory.length === 0) {
        memory.unshift(-parseFloat(currentInput || 0));
    } else {
        memory[0] -= parseFloat(currentInput || 0); 
    }
    shouldResetScreen = true; 
    updateMemoryButtons(); 
}

function memoryStore() { 
    memory.unshift(parseFloat(currentInput || 0)); 
    shouldResetScreen = true; 
    updateMemoryButtons(); 
}

document.addEventListener('click', (event) => {
    const memOverlay = document.getElementById('memory-overlay');
    const histOverlay = document.getElementById('history-overlay');
    const mListBtn = document.getElementById('m-list-btn');
    const historyBtn = document.querySelector('.history-icon');

    // Close Memory Overlay
    if (memOverlay.style.display === 'flex' && 
        !memOverlay.contains(event.target) && 
        !mListBtn.contains(event.target)) {
        memOverlay.style.display = 'none';
    }

    // Close History Overlay
    if (histOverlay.style.display === 'flex' &&
        !histOverlay.contains(event.target) &&
        !historyBtn.contains(event.target)) {
        histOverlay.style.display = 'none';
    }
});

document.addEventListener('keydown', (event) => {
    if ((event.key >= 0 && event.key <= 9) || event.key === '.') appendNumber(event.key);
    if (event.key === '=' || event.key === 'Enter') {
        event.preventDefault(); calculate();
    }
    if (event.key === 'Backspace') backspace();
    if (event.key === 'Escape') clearAll();
    if (event.key === '+' || event.key === '-' || event.key === '*' || event.key === '/') appendOperator(event.key);
});

/* Mode Switching */
function toggleCalculatorMode() {
    if (currentMode === 'standard') {
        switchMode('scientific');
    } else {
        switchMode('standard');
    }
}

function switchMode(mode) {
    currentMode = mode;
    resetScreen();
    clearAll();
    
    // Update Title
    const titleEl = document.getElementById('mode-title');
    if(titleEl) titleEl.innerText = mode.charAt(0).toUpperCase() + mode.slice(1);
    
    // Toggle Keypads
    const stdPad = document.querySelector('.keypad:not(.scientific)'); // The one without .scientific class
    const sciPad = document.getElementById('scientific-keypad');
    
    if (mode === 'scientific') {
        if(stdPad) stdPad.style.display = 'none';
        
        // Show Toolbar
        const tb = document.getElementById('sci-toolbar');
        if(tb) tb.style.display = 'flex';

        if(sciPad) {
            sciPad.style.display = 'grid';
            // Move overlays to sci keypad to ensure positioning is correct relative to parent
            const memOverlay = document.getElementById('memory-overlay');
            const histOverlay = document.getElementById('history-overlay');
            if(memOverlay) sciPad.insertBefore(memOverlay, sciPad.firstChild);
            if(histOverlay) sciPad.insertBefore(histOverlay, sciPad.firstChild);
        }
        // Resize window request?? No, user can resize.
    } else {
        if(stdPad) {
            stdPad.style.display = 'grid';
            // Move overlays back
            const memOverlay = document.getElementById('memory-overlay');
            const histOverlay = document.getElementById('history-overlay');
            if(memOverlay) stdPad.insertBefore(memOverlay, stdPad.firstChild);
            if(histOverlay) stdPad.insertBefore(histOverlay, stdPad.firstChild);
        }
        if(sciPad) sciPad.style.display = 'none';

        // Hide Toolbar
        const tb = document.getElementById('sci-toolbar');
        if(tb) tb.style.display = 'none';
    }
}

function unimplemented(feature) {
    alert(feature + ' not implemented yet!');
}

/* 
   Old duplicate mathFunc was here. 
   Removed to prefer the unified function at the bottom.
*/

function factorial() {
    const n = parseInt(currentInput);
    if (isNaN(n)) return;
    
    if (n < 0) {
        currentInput = 'Invalid Input';
        return;
    }
    // Limit to reasonable number to prevent freeze
    if (n > 170) {
        currentInput = 'Infinity';
        shouldResetScreen = true;
        updateDisplay();
        return;
    }

    let res = 1;
    for(let i=1; i<=n; i++) res *= i;
    currentInput = String(res);
    historyText = `fact(${n})`;
    shouldResetScreen = true;
    updateDisplay();
}


// Unified mathFunc
function mathFunc(funcName) {
    if (funcName === 'PI') {
        currentInput = String(Math.PI);
        shouldResetScreen = true;
        updateDisplay();
        return;
    }
    if (funcName === 'E') {
        currentInput = String(Math.E);
        shouldResetScreen = true;
        updateDisplay();
        return;
    }

    const current = parseFloat(currentInput);
    if(isNaN(current)) return;
    
    let res = 0;
    let name = funcName;
    
    if (funcName === 'log10') { res = Math.log10(current); name = 'log'; }
    else if (funcName === 'log') { res = Math.log(current); name = 'ln'; }
    else if (funcName === '10x') { res = Math.pow(10, current); name = '10^'; }
    else if (funcName === 'abs') { res = Math.abs(current); name = 'abs'; }
    
    historyText = `${name}(${current})`;
    currentInput = String(res);
    shouldResetScreen = true;
    updateDisplay();
}


function mathTrig(funcName) {
    const current = parseFloat(currentInput);
    if(isNaN(current)) return;
    let res = 0;
    if (funcName === 'sin') res = Math.sin(current); 
    if (funcName === 'cos') res = Math.cos(current);
    if (funcName === 'tan') res = Math.tan(current);
    
    // Check for precision issues close to 0
    if (Math.abs(res) < 1e-15) res = 0;

    historyText = `${funcName}(${current})`;
    currentInput = String(res);
    shouldResetScreen = true;
    updateDisplay();
}


function toggleTrigMenu() {
    const popup = document.getElementById('trig-popup');
    popup.classList.toggle('open');
    // Simple click outside implementation
    if (popup.classList.contains('open')) {
        setTimeout(() => {
            document.addEventListener('click', closeTrigMenuOutside);
        }, 0);
    }
}

function closeTrigMenuOutside(event) {
    const popup = document.getElementById('trig-popup');
    if (!popup.contains(event.target) && !event.target.closest('.sci-toolbar-btn')) {
        popup.classList.remove('open');
        document.removeEventListener('click', closeTrigMenuOutside);
    }
}

// Ensure mathTrig closes menu
// Wrap mathTrig to close menu?
const originalMathTrig = mathTrig;
mathTrig = function(funcName) {
    originalMathTrig(funcName);
    document.getElementById('trig-popup').classList.remove('open');
}



// Initialize with default mode
document.addEventListener('DOMContentLoaded', () => {
    switchMode(currentMode);
});

