# Audio Design 

Scope: audio resource organization, random sampling for variety, dB level standards for audio mixing, and procedural fallback behavior across all gameplay SFX.

<!-- acceptance-status-summary:start -->
Summary: 6💡 5🔧 0💻 0🎮 0✅ 0⚠️ 0⛔ 0🗑️
<!-- acceptance-status-summary:end -->




---

## Overview

This document establishes standards for:
- **Random Audio Sampling**: Using multiple audio samples to provide acoustic variety while maintaining consistent playback behavior.
- **dB Level Standards**: Calibrated loudness targets for mixing across different SFX categories.
- **Resource Organization**: Directory structure and naming conventions for audio assets.
- **Procedural Fallback**: Automatic synthetic fallback when audio assets are unavailable.

---

## Resource Organization

### SSVR-0019: Audio folder structure by category
- **Status:** 🔧 Implemented
- Given audio assets are distributed across gameplay categories
- When placing new audio files
- Then place them in one of the following organized locations:
  - `Assets/Resources/Audio/Gunshots/` — real firearm discharge recordings
  - `Assets/Resources/Audio/Plates/` — steel target impact sounds (prefix-sorted by size: `8in_`, `10in_`, `12in_`, `14in_`, `gong_`)
  - `Assets/Resources/Audio/range-officer/` — timer/range-officer call-outs (e.g., `shot-timer_*.wav`, `shooter-ready-*.wav`)
  - `Assets/Resources/Audio/range-officer-2/` — additional timer/range-officer call-outs that belong in the same playback pool
  - `Assets/Resources/Audio/small gunshots/` — secondary gunshot library for variant playback
- And files follow lowercase naming with underscores for multi-word identifiers.

---

## Random Audio Sampling

### SSVR-0020: Random sampling for repeated gameplay events
- **Status:** 🔧 Implemented
- Given a gameplay event fires multiple times per session (e.g., start timer beeps, target rings)
- When the event is triggered
- Then the audio system selects a random clip from an available sample pool
- And sequential plays of the same event use different samples (acoustic variety)
- And non-gunshot events fall back to procedurally generated audio if no real samples exist.

> **Examples:**
> - `RandomStartBeep()` selects one of the loaded range-officer / shot-timer callout samples.
> - `RandomPlateImpact()` returns random samples from the `Plates` folder or related root-audio matches.
> - `RandomLoadedGunshot()` returns random real gunshot samples.

### SSVR-0021: Non-gunshot fallback behavior when samples are unavailable
- **Status:** 🔧 Implemented
- Given a non-gunshot random-sampling audio method is called
- When the sample pool is empty (no assets loaded)
- Then the system automatically generates a synthetic procedural tone as fallback
- And the fallback tone has equivalent loudness to real samples for mix consistency.

> **Examples:**
> - `RandomStartBeep()` → falls back to `StartBeep()` (1000 Hz tone, 0.11s duration, 0.55 amplitude).
> - `RandomPlateImpact()` → falls back to `TargetRing()` (1400 Hz tone, 0.22s duration, 0.35 amplitude).

### SSVR-0022: Gunshot playback prefers real authored clips and never synthesizes a fake gunshot fallback
- **Status:** 🔧 Implemented
- Given firearm discharge audio is triggered
- When the game resolves which clip to play
- Then an explicitly assigned firearm `shotClip` is preferred first
- And otherwise the game selects from real gunshot assets loaded from `Resources/Audio`
- And the gunshot path does not fall back to a procedural synthetic gunshot tone.

### SSVR-0023: Local gunshot playback preserves authored clip fidelity
- **Status:** 🔧 Implemented
- Given a real gunshot WAV is used for the local in-hand firearm
- When that clip is imported and played back in Unity
- Then the import path keeps the clip unnormalized, non-3D, PCM, preserve-sample-rate, and decompress-on-load
- And the local firearm `AudioSource` plays it as a non-spatialized in-hand sound without doppler or reverb coloration
- And the runtime does not accidentally make the shot sound pitched-up, phasey, or overprocessed relative to the source asset.

> **Implementation notes:** `CreateStageSceneTool.FirearmFactory` now enforces the gunshot importer settings during scene/firearm generation, and `FirearmController.ConfigureAudioSourceForLocalGunshotPlayback()` neutralizes local-source playback settings for the player's own gunshot.

### SSVR-0024: Prefix-based random clip selection
- **Status:** 💡 Proposed
- **Priority:** 🔵 P4 - Eventually
- Given steel target sounds are organized by size prefix (e.g., `8in_`, `12in_`, `gong_`)
- When a target is hit
- Then the audio system retrieves clips matching the target's size category
- And returns a random sample from that bucket
- And falls back to a broader category (e.g., `12in_` as universal fallback) if the preferred size has no samples.

