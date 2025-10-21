for i in `seq 1 10 `
do
  sleep 15
  python main$i.py &
done

