for i in `seq 1 20 `
do
  sleep 10
  python main$i.py &
done

