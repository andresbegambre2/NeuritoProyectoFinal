"""Vista interactiva Pygame para inspeccionar decisiones y variables del ecosistema."""
import sys,random
from pathlib import Path
import pygame
from .ecosistema import ESCENARIOS,World,features
from .entrenar import train_all,load_model
from .red import MLP

CELL=24; PAD=16; SIDE=300

def main():
    base=Path(__file__).resolve().parents[1]; models=base/'modelos'
    if not (models/'prey_model.npz').exists():train_all(models)
    nets={'prey':load_model(models/'prey_model.npz'),'predator':load_model(models/'predator_model.npz')}
    pygame.init(); screen=pygame.display.set_mode((PAD*2+24*CELL+SIDE,PAD*2+24*CELL));pygame.display.set_caption('Neurito | NeuroEcosistema')
    font=pygame.font.SysFont('segoeui',17);small=pygame.font.SysFont('segoeui',14)
    scenario='abundancia'; policy_name='Neuronal'; world=World(2026,scenario);tick=0;paused=True;selected=None
    clock=pygame.time.Clock(); running=True
    def policies():
        if policy_name=='Aleatoria':
            return {'prey':lambda x:__import__('numpy').random.randint(0,9,len(x)),'predator':lambda x:__import__('numpy').random.randint(0,9,len(x))}
        from .ecosistema import rule_policy,policy_from_model
        return {'prey':policy_from_model(nets['prey'],'prey') if policy_name=='Neuronal' else rule_policy('prey'), 'predator':policy_from_model(nets['predator'],'predator') if policy_name=='Neuronal' else rule_policy('predator')}
    while running:
        for e in pygame.event.get():
            if e.type==pygame.QUIT:running=False
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_ESCAPE:running=False
                elif e.key==pygame.K_SPACE:paused=not paused
                elif e.key==pygame.K_n:scenario={'abundancia':'escasez','escasez':'presion','presion':'abundancia'}[scenario];world=World(2026+tick,scenario);tick=0
                elif e.key==pygame.K_p:policy_name={'Neuronal':'Aleatoria','Aleatoria':'Reglas'}[policy_name] if policy_name!='Reglas' else 'Neuronal'
                elif e.key==pygame.K_r:world=World(2026,scenario);tick=0
                elif e.key==pygame.K_RIGHT and paused:world.step(policies(),1);tick+=1
        if not paused:world.step(policies(),1);tick+=1
        screen.fill((20,27,38)); ox=PAD;oy=PAD
        pygame.draw.rect(screen,(36,47,62),(ox,oy,24*CELL,24*CELL))
        for x,y in world.obstacles:pygame.draw.rect(screen,(91,102,113),(ox+x*CELL,oy+y*CELL,CELL-1,CELL-1))
        for x,y in world.food:pygame.draw.circle(screen,(72,210,112),(ox+x*CELL+CELL//2,oy+y*CELL+CELL//2),5)
        for (x,y),energy in world.prey.items():pygame.draw.circle(screen,(65,180,245),(ox+x*CELL+CELL//2,oy+y*CELL+CELL//2),max(4,int(8*energy)))
        for (x,y),energy in world.predators.items():pygame.draw.circle(screen,(245,89,83),(ox+x*CELL+CELL//2,oy+y*CELL+CELL//2),max(5,int(9*energy)))
        px=ox+24*CELL+20; y=PAD
        title=font.render('NEURITO · NEUROECOSISTEMA',True,(238,242,248));screen.blit(title,(px,y));y+=38
        info=[f'Escenario: {scenario}',f'Política: {policy_name}',f'Paso: {tick}',f'Presas vivas: {len(world.prey)}',f'Depredadores: {len(world.predators)}',f'Alimento consumido: {world.consumed}',f'Capturas: {world.captures}',f'Energía media presas: {sum(world.prey.values())/max(1,len(world.prey)):.2f}','', 'ESPACIO iniciar/pausar','→ un paso (pausado)','N cambiar escenario','P alternar política','R reiniciar','ESC salir','','Verde alimento · Azul presa','Rojo depredador · Gris obstáculo']
        for line in info:screen.blit(small.render(line,True,(211,221,233)),(px,y));y+=23
        if world.prey:
            pos=next(iter(world.prey));x=features(world,'prey',pos,world.prey[pos]);act=int(nets['prey'].predict(x[None,:])[0]); labels=['↖','↑','↗','←','•','→','↙','↓','↘']
            screen.blit(font.render(f'Decisión presa de muestra: {labels[act]}',True,(255,216,118)),(px,y+10))
        pygame.display.flip();clock.tick(12)
    pygame.quit()
if __name__=='__main__':main()

