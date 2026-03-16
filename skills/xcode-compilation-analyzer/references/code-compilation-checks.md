# Code Compilation Checks

Use this reference when a build benchmark shows compilation dominating build time.

## Primary Evidence Sources

- `xcodebuild -showBuildTimingSummary`
- build log compile tasks
- `-warn-long-function-bodies`
- `-warn-long-expression-type-checking`
- `-debug-time-compilation` (per-file compile time ranking)
- `-debug-time-function-bodies` (unfiltered per-function timing)
- `-driver-time-compilation` (driver overhead)
- `-stats-output-dir` (detailed compiler statistics as JSON)

## Triage Questions

1. Is one file or expression dominating compile time?
2. Is the issue mostly Swift type-checking, mixed-language bridging, or header import churn?
3. Are multiple files in the same module paying the same module-setup cost repeatedly?
4. Is `SwiftEmitModule` disproportionately large for any target? If a single-line change triggers 60s+ of module emission, the target is likely too large or heavily macro-dependent.
5. Does `Planning Swift module` dominate incremental builds? If modules are replanned but no compiles are scheduled, build inputs are being invalidated unexpectedly.

## Checklist

### Explicit typing

- Add explicit property or local variable types when initialization expressions are complex.
- Prefer intermediate typed variables over one giant inferred expression.

### Expression simplification

- Break long chains into smaller expressions.
- Split complex result-builder code into smaller helpers or subviews.
- Replace nested ternaries or overloaded generic chains with simpler steps.

### Delegate typing

- Avoid `AnyObject?` or overly generic delegate surfaces.
- Prefer a named delegate protocol so the compiler has a narrower lookup space.

### Objective-C and Swift bridging

- Keep the Objective-C bridging header narrow.
- Move internal-only Objective-C declarations out of the bridging surface.
- Mark Swift members `private` when they do not need Objective-C visibility.

### Framework-qualified imports

- Prefer `#import <Framework/Header.h>` or module imports when a module map exists.
- Watch for textual includes that defeat module-cache reuse.

### Access control and dispatch optimization

- Mark classes not intended for subclassing as `final`. This eliminates virtual dispatch overhead and lets the compiler de-virtualize method calls, reducing both compile and runtime cost.
- Use `private` or `fileprivate` for properties and methods not used outside their declaration or file. Narrower visibility reduces the compiler's symbol search space.
- Prefer `internal` (the default) over `public` unless the symbol genuinely crosses module boundaries. Wider access forces the compiler to consider more call sites.

### Value types over reference types

- Prefer `struct` and `enum` over `class` when reference semantics are not needed. Value types are simpler for the compiler to reason about and do not require vtable dispatch.
- When a class exists solely to group data without identity semantics, convert it to a struct.

### SwiftUI view decomposition

- Extract subviews into dedicated `struct View` types instead of using `@ViewBuilder` helper properties. Separate structs reduce the type-checker scope per `body` property.
- Break monolithic `body` properties (roughly 50+ lines) into smaller composed subviews. Large result-builder bodies are among the most expensive expressions to type-check.
- Avoid deeply nested `Group`/`VStack`/`HStack` hierarchies within a single body.

### Closure and chain patterns

- Avoid long method chains like `.map().flatMap().filter().reduce()` without intermediate type annotations. Each link in the chain multiplies the type-checker's candidate set.
- Break complex closures into named functions with explicit parameter and return types.
- Add explicit return types to closures passed to generic functions so the compiler does not need to infer them from context.

### Generic constraint complexity

- Minimize deeply nested generic constraints (e.g., `where T: Collection, T.Element: Comparable, T.Element.SubSequence: ...`). Each additional constraint widens the compiler's search space.
- Use type aliases to flatten complex generic stacks into readable names.
- Prefer `some Protocol` (opaque return types) over unconstrained generics when the concrete type does not need to be visible to callers.

### Module emission and planning overhead

- Check `SwiftEmitModule` time in the Build Timing Summary. Large modules with many public symbols take longer to emit, and this cost is paid on every incremental build that touches the module.
- If `SwiftEmitModule` exceeds compile time for the same target, the module's public API surface may be unnecessarily wide -- narrow access control or split the module.
- Check `Planning Swift module` time. If it is significant in incremental builds, escalate to `xcode-project-analyzer` to investigate unexpected input invalidation or misconfigured scripts.

### Precompiled and prefix headers

- For mixed-language projects with large Objective-C codebases, verify that prefix headers are not bloated with unnecessary imports. Every import in a prefix header is parsed for every translation unit.
- Migrate away from prefix headers toward explicit module imports where possible.

## Recommendation Heuristics

- High impact: repeated type-check warnings in a hot module, giant bridging headers, or a few files dominating compile time.
- Medium impact: several moderate hotspots in result builders or overloaded generic code.
- Low impact: isolated warnings without measurable benchmark impact.

## Escalation Guidance

Hand findings to `xcode-project-analyzer` when:

- build scripts dominate instead of compilation
- module reuse is blocked by project settings
- target structure or explicit-module settings appear to be the real bottleneck
- `Planning Swift module` overhead points to input invalidation or script-related causes rather than source complexity
