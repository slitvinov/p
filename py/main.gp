set term png font size 20 linewidth 2
set output "scan.png"
set key bottom
plot [0:60][20:80] \
     "<grep white p.txt" w p pt 7 lc 1 t "free" , \
     "<grep black p.txt" w p pt 7 t "obstacles", \
     "<grep visited p.txt" w p ps 3 pt 7 t "visited"    


