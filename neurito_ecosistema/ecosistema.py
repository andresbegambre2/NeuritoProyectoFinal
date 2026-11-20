"""Entorno discreto presa-depredador; las reglas solo generan etiquetas de entrenamiento."""
import numpy as np
ACCIONES=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,0),(0,1),(1,-1),(1,0),(1,1)]
ESCENARIOS={
 "abundancia":dict(food=22,predators=2,obstacles=0),
 "escasez":dict(food=7,predators=2,obstacles=0),
 "presion":dict(food=16,predators=5,obstacles=18),
}

def unit(v):
    v=np.asarray(v,dtype=float); n=np.linalg.norm(v)
    return v/n if n>0 else np.zeros(2)

def features(world,kind,pos,energy):
    W=world; food=W.nearest(pos,W.food); target=W.nearest(pos,W.prey if kind=='predator' else W.predators)
    toward_food=unit(np.array(food)-pos) if food is not None else np.zeros(2)
    toward=unit(np.array(target)-pos) if target is not None else np.zeros(2)
    away=-toward
    # 6 features: vector al objetivo primario, vector amenaza, energía, alimento cercano
    if kind=='prey': return np.array([*toward_food,*away,*[energy],float(food is not None)])
    return np.array([*toward,*toward_food,*[energy],float(target is not None)])

def expert_label(x,kind):
    primary=x[:2]
    # Evitar amenaza tiene prioridad alta para presas; perseguir presa para depredador.
    if kind=='prey' and np.linalg.norm(x[2:4])>0.1: primary=unit(1.6*x[2:4]+0.55*x[:2])
    if kind=='predator' and np.linalg.norm(primary)<0.1: primary=np.zeros(2)
    score=[np.dot(unit(a),primary) if a!=(0,0) else -0.03 for a in ACCIONES]
    return int(np.argmax(score))

class World:
    def __init__(self,seed,scenario='abundancia',size=24,max_steps=250):
        self.rng=np.random.default_rng(seed); self.size=size; self.cfg=ESCENARIOS[scenario]
        self.obstacles=set(); self.food=set(); self.prey={}; self.predators={}; self.captures=0; self.consumed=0; self.tick=0; self.first_capture=None
        self.max_steps=max_steps; self.termination_reason=None
        cells=[(x,y) for x in range(size) for y in range(size)]
        self.obstacles=set()
        for i in self.rng.choice(len(cells),size=self.cfg['obstacles'],replace=False): self.obstacles.add(cells[int(i)])
        self.food=set(self._empty_positions(self.cfg['food']))
        self.prey={p:1.0 for p in self._empty_positions(12)}
        self.predators={p:1.0 for p in self._empty_positions(self.cfg['predators'])}
    def _empty_positions(self,n):
        out=[]; attempts=0
        while len(out)<n and attempts<10000:
            p=(int(self.rng.integers(self.size)),int(self.rng.integers(self.size))); attempts+=1
            if p not in self.obstacles and p not in self.food and p not in self.prey and p not in self.predators and p not in out: out.append(p)
        return out
    def nearest(self,pos,targets):
        if not targets:return None
        return min(targets,key=lambda p:abs(pos[0]-p[0])+abs(pos[1]-p[1]))
    def step(self,policies,steps=1):
        for _ in range(steps):
            if self.termination_reason is not None:
                break
            self.tick+=1
            for kind,pop in [('prey',self.prey),('predator',self.predators)]:
                updated={}
                for pos,en in list(pop.items()):
                    x=features(self,kind,pos,en); action=int(policies[kind](x[None,:])[0]); dx,dy=ACCIONES[action]
                    nxt=(int(np.clip(pos[0]+dx,0,self.size-1)),int(np.clip(pos[1]+dy,0,self.size-1)))
                    if nxt in self.obstacles or nxt in updated: nxt=pos
                    en-=0.006 if kind=='prey' else 0.012
                    if kind=='prey' and nxt in self.food: en=min(1.0,en+0.32); self.food.remove(nxt); self.consumed+=1
                    if kind=='predator' and nxt in self.prey:
                        del self.prey[nxt]; self.captures+=1
                        if self.first_capture is None:self.first_capture=self.tick
                        en=min(1.,en+0.32)
                    if en>0: updated[nxt]=en
                if kind=='prey': self.prey=updated
                else:self.predators=updated
            if self.rng.random()<0.25:
                p=self._empty_positions(1)
                if p:self.food.add(p[0])
            if not self.prey:
                self.termination_reason='extincion_presas'
            elif not self.predators:
                self.termination_reason='extincion_depredadores'
            elif self.tick>=self.max_steps:
                self.termination_reason='limite_de_pasos'
        return {'survivors':len(self.prey),'predators_alive':len(self.predators),'food_eaten':self.consumed,'captures':self.captures,'time_to_first_capture':self.first_capture,'prey_energy':float(np.mean(list(self.prey.values()))) if self.prey else 0.,'predator_energy':float(np.mean(list(self.predators.values()))) if self.predators else 0.,'steps':self.tick,'termination_reason':self.termination_reason or 'en_curso'}

def policy_from_model(model,kind):
    return lambda X:model.predict(X)

def rule_policy(kind):
    return lambda X:np.array([expert_label(x,kind) for x in X])

def random_policy(seed):
    rng=np.random.default_rng(seed)
    return lambda X:rng.integers(0,len(ACCIONES),size=len(X))

def collect_data(seed=42,n=9000):
    rng=np.random.default_rng(seed); X={'prey':[],'predator':[]}; y={'prey':[],'predator':[]}
    for i in range(n):
        # Distribución de estados sintéticos balanceada y reproducible; input feature order is shared.
        kind='prey' if i%2==0 else 'predator'
        food=unit(rng.normal(size=2)) if rng.random()<.85 else np.zeros(2)
        threat=unit(rng.normal(size=2)) if rng.random()<.45 else np.zeros(2)
        energy=float(rng.random()); x=np.array([*food,*threat,energy,float(np.linalg.norm(food)>0)])
        X[kind].append(x); y[kind].append(expert_label(x,kind))
    return {k:(np.array(X[k]),np.array(y[k])) for k in X}

