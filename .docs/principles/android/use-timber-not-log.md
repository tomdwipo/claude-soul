# Timber, never android.util.Log
**When this applies:** writing or reviewing any logging in production Kotlin.
**Principle:** log through Timber so tests stay green; `Log.*` is a unit-test landmine.
**Why:** `android.util.Log` is not mocked in JVM tests → `Method d not mocked` breaks CI; Timber is a no-op when no Tree is planted (test env).
**How to apply:**
- Use `Timber.d/w/e`; the exception is the FIRST arg: `Timber.e(e, "msg")`, not `Timber.e("msg", e)`.
- No TAG needed — DebugTree derives it from the class name.
- `lintChecks(libs.timber)` flags `Log.*` per module.
