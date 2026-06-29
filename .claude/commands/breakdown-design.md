# breakdown-design Command

Create a detailed step-by-step implementation plan for $ARGUMENTS with comprehensive before/after code examples
create file at .docs/year(YYYY)/month(MM)/day(DD)/{number-in-DD-folder(01)}-{Feature Spec}/{Feature Spec}-implementation-plan.md 
if requirement is clear or no have follow up question.
think hard and provide a comprehensive implementation plan with before/after code examples for each step.
follow YAGNI principle so dont create dead code or unnecessary files.
max 29000 characters. If the result exceeds 29000 characters, leave it as is — do NOT truncate, summarize, or drop sections to fit the limit. Completeness of the implementation plan takes precedence over the character cap.

## Template Structure

### Step-by-Step Implementation Plan with Before/After Code

Provide a breakdown that includes:
1. **Clear Step Numbering**: Each step should be numbered and have a descriptive title
2. **Before/After Code Blocks**: Show exact code changes for each step (add comments for code what you are changing)
3. **Technical Rationale**: Explain why each change is needed
4. **Dependencies**: Note any imports or setup required
5. **Testing Considerations**: How to verify each step works
6. **Observability logging**: Add logging at the appropriate level — see §Observability for the full Decision Guide:
   - `Timber.e(throwable, "…")` — errors with a Throwable (records a non-fatal in Crashlytics)
   - `Timber.e("…")` — errors without a Throwable (breadcrumb + pattern scan)
   - `Timber.w("…")` — degraded-behaviour paths in real app logic (breadcrumb + pattern scan)
   - `Timber.d("…")` — diagnostics + monitoring/instrumentation chatter (breadcrumb only)
   - `Timber.i("…")` — lifecycle / info-level milestones (breadcrumb only)
   Fall back to `Log.d/i/w/e("TAG", "…")` if Timber is not on the module classpath.
7. **Unit Testing**: Include unit tests for each step
8. **Flow Diagram Update**: Include an ASCII flow diagram showing the BEFORE and AFTER user/data flow (screen transitions, ViewModel ↔ UseCase ↔ Repository calls, branches, side-effects). Use ASCII box-drawing (`┌─┐ │ └─┘ → ↓ ↑`) — no Mermaid, no images. If the change does not alter any flow (pure refactor / cosmetic), write `Flow Diagram: N/A — no flow change` and explain in one line why.

## Example Output Format

# Step-by-Step Implementation Plan with Before/After Code

## Step 1: Add Required Import

**BEFORE:**
```kotlin
package com.example.feature

import androidx.compose.runtime.Composable
// ... existing imports
```

**AFTER:**
```kotlin
package com.example.feature

import androidx.compose.runtime.Composable
import com.example.newdependency.RequiredClass // ✅ Import new dependency for processing logic
// ... existing imports
```

## Step 2: Modify Function Signature

**BEFORE:**
```kotlin
fun processData(input: String) {
    // existing logic
}
```

**AFTER:**
```kotlin
fun processData(input: String, options: ProcessOptions? = null) { // ✅ Add optional parameter for custom processing
    // existing logic
}
```

## Step 3: Update Function Implementation

**BEFORE:**
```kotlin
fun processData(input: String, options: ProcessOptions? = null) {
    if (input.isNotEmpty()) {
        return input.uppercase()
    }
    return ""
}
```

**AFTER:**
```kotlin
fun processData(input: String, options: ProcessOptions? = null) {
    when {
        options?.customProcessing == true -> {
            return options.processor.process(input)
        }
        // ✅ Handle input validation and sanitization
        input.isNotEmpty() -> {
            return input.uppercase()
        }
        else -> {
            return ""
        }
    }
}
```

## Step 4: Fix DropdownSelectorField Display Behavior

### PaymentTypeSelector Component Enhancement

**BEFORE:**
```kotlin
@Composable
private fun PaymentTypeSelector(
    selectedPaymentType: HealthPaymentType?,
    onShowBottomSheet: () -> Unit,
    modifier: Modifier = Modifier
) {
    val displayText = selectedPaymentType?.displayName ?: stringResource(R.string.bpjs_payment_type_placeholder)

    DropdownSelectorField(
        label = stringResource(R.string.bpjs_payment_type_label),
        selectedOption = null, // ❌ ISSUE: Always null, displayText ignored
        placeholder = displayText, // ❌ ISSUE: Using placeholder for selected value
        onClick = onShowBottomSheet,
        modifier = modifier.testDescriptionTag(BillerAutomationConstant.DROPDOWN_HEALTH_PAYMENT_TYPE)
    )
}
```

