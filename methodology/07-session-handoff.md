# 07 - Session handoff (the resume contract)

A new session must be able to resume any problem with ZERO loss: full understanding of what is
proved, what is in flight, and what to do next, without reading the chat history that produced
it. The repository is the memory; this document defines the file that makes it instant.

## The RESUME.md file (per problem, mandatory)

`program/<problem>/RESUME.md` is the SINGLE FIRST-READ for a fresh session. It is updated:
- at the END of every working session (mandatory, before the closing commit), and
- mid-session whenever a major result lands or the in-flight derivation changes.

Required sections, in order:

1. **State in one screen.** What is proved/established, with the KEY FORMULAS inline (not
   pointers): the objects a mathematician needs in front of them. Labeled [MV]/[D]/[C] as
   everywhere else.
2. **The objects table.** The named artifacts of the problem (maps, ideals, equations,
   machines) with their one-line definitions and the experiment that owns each.
3. **Experiment index.** One line per EXP-NNN: question, verdict, the single load-bearing
   output. (The wiki has the long form; this is the scan version.)
4. **In flight.** The CURRENT experiment(s): the hypothesis being tested, any mid-derivation
   insight not yet in a verdict (write the mathematics down, not a pointer to it), and the
   exact state of partial runs (which parts passed, which are pending).
5. **Next actions, ordered.** Numbered, concrete, with the exact commands to run and the
   expected decision points. A new session should be able to start at item 1 within minutes.
6. **Where everything lives.** The path map: experiments, wiki, manuscripts, program files,
   baked artifacts, web app, diffusion assets (with repo-relative paths).
7. **Gotchas.** Solver artifacts and workarounds discovered (with the EXP that documented
   them), runtime caps, environment facts (venv, GPU), and conventions that bite.

## Rules

- RESUME.md is DERIVED from the primary records (verdicts, log, backlog): never the only place
  a fact lives; always the fastest place to find it. On conflict, the experiment record wins
  and RESUME.md is corrected.
- Mid-derivation mathematics (the thinking between experiments) goes into the NEXT
  experiment's hypothesis.md at declaration time; RESUME.md carries it only while no
  hypothesis file exists yet.
- The closing commit of every session touches: RESUME.md, `state.md` (heartbeat), `backlog.md`
  (row statuses), `history/log.md` (the dated entry), and the CHANGELOG when a version ships.
  A session that ends without this closing pass is an incomplete session.
- The management repo (`plans/caos-research/` in CAOS_MANAGE) keeps the portfolio-level
  mirror (findings F-numbers, history rows); RESUME.md is the problem-level deep state.
