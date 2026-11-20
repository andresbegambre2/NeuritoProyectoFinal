"""Experimentos comparables: escenario x política x semilla."""
import csv, json
from pathlib import Path
import numpy as np
from .ecosistema import ESCENARIOS,World,rule_policy,random_policy,policy_from_model
from .entrenar import train_all,load_model
from .red import MLP

REPETICIONES=30
SEMILLA_BASE=1000
HORIZONTE=250

def main():
    base=Path(__file__).resolve().parents[1]; data_dir=base/'evidencia'; models=base/'modelos'
    training=train_all(models,epochs=120,seed=42)
    learned={k:load_model(models/f'{k}_model.npz') for k in ('prey','predator')}
    untrained={k:MLP(6,(32,24),9,seed=42+i) for i,k in enumerate(('prey','predator'))}
    policies={
      'neuronal_entrenada':{k:policy_from_model(learned[k],k) for k in learned},
      'neuronal_sin_entrenar':{k:policy_from_model(untrained[k],k) for k in untrained},
      'reglas_experto':{k:rule_policy(k) for k in learned},
      'aleatoria':None,
    }
    rows=[]
    for scenario in ESCENARIOS:
      for name,pol in policies.items():
       for repetition in range(REPETICIONES):
        episode_seed=SEMILLA_BASE+repetition
        world=World(episode_seed,scenario,max_steps=HORIZONTE)
        episode_policy=pol if pol is not None else {
          'prey':random_policy(episode_seed+8000),
          'predator':random_policy(episode_seed+9000),
        }
        stats=world.step(episode_policy,steps=HORIZONTE)
        rows.append({'scenario':scenario,'policy':name,'seed':episode_seed,**stats})
    data_dir.mkdir(exist_ok=True)
    with (data_dir/'episodios.csv').open('w',newline='',encoding='utf-8-sig') as f:
      writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    # Comparación pareada aleatoria - neuronal entrenada sobre las mismas semillas.
    paired=[]
    for scenario in ESCENARIOS:
      by_key={(r['policy'],r['seed']):r for r in rows if r['scenario']==scenario}
      for metric in ('survivors','food_eaten','captures'):
        differences=np.array([by_key[('aleatoria',seed)][metric]-by_key[('neuronal_entrenada',seed)][metric]
                              for seed in range(SEMILLA_BASE,SEMILLA_BASE+REPETICIONES)])
        mean=float(np.mean(differences)); sd=float(np.std(differences,ddof=1))
        margin=2.045*sd/np.sqrt(len(differences))
        paired.append({'scenario':scenario,'comparison':'aleatoria_menos_neuronal_entrenada','metric':metric,
                       'n':len(differences),'mean_difference':round(mean,3),'sd_difference':round(sd,3),
                       'ci95_low':round(mean-margin,3),'ci95_high':round(mean+margin,3)})
    groups={}
    for r in rows:groups.setdefault((r['scenario'],r['policy']),[]).append(r)
    summary=[]
    for (scenario,policy),rs in groups.items():
      capture_times=[r['time_to_first_capture'] for r in rs if r['time_to_first_capture'] is not None]
      row={'scenario':scenario,'policy':policy,'n':len(rs),'episodes_with_capture':len(capture_times)}
      for metric in ('survivors','food_eaten','captures','prey_energy','predator_energy','steps'):
        vals=[r[metric] for r in rs]
        row[metric]=round(float(np.mean(vals)),3)
        row[metric+'_sd']=round(float(np.std(vals,ddof=1)),3)
      row['time_to_first_capture_mean']=round(float(np.mean(capture_times)),3) if capture_times else None
      row['time_to_first_capture_sd']=round(float(np.std(capture_times,ddof=1)),3) if len(capture_times)>1 else None
      row['termination_counts']={reason:sum(r['termination_reason']==reason for r in rs) for reason in sorted({r['termination_reason'] for r in rs})}
      summary.append(row)
    (data_dir/'resumen.json').write_text(json.dumps({'training':training,'episodes':summary,'paired_comparisons':paired},indent=2),encoding='utf-8')
    with (data_dir/'resumen.csv').open('w',newline='',encoding='utf-8-sig') as f:
      w=csv.DictWriter(f,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
    print('Modelos y evidencia guardados en',data_dir)
    for r in summary:print(r)
if __name__=='__main__':main()


