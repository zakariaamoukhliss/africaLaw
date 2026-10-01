# africa-laws.org (static site)

Static copy of https://www.africa-laws.org, served by **Cloudflare Pages**. Large documents (PDF/Word/PowerPoint) are **not** in this repo; they are on **Cloudflare R2** at `https://files.africa-laws.org/<same relative path>`.

```
public/            <- the whole site (Cloudflare Pages "build output directory")
  index.html, <slug>/index.html, css/, js/, img/, fonts/, favicon/
  _redirects       <- old .php URLs -> new URLs; old document URLs -> R2
  _headers         <- security + cache headers
  sitemap.xml, robots.txt, ads.txt
docs/R2_UPLOAD.md  <- how to upload/verify the documents on R2
```

There is no build step and no server-side code. The store, cart, checkout, sign-in and currency switcher were removed, and the newsletter/contact forms are now `mailto:` links.

## Deploy (Cloudflare Pages)

1. Push this repo to GitHub.
2. Cloudflare dashboard -> **Workers & Pages -> Create -> Pages -> Connect to Git**, pick the repo.
3. Build settings: **Framework preset** `None`, **Build command** *(empty)*, **Build output directory** `public`.
4. Deploy, then check the `*.pages.dev` preview URL (pages, images, `/laws/`, a few document links).
5. Only after the documents are on R2 and `files.africa-laws.org` works, add the custom domains `www.africa-laws.org` (and redirect the apex `africa-laws.org` to `www`) and switch DNS.

Every push to the production branch redeploys automatically.

## Documents (Cloudflare R2)

Bucket `africa-laws-files`, public through the custom domain `files.africa-laws.org`. Object keys equal the original relative paths (`Morocco/Civil law/....pdf`). See [docs/R2_UPLOAD.md](docs/R2_UPLOAD.md).

## Limits this repo respects

- Cloudflare Pages: max 20,000 files per deployment, max 25 MiB per file, `_redirects` max 2,000 static + 100 dynamic rules.

## Contact

Site email shown on the pages: lawsafrica@gmail.com
