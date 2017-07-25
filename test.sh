#!/bin/bash

PROJECT=$1
if [[ $# -eq 0 ]]; then
	PROJECT="all"
fi

function test_project_hdl {
	if [[ $PROJECT =~ ^($1|all)$ ]]; then
		echo "-- Project $1 --"
		echo ""
		for TEST in nand2tetris/projects/0$1/$2*.tst; do
			echo $TEST
			./nand2tetris/tools/HardwareSimulator.sh $TEST
			echo ""
		done
	fi
}

function test_files_hdl {
	for FILE; do
		echo $FILE
		./nand2tetris/tools/HardwareSimulator.sh $FILE
		echo ""
	done
}

function test_files_hack {
	for FILE; do
		echo $FILE
		./nand2tetris/tools/CPUEmulator.sh $FILE
		echo ""
	done
}

test_project_hdl 1

test_project_hdl 2

test_project_hdl 3 "*/"

if [[ $PROJECT =~ ^(4|all)$ ]]; then
	echo "-- Project 4 --"
	echo ""

	for ASMFILE in nand2tetris/projects/04/*/*.asm; do
		./nand2tetris/tools/Assembler.sh $ASMFILE
	done

	FILE1="nand2tetris/projects/04/mult/Mult.tst"
	FILE2="nand2tetris/projects/04/fill/FillAutomatic.tst"

	echo ""
	test_files_hack $FILE1 $FILE2
fi

if [[ $PROJECT =~ ^(5|all)$ ]]; then
	echo "-- Project 5 --"
	echo ""
	for TEST in nand2tetris/projects/05/*.tst; do
		if [[ $TEST != *Computer* ]] && [[ $TEST != *Mem* ]]; then
			echo $TEST
			./nand2tetris/tools/HardwareSimulator.sh $TEST
			echo ""
		fi
	done
fi
