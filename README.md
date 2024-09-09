# Swagger Pet Store API Test Automation

## Overview

This repository provides a test automation framework for the **Swagger Pet Store API**. It uses **Behave**, a BDD framework, to define and execute test cases for various CRUD operations on pets, as well as image uploads.

## Features

- **CRUD Operations:**
  - Create a new pet
  - Failed to create a new pet
  - Update pet details (via JSON and form data)
  - Fetch pet by status
  - Delete a pet
- **Image Upload:**
  - Upload images for pets

## Project Structure

* features: comprise of feature files for PET store pet endpoint tests
* steps: step defs from behave to python glue
* reusables: base and asserts library for reusability and base test class to inherit
* environment.py: file for before and after hooks
* behave.ini: configuration for behave
* test_data: keeping test data file(s)s



## Setup Instructions

1. Clone the repository
  ```bash
  git clone https://github.com/rajeshkumargit/python-petstore-apitests.git
  ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
    ```
3. Run tests
   ```bash
   behave --junit --junit-directory reports
   ```

## Github Actions

1. For CI Run, please navigate to Github actions tab of the github repo: https://github.com/rajeshkumargit/python-petstore-apitests.git
2. Run the build by committing to the branch or by manually clicking on the **Run Workflow** button
3. View the steps in the build log
4. Click on Summary tab to view detailed test results
