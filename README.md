# MAY2026-Team-096
# ClinicCare EHR System: Developer's Guide

This guide defines the engineering standards, workflow, and architectural rules for contributing to the ClinicCare system.

## Table of Contents

1. [Architecture Standards (Modular Monolith)](#1-architecture-standards-modular-monolith)
2. [Branching Strategy](#2-branching-strategy)
3. [The Daily Developer Workflow](#3-the-daily-developer-workflow)
4. [Project Board Automation](#4-project-board-automation)

## Quick Reference

| Topic | Rule |
|---|---|
| Architecture | Modular Monolith — domain-first packages, `api` vs `internal` |
| Cross-module calls | Only through public Facade interfaces, never direct DB access |
| Default branch | `develop` |
| Release branch | `master` (mirrors production) |
| Feature branches | `feature/<issue-number>-<short-description>` |
| Hotfix branches | `hotfix/*`, branched from `master` |
| Commit style | Conventional Commits (`feat:`, `fix:`, `refactor:`, `docs:`) + issue closing keyword |
| PR requirement | 1 approval minimum, targets `develop` |
| Board automation | `Closes #12` / `Resolves #12` / `Fixes #12` in commits or PR body |

---

## 1. Architectural Standards (Modular Monolith)

We follow a strict **Modular Monolith** architecture. Code is grouped by **business domain** (e.g. `patients`, `appointments`, `billing`), never by technical layer.

### Directory Structure Rules

Every domain module must be split into exactly two packages:

| Package | Contents | Visibility |
|---|---|---|
| `api` | Public interfaces and Data Transfer Objects (DTOs) | The **only** files other modules may import |
| `internal` | Business logic, entities, controllers, repositories | Package-private — never imported by other modules |

### Cross-Module Communication

Modules must never query another module's database tables directly. All cross-module communication must flow through the public **Facade interfaces**.

**Public contract** (`com.cliniccare.billing.api`):

```java
package com.cliniccare.billing.api;

import java.util.UUID;

public interface BillingFacade {
    InvoiceDto generateInvoice(UUID appointmentId);
}
```

**Internal implementation** (`com.cliniccare.billing.internal`):

```java
package com.cliniccare.billing.internal;

import com.cliniccare.billing.api.BillingFacade;
import com.cliniccare.billing.api.InvoiceDto;
import java.util.UUID;
import org.springframework.stereotype.Service;

@Service
class BillingServiceImpl implements BillingFacade {

    private final BillingRepository repository;

    public BillingServiceImpl(BillingRepository repository) {
        this.repository = repository;
    }

    @Override
    public InvoiceDto generateInvoice(UUID appointmentId) {
        return new InvoiceDto();
    }
}
```

`BillingServiceImpl` is package-private — it can only be constructed and wired within the `billing` module. Other modules that need an invoice call `BillingFacade.generateInvoice(...)`, never `BillingServiceImpl` or `BillingRepository` directly.

---

## 2. Branching Strategy

| Branch | Purpose |
|---|---|
| **`develop`** | The default integration branch. All active development merges here. |
| **`master`** | The stable release branch. Strictly mirrors production. |
| **`feature/*`** | Short-lived branches tied to a specific GitHub Issue. |
| **`hotfix/*`** | Emergency fixes branching directly from `master`. |

### Step 1: Claim an Issue

Never write code without an assigned GitHub Issue. If a task does not exist, create one using the standard Feature or Bug templates.

### Step 2: Sync and Branch

Always branch off the latest `develop` branch. Your branch name must include the issue number.

```bash
git checkout develop
git pull origin develop
git checkout -b feature/42-extract-billing-module
```

---

## 3. The Daily Developer Workflow

### Step 3: Smart Commits

We use conventional commit prefixes to maintain a clean history. You must include the GitHub Issue number using the closing syntax to automate the project board.

| Prefix | Use for |
|---|---|
| `feat:` | A new feature |
| `fix:` | A bug fix |
| `refactor:` | Structural code changes (e.g. LLD extraction) |
| `docs:` | Documentation updates |

```bash
git add .
git commit -m "feat: implement internal billing facade (Closes #42)"
```

### Step 4: Pull Requests

- Push your feature branch to the remote repository.
- Open a Pull Request targeting the `develop` branch.
- Ensure the PR description links to the original issue.
- At least 1 approval is required before merging.
- Delete the feature branch after a successful merge.

---

## 4. Project Board Automation

Our GitHub Project board runs on an automated, event-driven system. Cards move automatically based on your Git workflow — you should rarely need to drag and drop cards manually.

### The Magic Keywords

To link your code to a board ticket, use one of the following keywords followed by the issue number:

- **For Features/Tasks:** `Closes #12` or `Resolves #12`
- **For Bugs:** `Fixes #12`

**Where to use them:**

1. **Commit Messages:** `git commit -m "fix: resolve login bug (Fixes #12)"`
2. **Pull Request Descriptions:** Include `Closes #12` in the body of your PR.

### The Automated Lifecycle

1. **Todo:** Creating a new Issue automatically places it in the "Todo" column.
2. **In Progress:** Pushing your branch and opening a **Draft Pull Request** with the linking keyword automatically moves the card to "In Progress".
3. **Done:** When the PR is approved and **Merged** into `develop`, GitHub automatically closes the issue and moves the card to "Done".