**AFTER:**
```kotlin
@Composable
private fun PaymentTypeSelector(
    selectedPaymentType: HealthPaymentType?,
    onShowBottomSheet: () -> Unit,
    modifier: Modifier = Modifier
) {
    DropdownSelectorField(
        label = stringResource(R.string.bpjs_payment_type_label),
        selectedOption = selectedPaymentType?.displayName, // ✅ FIX: Show selected value properly
        placeholder = stringResource(R.string.bpjs_payment_type_placeholder), // ✅ FIX: Proper placeholder for empty state
        onClick = onShowBottomSheet,
        modifier = modifier.testDescriptionTag(BillerAutomationConstant.DROPDOWN_HEALTH_PAYMENT_TYPE)
    )
}
```

## Roborazzi Screenshot Plan (mandatory when plan touches UI)

If any step in the plan modifies a `*Screen.kt`, a Composable in `core-ui/`, or anything renderable, the plan MUST include both subsections below. If the plan touches no UI, write `Visual Intent Map: N/A — no UI changes` and skip the rest. Do not invent UI scope where there is none.

### Visual Intent Map (required table)

One row per (screen, state). `state` covers the meaningful UI states the screen renders: at minimum `default`; add `loading`, `empty`, `error`, and any feature-specific states the screen actually has. Anti-aliasing noise is real, so VERIFY-ONLY rows use a 0.1% pixel-diff threshold; RE-RECORD rows do not care about the prior baseline.

| Screen | State | Module | Intended delta | Baseline action | Figma node |
|--------|-------|--------|----------------|-----------------|------------|
| InfoConnectedDeviceScreen | default | feature-login | Browser icon swap → Chrome PNG | RE-RECORD | `abc123XYZ` / `456:789` |
| InfoConnectedDeviceScreen | loading | feature-login | none | VERIFY-ONLY | — |
| LoginScreen | default | feature-modules | none (regression guard) | VERIFY-ONLY | — |

**Figma node** = `{fileKey}` / `{nodeId}` (the two fragments from the Figma URL: `https://www.figma.com/design/{fileKey}/...?node-id={nodeId}`). The literal node id from the URL uses `-` (e.g. `456-789`); when calling MCP convert to `:` form (`456:789`). RE-RECORD rows MUST fill this column; VERIFY-ONLY rows use `—`.

### Asset Manifest (per RE-RECORD row; omit if no assets)

When a RE-RECORD row's "Intended delta" requires a Figma-side image/icon that does not yet exist as a drawable resource in the codebase (or the existing resource is wrong), list those child nodes here so `do-implementation` can fetch them from Figma and stage them under `res/drawable*/` automatically. **The bot does NOT modify Kotlin source** — it only places the asset files. The Compose code must already reference the drawable by name (`R.drawable.{name}`); if it doesn't, that's a code-step in the plan, not an asset step.

Per-row sub-table (one block per row that has any assets):

```
**Assets — InfoConnectedDeviceScreen / default**
| Asset purpose      | Figma child node | Target drawable     | Format | Density            |
|--------------------|------------------|---------------------|--------|--------------------|
| Chrome browser icon | `456:790`       | `ic_browser_chrome` | svg    | n/a (vector)       |
| Hero illustration   | `456:812`       | `img_hero_devices`  | png    | xxxhdpi (4x scale) |
```

Rules:
- **Format `svg`** → fetched via `mcp__figma__get_image_render(format="svg", scale=1)`, written to `{module}/figma-svg/{drawable}.svg` (a stash folder, not `res/drawable/`). The dev converts to VectorDrawable XML via Android Studio Vector Asset Studio before commit. The bot writes an `↪️ convert` line to the AC pointing at the stashed file. Rationale: automated SVG→VectorDrawable is unreliable for arbitrary Figma exports (gradients, masks, blends); a 2-second IDE step is cheaper than fighting the converter.
- **Format `png`** → fetched via `mcp__figma__get_image_render(format="png", scale=N)` where N matches the density. Written directly to `{module}/src/main/res/drawable-{density}/{drawable}.png`. Density values: `mdpi`=1, `hdpi`=1.5, `xhdpi`=2, `xxhdpi`=3, `xxxhdpi`=4. Default to `xxxhdpi` (4x) if the row needs only one density.
- **Multiple densities** for the same asset → repeat the row per density (Asset purpose unchanged, Density changes). The bot fetches once per density and writes each to its own folder.
- **Idempotency**: if the target file already exists and is non-empty, the bot skips that asset and writes `(skipped — already staged)` to the AC. This makes re-running `/do-implementation` cheap when only one screen/asset changed.
- **No Kotlin edits**: the bot will NOT add `painterResource(R.drawable.{name})` to a Composable. Where the asset is used must be declared as a separate code-step in the implementation plan (with a BEFORE/AFTER block like every other code change).

