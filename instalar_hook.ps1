# instalar_hook.ps1
# Ejecutar una sola vez para instalar el pre-commit hook.
# Desde la raíz del proyecto: .\instalar_hook.ps1

$origen = ".git_hooks\pre-commit"
$destino = ".git\hooks\pre-commit"

Copy-Item $origen $destino -Force
Write-Host ""
Write-Host "Pre-commit hook instalado correctamente." -ForegroundColor Green
Write-Host "   Ahora cada 'git commit' ejecutará los tests automáticamente." -ForegroundColor Cyan
Write-Host ""
