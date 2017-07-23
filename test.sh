echo "-- Project 1 --"
echo ""

for TEST in nand2tetris/projects/01/*.tst
do
	echo $TEST
	./nand2tetris/tools/HardwareSimulator.sh $TEST
	echo ""
done

echo "-- Project 2 --"
echo ""

for TEST in nand2tetris/projects/02/*.tst
do
	echo $TEST
	./nand2tetris/tools/HardwareSimulator.sh $TEST
	echo ""
done

echo "-- Project 3 --"
echo ""

for TEST in nand2tetris/projects/03/*/*.tst
do
	echo $TEST
	./nand2tetris/tools/HardwareSimulator.sh $TEST
	echo ""
done
