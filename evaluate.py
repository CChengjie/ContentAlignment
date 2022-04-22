import pandas as pd
def evaluate():
    df = pd.read_csv('./data/res2.csv')
    print("shape:",df.shape[0])
    hit = 0
    dif = 0
    for index in range(df.shape[0]):
        cmt2id = df.loc[index,'cmt2id']
        res2id = str(df.loc[index,'res2id']).replace('[','').replace(']','').replace(' ','').split(',')
        res2id = [int(x) for x in res2id]
        if cmt2id in res2id:
            hit = hit+1
            dif =dif + abs(res2id[0]-cmt2id)+abs(res2id[-1]-cmt2id)
        else:
            print("miss: ",index)
    print("hit = ",hit)
    acu = hit/df.shape[0]
    mae = dif/ (2*hit)
    print("acu = ",acu)
    print("mae = ",mae)

if __name__ == '__main__':
    evaluate()