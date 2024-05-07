# Set the project directory and Virtual Environment name
$venvName = ".venv"
$requirementsFile = "requirements.txt"

# Check if the requirements file exists and is not empty
if (-not (Test-Path $requirementsFile) -or (Get-Content $requirementsFile -Raw) -eq "") {
    Write-Host "Requirements file is missing or empty. Please make sure it exists and contains dependencies."
    exit
}

# Check if the Virtual Environment folder exists
$venvExists = Test-Path $venvName

if (-not $venvExists) {
    # Create Virtual Environment if it doesn't exist
    Write-Host "Creating Virtual Environment..."
    python -m venv $venvName
}

# Activate Virtual Environment if it exists
if ($venvExists) {
    Write-Host "+--------------------------------------------------------------------------------------+"
    Write-Host "Activating Virtual Environment..."
    & .\$venvName\Scripts\Activate.ps1
    Write-Host "+--------------------------------------------------------------------------------------+"
    Write-Host "Virtual Environment activated"
    Write-Host "+--------------------------------------------------------------------------------------+"
} else {
    Write-Host "Virtual Environment does not exist. Please run the script again after creating it."
    exit
}

# Install dependencies
Write-Host "Installing dependencies..."
python -m pip install -r $requirementsFile
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
Write-Host "+--------------------------------------------------------------------------------------+"
Write-Host "All modules installed successfully"
Write-Host "+--------------------------------------------------------------------------------------+"
