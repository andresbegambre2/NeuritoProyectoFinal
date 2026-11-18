"""Pequeña red MLP entrenada por retropropagación (NumPy)."""
import numpy as np

class MLP:
    def __init__(self, n_in, hidden=(32, 24), n_out=9, seed=42, lr=0.03):
        self.rng = np.random.default_rng(seed)
        sizes = [n_in, *hidden, n_out]
        self.W = [self.rng.normal(0, np.sqrt(2/a), (a,b)) for a,b in zip(sizes[:-1], sizes[1:])]
        self.b = [np.zeros((1,b)) for b in sizes[1:]]
        self.lr = lr

    def forward(self, X):
        acts=[X]; zs=[]
        for w,b in zip(self.W[:-1],self.b[:-1]):
            z=acts[-1]@w+b; zs.append(z); acts.append(np.maximum(0,z))
        z=acts[-1]@self.W[-1]+self.b[-1]; zs.append(z)
        z-=z.max(axis=1,keepdims=True); p=np.exp(z); p/=p.sum(axis=1,keepdims=True)
        return acts,zs,p

    def predict(self, X): return np.argmax(self.forward(np.asarray(X))[2],axis=1)

    def fit(self, X, y, epochs=120, batch=128):
        X=np.asarray(X,dtype=float); y=np.asarray(y,dtype=int); losses=[]
        for _ in range(epochs):
            order=self.rng.permutation(len(X)); total=0.
            for start in range(0,len(X),batch):
                ids=order[start:start+batch]; xb=X[ids]; yb=y[ids]
                acts,zs,p=self.forward(xb); n=len(ids)
                total+=-np.log(np.clip(p[np.arange(n),yb],1e-12,1)).sum()
                delta=p.copy(); delta[np.arange(n),yb]-=1; delta/=n
                gW=[None]*len(self.W); gb=[None]*len(self.b)
                gW[-1]=acts[-1].T@delta; gb[-1]=delta.sum(axis=0,keepdims=True)
                for j in range(len(self.W)-2,-1,-1):
                    delta=(delta@self.W[j+1].T)*(zs[j]>0)
                    gW[j]=acts[j].T@delta; gb[j]=delta.sum(axis=0,keepdims=True)
                for j in range(len(self.W)):
                    self.W[j]-=self.lr*gW[j]; self.b[j]-=self.lr*gb[j]
            losses.append(total/len(X))
        return losses
