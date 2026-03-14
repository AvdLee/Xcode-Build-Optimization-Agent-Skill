# Project Audit Checks

Use this reference when reviewing build-system configuration rather than source-level compile behavior.

## Target And Scheme Checks

- Confirm target dependencies are explicit and accurate.
- Remove dependencies that no longer reflect real build requirements.
- Ensure the scheme builds targets in `Dependency Order`.
- Look for oversized or monolithic targets that block parallel work.

## Build Script Checks

- Does each script need to run during incremental builds?
- Are input and output files declared?
- Should inputs and outputs be moved into `.xcfilelist` files?
- Can the script skip debug builds, simulator builds, or unchanged inputs?
- Would the script become parallelizable if dependency analysis were declared correctly?

## Build Setting Checks

- Debug compilation mode should usually favor incremental behavior.
- Release compilation mode should usually favor whole-module optimization behavior.
- `Build Active Architecture Only` should match debug vs release intent.
- `Debug Information Format` should avoid heavier-than-needed debug defaults.

## Module And Header Checks

- `DEFINES_MODULE` is enabled for custom frameworks that should benefit from module maps.
- Public headers are self-contained enough to compile as a module.
- Import statements use framework-qualified imports where available.
- targets that should share built modules use consistent options

## Explicit Module Dependency Checks

- Check whether explicit modules are enabled or expected in the current Xcode version and Swift mode.
- Look for repeated module builds caused by configuration drift.
- Compare preprocessor macros or other build options across sibling targets that import the same modules.

## Recommendation Prioritization

- High: serial script bottlenecks, missing dependency metadata, or configuration drift causing redundant module builds.
- Medium: stale target structure or noncritical scripts running too often.
- Low: settings cleanup without strong evidence of current impact.
