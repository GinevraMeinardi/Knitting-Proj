# KnittingProj

Simulatore di maglia che stima, con un modello geometrico, la quantità di
filato necessaria per un numero dato di maglie. Il nucleo di calcolo è in
C++20; script Python si occupano di fit e visualizzazione 3D
(matplotlib, PyVista).

## Come funziona
[Come modelli la singola maglia: curva, parametri, assunzioni.
Cosa viene fittato in Python e su quali dati.]

## Funzionalità
- [x] Stima lunghezza del filato per un numero x di maglie in stockinette
- [ ] Implementazione di punti più complessi: rib, cables, colorwork, increases/decreases
- [ ] Pattern personalizzati
- [ ] Stima in lunghezza e in peso per un pattern completo

## Requisiti
- Compilatore C++ con supporto C++20 (g++ da MSYS2 MinGW64)
- Opzionale: `make`
- Python 3.x con: numpy, matplotlib, pyvista

## Compilare ed eseguire

Da prompt dei comandi (Windows), spostati nella cartella del progetto:

```cmd
F:
cd percorso\del\progetto
```

**Con g++ direttamente:**

```cmd
g++ -std=c++20 Shape.cxx Swatch.cxx Test.C -o knit_calculator.exe
knit_calculator.exe
```

**Con il Makefile:**

```cmd
make
knit_calculator.exe
```

oppure `make run` per compilare ed eseguire in un colpo solo.

### Installare make su Windows
Da terminale MSYS2 MINGW64:

```bash
pacman -S mingw-w64-x86_64-make
cp /mingw64/bin/mingw32-make.exe /mingw64/bin/make.exe
```

Poi, da cmd, verifica con `make --version`.

## Script Python
- `stitch-parametric-curve.py`: visualizza con Matplotlib la curva parametrica 3D e ne calcola la lunghezza integrandola
- `stitch-parametric-curve-pyvista.py`: come sopra ma in pyvista per ovviare bug grafici, crea anche una gif della visualizzazione 3D
- `interpolation.py`: plot 2D + fit lineare dei 3 modelli insieme alle misure reali


## Limiti noti
- incertezza realtiva alta: le maglie sono dell'ordine di qualche mm e il righello ha incertezza di 1mm
- al momento non si parametrizza l'elasticità del filo
- da capire se la comprimibilità del filo incide in maniera significativa