> **See also:** [SSVR-0369](steel-target.md#ssvr-0369-steel-ring-sound-signature-by-size) — Steel ring sound by size.

---

## dB Level Standards

### SSVR-0025: Standard loudness dB target
- **Status:** 💡 Proposed
- **Priority:** 🔵 P4 - Eventually
- Given audio is mixed for consistent gameplay clarity
- When recording or processing audio samples
- Then normalize master clips to **−14 dBFS ± 1 dB** (−13 dBFS to −15 dBFS acceptable range)
- And reserve peaks up to **−3 dBFS** for occasional emphasis events (e.g., critical beeps, boss warnings).

> **Rationale:** −14 dBFS provides adequate headroom (~10 dB) before digital clipping in a standard QA environment while maintaining perceived loudness. Individual gameplay events (gunshot, impact) can peak within −3 dBFS to −6 dBFS without causing listener fatigue.

### SSVR-0026: Loud/emphasized event dB target
- **Status:** 💡 Proposed
- **Priority:** 🔵 P4 - Eventually
- Given certain audio events signal critical gameplay moments (e.g., false-start warning, boss activation)
- When these events are recorded or processed
- Then normalize them to **−9 dBFS ± 1 dB** (−8 dBFS to −10 dBFS acceptable range)
- And ensure peaks do not exceed **−3 dBFS** to avoid distortion.

> **Rationale:** This provides ~5 dB of perceived loudness increase vs. standard (≈1.4× perception), creating clear auditory distinction for warnings without aggressive clipping.

### SSVR-0027: dB is exponential, not linear
- **Status:** 💡 Proposed
- **Priority:** 🔵 P4 - Eventually
- Given audio engineers must account for logarithmic change in amplitude
- When adjusting dB levels for mixing or mastery
- Then calibrate expectations with the following reference:
  - **Every 6 dB change ≈ 2× change in perceived loudness** (approximately 1.995× amplitude).
  - **Every 20 dB change = 10× change in amplitude** (e.g., −14 dBFS is 10× smaller amplitude than −−6 dBFS).
  - **Formula: Amplitude = 10^(dB/20)** — this is the exponential relationship (dB uses a logarithmic scale).
  - Relative dB charts: A source at −6 dBFS vs. −12 dBFS has 2× the amplitude and ~1.4× perceived loudness.

> **Practical Example:**
> - Standard: −14 dBFS (amplitude = 10^(−14/20) ≈ 0.20)
> - Loud: −9 dBFS (amplitude = 10^(−9/20) ≈ 0.35) → 1.75× the amplitude, ≈1.2× louder perception.
> - Comparison: −3 dBFS (amplitude = 10^(−3/20) ≈ 0.71) vs. −14 dBFS → ~3.5× amplitude, ≈2.5× louder perception.

### SSVR-0028: Procedural fallback tone levels
- **Status:** 💡 Proposed
- **Priority:** 🔵 P4 - Eventually
- Given procedurally generated tones serve as fallback for missing real audio
- When `DefaultAudioClips` synthesizes tones
- Then calibrate their amplitude parameter to match expected dB mixing targets
- And test tones against real sample mixes to verify perceived loudness parity.

> **Current Mapping:**
> - `TriggerReset()` — 650 Hz, 0.035 s, **0.25 amplitude** (standard event level).
> - `StartBeep()` — 1000 Hz, 0.11 s, **0.55 amplitude** (emphasized event level).
> - `TargetRing()` — 1400 Hz, 0.22 s, **0.35 amplitude** (standard impact level).
> - `ShooterReady()` — 520 Hz, 0.12 s, **0.45 amplitude** (standard callout level).

---

## Fallback and Mixing

### SSVR-0029: Never silent — fallback to procedural tone
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given the game depends on audio feedback for immersion and accessibility
- When a gameplay event requires audio feedback
- Then the audio system must never play silence
- And if real asset loading fails, procedural fallback audio shall play instead
- And the fallback shall be registered in error logs for content pipeline visibility.

> **Implementation:** `DefaultAudioClips` procedurally generates all fallback tones; random-selection methods return real clips if available, or fallback-tone methods otherwise.

---

## Updates to Audio Resource Metadata

When adding new audio categories or sample pools:

1. **Update this AC document** with the new folder location and naming scheme.
2. **Add a new static list and loader method** to `DefaultAudioClips` (following `EnsureRangeOfficerClipsLoaded()` and `LoadRangeOfficerClipsFromResources()` pattern).
3. **Add a public random-selection method** (e.g., `RandomStartBeep()`) that returns clips from the pool with automatic fallback.
4. **Document dB level expectations** in the folder's README or this AC if the new category differs from standard.

---

## Related Audio Criteria

- [SSVR-0146](gong-button.md#ssvr-0146-gong-strike-sound-signature) — Gong strike sound auditory feedback.
- [SSVR-0369](steel-target.md#ssvr-0369-steel-ring-sound-signature-by-size) — Steel target impact audio by size.
- [SSVR-0371](steel-target.md#ssvr-0371-repeated-impact-audio-variation) — Impact audio variation for repeated hits.
- [SSVR-0372](steel-target.md#ssvr-0372-steel-ring-sound-sourced-from-wav-asset) — Steel ring sound must use a WAV asset, not a procedural tone.
- [SSVR-0373](steel-target.md#ssvr-0373-per-shot-pitch-variation-on-ring-sound) — Per-shot pitch randomization for ring sound naturalness.
- [SSVR-0006](accessibility.md#ssvr-0006-audio-cue-customization) — Audio cue customization for accessibility.
