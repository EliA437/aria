# Project Roadmap

### Phase 1: Foundation & Dataset 
- [ ] Decide chord encoding strategy (Roman numerals, pitch classes, etc.)
- [ ] Document music theory rules
- [ ] Collect/download chord datasets (jazz, pop, blues, classical, R&B)
- [ ] Create CSV format for progressions
- [ ] Validate dataset quality (spot-check 20 per genre)
- [ ] Create small test set for quick iteration

**Deliverable**: `dataset/raw/` with genre-specific progressions, `MUSIC_THEORY.md` written

---

### Phase 2: Model Training 
- [ ] Write data preprocessing script
- [ ] Design LSTM/Transformer architecture
- [ ] Implement training loop with validation
- [ ] Train baseline model (single genre)
- [ ] Expand to multi-genre with conditioning
- [ ] Evaluate model (accuracy, valid progressions %)
- [ ] Export to ONNX and quantize

**Deliverable**: `models/chord_generator.onnx`, trained model checkpoint, `RESULTS.md`

---

### Phase 3: JUCE Plugin Scaffold 
- [ ] Set up JUCE project with CMake
- [ ] Integrate ONNX Runtime C++ library
- [ ] Implement model inference wrapper
- [ ] Create basic plugin UI (genre, seed, length, temperature)
- [ ] Implement MIDI output
- [ ] Test in DAW (Reaper)

**Deliverable**: Working plugin loads and generates MIDI chords in DAW

---

### Phase 4: Integration & Testing 
- [ ] End-to-end testing across genres
- [ ] Performance profiling (latency, CPU)
- [ ] Cross-platform build (macOS + Windows)
- [ ] Optional: Model optimization (quantization, pruning)

**Deliverable**: Plugin builds and runs on macOS and Windows

---

### Phase 5: Polish & Documentation 
- [ ] UI/UX improvements (colors, tooltips, presets)
- [ ] Write comprehensive README
- [ ] Write ARCHITECTURE.md, TRAINING.md, BUILD_INSTRUCTIONS.md
- [ ] Create demo video (2–3 min)
- [ ] Generate example MIDI outputs per genre

**Deliverable**: Complete documentation and demo video

---

### Phase 6: Shipping & Resume 
- [ ] Final code cleanup and review
- [ ] Create GitHub Release (v1.0.0)
- [ ] Update resume and LinkedIn
- [ ] Prepare for interviews (practice demo, technical talking points)

**Deliverable**: Public release, resume updated, interview-ready

---

## Nice-to-Haves 

- Preset system (save/load settings)
- Alternative model architectures
- MIDI input support (continue from user progression)
- Sheet music visualization
- Blog post about the project
- CI/CD pipeline (GitHub Actions)