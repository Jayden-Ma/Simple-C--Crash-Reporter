$exe = [System.IO.Path]::GetTempFileName() + ".exe"; g++ -g main.cpp -o $exe; gdb -q -x check.py -ex "run < input.txt" --args $exe; Remove-Item $exe -ErrorAction SilentlyContinue

g++ -g main.cpp -o main.exe; gdb -q -x check.py -ex "run < input.txt" --args ./main.exe