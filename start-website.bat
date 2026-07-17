@echo off
chcp 65001 >nul
title 百洛生物官网 - 本地预览
cd /d "C:\Users\valle\WorkBuddy\2026-06-11-11-11-10"
echo ========================================
echo   百洛生物官网 本地预览服务
echo ========================================
echo.
echo  官网首页: http://localhost:8081/index.html
echo  后台管理: http://localhost:8081/manage-x7k2.html
echo  产品中心: http://localhost:8081/products.html
echo  新闻资讯: http://localhost:8081/news.html
echo  联系我们: http://localhost:8081/contact.html
echo.
echo  关闭此黑色窗口即停止服务
echo  电脑重启后需重新双击此文件
echo.
echo  若页面显示旧版/空白，请在浏览器按 Ctrl+F5 强制刷新
echo.
start http://localhost:8081/index.html
"C:\Users\valle\.workbuddy\binaries\python\versions\3.13.12\python.exe" -m http.server 8081 --bind 127.0.0.1
pause
