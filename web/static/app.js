'use strict';

/* ---------- State ------------------------------------------ */
var allLogs      = [];
var activeFilter = 'all';

/* ---------- DOM Refs --------------------------------------- */
var logInput    = document.getElementById('logInput');
var logList     = document.getElementById('logList');
var filterRow   = document.getElementById('filterRow');
var resCount    = document.getElementById('res-count');
var dropzone    = document.getElementById('dropzone');
var fileIn      = document.getElementById('fileIn');
var classifyBtn = document.getElementById('classifyBtn');
var clearBtn    = document.getElementById('clearBtn');

/* ---------- Classify (calls Flask backend) ----------------- */
async function classifyLogs() {
  var raw = logInput.value.trim();
  if (!raw) return;

  var lines = raw.split('\n').filter(function (l) { return l.trim().length > 0; });

  classifyBtn.disabled    = true;
  classifyBtn.textContent = 'Classifying…';

  try {
    var resp = await fetch('/classify', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ logs: lines })
    });

    if (!resp.ok) {
      throw new Error('Server returned ' + resp.status);
    }

    var data = await resp.json();

    /* Normalise whatever your Flask endpoint returns.
       Supports two common shapes:
         1. { results: [{ text, type }, ...] }
         2. [{ text, type }, ...]                              */
    var results = Array.isArray(data) ? data : data.results;

    allLogs = results.map(function (item, i) {
      return {
        text: item.text  || lines[i] || '',
        type: normaliseType(item.type || item.label || item.level || '')
      };
    });

  } catch (err) {
    showError('Could not reach the classifier: ' + err.message);
    classifyBtn.disabled    = false;
    classifyBtn.textContent = '⚡ Classify';
    return;
  }

  classifyBtn.disabled    = false;
  classifyBtn.textContent = '⚡ Classify';

  activeFilter = 'all';
  resetFilterChips();
  document.querySelector('.filter-chip[data-filter="all"]').classList.add('active-all');
  renderLogs(allLogs);
  updateStats();
  filterRow.style.display = 'flex';
}

/* ---------- Normalise type strings from backend ------------ */
function normaliseType(raw) {
  var u = String(raw).toUpperCase().trim();
  if (u === 'CRITICAL' || u === 'FATAL' || u === 'CRIT') return 'crit';
  if (u === 'ERROR'    || u === 'ERR')                   return 'err';
  if (u === 'WARNING'  || u === 'WARN')                  return 'warn';
  if (u === 'INFO'     || u === 'DEBUG' || u === 'NOTICE') return 'info';
  return 'info'; /* safe default */
}

/* ---------- Rendering -------------------------------------- */
function labelOf(type) {
  return { crit: 'CRITICAL', err: 'ERROR', warn: 'WARNING', info: 'INFO' }[type] || 'INFO';
}

function renderLogs(logs) {
  if (!logs.length) {
    logList.innerHTML =
      '<div class="empty-state">' +
      '  <div class="empty-icon">&#11041;</div>' +
      '  <div class="empty-text">No results for this filter.</div>' +
      '</div>';
    resCount.textContent = '';
    return;
  }

  var html = logs.map(function (l) {
    var ts  = '';
    var msg = escapeHtml(l.text);

    var m = l.text.match(/^(\[[^\]]+\])\s*(.*)/);
    if (m) {
      ts  = '<span class="ts">' + escapeHtml(m[1]) + ' </span>';
      msg = escapeHtml(m[2]);
    }

    return (
      '<div class="log-item ' + l.type + '">' +
      '  <span class="badge ' + l.type + '">' + labelOf(l.type) + '</span>' +
      '  <span class="log-text">' + ts + '<span class="msg">' + msg + '</span></span>' +
      '</div>'
    );
  }).join('');

  logList.innerHTML    = html;
  resCount.textContent = logs.length + ' line' + (logs.length !== 1 ? 's' : '');
}

