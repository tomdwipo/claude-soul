# Stop the AS Gradle daemon before CLI Gradle
**When this applies:** running a CLI `./gradlew` task while Android Studio is open.
**Principle:** one `~/.gradle` home cannot safely host two daemons — stop AS's daemon before the CLI build.
**Why:** AS's daemon holds an exclusive lock on `~/.gradle/caches/journal-1`; the CLI build times out after 60s with "Timeout waiting to lock journal cache".
**How to apply:**
- `./gradlew --stop` first, then run the task.
- If a stale daemon persists: `pgrep -af GradleDaemon | awk '{print $1}' | xargs kill`.
