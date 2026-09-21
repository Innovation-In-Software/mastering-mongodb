#!/usr/bin/env python3
"""Shared ChatGPT + Playwright runner for Mastering MongoDB HD diagrams.

Same approach as MD287 new PPTs: 16:9 architecture PNG, diagram only,
resume-safe progress, persistent ChatGPT Chrome profile.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

TOOL = Path(
    r"D:\Current_work\Innovation in Software\Java Software Engineer bootcamp"
    r"\Java Software Engineer Bootcamp\scripts\chatgpt_slide_images"
)
sys.path.insert(0, str(TOOL))


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


def filename_for(item: dict) -> str:
    title = item["title"]
    for ch in '/\\:?*"|<>':
        title = title.replace(ch, "-")
    title = title.replace("`", "")
    return f"{item['slide']:03d} - {title}.png"


def load_progress(progress_file: Path) -> dict:
    if progress_file.is_file():
        return json.loads(progress_file.read_text(encoding="utf-8"))
    return {"done": {}, "failed": {}}


def save_progress(progress_file: Path, progress: dict) -> None:
    progress_file.write_text(json.dumps(progress, indent=2), encoding="utf-8")


def append_result(results_file: Path, row: list[str]) -> None:
    new_file = not results_file.exists()
    with results_file.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        if new_file:
            writer.writerow(
                ["timestamp", "slide", "title", "output", "status", "details"]
            )
        writer.writerow(row)


def parse_args(description: str) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=description)
    p.add_argument("--max", type=int, default=None)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--force", action="store_true")
    p.add_argument("--slides", type=str, default=None)
    p.add_argument("--timeout", type=int, default=240)
    p.add_argument("--login-timeout", type=int, default=900)
    p.add_argument("--pause-ms", type=int, default=2000)
    p.add_argument("--new-chat-every", type=int, default=8)
    p.add_argument("--headless", action="store_true")
    p.add_argument(
        "--profile",
        type=str,
        default="browser_profile",
        help="Chrome user-data folder name under chatgpt_slide_images/",
    )
    return p.parse_args()


def selected(diagrams: list[dict], args: argparse.Namespace) -> list[dict]:
    items = diagrams
    if args.slides:
        wanted = {int(x.strip()) for x in args.slides.split(",") if x.strip()}
        items = [d for d in diagrams if d["slide"] in wanted]
    return items


def run(
    *,
    description: str,
    out_dir: Path,
    log_dir: Path,
    progress_file: Path,
    results_file: Path,
    prompt_template: str,
    diagrams: list[dict],
) -> int:
    args = parse_args(description)
    profile_dir = Path(args.profile)
    if not profile_dir.is_absolute():
        profile_dir = TOOL / args.profile
    profile_dir.mkdir(parents=True, exist_ok=True)
    log(f"Chrome profile: {profile_dir}")
    items = selected(diagrams, args)
    out_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)
    progress = load_progress(progress_file)

    queue: list[tuple[dict, Path]] = []
    for item in items:
        dest = out_dir / filename_for(item)
        key = f"s{item['slide']:03d}"
        if (
            not args.force
            and dest.is_file()
            and dest.stat().st_size > 0
            and key in progress.get("done", {})
        ):
            continue
        if not args.force and dest.is_file() and dest.stat().st_size > 0:
            progress.setdefault("done", {})[key] = dest.name
            continue
        queue.append((item, dest))

    log(
        f"Diagrams: {len(items)} | queued: {len(queue)} | skipped: {len(items) - len(queue)}"
    )
    for item, dest in queue:
        log(f"  slide {item['slide']:03d}  {item['title']} → {dest.name}")

    if args.dry_run:
        return 0
    if not queue:
        log("Nothing to generate.")
        save_progress(progress_file, progress)
        return 0

    from playwright.sync_api import sync_playwright
    from chatgpt_automation import (
        generate_one_image,
        open_new_chat,
        wait_for_manual_login,
    )

    successes = 0
    failures = 0
    quota_hit = False

    with sync_playwright() as playwright:
        launch_kwargs = dict(
            user_data_dir=str(profile_dir),
            headless=args.headless,
            viewport={"width": 1400, "height": 900},
            accept_downloads=True,
            args=["--disable-blink-features=AutomationControlled", "--disable-dev-shm-usage"],
            ignore_default_args=["--enable-automation"],
        )
        try:
            context = playwright.chromium.launch_persistent_context(
                channel="chrome", **launch_kwargs
            )
            log("Launched Google Chrome for ChatGPT.")
        except Exception as exc:
            log(f"Chrome channel unavailable ({exc}); using Chromium.")
            context = playwright.chromium.launch_persistent_context(**launch_kwargs)

        page = context.pages[0] if context.pages else context.new_page()
        wait_for_manual_login(page, timeout_sec=args.login_timeout)
        open_new_chat(page)

        for i, (item, dest) in enumerate(queue, start=1):
            if args.max is not None and (successes + failures) >= args.max:
                break
            if args.new_chat_every and i > 1 and (i - 1) % args.new_chat_every == 0:
                open_new_chat(page)
            prompt = prompt_template.format(
                title=item["title"], show=item["show"]
            ).strip()
            log(f"[{i}/{len(queue)}] Slide {item['slide']:03d} — {item['title']}")
            try:
                generate_one_image(
                    page,
                    prompt=prompt,
                    dest=dest,
                    log_dir=log_dir,
                    timeout_sec=args.timeout,
                )
                if not dest.is_file() or dest.stat().st_size == 0:
                    raise RuntimeError("Download produced empty file")
                key = f"s{item['slide']:03d}"
                progress.setdefault("done", {})[key] = dest.name
                progress.get("failed", {}).pop(key, None)
                save_progress(progress_file, progress)
                append_result(
                    results_file,
                    [
                        datetime.now().isoformat(timespec="seconds"),
                        item["slide"],
                        item["title"],
                        dest.name,
                        "SUCCESS",
                        "",
                    ],
                )
                successes += 1
                log(f"SUCCESS → {dest.name} ({dest.stat().st_size} bytes)")
            except Exception as exc:
                failures += 1
                key = f"s{item['slide']:03d}"
                progress.setdefault("failed", {})[key] = str(exc)
                save_progress(progress_file, progress)
                append_result(
                    results_file,
                    [
                        datetime.now().isoformat(timespec="seconds"),
                        item["slide"],
                        item["title"],
                        dest.name,
                        "FAILED",
                        str(exc)[:300],
                    ],
                )
                log(f"FAILED: {exc}")
                if "QUOTA:" in str(exc) or "quota/limit reached" in str(exc).lower():
                    log("Aborting remaining diagrams — image quota exhausted.")
                    quota_hit = True
                    break
            page.wait_for_timeout(args.pause_ms)

        context.close()

    log(f"Finished. success={successes} failed={failures}")
    log(f"Output: {out_dir}")
    if quota_hit:
        return 3
    return 0 if failures == 0 else 2
