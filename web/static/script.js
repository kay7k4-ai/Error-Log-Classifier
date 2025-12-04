const themeToggle = document.getElementById("themeToggle");
const dropArea = document.getElementById("dropArea");
const fileInput = document.getElementById("fileInput");
const fileName = document.getElementById("fileName");

/* THEME TOGGLE */
themeToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark");
    themeToggle.textContent = document.body.classList.contains("dark") ? "☀️" : "🌙";
});

/* DRAG & DROP */
dropArea.addEventListener("click", () => fileInput.click());

fileInput.addEventListener("change", () => {
    if (fileInput.files.length > 0) {
        fileName.textContent = fileInput.files[0].name;
    }
});

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
