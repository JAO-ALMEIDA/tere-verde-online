param(
    [string]$PythonVersion = "3.12"
)

Write-Host "[1/6] Verificando Python $PythonVersion e Git..." -ForegroundColor Cyan
try {
    py -0p | Out-Null
} catch {
    Write-Host "Instalando Python $PythonVersion via winget..." -ForegroundColor Yellow
    winget install --id Python.Python.$PythonVersion --source winget -e --accept-package-agreements --accept-source-agreements | Out-Null
}

try {
    git --version | Out-Null
} catch {
    Write-Host "Instalando Git via winget..." -ForegroundColor Yellow
    winget install --id Git.Git --source winget -e --accept-package-agreements --accept-source-agreements | Out-Null
}

Write-Host "[2/6] Ajustando política de execução (CurrentUser -> RemoteSigned)..." -ForegroundColor Cyan
try {
    Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force | Out-Null
} catch {
    Write-Warning "Não foi possível alterar a ExecutionPolicy automaticamente. Rode como usuário com permissão ou ajuste manualmente."
}

Write-Host "[3/6] Criando ambiente virtual com Python $PythonVersion..." -ForegroundColor Cyan
if (Test-Path .venv) {
    Write-Host "Removendo venv anterior..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force .venv
}

py -$PythonVersion -m venv .venv

if (-not (Test-Path .\.venv\Scripts\Activate.ps1)) {
    throw "Falha ao criar o venv. Verifique se o Python $PythonVersion está instalado."
}

. .\.venv\Scripts\Activate.ps1

Write-Host "Python em uso:" -NoNewline; python -V

Write-Host "[4/6] Atualizando pip e instalando dependências..." -ForegroundColor Cyan
python -m pip install --upgrade pip
pip install -r requirements.txt

Write-Host "[5/6] Inicializando banco e populando dados..." -ForegroundColor Cyan
python -m src.app.cli init-db
python -m src.app.cli seed

Write-Host "[6/6] Iniciando aplicação (http://localhost:5000)..." -ForegroundColor Cyan
python run.py


