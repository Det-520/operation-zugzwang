# References — Operation Zugzwang

The references behind the game: the training objective, writing and style, the matrix game method, and doctrine (AFDP, JP) in `doctrine/`.

**Not in git:** the PDFs and their `text/` copies belong to their publishers. Run `python3 tools/fetch_third_party.py` from the project root to download them and make the text copies (it lists each source URL). If an Air Force site refuses the download, open the URL it prints in a browser and save the file to the path shown.

| File | What it is | Notes |
| --- | --- | --- |
| `training-objective.txt` | LLAB training objective 1.3 and its performance measures | Read-only. In git. |
| `PracticalAdviceOnMatrixGames.pdf` | Tom Mouat, *Practical Advice on Matrix Games* v15, from mapsymbs.com | Read-only. The method the game follows. Fetched. |
| `doctrine/` | AFDP and JP PDFs with text copies | Fetched. Indexed in `doctrine/README.md`. |
| `AFH_33-337_Tongue_and_Quill.pdf` | AFH 33-337, *The Tongue and Quill*, 27 May 2015, incorporating Change 1 (19 Nov 2015), certified current 27 Jul 2016. 370 pages. | Read-only. The Air Force's writing and correspondence handbook. Check the e-Publishing site for a newer edition before relying on fine format details. |
| `text/AFH_33-337_Tongue_and_Quill.txt` | Plain-text copy made with `pdftotext -layout` | For searching. The example documents and paper templates in ch. 14–16 are images, so they're missing from the text copy. Use the PDF for those. |
| `tongue-and-quill-summary.md` | Summary of the parts that matter for this project, with page numbers, plus how each handout should be written | Start here |

## Searching the text copy

The handbook prints page numbers as `- 163 -` on their own line, so you can jump to a page:

```bash
grep -n -E '^\s*- 163 -\s*$' text/AFH_33-337_Tongue_and_Quill.txt
grep -n -i 'signature block' text/AFH_33-337_Tongue_and_Quill.txt
```
