"""Entrenamiento reproducible de dos políticas MLP con etiquetas de experto."""
import json
from pathlib import Path
import numpy as np
from .red import MLP
from .ecosistema import collect_data

def train_all(out_dir,epochs=120,seed=42):
    out=Path(out_dir); out.mkdir(parents=True,exist_ok=True)
    data=collect_data(seed=seed,n=12000); summary={}; architecture=[]
    for i,kind in enumerate(('prey','predator')):
        X,y=data[kind]; cut=int(.8*len(X)); xtr,ytr=X[:cut],y[:cut]; xte,yte=X[cut:],y[cut:]
        model=MLP(6,(32,24),9,seed=seed+i,lr=.035)
        initial=float(-np.log(np.clip(model.forward(xte)[2][np.arange(len(xte)),yte],1e-12,1)).mean())
        before=float(np.mean(model.predict(xte)==yte)); initial_weights=[w.copy() for w in model.W]; history=model.fit(xtr,ytr,epochs=epochs)
        after=float(np.mean(model.predict(xte)==yte)); final=float(-np.log(np.clip(model.forward(xte)[2][np.arange(len(xte)),yte],1e-12,1)).mean())
        # Comparación de arquitectura: mismo conjunto, tasa, épocas y semilla; solo cambia el ancho.
        small=MLP(6,(16,12),9,seed=seed+i,lr=.035); small.fit(xtr,ytr,epochs=epochs)
        small_acc=float(np.mean(small.predict(xte)==yte))
        architecture.append({'species':kind,'hidden_layers':'16-12','accuracy':small_acc,'parameters':int(sum(w.size for w in small.W)+sum(b.size for b in small.b))})
        architecture.append({'species':kind,'hidden_layers':'32-24','accuracy':after,'parameters':int(sum(w.size for w in model.W)+sum(b.size for b in model.b))})
        np.savez(out/f'{kind}_model.npz',*model.W,**{f'b{i}':v for i,v in enumerate(model.b)})
        summary[kind]={'examples_train':len(xtr),'examples_test':len(xte),'epochs':epochs,'loss_before':initial,'loss_after':final,'accuracy_before':before,'accuracy_after':after,'parameter_count':int(sum(w.size for w in model.W)+sum(b.size for b in model.b)),'parameter_delta_l2':float(np.sqrt(sum(np.sum((w-w0)**2) for w,w0 in zip(model.W,initial_weights)))),'loss_history':history}
    summary['architecture_comparison']=architecture
    (out/'training_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    return summary

def load_model(path,seed=42):
    a=np.load(path); m=MLP(6,(32,24),9,seed=seed)
    m.W=[a['arr_0'],a['arr_1'],a['arr_2']]; m.b=[a['b0'],a['b1'],a['b2']]
    return m

