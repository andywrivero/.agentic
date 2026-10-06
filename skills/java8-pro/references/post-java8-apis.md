# Post-Java-8 APIs to avoid

Use this list when reviewing or writing code for a Java 8 target. The Java 8 alternative is shown after the arrow.

## Collections and streams
- `List.of`, `Set.of`, `Map.of`, `Map.entry`, `Map.ofEntries` (9); `List/Set/Map.copyOf` (10) → `Collections.unmodifiableList(Arrays.asList(...))`, `Collections.singletonList`, `Collections.emptyList`, or a project/Guava helper
- `Stream.toList` (16) → `collect(Collectors.toList())`
- `Stream.takeWhile`, `dropWhile`, `ofNullable`, three-argument `iterate` (9); `mapMulti` (16)
- `Collectors.filtering`, `flatMapping` (9); `toUnmodifiableList/Set/Map` (10) → `collectingAndThen(toList(), Collections::unmodifiableList)`; `teeing` (12)
- `Collection.toArray(IntFunction)` (11) → `toArray(new T[0])`

## Optional
- `ifPresentOrElse`, `or`, `stream` (9); no-arg `orElseThrow()` (10) → `orElseThrow(NoSuchElementException::new)`; `isEmpty` (11) → `!isPresent()`

## Strings and text
- `isBlank`, `strip*`, `lines`, `repeat` (11) → `trim().isEmpty()`, `trim()`, `split("\\R")`, `String.join("", Collections.nCopies(n, s))`
- `indent`, `transform` (12); `formatted` (15) → `String.format`
- `Character.toString(int)` (11)

## I/O and files
- `Files.readString`, `writeString`, `Path.of` (11) → `new String(Files.readAllBytes(p), UTF_8)`, `Files.write`, `Paths.get`
- `Files.mismatch` (12)
- `InputStream.readAllBytes`, `transferTo` (9); `readNBytes(int)`, `nullInputStream` (11) → manual buffer loop or project utility
- `ByteBuffer`/`CharBuffer` covariant `flip`, `clear`, `position`, `limit` (9) → compile with `--release 8`, or cast to `Buffer`

## Utilities and concurrency
- `Objects.requireNonNullElse`, `requireNonNullElseGet`, `checkIndex` (9)
- `Predicate.not` (11) → `x -> !pred.test(x)`
- `CompletableFuture.orTimeout`, `completeOnTimeout`, `failedFuture`, `delayedExecutor` (9)
- `Arrays.mismatch`, `Arrays.compare` (9); `Matcher.results`, `Scanner.tokens` (9)
- `StackWalker`, `ProcessHandle` (9); `java.net.http.HttpClient` (11)

## Date and time
- `LocalDate.datesUntil`, `LocalDate.ofInstant` (9); `Duration.toSeconds`, `toXxxPart`, `dividedBy(Duration)` (9) → `getSeconds()` and manual arithmetic

## Annotations and packages
- `javax.annotation.processing.Generated` (9) → `javax.annotation.Generated`
- `module-info.java` (9)
