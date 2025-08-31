for i in `seq 11 20 `
do
  sleep 5
  python main$i.py &
done

