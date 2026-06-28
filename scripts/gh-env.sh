#!/usr/bin/env bash
# GitHub CLI config — use ~/.local/gh-config when ~/.config is not writable.
# Fixes: mkdir ~/.config/gh: permission denied (root-owned .config)
export GH_CONFIG_DIR="${GH_CONFIG_DIR:-$HOME/.local/gh-config}"
mkdir -p "$GH_CONFIG_DIR"