Rules:
- `RE-RECORD` ⇒ this step intentionally changes the pixels. The describing text in **Intended delta** must be specific enough that a reviewer can match it to the diff image (e.g. "swap browser icon", "change CTA from primary green to grey", NOT "tweak UI").
- `VERIFY-ONLY` ⇒ this step must NOT change the pixels. List screens here as regression guards even when the plan only touches their ViewModel/data layer — that is the whole point.
- Every screen named anywhere in the implementation steps appears here. If it isn't in the table, `do-implementation` will treat any pixel diff on it as a regression.
- Baseline path: `.docs/screen/{module}/{ScreenName}_{state}.png`. Module folder is the Gradle module name (e.g. `feature-login`), not the sub-feature path.
- **Figma reference sibling (RE-RECORD rows only)**: `do-implementation` will fetch the node automatically via `mcp__figma__get_image_render(key=fileKey, ids=[nodeId], format="png", scale=1)` and save the PNG as `.docs/screen/{module}/{ScreenName}_{state}.figma.png` next to the Roborazzi baseline. The plan must supply `{fileKey}` and `{nodeId}` in the Figma node column above so the fetch is unattended. If the Figma MCP server is offline OR the node ID is unknown at planning time, write `MANUAL` in the Figma node column — the author then exports from Figma (mobile frame, 1x PNG) and stages the file by hand. Reviewer eyeballs the two PNGs side-by-side in the PR diff. **Exact pixel match is NOT required and NOT the verdict** — Figma export ≠ Roborazzi pixel-for-pixel (font hinting, sub-pixel AA, density rounding). The verdict is "visually identical to a reviewer". VERIFY-ONLY rows do not need a `.figma.png` — they assert "no pixel change vs prior baseline", which is regression-only and independent of design conformance.

### Screenshot Test Skeleton (one per screen listed above)

Include the `*ScreenshotTest.kt` as a `BEFORE: (does not exist)` / `AFTER:` block in the plan. Canonical shape — keep this exact structure so all features look the same:

**BEFORE:**
```kotlin
// (does not exist)
```

**AFTER:**
```kotlin
// path: feature-login/src/test/.../InfoConnectedDeviceScreenScreenshotTest.kt
@RunWith(RobolectricTestRunner::class)
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@Config(qualifiers = RobolectricDeviceQualifiers.Pixel5, sdk = [33])
class InfoConnectedDeviceScreenScreenshotTest {

    @get:Rule val composeTestRule = createComposeRule()
    @get:Rule val roborazziRule = RoborazziRule(
        composeRule = composeTestRule,
        captureRoot = composeTestRule.onRoot(),
        options = RoborazziRule.Options(
            outputDirectoryPath = ".docs/screen/feature-login",
            roborazziOptions = RoborazziOptions(
                compareOptions = RoborazziOptions.CompareOptions(changeThreshold = 0.001f)
            )
        )
    )

    @Test fun infoConnectedDeviceScreen_default() {
        composeTestRule.setContent {
            AppTheme {
                InfoConnectedDeviceScreen(state = sampleDefaultState())
            }
        }
    }

    @Test fun infoConnectedDeviceScreen_loading() {
        composeTestRule.setContent {
            AppTheme {
                InfoConnectedDeviceScreen(state = sampleLoadingState())
            }
        }
    }
}
```

If the target module does not yet apply `libs.plugins.roborazzi.plugin` and `testImplementation(libs.roborazzi*)`, the plan MUST include a Step 0: "Add Roborazzi to `{module}/build.gradle.kts`" with the exact additions, before any UI step.

### Self-verdict contract (carries into do-implementation)

The plan is the intent ledger. `do-implementation` will judge pixel diffs against this table on its own — it will NOT ask the user mid-run. A row not in the table = regression. A RE-RECORD row whose actual delta does not match the **Intended delta** description = regression. Be precise here. A RE-RECORD row whose `.figma.png` sibling cannot be staged (MCP auth fails, node id 404s, MANUAL file missing, or no node provided) does NOT halt — `do-implementation` records the gap as a `⚠️` line under §"Figma Reference Notes" of the AC and `/push-pr` surfaces it under `## Missing Figma References` in the PR description so the reviewer eyeballs against the Figma file directly.

