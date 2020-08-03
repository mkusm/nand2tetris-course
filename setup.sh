mv nand2tetris nand2tetris_temp
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=0B9c0BdDJz6XpZUh3X2dPR1o0MUE' -O nand2tetris.zip
unzip nand2tetris.zip
rm nand2tetris.zip
chmod +x nand2tetris/tools/*.sh
cp -r nand2tetris_temp/* nand2tetris
rm -rf nand2tetris_temp
