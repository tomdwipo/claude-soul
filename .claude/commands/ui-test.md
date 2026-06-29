# UI Test — Screenshot Benchmark Comparison

Run visual UI tests by comparing device screenshots against benchmark images.
Supports ADB actions (tap, type, swipe, back, wait, launch) to navigate through app flows.

## Arguments
$ARGUMENTS is the flow name (e.g., `login-flow`), matching a YAML file in `ui-tests/flows/`.

## Instructions

You are running an automated visual UI test. Follow these steps EXACTLY:

### Phase 1: Load Test Spec

1. Read the YAML file at `ui-tests/flows/$ARGUMENTS.yaml`
2. Parse the flow name, description, default_diff_threshold, and list of screens
3. If the file doesn't exist, tell the user and list available flows from `ui-tests/flows/`

### Phase 2: Run Each Screen Test

For EACH screen in the `screens` list, do the following IN ORDER:

#### Step A: Execute Actions (if specified)

If the screen has an `actions` list, execute each action IN ORDER using ADB:

| Action | YAML | ADB Command |
|--------|------|-------------|
| **tap** | `- tap: {x: 360, y: 800}` | `adb shell input tap 360 800` |
| **long_press** | `- long_press: {x: 360, y: 800}` | `adb shell input swipe 360 800 360 800 1000` |
| **type** | `- type: "hello"` | `adb shell input text "hello"` |
| **swipe** | `- swipe: {x1: 360, y1: 1200, x2: 360, y2: 400}` | `adb shell input swipe 360 1200 360 400 300` |
| **back** | `- back` | `adb shell input keyevent 4` |
| **home** | `- home` | `adb shell input keyevent 3` |
| **enter** | `- enter` | `adb shell input keyevent 66` |
| **wait** | `- wait: 2000` | `sleep 2` (value is in milliseconds) |
| **launch** | `- launch: "com.example.app.dev/com.example.app.ui.MainActivity"` | `adb shell am start -n <value>` |
| **clear_app** | `- clear_app: "com.example.app.dev"` | `adb shell pm clear <value>` |
| **hide_keyboard** | `- hide_keyboard` | `adb shell input keyevent 111` |
| **swipe_repeat** | `- swipe_repeat: {x1: 360, y1: 1200, x2: 360, y2: 300, count: 50}` | Repeat swipe N times (200ms between each) |
| **fetch_otp** | `- fetch_otp: {url: "https://...", phone: "<phone>"}` | Fetch OTP via curl, store in variable |
| **type_fetched_otp** | `- type_fetched_otp` | Type the previously fetched OTP digits one by one |

**swipe_repeat action**: Repeats a swipe gesture N times with 200ms delay between each:
```
for i in $(seq 1 <count>); do adb shell input swipe <x1> <y1> <x2> <y2> 200 && sleep 0.2; done
```
Useful for scrolling through long WebView content (TNC pages, privacy policies).

**fetch_otp action**: Fetches OTP code via curl API. Steps:
1. Run: `curl -s '<url>?phone=<phone>' -H 'Authorization: <auth>' -H 'Content-Type: application/json'`
2. Parse the JSON response and extract the `otp` field value
3. Store the OTP code in memory for `type_fetched_otp` to use
4. If fetch fails or `otp` is empty, report error and continue

**type_fetched_otp action**: Types the previously fetched OTP code character by character:
1. For each digit in the stored OTP, run: `adb shell input text "<digit>"` with 200ms pause between each
2. This handles OTP fields that auto-advance to the next input box after each digit

Execute each action one by one. Add a 300ms pause between actions automatically:
```
adb shell input tap 360 800 && sleep 0.3
```

If an action has no explicit wait after it, use the 300ms default. If the next action is `wait`, use that value instead.

For `type` actions with spaces or special characters, use `adb shell input text` with proper escaping. Replace spaces with `%s`:
```
adb shell input text "hello%sworld"
```

#### Step B: Wait (if specified)
- If `wait_seconds` > 0, run: `sleep <wait_seconds>`
- This runs AFTER all actions complete, giving the screen time to settle before capture

#### Step C: Capture Screenshot
Run this bash command:
```
adb shell screencap -p /sdcard/ui_test_capture.png && adb pull /sdcard/ui_test_capture.png /tmp/ui_test_current_<screen_id>.png && adb shell rm -f /sdcard/ui_test_capture.png
```
Replace `<screen_id>` with the screen's `id` field.

#### Step D: Check Benchmark Exists
- The benchmark path is: `ui-tests/<benchmark>` (from YAML)
- If the benchmark file doesn't exist, report it as **SKIP** with message "No benchmark found. Run: ./ui-tests/capture-benchmarks.sh <screen_id>"
- Continue to next screen

#### Step E: Compute Image Diff
Run ImageMagick compare to get RMSE diff percentage:
```
compare -metric RMSE /tmp/ui_test_current_<screen_id>.png ui-tests/<benchmark> /tmp/ui_test_diff_<screen_id>.png 2>&1
```

The output format is: `<value> (<normalized>)` where normalized is 0.0-1.0.
Extract the normalized value (the number in parentheses), multiply by 100 to get diff percentage.

If the compare command returns an error about image size mismatch, resize the current screenshot first:
```
convert /tmp/ui_test_current_<screen_id>.png -resize $(identify -format '%wx%h' ui-tests/<benchmark>)! /tmp/ui_test_current_<screen_id>_resized.png
```
Then re-run compare with the resized image.

#### Step F: Evaluate Result

**If diff_percentage ≤ threshold (from YAML, or default_diff_threshold):**
- Mark as **PASS**
- Record: screen_id, diff_percentage, "Auto-pass: within threshold"
- Do NOT read the images — no visual comparison needed

**If diff_percentage > threshold:**
- Mark as **NEEDS REVIEW**
- Read BOTH images using the Read tool:
  1. Read the benchmark image: `ui-tests/<benchmark>`
  2. Read the current screenshot: `/tmp/ui_test_current_<screen_id>.png`
  3. Read the diff image: `/tmp/ui_test_diff_<screen_id>.png`
- Compare the two images visually against the `expectation` text from YAML
- Determine if this is:
  - **PASS** — visual differences are cosmetic/acceptable (font rendering, anti-aliasing, minor color shifts)
  - **FAIL** — meaningful UI regression (missing elements, wrong layout, broken styling, wrong screen entirely)
- Record: screen_id, diff_percentage, your visual judgment reason

### Phase 3: Report Results

Print a results table in this exact format:

```
## UI Test Results: <flow_name>
<description>

| Screen | Diff % | Threshold | Result | Details |
|--------|--------|-----------|--------|---------|
| splash_screen | 2.3% | 8% | PASS | Auto-pass: within threshold |
| login_screen | 12.1% | 5% | FAIL | Missing password field |

Summary: X/Y passed, Z failed, W skipped
```

If any test FAILED, also show:
- Which screens failed and why
- The expectation vs what was actually seen
- Suggestion: "Run `./ui-tests/capture-benchmarks.sh <screen_id>` to update the benchmark if this is intentional"

### Phase 4: Cleanup

Run: `rm -f /tmp/ui_test_current_*.png /tmp/ui_test_diff_*.png`

### Important Rules

- NEVER skip a screen — test ALL screens in the YAML
- ALWAYS capture fresh screenshots — never reuse old captures
- If no device is connected (`adb devices` shows no device), stop immediately and tell the user
- If the app is not running on the device, tell the user to launch it first
- Report diff values with 1 decimal place (e.g., 3.2%, not 3.21847%)
- Execute ALL actions in order — do not skip any
- Add 300ms pause between each action for UI to respond
