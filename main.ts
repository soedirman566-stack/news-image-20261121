// main.ts -- entry point for the news-image-20261121 bounty.
//
// The entry itself is a single picture: entry.png, a broadsheet front
// page ("The Daily Globe") summing up the world news of Saturday
// 21 November 2026 in one 1024x1024 image. The page was composed from
// real, freely licensed news photographs by compose.py, which stays in
// this repository as the record of how the picture was made.
//
// All this program has to do is hand the picture in: copy the
// committed entry.png into the output directory the runner points at
// with the MAKEFUN_OUTPUT_DIR environment variable ("output" when the
// variable is not set), creating the directory first if it is missing.
// The copy is byte-for-byte, so the file the judges see is exactly the
// file committed here.

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "output";

mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));

console.log(`entry.png handed in to ${outDir}/entry.png`);
