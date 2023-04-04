cd "..\..\..\"

set pipreqs=".venv\Scripts\pipreqs.exe"

%pipreqs% src/mlbbetting --print --savepath requirements.txt

pause