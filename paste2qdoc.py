file = "questions"
linepairs = []
with(open(file,'r')) as f:
    for lines in f.readlines():
        qastr = lines.strip()
        qend = qastr.find('(')
        question = qastr[:qend]
        answer = qastr[qend:]
        #b = a[1].split(' (')
        #linepairs.append(b)
        #print(question + " " + answer )
        answer = answer.strip("()")
        linepairs.append((question.strip(),answer.strip()))
file2 = 'qdoc.mtq'
with(open(file2,'w')) as f:
        for q,a in linepairs:
            if(q,a):
                f.write((q + ":" + a))
