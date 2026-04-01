# Bug Tracking

## Schema missing

This was happening when legacy-init generated its requirements index through a separate README builder instead of the shared init template path.

Current status:

- Fixed by `RQMD-AI-038`, which now makes legacy-init and related init apply paths generate the requirements index through the same shared template path used by scaffold init, including the local schema guidance.
- `RQMD-CORE-035` now tracks continuing the packaged-resource migration for shipped templates and schema snippets so this kind of init-doc drift is less likely.


## VS Code terminal grapheme-width issue for `⚠️ Janky`

So as a result, the "⚠️ Janky" status line appears to be missing some space between the emoji and the text compared to other lines.

Likely cause:

- The interactive menu width logic in `src/rqmd/menus.py` still relies on simple Unicode-width heuristics.
- `⚠️` uses a variation-selector sequence that appears to render differently in the VS Code integrated terminal than rqmd's current width model expects.
- This is now tracked as `RQMD-INTERACTIVE-032`.

This is the actual rendered output:
```
Status                    Priority          
  1) 💡 Proposed            !) 🔴 Critical  
→ 2) 🔧 Implemented         @) 🟠 High      
  1) 💻 Desktop-Verified    #) 🟡 Medium    
  2) 🎮 VR-Verified         $) 🟢 Low       
  3) ✅ Done                %) 🔵 Eventually
  4) ⚠️ Janky               ^) ☁️ Dreams    
```

But this is what it ends up looking like rendered in my VS Code terminal:
```
Status                    Priority          
  1) 💡 Proposed            !) 🔴 Critical  
→ 2) 🔧 Implemented         @) 🟠 High      
  1) 💻 Desktop-Verified    #) 🟡 Medium    
  2) 🎮 VR-Verified         $) 🟢 Low       
  3) ✅ Done                %) 🔵 Eventually
  4) ⚠️Janky               ^) ☁️ Dreams    
```

Next step:

- Replace or harden the current width calculation so right-column alignment is based on grapheme-safe terminal width behavior rather than brittle emoji-range assumptions.