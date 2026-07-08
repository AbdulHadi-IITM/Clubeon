# MAY2026-Team-096
# Community Services Platform — Sports Club Edition: Developer's Guide

This guide defines the engineering standards, workflow, and software methodology for contributing to our **Sports Facility Booking & Club Management System** — an academic Software Engineering project built as a **Community Services Platform** for the sports-club subdomain, following **Scrum/Agile**.

## Table of Contents

0. [Project Overview](#0-project-overview)
1. [Architecture Standards (Modular Monolith)](#1-architecture-standards-modular-monolith)
2. [Branching Strategy](#2-branching-strategy)
3. [The Daily Developer Workflow](#3-the-daily-developer-workflow)
4. [Project Board Automation](#4-project-board-automation)
5. [Sprint Cadence & Definition of Done](#5-sprint-cadence--definition-of-done)

## Quick Reference

| Topic | Rule |
|---|---|
| Architecture | Modular Monolith — domain-first packages, `api` vs `internal` |
| Cross-module calls | Only through public Facade interfaces, never direct DB access |
| Default branch | `develop` |
| Release branch | `main` (mirrors the demo/production build) |
| Feature branches | `feature/<issue-number>-<short-description>` |
| Hotfix branches | `hotfix/*`, branched from `main` |
| Commit style | Conventional Commits (`feat:`, `fix:`, `refactor:`, `docs:`) + issue closing keyword |
| PR requirement | 1 approval minimum, targets `develop` |
| Board automation | `Closes #12` / `Resolves #12` / `Fixes #12` in commits or PR body |
| Methodology | Scrum — 2-week sprints, backlog-driven, board = source of truth |

---

## 0. Project Overview

**Problem statement:** Sports clubs with limited facilities (e.g. a fixed number of badminton courts) currently rely on fragmented tools — WhatsApp groups, spreadsheets, paper logs — to manage both casual public bookings and permanent member schedules. This causes double-bookings, scheduling conflicts, and frustrated members.

**Our solution:** A unified Sports Facility Booking & Club Management System that lets the public book available courts pay-as-you-go, while reserving guaranteed slots and premium features for permanent members — giving administrators one platform to manage availability, memberships, events, attendance, and communication.

### User Roles

| Tier | Role | Interaction |
|---|---|---|
| Primary | Public/Casual Players | Book courts pay-as-you-go; highest volume, most frequent users |
| Primary | Permanent/Premium Members | Guaranteed recurring slots + premium features |
| Primary | Club Owner/Admin | Manages court allocation, pricing, schedules, revenue |
| Secondary | Front-desk/Operations Staff | Handles walk-ins, conflict resolution, manual overrides |
| Secondary | Coaches/Trainers | Book/are assigned courts for sessions |
| Secondary | Event Organizers | Block larger slots for tournaments/group sessions |
| Tertiary | Maintenance/Facility Staff | Affected by scheduling, doesn't operate the system |
| Tertiary | Club Investors/Business Partners | Consume revenue/occupancy reports only |
| Tertiary | Guest Members | Use a court booked by a member; never touch the app |

### Candidate Domain Modules

These map to the workflows in scope (membership management, event organization, resource/court booking, volunteer/coach scheduling, issue tracking, communication) and should become our top-level modules:

- `users` — authentication, roles, profiles
- `memberships` — permanent/premium membership lifecycle, tiers, pausing/renewal
- `bookings` — court/resource reservation, availability, conflict resolution
- `events` — tournaments, group sessions, event scheduling
- `payments` — pay-as-you-go charges, membership dues, invoicing
- `attendance` — check-in/check-out tracking for bookings and sessions
- `notifications` — communication workflows (schedule changes, event/maintenance alerts)

---

## 1. Architecture Standards (Modular Monolith)

We follow a strict **Modular Monolith** architecture. Code is grouped by **business domain** (`bookings`, `memberships`, `payments`, etc. — see [Section 0](#0-project-overview)), never by technical layer (no app-wide `controllers/`, `services/`, `repositories/` folders).

> Stack is not finalized yet, so the rules and examples below are written stack-agnostically. Once the team picks a language/framework, translate the pseudo-code into that stack's idioms (e.g. Java packages, Python modules, or NestJS modules) but keep the `api` / `internal` boundary.

### Directory Structure Rules

Every domain module must be split into exactly two parts:

| Part | Contents | Visibility |
|---|---|---|
| `api` | Public interfaces / contracts and Data Transfer Objects (DTOs) | The **only** files other modules may import |
| `internal` | Business logic, entities, controllers, repositories/data access | Private to the module — never imported directly by other modules |

### Cross-Module Communication

Modules must **never** query another module's database tables directly. All cross-module communication flows through public **Facade interfaces** defined in the `api` part.

**Example: `bookings` module**

Public contract (`bookings/api`):

```
interface BookingFacade {
    Booking createBooking(courtId, userId, timeSlot)
    boolean isCourtAvailable(courtId, timeSlot)
}
```

Internal implementation (`bookings/internal`, not exported):

```
class BookingServiceImpl implements BookingFacade {
    constructor(bookingRepository, membershipFacade, notificationFacade) { ... }

    createBooking(courtId, userId, timeSlot) {
        // checks availability, resolves conflicts,
        // calls membershipFacade to confirm tier/priority,
        // calls notificationFacade to send confirmation
    }
}
```

Notice that when `bookings` needs to know a user's membership tier, it calls `MembershipFacade` from the `memberships` module's `api` — it never reads the `memberships` database tables directly. Same for sending a confirmation: it calls `NotificationFacade`, not an email/SMS library directly.

### Why This Matters

- **Conflict-safe booking logic stays in one place** — since `bookings` is the only module that touches booking data, double-booking bugs get fixed once, not per caller.
- **Membership rules stay authoritative** — priority rules (e.g. permanent members over walk-ins) live only inside `memberships`, exposed via its Facade, so every module (bookings, events, payments) sees the same rule.
- **Future extraction** — if `payments` ever needs to become a separate service (e.g. for PCI compliance), the Facade boundary is already the seam to cut along.

---

## 2. Branching Strategy

| Branch | Purpose | Branches from | Merges into |
|---|---|---|---|
| `develop` | Default integration branch. All active development merges here. | — | `main` (on release/demo milestone) |
| `main` | Stable branch. Mirrors the latest working demo/submission build. | — | — |
| `feature/*` | Short-lived branches tied to a specific GitHub Issue / backlog item. | `develop` | `develop` |
| `hotfix/*` | Emergency fixes to a broken `main` (e.g. right before a demo/submission). | `main` | `main` and `develop` |

### Naming Convention

```
feature/<issue-number>-<short-kebab-case-description>
```

Example:

```
feature/17-court-availability-calendar
```

---

## 3. The Daily Developer Workflow

### Step 1: Claim a Backlog Item

Never write code without an assigned GitHub Issue pulled from the current Sprint Backlog. If a task doesn't exist yet, add it to the Product Backlog using the standard **Feature** or **Bug** issue template, then move it into the sprint during Sprint Planning.

### Step 2: Sync and Branch

Always branch off the latest `develop`. The branch name must include the issue number.

```bash
git checkout develop
git pull origin develop
git checkout -b feature/17-court-availability-calendar
```

### Step 3: Smart Commits

Use Conventional Commit prefixes, plus a GitHub closing keyword so the Scrum board updates itself automatically (see [Section 4](#4-project-board-automation)).

| Prefix | Use for |
|---|---|
| `feat:` | A new feature |
| `fix:` | A bug fix |
| `refactor:` | Structural code changes |
| `docs:` | Documentation updates |

```bash
git add .
git commit -m "feat: add real-time court availability calendar (Closes #17)"
```

### Step 4: Pull Requests

- Push your feature branch to the remote repository.
- Open a Pull Request targeting `develop` (never `main` directly).
- Ensure the PR description links to the original issue with a closing keyword.
- **At least 1 approval** from a teammate is required before merging.
- **Delete the feature branch** after a successful merge.

---

## 4. Project Board Automation

Our GitHub Project board doubles as our **Scrum board**. It runs on an automated, event-driven system — cards move automatically based on your Git activity, so the board is always an honest reflection of sprint progress without manual updates.

### The Magic Keywords

| Keyword | Use for |
|---|---|
| `Closes #12` or `Resolves #12` | Features / user stories |
| `Fixes #12` | Bugs |

**Where to use them:**

1. **Commit messages** — e.g. `git commit -m "fix: resolve double-booking race condition (Fixes #23)"`
2. **Pull Request descriptions** — include `Closes #12` in the PR body.

### The Automated Lifecycle (mapped to Scrum board columns)

1. **Product Backlog → Sprint Backlog:** During Sprint Planning, an issue is added to the current sprint's milestone/board.
2. **In Progress:** Pushing your branch and opening a **Draft Pull Request** with the linking keyword automatically moves the card to "In Progress".
3. **In Review:** Marking the PR "Ready for review" moves the card to "In Review".
4. **Done:** When the PR is approved and **merged** into `develop`, GitHub automatically closes the linked issue and moves the card to "Done".

---

## 5. Sprint Cadence & Definition of Done

- **Sprint length:** 2 weeks (adjust to match the course/academic calendar).
- **Sprint Planning:** Pull top-priority Product Backlog items into the Sprint Backlog; break large items into issues sized to 1–3 days each.
- **Daily Standup:** Quick async or sync check-in — what you did, what's next, any blockers.
- **Sprint Review/Demo:** Demo completed, merged features on `develop` (or `main` if released) to the team/stakeholders.
- **Sprint Retrospective:** What went well, what didn't, one concrete process change for next sprint.

**Definition of Done** — an issue is only moved to "Done" when:

- [ ] Code follows the `api`/`internal` module boundary (no cross-module DB access).
- [ ] PR has at least 1 approval.
- [ ] PR is merged into `develop` with a closing keyword.
- [ ] Feature branch is deleted post-merge.
- [ ] Any new/changed behavior is documented (README, wiki, or inline docs).
