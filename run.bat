@echo off

setlocal EnableDelayedExpansion

for /f %%i in ('type urls.txt') do (
  set urls=!urls! %%i
)

scrapy crawl summary --nolog --output="-:json" -a urls="%urls%" || goto :END

:END
endlocal
