# Slopcannon cookbook sources

- This skill was built by cookbook archaeology. Patterns were taken from real usage in the WuBuTV repo, not invented from documentation alone.

- WuBuTV sources mined for patterns. The Slopcannon SLERM study in `musicvideo/notes/SLOPCANNON_SLERM_STUDY.md`. The staff workflow in `musicvideo/notes/MUSIC_VIDEO_WORKFLOW.md`. The Suno intake rules in `musicvideo/intake/README.md`. The STATION ledger and learning log for QC classes, wordmark gates, cliff handling and take history discipline.

- Public workflow shape studied. An AI music video workstation takes a song, named character references and a plot, and returns a timed video with scene by scene rerolls. That shape is public. No UI, credit system, branding or prompt format from that workstation was copied.

- Agent skill method studied. Anthropic Agent Skills use a folder with a `SKILL.md` file, YAML frontmatter with name and description, and progressive disclosure across three levels. The skill body stays lean and references load on demand.

- Cookbook method studied. Find patterns that repeat across three or more real examples, name each pattern after the use case it solves, stress test it, codify it and audit it. That method produced the five stages in this skill.

- Anti-slop gates studied. A pipeline that fires fluent output at scale without catching its own errors is a slop cannon in the bad sense. This skill avoids that shape with split stages, a QC pass with a checklist, take history, precision rerolls and a budget review before every volley. Confidence stays visible in the plan and the cutlist, never hidden in a confident caption.
