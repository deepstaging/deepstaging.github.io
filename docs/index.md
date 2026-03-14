# Deepstaging

**Stop wiring infrastructure. Start shipping domain logic.** Two packages that eliminate the busywork of .NET development — one for application developers, one for tooling authors.

---

<div class="grid cards" markdown>

- :material-code-braces:{ .lg .middle } **Deepstaging**

    ---

    Declare your intent with attributes. The compiler generates the infrastructure, catches the mistakes, and produces test stubs alongside it.

    Persistence, CQRS, validation, messaging, resilience, configuration, typed IDs — one package replaces MediatR, FluentValidation, AutoMapper, Polly, MassTransit, and your mocking framework. 50+ analyzers catch structural bugs before `dotnet run`.

    ```csharp
    [Runtime]
    [Uses(typeof(OrderStore))]
    [Uses(typeof(NotificationEffects))]
    public sealed partial class AppRuntime;
    ```

    That's a fully wired runtime with DI registration, test stubs, and compile-time capability verification. You didn't configure anything. You stated what exists.

    [:octicons-arrow-right-24: Get started](deepstaging/getting-started.md)
    [:octicons-book-24: Why Deepstaging?](deepstaging/why.md)

- :material-wrench:{ .lg .middle } **Deepstaging.Roslyn**

    ---

    A fluent toolkit that makes Roslyn's APIs feel like a standard library. Build source generators, analyzers, and code fixes without fighting the compiler.

    Query symbols. Project attributes safely. Emit code with builders. Test everything with snapshot assertions. Ship analyzers with code fixes that actually work.

    ```csharp
    var types = TypeQuery.From(compilation)
        .ThatAreClasses()
        .ThatArePartial()
        .WithAttribute("GenerateAttribute")
        .GetAll();
    ```

    No `SyntaxFactory` gymnastics. No `INamedTypeSymbol` null checks. Just find what you need and generate what you want.

    [:octicons-arrow-right-24: Get started](roslyn/getting-started.md)
    [:octicons-book-24: API Reference](roslyn/api/queries/index.md)

</div>

---

## How They Fit Together

Deepstaging.Roslyn is the foundation. Deepstaging is the product built on it.

If you're building .NET applications, you want **Deepstaging** — install one package and declare your architecture with attributes. The generators, analyzers, and code fixes are all built with Deepstaging.Roslyn under the hood, but you never need to touch it.

If you're building your own source generators, analyzers, or code fixes, you want **Deepstaging.Roslyn** — it's the toolkit that makes Roslyn development productive instead of painful.

```bash
# For application developers
dotnet add package Deepstaging --prerelease

# For tooling authors
dotnet add package Deepstaging.Roslyn --prerelease
```
