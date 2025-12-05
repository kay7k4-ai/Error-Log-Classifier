const themeToggle = document.getElementById("themeToggle");
const dropArea = document.getElementById("dropArea");
const fileInput = document.getElementById("fileInput");
const fileName = document.getElementById("fileName");

/* ---------------------------------
   THEME TOGGLE
----------------------------------*/
themeToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark");
    themeToggle.textContent = document.body.classList.contains("dark") ? "☀️" : "🌙";
});

/* ---------------------------------
   CLICK ON DROP AREA → OPEN FILE
----------------------------------*/
dropArea.addEventListener("click", () => {
    fileInput.click();
});

/* ---------------------------------
   WHEN FILE IS SELECTED
----------------------------------*/
fileInput.addEventListener("change", () => {
    if (fileInput.files.length > 0) {
        fileName.textContent = fileInput.files[0].name;
    }
});

/* ---------------------------------
   DRAG & DROP HANDLING
----------------------------------*/
dropArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropArea.classList.add("active");
});

dropArea.addEventListener("dragleave", () => {
    dropArea.classList.remove("active");
});

dropArea.addEventListener("drop", (e) => {
    e.preventDefault();
    dropArea.classList.remove("active");

    if (e.dataTransfer.files.length > 0) {
        fileInput.files = e.dataTransfer.files;
        fileName.textContent = e.dataTransfer.files[0].name;
    }
});

// CLEAR BUTTON
const clearBtn = document.getElementById("clearBtn");
const pasteBox = document.getElementById("pasteBox");
const resultBox = document.querySelector(".result-box");

clearBtn.addEventListener("click", () => {
    pasteBox.value = "";
    fileInput.value = "";
    fileName.textContent = "No file selected";

    if (resultBox) resultBox.innerHTML = "<div class='empty'>No logs classified yet.</div>";
});
