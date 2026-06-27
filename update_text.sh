echo "[BASH] Moving 1.txt from dir1 to root"
mv dir1/1.txt .
echo "[BASH] Resetting engine"
engine reset
echo "[BASH] Moving 1.txt from root to dir1"
mv 1.txt dir1
echo "[BASH] Updating Engine"
engine update 