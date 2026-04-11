#!/bin/bash
# Pre-generation gate hook
# Runs before any AIMLAPI API call to enforce model prompting guide consultation
# This hook prints a mandatory checklist that must be acknowledged

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           PRE-GENERATION GATE — MANDATORY CHECK             ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║ Before this generation, confirm you have:                   ║"
echo "║                                                             ║"
echo "║ □ Consulted model-prompting-guide.md for this shot type     ║"
echo "║ □ Selected model per routing matrix (Part 6)                ║"
echo "║ □ Used character identity header (Part 4) if people visible ║"
echo "║ □ Hero frame is native 9:16 with aspect_ratio param         ║"
echo "║ □ NO text/logos that will be in the animated video           ║"
echo "║ □ Motion prompt is 15-40 words, motion ONLY, has endpoint   ║"
echo "║ □ Negative prompt includes full template from guide          ║"
echo "║ □ generate_audio: false                                      ║"
echo "║ □ Reference images included (NBP Edit / Kontext Max)         ║"
echo "║ □ Budget check: this generation costs \$___                   ║"
echo "║                                                             ║"
echo "║ If ANY box is unchecked, DO NOT PROCEED.                    ║"
echo "╚══════════════════════════════════════════════════════════════╝"
