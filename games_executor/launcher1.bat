@echo off

REM Configurazione parametri
set NUM_TESTS=5
set H_FLAGS=grey b/w

REM Percorsi
set SERVER_PATH=%cd%\..\Test
set PLAYER_PATH=%SERVER_PATH%\..\LoDaLe_tablut

REM Svuota o crea la cartella Test/outputs
set OUTPUTS_DIR=outputs
if exist %OUTPUTS_DIR% (
    echo Cleaning outputs directory...
    rmdir /s /q %OUTPUTS_DIR%
)
mkdir %OUTPUTS_DIR%

REM Esegui le partite
echo Starting games...
for /L %%i in (1,1,%NUM_TESTS%) do (
    for %%h in (%H_FLAGS%) do (
        echo Test %%i with flag %%h

        REM Percorsi dei file di log per questa run
        set SERVER_LOG=%OUTPUTS_DIR%\server_test%%i_%%h.log
        set WHITE_LOG=%OUTPUTS_DIR%\white_test%%i_%%h.log
        set BLACK_LOG=%OUTPUTS_DIR%\black_test%%i_%%h.log

        REM Avvia il server
        start /b cmd /c java -jar "%SERVER_PATH%\Server.jar" > "%SERVER_LOG%" 2>&1
        set SERVER_PID=!ERRORLEVEL!

        REM Dai tempo al server per avviarsi completamente
        timeout /t 1 >nul

        REM Avvia i giocatori
        start /b cmd /c python "%PLAYER_PATH%\PLAYER.py" WHITE 60 127.0.0.1 %%h > "%WHITE_LOG%" 2>&1
        start /b cmd /c python "%PLAYER_PATH%\PLAYER.py" BLACK 60 127.0.0.1 %%h > "%BLACK_LOG%" 2>&1

        REM Aspetta che i processi completino
        REM Nota: il comando wait per PID non è nativo su Windows, quindi si può usare un workaround
        timeout /t 10 >nul
    )
)

REM Copia i log nella cartella logs
echo Copying logs to ./logs directory...
if not exist logs mkdir logs
xcopy /s /e /q %OUTPUTS_DIR%\* logs\

echo All tests completed!

REM Avvia il parsing dei log
echo Start parsing log files...
python extractor.py
