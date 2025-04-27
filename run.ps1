try {
    while ($true) {
        Write-Host "Starting program..."
        & "python" "./src/main.py"
        Write-Host "Program exited. Restarting in 2 seconds... Press Ctrl+C to stop."
        Start-Sleep -Seconds 2
    }
}
catch {
    Write-Host "Stopped by user."
    Write-Host "Error details:"
    Write-Host $_  # This shows the error that was caught
}