function updateStats() {
  var counts = { info: 0, warn: 0, err: 0, crit: 0 };
  allLogs.forEach(function (l) { counts[l.type]++; });
  document.getElementById('cnt-info').textContent = counts.info;
  document.getElementById('cnt-warn').textContent = counts.warn;
  document.getElementById('cnt-err').textContent  = counts.err;
  document.getElementById('cnt-crit').textContent = counts.crit;
}

/* ---------- Error Banner ----------------------------------- */
function showError(msg) {
  var existing = document.getElementById('error-banner');
  if (existing) existing.remove();

  var banner = document.createElement('div');
  banner.id = 'error-banner';
  banner.style.cssText = [
    'background:#3a1515',
    'color:#f87171',
    'border:1px solid #7f1d1d',
    'border-radius:8px',
    'padding:10px 14px',
    'font-family:var(--mono)',
    'font-size:12px',
    'margin:0 16px 12px',
    'display:flex',
    'align-items:center',
    'justify-content:space-between'
  ].join(';');

  banner.innerHTML =
    '<span>⚠ ' + escapeHtml(msg) + '</span>' +
    '<button onclick="this.parentElement.remove()" style="background:none;border:none;color:#f87171;cursor:pointer;font-size:16px;line-height:1">×</button>';

  logList.parentElement.insertBefore(banner, logList);
}

/* ---------- Filter ----------------------------------------- */
var filterActiveClasses = {
  all:  'active-all',
  info: 'active-info',
  warn: 'active-warn',
  err:  'active-err',
  crit: 'active-crit'
};

function setFilter(filter, btn) {
  activeFilter = filter;
  resetFilterChips();
  btn.classList.add(filterActiveClasses[filter] || 'active-all');

  var filtered = filter === 'all'
    ? allLogs
    : allLogs.filter(function (l) { return l.type === filter; });

  renderLogs(filtered);
}

function resetFilterChips() {
  document.querySelectorAll('.filter-chip').forEach(function (chip) {
    chip.className = 'filter-chip';
  });
}

/* ---------- Clear ------------------------------------------ */
function clearAll() {
  logInput.value      = '';
  allLogs             = [];
  activeFilter        = 'all';
  filterRow.style.display = 'none';
  resCount.textContent    = '';

  logList.innerHTML =
    '<div class="empty-state">' +
    '  <div class="empty-icon">&#11041;</div>' +
    '  <div class="empty-text">No logs classified yet.<br />Paste logs and hit Classify.</div>' +
    '</div>';

  resetFilterChips();
  document.querySelector('.filter-chip[data-filter="all"]').classList.add('active-all');

  ['info', 'warn', 'err', 'crit'].forEach(function (k) {
    document.getElementById('cnt-' + k).textContent = '0';
  });

  var banner = document.getElementById('error-banner');
  if (banner) banner.remove();
}

/* ---------- File Loading ----------------------------------- */
function loadTextFile(file) {
  if (!file) return;
  var reader = new FileReader();
  reader.onload = function (ev) {
    logInput.value = ev.target.result;
    classifyLogs();
  };
  reader.readAsText(file);
}

/* ---------- Drag & Drop ------------------------------------ */
dropzone.addEventListener('click', function () { fileIn.click(); });

fileIn.addEventListener('change', function (e) {
  loadTextFile(e.target.files[0]);
  fileIn.value = '';
});

dropzone.addEventListener('dragover', function (e) {
  e.preventDefault();
  dropzone.classList.add('drag-over');
});

dropzone.addEventListener('dragleave', function () {
  dropzone.classList.remove('drag-over');
});

dropzone.addEventListener('drop', function (e) {
  e.preventDefault();
  dropzone.classList.remove('drag-over');
  var file = e.dataTransfer.files[0];
  if (file) loadTextFile(file);
});

/* ---------- Button Events ---------------------------------- */
classifyBtn.addEventListener('click', classifyLogs);
clearBtn.addEventListener('click', clearAll);

/* ---------- Filter Chip Events ----------------------------- */
document.querySelectorAll('.filter-chip').forEach(function (chip) {
  chip.addEventListener('click', function () {
    setFilter(chip.dataset.filter, chip);
  });
});

/* ---------- Utility ---------------------------------------- */
function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}