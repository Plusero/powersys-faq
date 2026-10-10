# Editing the Dutch electricity market figures

The human-editable source is [generate-market-diagrams.py](../scripts/generate-market-diagrams.py). It draws text, rectangles, lines, and arrows using Python's standard-library XML writer.

The script generates both figures from scratch; it never reads an existing SVG as input. Python 3.9 or newer is required, with no additional packages.

## Edit and regenerate

1. Edit `market_sequence()` for the market overview or `auction_clock()` for the auction timetable. The `reserves` and auction-event lists contain repeated labels and positions. Shared colours and the font are defined near the top of the file.
2. Run from the repository root:

   ```sh
   python3 scripts/generate-market-diagrams.py
   ```

3. Open both SVGs in a browser or the article's Markdown preview. Check text wrapping, overlaps, arrows, and readability. The drawing uses explicit line breaks and coordinates; it does not automatically wrap long labels. Coordinates are SVG pixels; text `y` values are baselines. If a figure grows, update its height in `Drawing(...)` as well as the affected element positions.
4. Keep the source script and generated SVGs together in the change, then run:

   ```sh
   python3 scripts/generate-market-diagrams.py --check
   npm run check
   npm run build
   npm run validate
   git diff --check
   ```

The script can also be called by absolute path from another working directory. Output paths are resolved relative to the script, not your current directory. `--check` makes no changes and exits unsuccessfully if either output is missing or differs from the source.

## Generated outputs

- [Market sequence](../src/assets/diagrams/dutch-market-sequence.svg)
- [Auction clock](../src/assets/diagrams/dutch-market-auction-clock.svg)

The SVGs retain editable text and vector shapes with their own presentation attributes, so they work without the website stylesheet. Direct SVG edits are possible, but regeneration overwrites them: make lasting changes in the Python source.

The [article](../src/content/faqs/electricity-markets-netherlands.md) embeds these files using relative Markdown image paths. Astro handles their built URLs and deployment base path. Captions and image alternative text remain in the article; SVG titles and descriptions are in the generator. Update both when changing meaning or timing, and check the official sources cited in the article.

Normal website builds use the checked-in SVGs and do not require Python or regenerate the diagrams. The generator's `--check` verifies source/output consistency, not visual layout or the accuracy of market rules.
