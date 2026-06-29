# Load before use at the network boundary
**When this applies:** a ViewModel cache (StateFlow) is hydrated asynchronously from DataStore and then read at a network call.
**Principle:** never trust an async-hydrated cache at the boundary — re-read DataStore in the same coroutine that fires the call.
**Why:** PROJ-9420 — OTP request sent `{phone:""}` because populator and consumer ran on independent `viewModelScope.launch` blocks with no happens-before; failed on process-death recreation / fast-tap.
**How to apply:**
- `await dataStoreRepository.getData()` inside the function that fires the call; `ifBlank { cache }` as fallback.
- Abort + `Timber.w` (no pattern-trigger words) rather than POST blank fields.
- Never `runBlocking` to hydrate in `init` (banned since PROJ-8679).
- Catalog rule: `.docs/common-issues/viewmodel-datastore-hydration-race.md`.
