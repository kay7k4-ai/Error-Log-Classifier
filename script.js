const modeToggle = document.getElementById('modeToggle');
const body = document.body;

// Load saved theme on page load
if (localStorage.getItem('theme') === 'dark') {
  body.classList.add('dark-mode');
  modeToggle.textContent = '☀️ Light Mode';
}

modeToggle.addEventListener('click', () => {
  body.classList.toggle('dark-mode');
  if (body.classList.contains('dark-mode')) {
    modeToggle.textContent = '☀️ Light Mode';
    localStorage.setItem('theme', 'dark');
  } else {
    modeToggle.textContent = '🌙 Dark Mode';
    localStorage.setItem('theme', 'light');
  }
});

function classifyLog() {
  const fileInput = document.getElementById('logfile');
  const textArea = document.getElementById('logtext');
  const resultDiv = document.getElementById('results');

  let logData = '';

  if (textArea.value.trim()) {
    logData = textArea.value.trim();
    processLogs(logData, resultDiv);
  } else if (fileInput.files.length) {
    const file = fileInput.files[0];
    const reader = new FileReader();
    reader.onload = function(e) {
      logData = e.target.result;
      processLogs(logData, resultDiv);
    };
    reader.readAsText(file);
  } else {
    alert('Please upload a log file or write/paste logs before classification.');
  }
}

function processLogs(logData, resultDiv) {
  const lines = logData.split('\n').slice(0, 15);
  const highlighted = lines.map(line => {
    if (/error/i.test(line)) {
      return `<span class="error-highlight">${line}</span>`;
    } else if (/warn/i.test(line)) {
      return `<span class="warning-highlight">${line}</span>`;
    }
    return line;
  });
  resultDiv.innerHTML = highlighted.join('<br/>') + '\n\n[Your classified results will appear here after backend integration]';
}
