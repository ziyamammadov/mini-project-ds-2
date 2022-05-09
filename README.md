# Mini-project 2
The Team: **Ziya Mammadov** and **Konstantin Tenman**

Mini project for the Distributed Systems course where *Generals Byzantine* algorithm was implemented.
## To run the program
`/Generals_Byzantine_program.sh N` where **N** is amount of processes
## Program video
https://github.com/ziyamammadov/mini-project-ds-2/blob/main/video.mov
## Commands
```
./Generals_Byzantine_program.sh 4
Input the command: actual-order attack
G1, primary, majority=attack, state=NF
G2, secondary, majority=attack, state=NF
G3, secondary, majority=attack, state=NF
G4, secondary, majority=attack, state=NF
Execute order: attack! Non-faulty nodes in the system – 3 out of 4 quorum suggest attack

Input the command: actual-order retreat
G1, primary, majority=retreat, state=NF
G2, secondary, majority=retreat, state=NF
G3, secondary, majority=retreat, state=NF
G4, secondary, majority=retreat, state=NF
Execute order: retreat! Non-faulty nodes in the system – 3 out of 4 quorum suggest retreat

Input the command: g-state 3 faulty
G1, state = NF
G2, state = NF
G3, state = F
G4, state = NF

Input the command: g-state
G1, primary, state=NF
G2, secondary, state=NF
G3, secondary, state=F
G4, secondary, state=NF

Input the command: g-kill 1 
G2, state=NF
G3, state=F
G4, state=NF

Input the command: g-state
G2, primary, state=NF
G3, secondary, state=F
G4, secondary, state=NF

Input the command: actual-order attack
G2, primary, majority=attack, state=NF
G3, secondary, majority=undefined, state=F
G4, secondary, majority=undefined, state=NF
Execute order: cannot be determined – not enough generals in the system! 1 faulty node in the system - 2 out of 3 quorum not consistent

Input the command: g-add 2
G2, primary
G3, secondary
G4, secondary
G5, secondary
G6, secondary

Input the command: g-state
G2, primary, state=NF
G3, secondary, state=F
G4, secondary, state=NF
G5, secondary, state=NF
G6, secondary, state=NF

Input the command: actual-order attack
G2, primary, majority=attack, state=NF
G3, secondary, majority=attack, state=F
G4, secondary, majority=attack, state=NF
G5, secondary, majority=attack, state=NF
G6, secondary, majority=attack, state=NF
Execute order: attack! 1 faulty nodes in the system – 3 out of 5 quorum suggest attack
Input the command: exit
```
### exit
```
Input the command: exit
Program exited  
```
## Credits
https://courses.cs.ut.ee/LTAT.06.007/2022_spring/uploads/Main/Mini-project2-DS2022.pdf