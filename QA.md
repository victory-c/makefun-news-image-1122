# Local verification record

This is a record of actual local execution, not a make.fun score.

## Image and runtime

- Complete RGB PNG: 1024 × 1024 pixels, 121,838 bytes.
- SHA-256: `9b7ca5f66fcd9b9156280bf94c4583f57690d1ca8698e85abb8a74f7bb1a37cc`.
- Seven standard-library acceptance tests passed on CPython 3.13.18 and 3.14.9.
- Two independent subprocesses with different Python hash seeds and time zones produced byte-identical images matching the committed preview.
- Full signature, IHDR, chunk CRC, compressed-data, scanline-length and IEND checks passed.
- All 63 text runs are within the canvas. No text-to-text or illustration-to-text bounding-box intersections.
- A CPython 3.13 constrained probe passed with a 512 MiB address-space limit, 60-second CPU limit, audit-hook denial of network and child-process actions, and writes restricted to its output directory. Its output matches the reference SHA-256.
- One observed CPython 3.13 render took 2.057 seconds. This is a local measurement, not a promise about the grading container.
- Docker's socket was not accessible to this user. The constrained probe is not represented as a Docker run or a full reproduction of make.fun's isolation.

## Browser and reading checks

- Headless Chromium via Playwright decoded the PNG successfully.
- Preview displayed at exactly 1024 × 1024 on desktop and 390 × 390 at a 390-pixel viewport; no horizontal mobile overflow.
- The screenshot of the desktop image was pixel-identical to the original PNG using Pillow's pixel difference.
- No browser page errors or external network requests during the preview check.
- Screenshots are written to `out/desktop-final.png`, `out/mobile-final.png`, and `out/browser-image.png` by `tools/browser_check.mjs`.
- Tesseract.js English OCR on the second layout returned confidence 87 and exposed artwork intruding into paragraphs. The third layout moved the ship and chip and scaled the lower-row illustrations. New illustration-boundary regression tests passed. OCR returned confidence 88 on the corrected image and recovered the substantive headlines and body copy.
- OCR is an imperfect machine-reading check, not a substitute for human visual review. This session had no functioning vision/image-display tool, so no claim of agent visual inspection is made. Screenshots remain available for the user to inspect.

## Iteration record

1. Original renderer, palette, typography, seven-story composition, first rendered PNG.
2. Corrected temporal framing for Brazil's Sunday toll update, reduced baked typography from 100 font instances to the 17 actually used, corrected the sports-strip illustration fit, added dated primary reporting notes and deterministic tests.
3. Moved/scaled artwork after OCR exposed paragraph interference; added geometry-based illustration collision regression coverage; exercised desktop/mobile Chromium and exact Python 3.13 constrained execution.

Each stage was committed and pushed without rewriting history.

## Kit boundary

The authoritative RULES.txt says this competition has no local scoring grader. The required code-only kit check passes competition window, snapshot caps, MIT license, and Python entrypoint, but fails `transcripts_present` because the wrapper, not this build session, is responsible for bundling and submitting transcripts after the session exits. Transcript-dependent checks are consequently skipped. The wrapper must run the check again with its genuine recorded-session bundle before submission. No fake transcript, score, or submission receipt was created.
