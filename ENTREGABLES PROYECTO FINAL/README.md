# Entregables del proyecto NeuroEcosistema

Esta carpeta reúne el informe, la bitácora y los datos con los que se pueden revisar las conclusiones. El código de la simulación está en la raíz del repositorio, dentro de `neurito_ecosistema/`; las instrucciones completas están en el `README.md` de la raíz.

## Archivos incluidos

- `INFORME_TECNICO.docx` y `INFORME_TECNICO.pdf`: informe de cuatro páginas.
- `INFORME_TECNICO.md`: versión editable del informe.
- `BITACORA_DECISIONES.md`: nueve decisiones, las alternativas consideradas y su justificación.
- `AUDITORIA_PROPUESTA.md`: revisión de requisitos y temas que se deben explicar en la sustentación.
- `evidencia/episodios.csv`: detalle de los 360 episodios.
- `evidencia/resumen.csv` y `resumen.json`: métricas resumidas y comparaciones.
- `evidencia/graficas/`: supervivencia por escenario y pérdida durante el entrenamiento.
- `modelos/`: pesos de las dos redes y resumen del entrenamiento.

Para ejecutar la simulación, abre PowerShell en la raíz del repositorio, instala lo indicado en `requirements.txt` y ejecuta `python -m neurito_ecosistema.visualizar`. En Windows también está el acceso directo `INICIAR_SIMULACION.bat`.

El resultado principal es que la red aprendió a imitar la regla experta, aunque la política aleatoria dejó más presas vivas en los tres escenarios. El informe presenta ese resultado sin atribuir a la red una ventaja que las pruebas no mostraron.
