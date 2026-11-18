"""Experimentos comparables: escenario x política x semilla."""
import csv, json
from pathlib import Path
import numpy as np
from .ecosistema import ESCENARIOS,World,rule_policy,random_policy,policy_from_model
from .entrenar import train_all,load_model
from .red import MLP

def main():
    base=Path(__file__).resolve().parents[1]; data_dir=base/'evidencia'; models=base/'modelos'
    training=train_all(models,epochs=120,seed=42)
    learned={k:load_model(models/f'{k}_model.npz') for k in ('prey','predator')}
    untrained={k:MLP(6,(32,24),9,seed=42+i) for i,k in enumerate(('prey','predator'))}
    policies={
      'neuronal_entrenada':{k:policy_from_model(learned[k],k) for k in learned},
      'neuronal_sin_entrenar':{k:policy_from_model(untrained[k],k) for k in untrained},
      'reglas_experto':{k:rule_policy(k) for k in learned},
      'aleatoria':{k:random_policy(100+k.__len__()) for k in learned},
    }
    rows=[]
    for scenario in ESCENARIOS:
      for name,pol in policies.items():
       for seed in range(10):
        world=World(seed+1000,scenario)
        stats=world.step(pol,steps=250)
        rows.append({'scenario':scenario,'policy':name,'seed':seed+1000,**stats})
    data_dir.mkdir(exist_ok=True)
    with (data_dir/'episodios.csv').open('w',newline='',encoding='utf-8-sig') as f:
      writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    groups={}
    for r in rows:groups.setdefault((r['scenario'],r['policy']),[]).append(r)
    summary=[]
    for (scenario,policy),rs in groups.items():
      summary.append({'scenario':scenario,'policy':policy,'n':len(rs),**{k:round(float(np.mean([r[k] for r in rs])),3) for k in ('survivors','food_eaten','captures','prey_energy','time_to_first_capture')},**{k+'_sd':round(float(np.std([r[k] for r in rs],ddof=1)),3) for k in ('survivors','food_eaten','captures','prey_energy')}})
    (data_dir/'resumen.json').write_text(json.dumps({'training':training,'episodes':summary},indent=2),encoding='utf-8')
    with (data_dir/'resumen.csv').open('w',newline='',encoding='utf-8-sig') as f:
      w=csv.DictWriter(f,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
    print('Modelos y evidencia guardados en',data_dir)
    for r in summary:print(r)
if __name__=='__main__':main()


