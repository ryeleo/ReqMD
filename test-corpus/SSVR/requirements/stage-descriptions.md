# Stage Descriptions 

Scope: `.stage` file authoring format, parser behavior, defaults, and runtime consumption contract.

<!-- acceptance-status-summary:start -->
Summary: 2💡 1🔧 0💻 0🎮 15✅ 0⛔ 0🗑️
<!-- acceptance-status-summary:end -->





## File Location And Discovery

### SSVR-0341: Stage files live under resources stage path
- **Status:** ✅ Done
- Given stage descriptions are authored for runtime discovery
- When they are added to the project
- Then `.stage` files are stored under `Assets/Resources/Stages/` so Unity can load them as text assets.

### SSVR-0342: Stage builder can consume assigned stage file
- **Status:** ✅ Done
- Given a `.stage` text asset is assigned to `StageBuilder`
- When stage build is triggered
- Then the assigned stage file is parsed and used as the source stage definition.

### SSVR-0343: Fallback behavior without assigned stage file
- **Status:** ✅ Done
- Given no stage file is assigned to `StageBuilder`
- When stage build is triggered
- Then the builder falls back to the hardcoded Smoke and Hope layout.

## Top-Level File Structure

### SSVR-0344: Stage file uses name and targets sections
- **Status:** ✅ Done
- Given a valid `.stage` file
- When the parser reads the file
- Then it supports a top-level `name:` field and a top-level `targets:` section.

### SSVR-0345: Targets section must be indented under column-zero key
- **Status:** ✅ Done
- Given a `.stage` file contains target entries
- When the parser evaluates structure
- Then the `targets:` key is expected at column 0
- And individual target lines are expected to be indented beneath it.

### SSVR-0346: Comments are ignored
- **Status:** ✅ Done
- Given a `.stage` file contains comment lines beginning with `#`
- When parsing occurs
- Then those comment lines do not affect the resulting stage definition.

### SSVR-0347: Stage file supports optional description field
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given a `.stage` file is authored
- When a top-level `description:` field is present
- Then the parser reads it as a free-form string
- And it may span multiple lines or be left empty without affecting parse or runtime behavior.

## Target Specification Syntax

### SSVR-0348: Target specs are quoted pipe-separated strings
- **Status:** ✅ Done
- Given a target entry is defined in a `.stage` file
- When it is parsed
- Then the target value is a quoted string containing three or four pipe-separated fields.

### SSVR-0349: Size field supports canonical target sizes
- **Status:** 💡 Proposed
- **Priority:** 🟡 P2 - Medium
- Given plates are round with a diameter, and gongs are 18x24 portrait rectangles
- When the parser evaluates targetsize
- Then it supports sizes valid Target sizes: 
    - `gong` or `18inx24in` or `18x24`, 
    - `32in` or `32`, 
- **Status:** ✅ Done
    - `28in` or `28`, 
    - `26in` or `26`, 
    - `24in` or `24`, 
    - `22in` or `22`, 
    - `20in` or `20`, 
    - `18in` or `18`, 
    - `16in` or `16`, 
    - `14in` or `14`, 
    - `12in` or `12`, 
    - `10in` or `10`, 
    - `8 in` or `8`, 
    - `6in` or `6`,
    - `4in` or `4`,
    - `2in` or `2`,


### SSVR-0350: Distance field uses yards
- **Status:** 🔧 Implemented
- Given a target spec distance field is provided
- When the parser evaluates distance
- Then yard-based formats like `7yd`, `7 yd`, `7 yard`, and `7 yards` are accepted as equivalent meanings.

### SSVR-0351: Offset field supports left, right, and center forms
- **Status:** ✅ Done
- Given a target spec offset field is provided
- When the parser evaluates lateral offset
- Then left and right offsets in feet are accepted
- And centered forms like `center`, `centered`, or `0` are accepted.

### SSVR-0352: Decimal feet are the preferred new-file notation
- **Status:** ✅ Done
- Given new `.stage` files are authored
- When offsets or heights are written
- Then decimal feet are treated as the preferred notation for clarity and compute-friendliness.

### SSVR-0353: Optional height field is supported
- **Status:** ✅ Done
- Given a target spec includes a fourth pipe-separated field
- When the parser evaluates the target
- Then that fourth field is interpreted as target center height above ground.

### SSVR-0354: Omitted target height uses target-type defaults
- **Status:** ✅ Done
- Given a target spec omits the optional height field
- When the target is parsed
- Then the parser or builder applies the documented default target height behavior for the target type.

## Stop Plate Semantics

### SSVR-0355: Stop Plate label is auto-detected
- **Status:** ✅ Done
- Given a target label is `Stop Plate` or `stop`
- When the parser builds target definitions
- Then that target is marked as the stop plate for the stage.

## Runtime Consumption Contract

### SSVR-0356: Stage definitions feed stage scene geometry
- **Status:** ✅ Done
- Given a stage definition has been parsed successfully
- When `StageBuilder` consumes it
- Then the parsed stage definition is used to build the scene geometry for that stage.

### SSVR-0357: Bay theming is not authored in stage files
- **Status:** ✅ Done
- Given a `.stage` file is authored
- When bay materials and surface theming are configured
- Then bay theming remains controlled by `StageBuilder` inspector overrides
- And not by the `.stage` file schema.
