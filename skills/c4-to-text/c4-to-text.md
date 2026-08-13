# C4-to-Text — Representing C4 Architecture in Tables and Prose

A reference for producing a **plain-Markdown, diagram-free** description of a software system's
architecture at the three most-used C4 levels: **System Context**, **Container**, and **Component**.

The output is a Markdown document that a reader can fully understand in a terminal, a code review, a
diff, or any viewer that renders Markdown but **cannot render diagrams** (Mermaid, PlantUML,
Structurizr, images). Every element, every relationship, and every legend that a diagram would carry
is expressed instead as **tables and short prose**.

Reference distilled from [c4model.com/diagrams](https://c4model.com/diagrams). C4 is created by
Simon Brown (CC BY 4.0).

> **Why text instead of a picture?** A C4 diagram encodes three things: a set of *elements* (boxes),
> a set of *relationships* (labelled arrows), and a *legend*. All three are tabular data wearing a
> visual costume. Strip the costume and you lose nothing that an engineer needs to reason about the
> architecture — you gain greppability, diffability, and readability anywhere Markdown renders.

---

## The core idea

C4 is a hierarchy of zoom levels — "Google Maps for code". You zoom out to see the whole landscape,
then progressively zoom in. This document covers the three static-structure levels:

| Level | Diagram | Zoom | Scope | This doc's section |
|---|---|---|---|---|
| 1 | System Context | Widest | A single **software system** and its surroundings | [Level 1](#level-1--system-context) |
| 2 | Container | Inside one system | The **containers** (apps / data stores) within it | [Level 2](#level-2--container) |
| 3 | Component | Inside one container | The **components** inside a single container | [Level 3](#level-3--component) |

Prefer generating Component diagrams from code so it does not drift.

Each level maps onto the **same two-table shape**:

1. An **Elements** table — the boxes: what they are, their type, technology, and responsibility.
2. A **Relationships** table — the arrows: who talks to whom, in which direction, why, and how.

Everything below is a refinement of that shape per level, plus the conventions that keep the text
unambiguous in the absence of a picture.

---

## Universal conventions (apply at every level)

These substitute for the visual cues a diagram would give you. Follow them consistently so a reader
never has to guess.

### Elements must be self-describing

Every element gets, at minimum: a **name**, an **element type** (Person, Software System, Container,
Component — plus in/external), and a **short responsibility** sentence. Containers and components
also carry a **technology**. This is exactly the information a well-drawn C4 box carries.

### Relationships are directional and labelled

A diagram's arrow has a direction, a verb phrase, and often a protocol. Preserve all three:

- **Direction:** encode it as a distinct **From** and **To** column — never a symmetric "connects
  to". If two elements talk both ways, either use two rows or an explicit `<->` marker with a label
  that reads correctly in both directions.
- **Label:** an active verb phrase describing the dependency, e.g. "Makes payments using", "Sends
  e-mails to", "Reads product data from". The sentence *From + label + To* must read as English.
- **Technology / protocol:** where it matters, in its own column, e.g. `HTTPS/JSON`, `gRPC`,
  `JDBC`, `SMTP`, `AMQP`.

### Mark what is external vs in-scope

A diagram uses colour or a border to show what you own versus what you depend on. In text, add a
**boundary/scope marker** — a column value or a suffix — for example `[in scope]` vs `[external]`,
or an `Ext` type suffix (`Software System (External)`). Never leave the reader unsure which side of
the boundary an element sits on.

### Always include a legend / key

Diagrams should carry a key; so should the text. Add a short **Legend** section that defines the
element-type vocabulary and any status/scope markers you use, so the notation is never assumed to be
self-evident.

### Title every level with its type and scope

Head each section with the diagram type **and** the name of the thing in scope — e.g. "Container
view — Internet Banking System" — so a reader always knows which zoom level they are reading and
what its boundary is.

### Keep detail at the right altitude

Match the diagram's discipline about detail:

- **System Context:** people and systems only — no technologies, protocols, or internals.
- **Container:** technology choices and inter-container protocols — but **no deployment concerns**
  (clustering, load balancers, replication, scaling live in a separate deployment view).
- **Component:** internal decomposition and implementation detail of *one* container.

---

## Recommended document skeleton

A complete C4-to-text document, top to bottom:

```markdown
# Architecture — <System Name> (C4, text form)

<1–3 sentence summary of what the system is and does.>

## Legend
<element-type vocabulary + scope/status markers used below>

## Level 1 — System Context: <System Name>
### Elements
<table>
### Relationships
<table>
### Notes
<prose: anything the tables can't carry>

## Level 2 — Containers: <System Name>
### Elements
<table>
### Relationships
<table>
### Notes

## Level 3 — Components: <Container Name>   (repeat per container that warrants it)
### Elements
<table>
### Relationships
<table>
### Notes
```

---

## Level 1 — System Context

**Scope:** a single software system.
**Primary element:** the software system in scope.
**Supporting elements:** the people (users, actors, roles, personas) and other software systems it
interacts with — these external systems are typically outside your control.
**Audience:** everybody, technical and non-technical, inside and outside the team.

Communicate: what the system is and broadly does, who uses it, and how it fits the surrounding
system landscape. Deliberately omit technology and internal detail.

### Elements table

| Name | Type | In scope? | Responsibility |
|---|---|---|---|
| *&lt;the system&gt;* | Software System | In scope | What it does, in one line. |
| *&lt;a user role&gt;* | Person | — | Who they are and what they use it for. |
| *&lt;a dependency&gt;* | Software System (External) | External | What that system provides. |

- **Type** vocabulary at this level: `Person`, `Person (External)`, `Software System`, `Software
  System (External)`.
- The **in-scope** system is the one everything else orbits; mark it clearly.

### Relationships table

| From | To | Description | Technology |
|---|---|---|---|
| *Person* | *System* | "Views balances and makes payments using" | — |
| *System* | *External system* | "Sends e-mails using" | SMTP |

At Level 1 the **Technology** column is often empty — protocol detail is usually below the altitude
of a context view. Include it only where it genuinely aids the shared understanding.

### Worked example — Internet Banking System (Context)

**Elements**

| Name | Type | In scope? | Responsibility |
|---|---|---|---|
| Internet Banking System | Software System | In scope | Lets customers view account information and make payments via the web. |
| Personal Banking Customer | Person | — | A bank customer with one or more personal accounts. |
| Core Banking System | Software System (External) | External | Stores core banking data: customers, accounts, transactions. |
| E-mail System (AWS SES) | Software System (External) | External | Cloud-based e-mail delivery service. |

**Relationships**

| From | To | Description | Technology |
|---|---|---|---|
| Personal Banking Customer | Internet Banking System | Views account balances and makes payments using | — |
| Internet Banking System | Core Banking System | Gets account information from and makes payments using | — |
| Internet Banking System | E-mail System (AWS SES) | Sends e-mails using | SMTP |
| E-mail System (AWS SES) | Personal Banking Customer | Sends e-mails to | SMTP |

---

## Level 2 — Container

**Scope:** the single software system in scope, now opened up.
**Primary elements:** the **containers** inside it.
**Supporting elements:** the people and external systems directly connected to those containers
(carried over from Level 1).
**Audience:** technical people — architects, developers, operations/support.

> **A "container" in C4 is not a Docker container.** It is a separately runnable or deployable unit
> that executes code or stores data — something that must be running for the system to work.
> Examples: a server-side web app, a client-side SPA, a mobile app, a desktop app, a serverless
> function or batch job, a database schema, a file system or object store (e.g. an S3 bucket), a
> shell script.

Communicate: the high-level shape of the system and how responsibilities are distributed, the major
**technology choices** (annotate every container), and how containers **communicate** (protocols).
**Exclude deployment** — clustering, load balancers, replication, failover, scaling belong in a
separate deployment view because they vary per environment.

### Elements table

Add a **Technology** column — it is the defining extra detail of a container view.

| Name | Type | Technology | In scope? | Responsibility |
|---|---|---|---|---|
| *&lt;a container&gt;* | Container | *e.g. Java/Spring MVC* | In scope | What it is responsible for. |
| *&lt;a data store&gt;* | Container (Database) | *e.g. Oracle* | In scope | What it stores. |
| *&lt;a user&gt;* | Person | — | — | Carried from context. |
| *&lt;a dependency&gt;* | Software System (External) | — | External | Carried from context. |

- **Type** vocabulary adds container variants: `Container`, `Container (Database)`, `Container
  (Queue)`, and their `(External)` forms — alongside the Level-1 `Person` and `Software System`
  types for the surrounding elements.

### Relationships table

The **Technology / Protocol** column now carries real weight — how containers talk is a primary
message of this level.

| From | To | Description | Technology |
|---|---|---|---|
| *SPA* | *API app* | "Makes API calls to" | HTTPS/JSON |
| *API app* | *Database* | "Reads from and writes to" | JDBC |
| *API app* | *External system* | "Makes calls to" | HTTPS/XML |

### Worked example — Internet Banking System (Containers)

**Elements**

| Name | Type | Technology | In scope? | Responsibility |
|---|---|---|---|---|
| Web Application | Container | Java / Spring MVC | In scope | Delivers static content and the single-page app to customers' browsers. |
| Single-Page Application | Container | JavaScript / Angular | In scope | Provides internet-banking functionality in the browser. |
| Mobile App | Container | Xamarin | In scope | Provides a subset of internet-banking functionality on mobile. |
| API Application | Container | Java / Spring MVC | In scope | Provides internet-banking functionality via a JSON/HTTPS API. |
| Database | Container (Database) | Oracle | In scope | Stores user registration, hashed auth credentials, access logs, etc. |
| Personal Banking Customer | Person | — | — | A bank customer with personal accounts. |
| Core Banking System | Software System (External) | — | External | Core banking data and transactions. |
| E-mail System (AWS SES) | Software System (External) | — | External | Cloud e-mail delivery. |

**Relationships**

| From | To | Description | Technology |
|---|---|---|---|
| Personal Banking Customer | Web Application | Visits `bigbank.com/ib` using | HTTPS |
| Personal Banking Customer | Single-Page Application | Views balances and makes payments using | — |
| Personal Banking Customer | Mobile App | Views balances and makes payments using | — |
| Web Application | Single-Page Application | Delivers to the customer's browser | — |
| Single-Page Application | API Application | Makes API calls to | HTTPS/JSON |
| Mobile App | API Application | Makes API calls to | HTTPS/JSON |
| API Application | Database | Reads from and writes to | JDBC |
| API Application | Core Banking System | Makes API calls to | HTTPS/XML |
| API Application | E-mail System (AWS SES) | Sends e-mail using | SMTP |

---

## Level 3 — Component

**Scope:** a **single container** in scope.
**Primary elements:** the **components** inside that container — their responsibilities and
implementation detail.
**Supporting elements:** the other containers (in the same system) plus the people and external
systems directly connected to these components.
**Audience:** software architects and developers.
Prefer **generating it from the codebase** — the component-to-code mapping drifts stale faster than any
other level when maintained.

> A **component** is a grouping of related functionality behind a well-defined interface. Components
> are **not** separately deployable — they run inside a container.

Communicate: how the container decomposes into components, what each is responsible for, and the
technology / implementation behind each and how they collaborate.

Because you may document more than one container this way, **repeat the two-table block once per
container**, each under a heading naming the container in scope.

### Elements table

Same shape as the container view; **Technology** here means the component's implementation
(framework, library, layer), and you should scope each table to one container.

| Name | Type | Technology | Responsibility |
|---|---|---|---|
| *&lt;a component&gt;* | Component | *e.g. Spring MVC Rest Controller* | What this component does. |
| *&lt;a component&gt;* | Component | *e.g. Spring Bean* | What this component does. |

- **Type** vocabulary: `Component`, `Component (Database)`, `Component (Queue)` and `(External)`
  variants; supporting elements keep their `Container`, `Person`, `Software System` types.

### Relationships table

Include both **component-to-component** calls inside the container and **component-to-outside** calls
(to other containers, external systems, or people).

| From | To | Description | Technology |
|---|---|---|---|
| *Controller* | *Service component* | "Uses" | — |
| *Service component* | *Database* | "Reads from and writes to" | JDBC |
| *Service component* | *External system facade* | "Uses" | — |

### Worked example — API Application container (Components)

**Elements** *(components inside the API Application)*

| Name | Type | Technology | Responsibility |
|---|---|---|---|
| Sign In Controller | Component | Spring MVC Rest Controller | Allows users to sign in to the internet banking system. |
| Accounts Summary Controller | Component | Spring MVC Rest Controller | Provides customers with a summary of their bank accounts. |
| Security Component | Component | Spring Bean | Provides functionality for signing in and checking credentials. |
| Mainframe Banking System Facade | Component | Spring Bean | A facade over the Core Banking System. |

**Relationships**

| From | To | Description | Technology |
|---|---|---|---|
| Single-Page Application *(container)* | Sign In Controller | Makes API calls to | HTTPS/JSON |
| Single-Page Application *(container)* | Accounts Summary Controller | Makes API calls to | HTTPS/JSON |
| Sign In Controller | Security Component | Uses | — |
| Accounts Summary Controller | Mainframe Banking System Facade | Uses | — |
| Security Component | Database *(container)* | Reads from and writes to | JDBC |
| Mainframe Banking System Facade | Core Banking System *(external)* | Makes API calls to | HTTPS/XML |

---

## Legend template

Drop a section like this near the top of any C4-to-text document and keep the columns you actually
use.

```markdown
## Legend

**Element types**
- Person — a human user, actor, role, or persona.
- Software System — the highest level of abstraction; something that delivers value. `(External)` = outside our control.
- Container — a separately runnable/deployable app or data store (NOT a Docker container). `(Database)` / `(Queue)` variants noted.
- Component — a grouping of related functionality inside a container; not separately deployable.

**Scope markers**
- In scope — the system/container this view zooms into and everything we own inside it.
- External — a dependency outside our responsibility.

**Relationship columns**
- From → To is directional. The Description reads as "From <description> To".
- Technology names the protocol/format where it matters (e.g. HTTPS/JSON, JDBC, SMTP); "—" means unspecified/not relevant at this level.
```

---

## Quality checklist

Before considering a C4-to-text document done:

- [ ] Each level is titled with its **type and the thing in scope**.
- [ ] Every element has a **name, type, and one-line responsibility**; containers and components also
      have a **technology**.
- [ ] Every element is marked **in-scope or external** (no ambiguity about the boundary).
- [ ] Every relationship has a **direction (From/To)**, an **active-verb description** that reads as
      English, and a **protocol where it matters**.
- [ ] A **legend** defines the element-type vocabulary and scope markers used.
- [ ] Detail sits at the **right altitude** per level (no protocols in Context; no deployment in
      Container).
- [ ] Only the **levels that add value** are included; Component views are scoped one-container-per
      block and ideally generated from code.

---

*Local reference for the `c4-to-text` skill. Definitions and guidance summarised from c4model.com
(C4 model by Simon Brown, CC BY 4.0). The Internet Banking System example is C4's canonical example,
reused here across levels. Verify against the source for the latest wording.*
