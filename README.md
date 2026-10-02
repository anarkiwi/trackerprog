# trackerprog

C64 SID tune decompilation on [deity-informant](https://github.com/anarkiwi/deity-informant)'s 6510 lifter and P-Code VM. `tuneprog` turns a `.sid` into a certified per-tick program plus pseudocode; `trackerprog` binds that program's planes to one universal tracker player, certified against the VM.

## Components

- `tuneprog/` — the tuneprog decompiler: pipeline S0-S8, IR, verification and certificates (`docs/tuneprog-architecture.md`). `tuneprog/deity.py` locates the deity-informant source checkout (`$DEITY_INFORMANT_SRC`) for its SLEIGH build and demo.
- `trackerprog/` — the trackerprog: `universal.py` (the one player), the binding lift (`bind.py`, `lift.py`), and `passes/` (the L0-L6 compiler passes).
- `ghidra/6510/headless/` — Ghidra headless oracles over deity-informant's 6510 SLEIGH module: `ExportHighPcode.java` (facts-driven high P-Code/C export), `EmulateTrace.java` (P-Code emulator semantic oracle), `run.sh` (run via `Dockerfile.ghidra`).
- `docs/tuneprog-architecture.md` — **the canonical tuneprog reference**: definitions, pipeline S0-S8, the lift end to end, the IR, verification and the certificate schema, presentation, CLI and tools, the machine model and its boundaries, the certified exemplars, the module map, the process.
- `docs/playroutine-anatomy.md` — field guide: nine C64 playroutines reverse engineered to the byte (Hubbard, Galway, Follin, Walker, JCH, GoatTracker, SID Wizard, defMON, lft's Blackbird), the 6502 technique catalogue behind them, and what a decompiler must model.
- `docs/tuneprog-backlog.md` — open tuneprog work by lever (mechanism, evidence, owner, size, acceptance), the done ledger, the execution order.
- `docs/prototype-trackerprog.md` — the trackerprog specification: the object, its observable and certificate, the schema, the universal player, bounded accumulators, the T0-T3 lift, refusals and acceptance.
- `docs/trackerprog-backlog.md` — open trackerprog work (mechanism, size, acceptance command), the six settled decisions, the checks a tenth family must run, the presentation gaps.
- `docs/trackerprog-review.md` — the critical review of the player and the spec: the verdict, the per-row outcome, and what measurement refuted.
- `docs/prototype-*-trackerprog.md` — nine hand transliterations, one per family (Hubbard, GoatTracker 2, SID Wizard, defMON, JCH V20, Follin, Blackbird, Walker, Galway): ground truth, the forms the family forced, and its certificate numbers.
- `docs/prototype-automatas.md`, `-follin.md`, `-goattracker.md`, `-sidwizard.md`, `-jch.md` — the certified exemplars (defMON, Follin's *Ghouls'n'Ghosts*, GoatTracker 2, SID Wizard 1.6/1.9, JCH NewPlayer V20): ground truth, what broke, the generic fix, the evidence.
- `docs/prototype-kernal-entry.md` — the installed-handler family (PSID `play == 0`, CINV entries): entry convention, screened population, two evidence certificates.
- `docs/prototype-nmi.md` — the second interrupt (a CIA #2 NMI as the schedule's second entry): the population by handler kind, the chip model it needed, the interleaving against `sidplayfp`, the first two-entry certificate.
- `docs/prototype-lifter.md` — the trackerprog as a **binding** of a certified tune's planes to the one player: S6's roles and T2's cursors bound to the player's own cells, T2's score as section 3.6's fields, T1's records as section 5's, T0's write sites as what produces. Commando song 1 renders at 0 divergences over 11,780 ticks at 1.42x its load band (the hand reading's 1.36x, the lowering it replaced 2.46x); *Guldkornekspressen Intro* runs through the same emitter and diverges at tick 0, with the field it names.
- `docs/prototype-passes.md` — the tuneprog-to-trackerprog lift stated as **compiler passes**: six levels (structured tick, phase-normal form as a region tree, typed, materialised, selected, canonical), each validated by rendering it against the level before it; the idioms the nine families forced, one code path a level; the construct expansions round-tripped over all 1,190 instances of the thirty hand objects (1,135 expandable, all of them out and back, all 296 accumulator records among them, 55 named by the one form no expansion reaches); one synthetic program taken L0 to L6 at 0 divergences; and the nine families from L0 as a measured surface (`tools/trackerprog_surface.py`), where L1 holds on eight of ten subjects over their whole horizons, L2 holds on none, and no level above L2 has yet run on a real tune.
- `docs/prototype-commando-floor.md` — the complexity floor of one simple tune: print cost against the tune's own bytes, where its statements live, a hand-factored form, and the region-typing rule that would produce it.
- `docs/survey-tuneprog.md` — the pipeline over the stratified 7,023-tune HVSC sample: certification rate by family, failure classes, refusal reasons, stack/entry/fold distributions, cost and the fast-tracer verdict.
- `docs/ghidra-highpcode-export.md` — the independent baseline: SMC cells as SLEIGH context values, the facts export, the headless high-P-Code/C export, and the oracles comparing Ghidra with the tuneprog.
- `tools/` — `tuneprog_certify.py` (end-to-end certification driver, chunked against a CPU budget; `docs/certificates/` holds the exemplars' certificates), `tuneprog_recert.py` (reproduces every certificate and diffs it field for field), `tuneprog_period.py` (why a subtune has no state repeat: counter, drifting accumulator, or aperiodic), `tuneprog_floor.py` (load-band split, `xz` description lengths, printed statements by code range and kind, 16-bit pair check).
- `tools/trackerprog_*.py` — one hand transliteration per family, each rendered by `trackerprog/universal.py` and certified against the PcodeVM (`--certify --source <tuneprog certificate>`; `--budget`/`--resume` where a horizon exceeds one invocation), plus `trackerprog_sizes.py` (section 9.1's object-against-load-band table, or one object with `--object`) `trackerprog_poison.py` (the poison harness: an object, a stated mutation and a build set, rendered both ways over each build's whole horizon) and `trackerprog_surface.py` (the L0-to-L6 surface over the certified exemplars: how far each tune gets, and the cause where it stops).
- `tools/survey/` — HVSC survey instruments behind `docs/tuneprog-architecture.md` §9.3: `tracer.py` (dynamic per-site tracer on `PcodeVM`), `run.py` (stratified parallel driver), `headers.py` (static census), `report.py` (markdown tables), `tuneprog_sweep.py` (the whole pipeline over the same sample, resumable), `tuneprog_report.py` (its tables).
- `tools/doclinks.py` — every `[text](target)` in `docs/` and `README.md` resolved: the file, and the `#anchor` against the target's own headings.

## Install

```bash
git clone https://github.com/anarkiwi/deity-informant && pip install -e "deity-informant[dev]"
pip install -e ".[dev]"          # + ".[oracle]" for pysidtracker (sidplayfp oracle, needs Docker + HVSC)
```

deity-informant is installed from a source checkout because the SLEIGH build (`ghidra/6510/`) and `examples/hello_world.py` are not in its wheel; set `DEITY_INFORMANT_SRC` if the checkout is not the one `deity_informant` is imported from.

## CLI

```bash
tuneprog TUNE.sid --out DIR [--song N | --songs all] [--seconds S | --calls N | --until-period] \
         [--sid-model 6581|8580] [--no-merge] [--closure trace|static] [--resume] [--budget S] [--no-verify] [--no-text]
```

## Python API

```python
from tuneprog import find_entries, run_trace, pipeline, printer, verify
image, schedule = find_entries(open("tune.sid", "rb").read())
trace = run_trace(image, schedule[0], calls=1000)         # S0/S1: one instrumented run
prog, regions, procs = pipeline.build(trace, "tune.sid")  # S2/S3/S4: the certified program
cert = verify.certify(prog, verify.verify(prog, trace))   # S8: per-call equivalence + periodicity
view, structured, names = pipeline.present(prog)          # S5/S6 over a copy
text = printer.render(view, structured, names, cert)      # S7: the tuneprog.md artefact
```

```bash
python3 tools/tuneprog_certify.py TUNE.sid --out DIR --until-period --resume   # exit 2 = run again
python3 tools/tuneprog_recert.py --out out/recert --resume                     # reproduce every certificate
python3 tools/tuneprog_period.py TUNE.sid --song 1 --out DIR --resume          # why a subtune never repeats
```

## Ghidra

`docker build -f Dockerfile.ghidra -t tp-ghidra . && docker run --rm tp-ghidra` runs the headless smoke oracles (`--build-arg DEITY_REF=...` pins deity-informant); `.github/workflows/nightly.yml` runs the three oracles over every certificate.

## Tests

```bash
black --check tuneprog/ trackerprog/ tests/ tools/ ghidra/ && pylint tuneprog/ trackerprog/
pytest tests/ -m "not oracle and not hvsc" -n auto --cov=tuneprog --cov=trackerprog --cov-fail-under=85
pytest tests/ -m oracle -n auto      # sidplayfp oracle (Docker + HVSC)
pytest tests/ -m hvsc -n auto        # tuneprog front end + certificates on HVSC exemplars
```
