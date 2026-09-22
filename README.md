# aria
An AI model specialized in music theory, with a user-friendly interface, for your DAW.

## Quick Start

### Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Build
```bash
cd plugin/
mkdir build && cd build
cmake ..
cmake --build . --target chord-vst_VST3
```

### Train
```bash
python training/preprocess.py
python training/train.py --config training/config.yaml
python training/export_onnx.py
```

## Documentation

- [ROADMAP.md](./ROADMAP.md) — Project timeline

## License

MIT License