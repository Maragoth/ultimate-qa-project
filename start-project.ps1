# Run this script to start DB (Docker), Backend API, and Frontend:
# PS> ./start-project.ps1

# Start DB via Docker with persistent volume
Write-Output "Starting PostgreSQL Docker container..."
docker start conduit-db 2>$null | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Output "Container not found. Running new one with volume..."
    docker run --name conduit-db -e POSTGRES_PASSWORD=postgres -p 5432:5432 -v conduit-db-data:/var/lib/postgresql/data -d postgres
}

# Start Backend API (new PowerShell window)
Write-Output "Starting Backend API..."
Start-Process powershell -ArgumentList "cd node-express-realworld-example-app; npx nx serve api"

# Wait for backend to boot
Start-Sleep -Seconds 5

# Start Frontend (new PowerShell window)
Write-Output "Starting Frontend..."
Start-Process powershell -ArgumentList "cd react-redux-realworld-example-app; npm start"

Write-Output "✅ All services are starting up!"
