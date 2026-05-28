# Intervalos do AGENT

Os intervalos de AGENT representam blocos de raciocínio autônomo (agentes ReAct, ciclos de planejamento, tomada de decisão em várias etapas).

**Obrigatório:** `openinference.span.kind` = "AGENT"

## Exemplo

```json
{
  "openinference.span.kind": "AGENT",
  "input.value": "Book a flight to New York for next Monday",
  "output.value": "I've booked flight AA123 departing Monday at 9:00 AM"
}
```
