reason=$1" 修改时间 "`date '+%Y/%m/%d %H:%M:%S'`
echo $reason
git add *
git commit -m "$reason"
git push