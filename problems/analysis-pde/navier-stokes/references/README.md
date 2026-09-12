# navier-stokes: archived reference PDFs

Archived copies of the primary sources this problem is built on, retrieved 2026-09-11 and committed on
Felipe's explicit instruction so that the record is reproducible from the repository alone. The index
with read depth, full hashes and the role each source plays is
[`../context/references.md`](../context/references.md).

## Why these are here

Every claim in the context dossiers is transcribed from one of these files. A dossier that cites a URL
alone degrades the moment the URL moves, and two of these sources are hosted on a personal academic
page and a vendor CDN rather than on a permanent archive. Committing the bytes we actually read, with
the hash we actually verified, makes the transcription auditable later by anyone, including us.

## Provenance and integrity

| file | retrieved from | bytes | sha256 |
|---|---|---|---|
| `openai-navier-stokes.pdf` | `cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf` | 2,959,204 | `0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f` |
| `openai-euler.pdf` | `cdn.openai.com/pdf/315b36cd-ec98-4023-8342-93345194ece1/euler.pdf` | 535,142 | `a0c234518e6c489e16996805023eb2e75c00b7c03455f7a3a5be2c124954bfdd` |
| `ab-statement.pdf` | `cims.nyu.edu/~tristanb/statement.pdf` | 53,497 | `8d7723941bcda2fa55c1e74faa6298e04c706d17ff8abd2ad01878039c621f9d` |
| `ab-euler.pdf` | `cims.nyu.edu/~tristanb/euler.pdf` | 1,105,306 | `97ef408bff09b4f6ed9f3867734d1eb2245f3f34e6334b28136c84c02d0ae8d8` |
| `ab-ipm.pdf` | `cims.nyu.edu/~tristanb/ipm.pdf` | 704,785 | `b3ebdbb8d9a93dcca5f3b3f8796e63f7f28b48e0b0e258b909110a4b69c72a12` |
| `ab-boussinesq.pdf` | `cims.nyu.edu/~tristanb/boussinesq.pdf` | 846,615 | `895a628d1783bcb039374686f50b895b5f450f53b8ef8aa173523487a7a4a21b` |
| `cmz-ipm-2410.22920.pdf` | `arxiv.org/pdf/2410.22920v3` | 549,167 | `14c3a2423cbcec2d6ca5c54258ae4bd978f66631165fdb6217248bda280d45e8` |
| `abc-nonuniqueness-2112.03116.pdf` | `arxiv.org/pdf/2112.03116` | 426,725 | `b2dcf166c3832a4ba627ecf634ad9d8aa1dd6f693c4cc8ca33e6e37f53fd0329` |
| `tao-averaged-1402.0290.pdf` | `arxiv.org/pdf/1402.0290` | 1,052,688 | `743c802bd9ecf90ec8d022292885f886a321ab1f7c2dfb601b3c860b98b3f07d` |
| `elgindi-euler-1904.04795.pdf` | `arxiv.org/pdf/1904.04795` | 664,080 | `139d50284b491ee1e68e66f4b0690f8e0b0770fd2989a797c4909bf46a9d79ee` |
| `chen-hou-2210.07191.pdf` | `arxiv.org/pdf/2210.07191` | 5,181,971 | `2714863f3fe0f5411a297945f678a87a463c4b5e194a1fa233bd42c4b0455697` |
| `hou-wang-yang-2509.25116.pdf` | `arxiv.org/pdf/2509.25116` | 2,148,337 | `2d369eade29bd0d5e8dfc6d7def7ed19b8282ab4450860978f3691176d9f8318` |
| `dm-unstable-2509.14185.pdf` | `arxiv.org/pdf/2509.14185` | 2,225,069 | `ade2c449cbbc9314504fcf715f91f33d706960c93dea5cb2c6133cf8a5772613` |

Total 18,452,586 bytes across 13 files. Verify any of them with
`python -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" <file>`.

## Rights

Copyright in every file below belongs to its authors. Nothing here is our work and nothing here is
relicensed by being committed; the repository license covers our own content only. The arXiv items are
redistributed under the terms their authors selected on arXiv, which differ per item and are recorded
on each abstract page rather than inside the PDF. The two `cdn.openai.com` items and the four
`cims.nyu.edu` items carry no license statement in the document itself, so they are archived here as
retrieved, for citation and verification, with the source URL and retrieval date above.

If an author would prefer their file not be mirrored here, remove the file and keep the row above: the
URL, date and hash preserve the audit trail on their own, which is the only property this directory
actually needs.

## Reading state

Read depth per source is marked `[V]`, `[P]` or `[U]` in
[`../context/references.md`](../context/references.md) and is the authoritative record of what we have
actually read as opposed to what we merely hold. Holding a PDF is not having read it, and the dossiers
depend on that distinction.
