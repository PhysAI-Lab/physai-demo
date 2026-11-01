# PhysAI Lab · UBC

Research website for Peter Yichen Chen and PhysAI Lab, implemented as a portable static website for GitHub Pages.

## Pages

- `index.html`: robotics-led homepage with selected projects and research news.
- `research.html`: three research directions, with related projects.
- `publications.html`: searchable bibliography with year, topic, publication status, and collection filters; citation previews.
- `demos.html`: research previews and source project/code links.
- `people.html`: principal investigator, one postdoctoral fellow, eight current doctoral researchers (including co-advised students), two incoming PhD students, one master’s student, and two visiting students.
- `news.html`: verified recognition, research updates, and press.
- `join.html`: graduate, postdoctoral, and collaboration information.

## Publish

In GitHub **Settings → Pages**, choose **Deploy from a branch → main → /(root) → Save**. No build workflow or npm installation is required. Keep `.nojekyll` at the repository root.

Expected URL: https://chensiyuan030105.github.io/physai-demo/

## Maintain

Bibliographic content lives in `data/publications.json`. Run `python tools/build.py` after editing it. The generator uses only the Python standard library. Team profile content currently lives in the `PEOPLE`, `POSTDOCS`, `INCOMING`, `MASTERS`, and `VISITORS` lists in `tools/build.py`; `data/people.json` is a generated export. Other editorial sections also live in the generator.

Shared appearance and behavior are in `assets/site.css` and `assets/site.js`. Generated HTML works without JavaScript; filtering and preview dialogs are progressive enhancements.

The current design follows the restrained academic typography and team presentation of the supplied Cong Lab reference: factual page headings, editorial research rows, and a compact header. Cormorant Garamond, Karla, Josefin Sans, and IBM Plex Mono are self-hosted under the included SIL Open Font License files in `assets/fonts/`.

## Sources and attribution

See `SOURCES.md`. The collection includes Peter's work with collaborators, work at earlier institutions, and current members' independent collaborations. These are identified in the publication filters rather than attributed indiscriminately to UBC PhysAI.

Preprints are explicitly labeled. Accepted future-conference work is grouped with published/accepted work. Generic BibTeX entries are generated from the displayed public metadata; consult the publisher/project for the canonical citation.

Thumbnails are optimized local WebP files. `data/media-map.json` records their original URLs. Research preview videos and animations load on demand from their authors' original hosting; they are not mirrored in this repository. Project media remain credited to their respective authors. Thumbnails are derived previews, not new research results.

Profile images are used only when identified on the person's public website; initials are used otherwise. The roster was assembled from Peter's joining page and members' own pages on 2026-10-30; the lab should review it as membership changes.

## Move to a permanent domain or another host

The site uses relative internal links and requires only static hosting. Copy the generated HTML, assets, and `.nojekyll` to the new host. Configure DNS and the hosting domain setting separately. No custom domain has been registered or bound by this repository. To keep GitHub Pages behind a UBC subdomain, first obtain approval and DNS instructions from UBC CS IT.

The homepage prioritizes robotics, Real2Sim, and contact-aware world models. The archive includes 63 publications; Mengdi Wang’s and Guanxiong Chen’s earlier collaborations retain their original author credits and are labeled Member collaborations. See `TEAM_SOURCES.md` for role verification.
