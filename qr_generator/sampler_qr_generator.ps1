function Find-PythonInstallation {
    $pythonCommandList = @("python", "python2", "python3", "py")
    $pythonInstalled = $false
    # Test if the Python command is available in the system
    # if (Test-Path (Get-Command $pythonCommand -ErrorAction SilentlyContinue)) {
    #     # Check if the Python version matches the expected version
    #     $pythonVersionOutput = & $pythonCommand --version 2>&1
    #     if ($pythonVersionOutput -match "Python $pythonVersion") {
    #         $pythonInstalled = $true
    #     }
    # }
    foreach ($command in $pythonCommandList) {
      <# $itemj is the current item #>
      if (Test-Path (Get-Command $command -ErrorAction SilentlyContinue)) {
          # Check if the Python version matches the expected version
          $pythonVersionOutput = & $command --version 2>&1
          if ($pythonVersionOutput -match "Python $pythonVersion") {
              $pythonInstalled = $command
              Write-Host "Python is installed"
              Write-Host $pythonVersionOutput
              Write-Host $command
          }
      }
    }

    return $pythonInstalled
}


# Check if Python 3 is installed
$pythonInstalled = Find-PythonInstallation
