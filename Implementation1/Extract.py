from ExtractThread import ExtractingThread
from Movement import MovementThread, ExtendThread
import binascii
if __name__ == "__main__":
    filename = "ALABAMAA.EXE"
    with open(filename, 'r') as f:
        content = f.read()
        newcontent = binascii.hexlify(content)
    start = 0
    end = 32
    partitioned_sigs = []
    while(end<len(newcontent)+32):
        sig1 = newcontent[start:end:]
        start += 32
        end += 32
        partitioned_sigs.append(sig1)
    partitioned_sigs_half1 = partitioned_sigs[:int(len(partitioned_sigs)/2):]
    partitioned_sigs_half2 = partitioned_sigs[int(len(partitioned_sigs))/2::]
    ExThread1 = ExtractingThread(partitioned_sigs_half1)
    ExThread2 = ExtractingThread(partitioned_sigs_half2)

    ExThread1.start()
    ExThread2.start()

    while(True):
        print "Still running..."
        if not ExThread1.isAlive() and not ExThread2.isAlive():
            if ExThread2.top[1] < ExThread1.top[1]:
                cur_top = ExThread2.top
            else:
                cur_top = ExThread1.top
            break
    print cur_top
    print "First process ended..."
    iterations = 0
    while(cur_top[1]>0.2 and iterations != 50):
        print "Still running..."
        location = newcontent.find(cur_top[0])
        mthread = MovementThread(cur_top, location, newcontent)
        ethread = ExtendThread(cur_top, location, newcontent)

        mthread.start()
        ethread.start()
        
        while(True):
            if not mthread.isAlive() and not ethread.isAlive():
                if cur_top[1] > mthread.cur_top[1] and ethread.cur_top[1] > mthread.cur_top[1]:
                    cur_top = mthread.cur_top
                elif cur_top[1] > ethread.cur_top[1] and mthread.cur_top[1] > ethread.cur_top[1]:
                    cur_top = ethread.cur_top
                break
        iterations = iterations + 1
    print "Process ended, final result:",
    print cur_top