## Benchmark Mapping
map each implementation step to the closest AN- (android) benchmarks from folder .docs/benchmark/benchmark.md.
can add multiple benchmarks if needed.
inform the benchmark mapping at the bottom of document.


## Summary of Changes:
1. **Import Addition**: Add required dependency import
2. **Function Signature**: Add optional parameter with default value
3. **Logic Enhancement**: Implement conditional processing based on options
4. **Backward Compatibility**: Maintain existing behavior with default parameter

**Key Insights:**
- Each step builds upon the previous one
- Backward compatibility is preserved throughout
- Code examples show exact changes needed
- Technical rationale explains the "why" behind each change

---

## Observability: CrashlyticsLogTree Capture Awareness

When any implementation involves logging (`Timber.d/i/w/e`), always consider the CrashlyticsLogTree capture chain.
This is critical because a wrong log level can create non-fatal noise in Crashlytics production dashboards.

### Capture Layers

| Layer | Priority Gate | API Called | Effect in Crashlytics |
|-------|--------------|-----------|----------------------|
| **Breadcrumb** | `DEBUG+` | `crashlytics.log()` | Shows in crash timeline only, no alert |
| **Direct exception** | `ERROR+` with non-null `Throwable` | `crashlytics.recordException(t)` | Creates non-fatal issue |
| **Pattern detection** | `WARN+` | `patternDetector.scan()` → `recordException(PreCrashSignal)` | Creates non-fatal issue if pattern matches |

### Pattern Detection Triggers (LogPatternDetector)

| Category | Pattern Match | Threshold |
|----------|--------------|-----------|
| `STRICT_MODE` | "StrictMode policy violation" | Any |
| `PRE_ANR` | "Skipped N frames" / "Main thread blocked for Nms" | >30 frames / >3000ms |
| `GC_PRESSURE` | dalvikvm/art tags, "GC_FOR_ALLOC", "OutOfMemoryError" | Any |
| `SLOW_QUERY` | "query took" or Room tag + "ms" | Any |
| `NETWORK_FAIL` | HTTP 5xx, SocketTimeout, UnknownHost, ConnectException, SSLHandshake | Any |

Throttle: max 8 non-fatals per signal type per session.

### Decision Guide for Log Levels

```
Is this an error the developer MUST act on?
  → YES + have Throwable  → Timber.e(throwable, "...")  [records non-fatal]
  → YES + no Throwable     → Timber.e("...")             [breadcrumb + pattern scan]

Is this a warning about degraded behavior?
  → YES, but from monitoring/instrumentation tool → Timber.d("...")  [breadcrumb only, avoids pattern scan noise]
  → YES, from real app logic                      → Timber.w("...")  [breadcrumb + pattern scan]

Is this informational / diagnostic?
  → Timber.d("...")  [breadcrumb only]
```

### In Implementation Plans

When a step adds or changes a `Timber.*` call:
1. **State which capture layer it hits** (breadcrumb / pattern scan / non-fatal)
2. **Flag if the message text matches any pattern** (e.g. contains "Main thread blocked", "query took", HTTP status codes)
3. **Warn if monitoring/instrumentation code uses WARN+** — this is the #1 source of Crashlytics noise

## Usage Guidelines

When using this command:
- read all readme.md files related to the module if available for context
- Focus on showing concrete code transformations
- Include file paths and line numbers when relevant
- Explain the impact of each change
- Consider error handling and edge cases
- Provide testing strategies for each step
- if work for data layer, include api endpoints and response models

## Coding Guidelines
Always follow these guidelines:
1. Define the data model before writing code
2. Start with mock data instead of a database
3. Create a component library and split code into multiple files
4. Centralize state management
5. Batch implementation into smaller chunks
6. Double-check you're changing the correct files
7. Ask follow-up questions if requirements are unclear
8. Ensure code is readable and maintainable
## Avoid Repeating Mistakes

Before creating the plan, read the **Common Issues** section in CLAUDE.md for known gotchas.

If you encounter a new mistake during planning, add it to CLAUDE.md Common Issues section with:
- What went wrong
- How it was fixed

Keep it short. This helps future sessions not repeat the same mistake.
