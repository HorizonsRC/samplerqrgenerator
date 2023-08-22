Get-Content .env | foreach {
  $name, $value = $_.split('=')
  if ([string]::IsNullOrWhiteSpace($name) || $name.Contains('#')) {
    continue
  }
  Set-Content env:\$name $value
}

function Find-PythonInstallation {
    $pythonCommandList = @("python", "python2", "python3", "py")
    
    foreach ($command in $pythonCommandList) {
        $pythonExecutable = (Get-Command $command -ErrorAction SilentlyContinue).Source
        if ($pythonExecutable) {
            return $pythonExecutable
        }
    }

    return $null
}

echo "Checking if Python is installed"
$pythonExecutable = Find-PythonInstallation

if ($pythonExecutable) {
    Write-Host "Python is installed. Executable path: $pythonExecutable"
} else {
    Write-Host "Python is not installed."
}

echo "Checking if virtual environment exists"
if (-not (Test-Path -Path $venvPath)) {
  # Create virtual environment
  $pythonExecutable -m venv $env:VENV_PATH
}

echo "Activating the virtual environment"
Activate-VirtualEnvironment

echo "Installing pip requirements"
pip install -r $env:REQUIREMENTS

# Function to activate the virtual environment
function Activate-VirtualEnvironment {
  if (-not (Test-Path -Path "$env:VENV_PATH\Scripts\Activate.ps1")) {
    Write-Host "Virtual environment not found or not set up properly."
    exit 1
  }

  . "$env:VENV_PATH\Scripts\Activate.ps1"
}

# Function to deactivate virtual environment
function Deactivate-VirtualEnvironment {
  if ($ExecutionContent.SessionState.Path.GetUnresolvedProviderPathFromPSPath("$env:VENV_PATH\Scripts\Activate.ps1") -ne $null) {
    Deactivate
  }
}

$pythonCommand = "$pythonExecutable $env:QR_SCRIPT_PATH"

if ($env:LABEL_SIZE || $env:MULTIPLES) {
  $pythonCommand += " -f"
  if ($env:LABEL_SIZE) {
    $pythonCommand += " $env:LABEL_SIZE" }
}

# Create a new FileSystemWatcher instance
$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = (Get-Item $xmlFilePath).Directory.FullName
$watcher.Filter = (Get-Item $xmlFilePath).Name

# Set up the events to watch for
$watcher.NotifyFilter = [System.IO.NotifyFilters]::LastWrite

# Define the event handler function
$lastProcessedTimestamp = $null

$eventHandler = {
    $changeType = $eventArgs.ChangeType
    $timestamp = Get-Date
    Write-Host "$changeType detected at $timestamp, with previous change at $lastProcessedTimestamp"

    # If we have processed an event recently, skip this one
    if ($lastProcessedTimestamp -and ($timestamp - $lastProcessedTimestamp).TotalSeconds -lt 5) {
        Write-Host "Skipping event due to recent processing"
        return
    }

    # Update the last processed timestamp $lastProcessedTimestamp = $timestamp # For example, call your Python script to process the XML file
    # Start-Process python -ArgumentList "your_script.py"
    Write-Host "Processing this one!"
    $pythonExecutable $env:QR_SCRIPT_PATH $env:XML_PATH -f ()
}

# Register the event handler
Register-ObjectEvent -InputObject $watcher -EventName Changed -SourceIdentifier "FileChanged" -Action $eventHandler

# Start watching for changes
$watcher.EnableRaisingEvents = $true

# Wait indefinitely (Ctrl+C to exit)
try {
    while ($true) {
        Start-Sleep -Seconds 1
    }
} finally {
    # Clean up and unregister the event handler
    Unregister-Event -SourceIdentifier "FileChanged"
    $watcher.Dispose()
}
