# Error-Log-Classifier
A Python-based project to automatically classify error logs
# OJT Project – Error Log Classification (Python)

## 📌 Project Overview
This project focuses on building a Python-based system that can automatically classify error logs.  
The goal is to understand how errors are generated, captured, structured, and processed so that they can later be used for classification and analysis.

---

# 🗓 Day 1 – Project Setup & Understanding

### ✔ 1. Project Initialization
- Reviewed the PRD (Project Requirement Document)
- Understood the main objective: **automatic error log classification**
- Set up the project folder and environment

### ✔ 2. Repository Setup
- Created/Joined GitHub repository
- Set up VS Code environment and basic workspace

### ✔ 3. Basic Research
- Explored what error logs contain:
  - Exception type  
  - Message  
  - Stack trace  
- Understood why log classification is important (debugging, automation, error grouping)

**Summary:**  
Day 1 focused on understanding the scope of the project and preparing the development environment.

---

# 🗓 Day 2 – Error Generation, Logging & Debugging Foundation

### ✔ 1. Generated Controlled Runtime Errors
Created a Python script that intentionally triggers an error (IndexError).  
Purpose: Learn how real-world errors appear before classification.

### ✔ 2. Logged the Error Into a File
- Extracted full traceback
- Stored details into a `.log` file
- Observed how error logs are structured in text format  
This is the raw input that will later be classified by the system.

### ✔ 3. Debugging Using VS Code
- Used breakpoints  
- Inspected call stack and variables  
- Understood how Python executes code and where errors occur  

### ✔ 4. Implemented a Fixed Version
Created a second script with validation logic to prevent the error.  
This helps understand:
- error handling
- boundary checks
- safe coding practices

### ✔ 5. Documentation & Evidence
- Organized files under the `day2/` folder  
- Saved screenshots of:
  - Terminal error output  
  - Debugger paused view  
  - Correct output after fixing  

**Summary:**  
Day 2 was about building the foundation for the main project by learning how errors are created, logged, and analyzed.  
This prepares the data pipeline needed for future classification tasks.

---

# 📁 Project Structure (so far)

