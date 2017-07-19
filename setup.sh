mv nand2tetris nand2tetris_temp
wget -O nand2tetris.zip http://nand2tetris.org/software/nand2tetris.zip
unzip nand2tetris.zip
rm nand2tetris.zip
chmod +x nand2tetris/tools/*.sh
cp -r nand2tetris_temp/* nand2tetris
rm -rf nand2tetris_temp
