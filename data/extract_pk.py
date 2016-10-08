import os
from six.moves import cPickle
import numpy as np

def save_as_pk(data,filename):
    fout = open(filename,'wb')
    cPickle.dump(data,fout,protocol=cPickle.HIGHEST_PROTOCOL)
    fout.close()

def get_match_detail(m):
    w = m['radiant_win']
    radiant=[]
    dire = []
    for p in m['players']:
        if p['player_slot'] >= 128:
            dire.append(p['hero_id'])
        else:
            radiant.append(p['hero_id'])
    if len(radiant)!=5 or len(dire)!=5:
        return (-1,-1)
    return (w,radiant + dire)

if __name__ == '__main__':
    list_dirs = os.walk("matches") 
    y = []
    x = []
    for root, dirs, files in list_dirs: 
        for f in files: 
            filename = os.path.join(root, f)
            if not "pk" in filename:
                continue
            fin = open(filename,'rb')
            matches = cPickle.load(fin)
            fin.close()
            print filename

            for m in matches:
                a,b = get_match_detail(m)
                if a==-1:
                    continue
                y.append(a)
                x.append(b)
            
    X = np.array(x)
    Y = np.array(y)
    N = X.shape[0]
    print 'number of examples = ',N
    train_x = X[:int(N*.9),:]
    train_y = Y[:int(N*.9)]
    valid_x = X[int(N*.9):int(N*.95),:]
    valid_y = Y[int(N*.9):int(N*.95)]
    test_x = X[int(N*.95):,:]
    test_y = Y[int(N*.95):]
    save_as_pk((train_x, train_y),"200k/train.pk")
    save_as_pk((valid_x, valid_y),"200k/valid.pk")
    save_as_pk((test_x, test_y),"200k/test.pk")
    

    
    #train_x = 