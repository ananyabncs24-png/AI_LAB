#vacuum cleaner code
#let o represent dirty
status=[0,0,0];
status[1]=0;#consider 1 as dirty
status[2]=0;#consider 2 as dirty
current_pos=1;
while status[1]==0 or status[2]==0:
    print(f"{current_pos} is dirty")
    if status[current_pos]==0:
      print(f"{current_pos} is cleaned");
      status[current_pos]=1
      if current_pos==1:
        print("move right to 2")
        current_pos=2;
      else:
        print("move left to 1")
        current_pos=1;
print("Both rooms are clean")
