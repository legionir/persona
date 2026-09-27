#!/usr/bin/env node
/**
 * Functional test for index.html (the Persona Finder).
 *
 * index.html is a single static file that fetches personas.json and
 * skills/index.json and renders 209 personas (190 roles + 19 composites).
 * Nothing in the Python pipeline touches it, so without this harness a
 * regression in the page ships silently.
 *
 * What it covers:
 *   - both data files load and the counts they advertise are right
 *   - the default view renders every persona exactly once
 *   - the Role type filter covers SUPERVISOR / EXECUTOR / Composite
 *   - selecting Composite disables the role-only facets
 *   - search works across both kinds, and the empty state appears
 *   - sorting, reset, and facet filtering still behave
 *
 * Usage:
 *     node scripts/test_web.js          # needs jsdom: npm install
 *
 * The script reads the real files from the repository root, so run it from
 * anywhere — it resolves paths relative to itself.
 */
"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");

let JSDOM;
try {
  ({ JSDOM } = require("jsdom"));
} catch (e) {
  console.error(
    "SKIP: jsdom is not installed.\n" +
    "      Install the dev dependencies first:  npm install\n" +
    "      (jsdom is only needed to run this test; the site itself has no dependencies.)"
  );
  process.exit(0);
}

const readJson = (rel) => JSON.parse(fs.readFileSync(path.join(ROOT, rel), "utf8"));
const personas = readJson("personas.json");
const skills = readJson("skills/index.json");
const html = fs.readFileSync(path.join(ROOT, "index.html"), "utf8");

