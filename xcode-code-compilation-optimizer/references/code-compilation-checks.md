# Code Compilation Checks

Use this reference when a build benchmark shows compilation dominating build time.

## Primary Evidence Sources

- `xcodebuild -showBuildTimingSummary`
- build log compile tasks
- `-warn-long-function-bodies`
- `-warn-long-expression-type-checking`

## Triage Questions

1. Is one file or expression dominating compile time?
2. Is the issue mostly Swift type-checking, mixed-language bridging, or header import churn?
3. Are multiple files in the same module paying the same module-setup cost repeatedly?

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

## Recommendation Heuristics

- High impact: repeated type-check warnings in a hot module, giant bridging headers, or a few files dominating compile time.
- Medium impact: several moderate hotspots in result builders or overloaded generic code.
- Low impact: isolated warnings without measurable benchmark impact.

## Escalation Guidance

Hand findings to `xcode-project-optimizer` when:

- build scripts dominate instead of compilation
- module reuse is blocked by project settings
- target structure or explicit-module settings appear to be the real bottleneck
