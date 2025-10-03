import matplotlib.pyplot as plt

def text_report(runs,batsman):
    l, over = analyze(runs, batsman)
    x, y,z= l.display()
    
    print("\n\n----- MATCH REPORT -----\n")
    
    print("Over-wise Scores:\n")
    print("Over\tRuns\tWickets\n")
    for i in over:
        print(f"{i[0]}\t\t{i[1]}\t\t{i[2]}\n")
    
    print("\nPartnership Scores:\n")
    print("Partnership\t\tRuns_Scored\t\tScored_in_(No. of Balls)\n")
    for i in range(len(x)):
        print(f"{x[i]}\t\t\t\t{y[i]}\t\t\t\t{z[i]}\n")
    
    total_runs = sum(y)
    total_wickets = sum([i[2] for i in over])
    print(f"\nTotal Runs: {total_runs}")
    print(f"Total Wickets: {total_wickets}\n")

class node:
    def __init__(self,A,B):
        self.batters=str(A)+"-"+str(B)
        self.runs=0
        self.balls=0
        self.next=None

class LL:  
    def __init__(self):
        self.head=node("","")

    def newpair(self,A,B):
        cur=self.head
        temp=node(A,B)
        while cur.next != None:
            cur=cur.next
        cur.next=temp
        return temp

    def display(self):
        cur=self.head
        tRuns=[]
        batters=[]
        balls=[]
        while cur.next != None:
            cur=cur.next
            tRuns.append(cur.runs)
            batters.append(cur.batters)
            balls.append(cur.balls)
        return batters,tRuns,balls

def analyze(runs, batsman):
    b=1
    bat1=batsman[0]
    bat2=batsman[b]
    l=LL()
    pair=l.newpair(bat1,bat2)
    w=0
    overruns=0
    overcount=1
    over=[]
    cur=bat1
    for i,n in enumerate(runs):
        if str(n).lower() == "w":
            pair.balls+=1
            w+=1
            b+=1
            if b<len(batsman):
                if cur==bat1:
                    bat1=batsman[b]
                    pair=l.newpair(bat1,bat2)
                    cur=bat1
                else:
                    bat2=batsman[b]
                    pair=l.newpair(bat2,bat1)
                    cur=bat2
            else: break
        else:
            if n=="WD":
                pair.runs+=1
                overruns+=1
                continue
            elif type(n)==str and n.startswith("LB"):
                n=int(n[2:])
            elif type(n)==str and n.startswith("B"):
                n=int(n[1:])
            pair.runs+=n
            pair.balls+=1
            overruns+=n
            if n%2==1:
                cur= bat2 if cur==bat1 else bat1
        
        if (i+1)%6==0:
            over.append((overcount,overruns,w))
            overcount+=1
            overruns=0
            w=0
            cur= bat2 if cur==bat1 else bat1
    
    over.append((overcount,overruns,w))
    overruns=0
    w=0
    return l,over

# def match_report_and_stats(runs_list, batsman_list):
#     runs=runs_list
#     batsman=batsman_list
#     l,over=analyze(runs, batsman)
#     text_report(runs,batsman)
#     x,y,z=l.display()
#     print(x,y,z)
#     plt.bar(x, y, color="orange")
#     for i in range(len(x)):
#         plt.text(i, y[i]+0.3, f"{z[i]} balls", ha='center', va='center',fontsize=10, fontweight="bold", color="black")
#     plt.xlabel("Batsman Pairs")
#     plt.ylabel("Runs")
#     plt.title("Partnership Runs")
#     plt.show()

# runs=[0,0,0,0,4,0,"LB1",0,0,2,4,0,1,1,1,1,0,4,4,0,6,1,"B1",1,0,1,0,2,1,1,0,0,1,2,1,4,1,1,1,0,2,6,1,2,0,4,1,0,"WD",1,6,"B1",2,1,1,0,1,6,"W",1,2,1,1,4,0,4,1,1,4,0,1,1,2,"WD",0,1,"WD",2,1,"W",0,0,1,"W",1,1,2,2,0,6,"W",1,1,2,1,"W",0,1,1,"W",0,"WD",0,"W",0,"W",1,4,0,2,"W",0,2,0,0,1,1,1,"W"]
# batters=["Sahibzada Farhan","Fakhar Zaman","Saim Ayub","Mohammad Haris","Salman Ali Agha","Hussain Talt","Mohammad Nawaz","Shaheen Afridi","Faheem Ashraf","Haris Rauf","Abrar Ahmed"]

# match_report_and_stats(runs,batters)