const dom = new JSDOM(html, {
  url: "http://localhost:8000/index.html",
  runScripts: "dangerously",
  pretendToBeVisual: true,
  beforeParse(window) {
    // Serve the repository over a fake HTTP origin so the page's relative
    // fetches resolve exactly as they do on GitHub Pages.
    window.fetch = (u) => {
      const rel = String(u).replace(/^https?:\/\/[^/]+\//, "");
      try {
        const body = fs.readFileSync(path.join(ROOT, rel), "utf8");
        return Promise.resolve({
          ok: true, status: 200,
          json: () => Promise.resolve(JSON.parse(body)),
        });
      } catch (e) {
        return Promise.resolve({ ok: false, status: 404, json: () => Promise.reject(e) });
      }
    };
  },
});

const w = dom.window;
const d = w.document;
const $ = (id) => d.getElementById(id);
const cards = () => d.querySelectorAll("#grid .card");

const out = [];
const ok = (label, cond, extra = "") =>
  out.push(`${cond ? "PASS" : "FAIL"}  ${label}${extra ? " — " + extra : ""}`);
const fire = (el, type = "change") =>
  el.dispatchEvent(new w.Event(type, { bubbles: true }));

const ROLE_ONLY = ["fGroup", "fDomain", "fCategory", "fSeniority"];

setTimeout(() => {
  // ---------- boot ----------
  ok("both data files load",
     $("stats").textContent.includes("190") && $("stats").textContent.includes("19"),
     $("stats").textContent.replace(/\s+/g, " ").trim());
  ok("no error banner", $("empty").hidden === true);

  // ---------- default view ----------
  ok("every persona renders exactly once", cards().length === personas.totals.roles + skills.totals.composites,
     `${cards().length} cards`);
  ok("count line", $("count").textContent ===
     `${cards().length} of ${cards().length} results`, $("count").textContent);

  // ---------- the Role type dropdown ----------
  const opts = [...$("fType").options].map((o) => [o.value, o.textContent]);
  ok("Role type carries All / SUPERVISOR / EXECUTOR / Composite",
     JSON.stringify(opts) === JSON.stringify(
       [["", "All"], ["SUPERVISOR", "SUPERVISOR"], ["EXECUTOR", "EXECUTOR"], ["COMPOSITE", "Composite"]]),
     JSON.stringify(opts));

  // ---------- Composite ----------
  $("fType").value = "COMPOSITE";
  fire($("fType"));
  ok("Composite -> 19 cards", cards().length === skills.totals.composites,
     `${cards().length} cards`);
  ok("count line reflects the whole library",
     $("count").textContent === `${skills.totals.composites} of ${personas.totals.roles + skills.totals.composites} results`,
     $("count").textContent);
  ok("role-only facets disabled", ROLE_ONLY.every((id) => $(id).disabled === true));
  ok("role-only facets cleared", ROLE_ONLY.every((id) => $(id).value === ""));
  ok("facet wrappers dimmed", d.querySelectorAll("#filters .off").length === ROLE_ONLY.length,
     `${d.querySelectorAll("#filters .off").length} dimmed`);
  ok("sort stays available", $("fSort").disabled === false);
  ok("every card is a composite",
     [...cards()].every((c) => c.querySelector(".badge.comp")));
  const chipCounts = [...cards()].map((c) => c.querySelectorAll(".chip").length);
  ok("composite cards carry only their own chips",
     chipCounts.every((n) => n === 2 || n === 3),
     `chip counts: ${JSON.stringify([...new Set(chipCounts)])}`);
  ok("lens chip where the spec has one",
     [...cards()].filter((c) => c.textContent.includes("lenses")).length ===
     skills.skills.filter((s) => s.type === "COMPOSITE" && s.lenses).length,
     `${[...cards()].filter((c) => c.textContent.includes("lenses")).length} cards`);
  ok("titles drop the '— Master Prompt (vN)' suffix",
     ![...cards()].some((c) => c.querySelector("h2").textContent.includes("Master Prompt")));
  ok("master prompt link present",
     !!d.querySelector("#grid .card .foot a[href*='prompts/composite/']"));
  ok("skill link present",
     !!d.querySelector("#grid .card .foot a[href*='skills/']"));

  // ---------- search within Composite ----------
  $("q").value = "forensic";
  fire($("q"), "input");
  setTimeout(() => {
    ok("search 'forensic' inside Composite", cards().length === 8, `${cards().length} cards`);

    // ---------- empty state ----------
    $("q").value = "zzzznotathing";
    fire($("q"), "input");
    setTimeout(() => {
      ok("empty state appears", $("empty").hidden === false);

      // ---------- back to All ----------
      $("q").value = "";
      $("fType").value = "";
      fire($("fType"));
      ok("All -> every persona again",
         cards().length === personas.totals.roles + skills.totals.composites);
      ok("facets re-enabled", ROLE_ONLY.every((id) => $(id).disabled === false));
      ok("dimming cleared", d.querySelectorAll("#filters .off").length === 0);

      // ---------- each type count ----------
      $("fType").value = "SUPERVISOR";
      fire($("fType"));
      ok("SUPERVISOR -> 75", cards().length === personas.totals.supervisors,
         `${cards().length} cards`);
      $("fType").value = "EXECUTOR";
      fire($("fType"));
      ok("EXECUTOR -> 115", cards().length === personas.totals.executors,
         `${cards().length} cards`);

      // ---------- a role-only facet excludes composites ----------
      $("fType").value = "";
      $("fDomain").value = "Design";
      fire($("fType"));
      fire($("fDomain"));
      const inDesign = cards().length;
      ok("domain facet narrows to roles", inDesign > 0 && inDesign < personas.totals.roles,
         `${inDesign} cards`);
      ok("a role-only facet never returns a composite",
         ![...cards()].some((c) => c.querySelector(".badge.comp")));

      // ---------- sorting ----------
      $("fDomain").value = "";
      $("fSort").value = "type";
      fire($("fSort"));
      ok("sort by type puts composites first",
         d.querySelector("#grid .card .badge").classList.contains("comp"),
         d.querySelector("#grid .card .badge").textContent);

      // ---------- reset ----------
      fire($("reset"), "click");
      ok("reset restores every persona",
         cards().length === personas.totals.roles + skills.totals.composites);
      ok("reset clears every control",
         ["fType", ...ROLE_ONLY].every((id) => $(id).value === "") &&
         $("fSort").value === "default" && $("q").value === "");

      // ---------- cross-kind search ----------
      $("q").value = "audit";
      fire($("q"), "input");
      setTimeout(() => {
        const hits = cards().length;
        ok("search 'audit' spans both kinds",
           hits > skills.totals.composites &&
           [...cards()].some((c) => c.querySelector(".badge.comp")),
           `${hits} cards`);

        console.log(out.join("\n"));
        const failed = out.filter((l) => l.startsWith("FAIL")).length;
        console.log(`\n${out.length - failed}/${out.length} checks passed`);
        process.exit(failed ? 1 : 0);
      }, 250);
    }, 250);
  }, 250);
}, 700);
