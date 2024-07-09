# Information Extractor Project - README

## Overview
The Information Extractor project is designed to process a database of medical data, extract key information, and transform it into a more readable and usable format. This system consists of three main components: the Prompt Generator, the Automation System, and the Interpreter System.

## Components

### 1. Prompt Generator
The Prompt Generator is responsible for breaking down the medical database into manageable chunks and transforming these chunks into prompts that can be understood by large language models (LLMs).

**Process:**
- Splits the medical data into chunks.
- Creates a prompt template for each chunk.
- Example prompt: "Create a CSV with the diagnosis based on the symptoms and severity levels listed in the table below. Possible diagnoses are [Malaria, Typhoid Fever, Both, None]. (Chunk[0])."
- Saves the generated prompts into a JSON file.
  
**Technologies Used:**
- `pandas`
- `os`
- `json`

### 2. Automation System
The Automation System takes the generated prompts and inputs them into various LLMs (GPT, Gemini, Perplexity). It then collects the outputs from these models.

**Process:**
- Loads the saved prompts.
- Inputs the prompts into the LLMs.
- Collects and stores the outputs in a JSON file.

**Technologies Used:**
- `pyautogui`
- `pyperclip`

### 3. Interpreter System
The Interpreter System converts the JSON outputs from the Automation System into a more user-friendly format, such as an Excel file.

**Process:**
- Reads the JSON output file.
- Converts the data into an Excel file.

## Usage

### Step-by-Step Guide

1. **CSV Converter**: Run `csv_converter.py` to prepare the initial CSV file.
2. **Prompt Generator**: Run `prompt_generator.py` to generate the prompts and save them as a JSON file.
3. **Main Automation**: Run `main.py` to input the prompts into the LLMs and collect the outputs.
4. **Output Cleaner**: Run `output_cleaner.py` to convert the JSON outputs into an Excel file.

## Development Environment

We use Visual Studio Code (VS Code), a free and versatile coding editor that supports numerous extensions and facilitates quick coding initiation. Our development environment is based on Python, leveraging its powerful libraries for efficient processing.

**Essential Python Packages:**
- `NumPy`
- `Pandas`
- `os`
- `json`
- `re`
- `pyperclip`
- `io`

## Conclusion

This project provides a streamlined system for extracting and interpreting medical data, utilizing the power of LLMs to enhance data readability and usability. By following the provided steps, users can efficiently transform complex medical databases into organized and actionable insights.
