# Elements-plan (prop sheets) — Easy-Taxi Belgium

De 4 vaste assets worden Higgsfield **Elements**. Elk Element krijgt een `element_id` dat we
in élke image/video-prompt injecteren via `<<<element_id>>>`, zodat identiteit locked blijft.

| Asset | Beschrijving | Model | Status |
|-------|--------------|-------|--------|
| `passenger` | Reiziger, man ~38, lichtblauwe polo + beige chino (lange broek) + witte sneakers | nano_banana | prop sheet gegenereerd |
| `driver` | Chauffeur, man ~45, antraciet polo + zwarte broek/schoenen | nano_banana | prop sheet gegenereerd |
| `mercedes` | Zwarte Mercedes E-Klasse sedan + subtiel taxi-daklicht | nano_banana | prop sheet gegenereerd |
| `suitcase` | Antraciet hardshell trolley, 4 wielen | nano_banana | prop sheet gegenereerd |

## Werkwijze video (na goedkeuring prop sheets)
- Frames: `nano_banana_2` met de Elements erin → start/eind-frames per shot.
- Video: `seedance_2_0` (sterke identiteit) of `kling3_0` (multi-shot, start+eind-frame, audio).
- 9:16 output, ~2–2.5s per clip.

## Logo / eindkaart
- Easy-Taxi Belgium logo = echte PNG, als overlay bij montage (NIET AI-hergenereerd).
- CTA: "Taxi nodig voor uw vakantie? Vul het formulier in"
