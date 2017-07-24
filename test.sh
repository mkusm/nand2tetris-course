
PROJECT=$1
if [[ $# -eq 0 ]]; then
	PROJECT="all"
fi

if [[ $PROJECT =~ ^(1|all)$ ]]; then
	echo "-- Project 1 --"
	echo ""

	for TEST in nand2tetris/projects/01/*.tst
	do
		echo $TEST
		./nand2tetris/tools/HardwareSimulator.sh $TEST
		echo ""
	done
fi

if [[ $PROJECT =~ ^(2|all)$ ]]; then
	echo "-- Project 2 --"
	echo ""

	for TEST in nand2tetris/projects/02/*.tst
	do
		echo $TEST
		./nand2tetris/tools/HardwareSimulator.sh $TEST
		echo ""
	done
fi

if [[ $PROJECT =~ ^(3|all)$ ]]; then
	echo "-- Project 3 --"
	echo ""

	for TEST in nand2tetris/projects/03/*/*.tst
	do
		echo $TEST
		./nand2tetris/tools/HardwareSimulator.sh $TEST
		echo ""
	done
fi

if [[ $PROJECT =~ ^(4|all)$ ]]; then
	echo "-- Project 4 --"
	echo ""

	for ASMFILE in nand2tetris/projects/04/*/*.asm
	do
		./nand2tetris/tools/Assembler.sh $ASMFILE
	done

	echo ""
	for TEST in nand2tetris/projects/04/*/*.tst
	do
		echo $TEST
		./nand2tetris/tools/CPUEmulator.sh $TEST
		echo ""
	done
fi
