# Laminate Talk content spec

Learner: Kemal, a Turkish mechanical engineer, expert in composite materials (analysis, calculations, manufacturing: prepreg, autoclave, RTM, NDT/UT, laminate theory, certification). He wants spoken English fluency for work meetings. No grammar teaching.

## Dialogue file format (UTF-8 text, one item per line, blank lines allowed)
```
## <id> | <English tag, 1-2 words> | <Turkish title> | <group>
brief: <Turkish: the situation and what the learner must explain, 1-2 sentences>
role: <English: who the partner is and what they care about, one line, lowercase start "a ...">
### 1
ideas: <Turkish point> ; <Turkish point> ; ...
chunks: <English chunk> = <Turkish gloss> ; ... (exactly 5)
T: <English> | <Turkish>
Y: <English> | <Turkish>
... (exactly 8 lines, alternating T, Y, T, Y..., starting with T)
### 2
... same
### 3
... same
```
- T = the partner (colleague, manager, customer...). Y = the learner (Kemal himself; he may be called Kemal).
- Separators are exact: ` | ` between English and Turkish, ` ; ` between items, ` = ` inside a chunk. Never use `|`, ` ; ` or ` = ` inside the text itself. Use `…` (single char) for an open chunk ending, like "The reason is that…".
- Level 1 (Temel): very short simple sentences, max 10-12 words, present/simple past. Level 2 (Orta): up to ~18 words, linking words (because, so, but, if), numbers. Level 3 (İleri): natural senior-colleague meeting English, idiomatic, precise technical vocabulary, 15-30 words for Y lines.
- The same story across the 3 levels (same facts), told more richly at higher levels.
- Chunks: reusable multi-word phrases (lexical chunks) that appear in that level's Y lines, useful in many meetings.
- Realistic composite-industry details: numbers, dates, materials, parts (brackets, panels, spars, fairings), standards, euros.
- Weave in naturally as many words as fit from the uncovered Oxford 3000 list (file un.txt in the same folder, space-separated). Never force a word that sounds wrong.
- Turkish must be natural, correct Turkish (not word-by-word).

## ideas: line (speaking plan for a 4/3/2 monologue)
The learner retells the topic alone as a short talk (like briefing a meeting). `ideas:` gives 4-6 Turkish prompts, in speaking order, of WHAT to say, not translations of dialogue lines. Each prompt is a short instruction with the concrete facts, e.g. "Durumu söyle: kalıp iki hafta gecikti" ; "Nedenini açıkla: tedarikçi teslim tarihini kaçırdı" ; "Etkisini anlat: ilk parça muayenesi mart sonuna kayıyor" ; "Kurtarma planını anlat: cumartesi mesaisi, paralel hazırlık" ; "Maliyeti ve riski belirt" ; "Sonraki adımı ve ne zaman bilgi vereceğini söyle". Level 1: 4 prompts, simple. Level 2: 5. Level 3: 5-6 including nuance (risk, trade-off, what you need from the listener). Prompts start with a Turkish imperative verb (Söyle, Açıkla, Anlat, Belirt, Öner, Sor...). Do not use ` ; ` inside a prompt; use commas.

## Validate
Run `python3 parse.py` in the folder; it must print without errors. It parses all d*.txt and i*.txt files.
