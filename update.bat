@echo off
chcp 65001 >nul
echo ================================
echo Обновление бота
echo ================================
echo.

echo 1. Добавляем изменения...
git add .
echo.

echo 2. Создаём коммит...
set /p msg="Введите описание изменений: "
git commit -m "%msg%"
echo.

echo 3. Отправляем на GitHub...
git push
echo.

echo ================================
echo ГОТОВО! Обновите бота в BotHost
echo ================================
pause