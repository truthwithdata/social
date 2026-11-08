# Truth with Data: social media pipeline

Claude drafts each week's posts as a pull request; Vishal approves the batch by merging it; a scheduled
task posts what is due from `main` at 07:55 and 18:55 UK time.

This repo is separate from the website (`truthwithdata/webstie`, deployed by Netlify) so that drafting,
merging and posting never trigger a Netlify deploy. Images and videos are served by **GitHub Pages** from
this repo at `https://truthwithdata.github.io/social/<path>` (Settings → Pages: deploy from `main`, root).
Pages rebuilds a minute or so after each push, so merge a week's PR at least 10 minutes before its first slot.
Old links to `https://truthwithdata.com/social/…` (sent newsletters, early posts) redirect here.

Drafting needs both repos side by side: `git clone …/social` and `git clone …/webstie` in the same folder.
Carousel charts (`blog/charts/…`), articles, `js/config.js` and `data/` are read from `../webstie`
(or from the path in `TWD_SITE`). Nothing in this pipeline changes the website repo.

| Path | What it is |
| --- | --- |
| `queue/<monday>.json` | One week of posts (format in `scripts/social_check.py`) |
| `img/<monday>/…`, `img/reddit/`, `img/brand/` | Slides, story images, Reels (MP4), Reddit charts, logo outro; served at https://truthwithdata.github.io/social/img/… |
| `specs/<monday>/*.json` | Carousel specs; render with `python3 scripts/make_carousel.py <spec>` |
| `analysis/` | Scripts behind any number that is not in a published article |
| `posted.json` | Log of what has been posted or skipped (id, platform, time, link); written only by the poster |
| `press/` | Press pitch drafts and a log of which articles have been pitched |
| `topics/` | Monthly topic shortlists (`log.json`) |
| `summaries/` | Monday weekly summaries |
| `scripts/` | `social_check.py` (validate, list due posts), `make_carousel.py`, `make_reel.py`, `make_logo_outro.py` |

Accounts: LinkedIn = Vishal's personal profile (`urn:li:person:QueTevIgLG`). Instagram = the
**truthwithdata** account only; never post to any other Instagram account. X = the Truth with Data account,
once connected. Newsletter = Kit. Reddit = **u/truthwithdata** only (Composio account `reddit_grame-menald`). The LinkedIn company page reposts by hand (the API connection has no
page permission).

## Weekly drafting (scheduled: Thursday evening)

1. Read the last two queue files and `posted.json` so the new week does not repeat an angle.
2. Pick the week's material: any article or tool published since the last batch first, otherwise a fresh
   angle on an existing one (each article has many findings; use a different one each time).
3. Schedule for the week starting next Monday, in the `08:00` and `19:00` slots only:
   - LinkedIn (personal): Tue, Wed, Thu at 08:00. Links go in `first_comment`, never the post body.
   - Instagram carousels: Tue and Thu 19:00, Sat 19:00 (6–8 slides, 1080x1350), each followed in the
     same slot by a story made from its first slide (`make_reel.py --story`), `kind: "story"`.
   - Instagram Reel: Wed 19:00, made from that week's strongest carousel with `scripts/make_reel.py`
     (7 slides max, about 20 s), `kind: "reel"`, with `video` and `cover`.
   - X: one thread on Wed 08:00.
   - Newsletter: Sun 08:00, `platform: "newsletter"`, one chart with three or four sentences, links to
     the week's articles, signed "Vishal". HTML in `text`, short `subject`.
   - Reddit: 3 or 4 posts a week, every other day at 19:00, each in a **different** community, never the
     same community twice within 10 days and never two posts on the same day. See "Reddit" below.
4. Every link to truthwithdata.com carries UTM tags:
   `?utm_source=<linkedin|x|instagram|newsletter|reddit>&utm_medium=<social|email>&utm_campaign=<post id or date>`.
5. Rules for every post: plain, specific, no hype, no emoji in LinkedIn text. **Every number must appear
   in a published article on the site, a data file in the website repo's `data/`, or a script in `analysis/` that
   you commit with it.** State uncertainty the way the article does. Never invent quotes, testimonials or
   follower numbers. Disclose any affiliate link or sponsorship.
6. Write specs, render carousels, stories and the Reel; look at every slide and a frame from the Reel.
7. Run `python3 scripts/social_check.py` (must pass).
8. Open a PR titled `Social posts: week of <date>`. In the description: the table of every post, the full
   texts, and two extras that are never posted automatically:
   - **Optional Reel idea for Vishal**: one 8–10 second clip he can generate in Gemini (Veo) and post by
     hand with trending audio. Give the exact Gemini prompt (vertical 9:16, 8 seconds, a concrete
     everyday scene that matches the week's topic, camera movement, lighting, "no text, no logos, no
     recognisable people"), the on-screen text to add in the Instagram editor (one line, a number from
     the article), and the caption.
   - **Reddit comment opportunities** (posted by hand, never automatically): three recent threads (link,
     under 14 days old) in the communities above where someone asks a question an article answers, each
     with a reply of 80–150 words that answers it fully on its own, with no link unless the community allows
     it. Commenting helpfully is what lets new-account posts survive Reddit's filters.
   - **Two Quora answers**: the question (search Quora/Google for real, recent questions matching an
     article; give the URL), a full answer of 120–200 words that is useful on its own with the article's
     numbers, and one closing line linking to the article.

## Reddit

Reddit works differently from the other platforms: each community has its own rules, moderators remove
anything that reads like promotion, and a new account is filtered harder. So:

- **Before drafting for a community**, read its rules (`REDDIT_GET_SUBREDDIT_RULES`) and follow them. Skip any
  community that bans self-promotion, links to blogs or tools, or AI-written content (as of Nov 2026:
  r/UKPersonalFinance, r/programming, r/learnprogramming, r/statistics, r/AskStatistics, r/ProgrammingLanguages,
  r/analytics, r/Economics, r/ProductManagement outside its Friday thread, r/artificial, r/Futurology,
  r/singularity, r/Infographics). r/HousingUK allows no links at all: text-only discussion posts there.
- **Communities that fit** (checked 7 Nov 2026): r/dataisbeautiful (charts, `[OC]` in the title, data sources
  and tools in the first top-level comment, plain titles, US politics only on Thursdays, personal data only on
  Mondays), r/datavisualization (chart craft; ask for design feedback), r/CRO (A/B testing), r/MachineLearning
  (`[P]` project posts with public code and real substance), r/cscareerquestionsuk (text only), r/dataanalysis,
  r/HousingUK (no links). Re-check rules each time; they change. Also read
  `proxy_execute("GET", "/api/v1/<sub>/post_requirements", "reddit")`: it lists required flair and blocked title
  words (r/MachineLearning requires flair, e.g. "Project", and blocks titles containing words such as "bot",
  "chatgpt", "rag", "agi"). r/dataisbeautiful does not let users set flair; `[OC]` in the title is enough.
- **Write for the community, not for the site.** Lead with the finding and the method, put the numbers in the
  post, say what's uncertain, end with a genuine question. At most two links, at the end (the write-up, and the
  public code on GitHub where there is some). No "check out my site", no hashtags, no emoji, no sales.
- **Visuals**: `kind: "image"` posts a chart natively. Use the article's own charts rendered to PNG at 2000 px
  wide (`rsvg-convert -w 2000 -b white ../webstie/blog/charts/<chart>.svg -o img/reddit/<chart>.png`), not the
  Instagram slides, and look at each one. Image posts have no body text, so the explanation and links go in
  `first_comment`, which is posted straight away as the first top-level comment.
- Titles describe the data plainly (max 300 characters). Every number follows the same sourcing rule as
  other posts.

## Posting (scheduled: 07:55 and 18:55 UK time, every day)

1. `git pull` on `main`, then `python3 scripts/social_check.py --due`. Nothing due: stop.
2. For each due item, in file order, using the Composio tools:
   - **LinkedIn**: for each image, download `image_urls[i]` in the Composio workbench, `upload_local_file`,
     then `LINKEDIN_CREATE_LINKED_IN_POST` with author `urn:li:person:QueTevIgLG`, `commentary` = text,
     `visibility` PUBLIC, `images` = [{name, mimetype, s3key}]. The response `x_restli_id` is the post URN.
     If the item has `video_url` instead of images (a native video post): `LINKEDIN_UPLOAD_VIDEO` with
     `video_url` (it waits until the video is ready and returns its `urn:li:video:...`), then
     `LINKEDIN_CREATE_VIDEO_POST` with that `video_urn`, `commentary` = text, `visibility` PUBLIC; the
     post URN is in the response. If the upload by URL fails, download the MP4 in the workbench,
     `upload_local_file`, and pass it as `file` instead.
     If `first_comment` is set, `LINKEDIN_CREATE_COMMENT_ON_POST` with actor = the person URN,
     object and target_urn = the post URN, message.text = first_comment.
   - **Instagram**: first confirm with `INSTAGRAM_GET_USER_INFO` (ig_user_id "me") that the username is
     `truthwithdata`; if not, or if the token fails, post nothing to Instagram and report it. Check
     `INSTAGRAM_GET_IG_USER_CONTENT_PUBLISHING_LIMIT`. Then by `kind`:
     carousel → `INSTAGRAM_CREATE_CAROUSEL_CONTAINER` with `child_image_urls` = image_urls and caption;
     reel → `INSTAGRAM_POST_IG_USER_MEDIA` with media_type REELS, video_url, cover_url, caption,
     share_to_feed true; story → `INSTAGRAM_POST_IG_USER_MEDIA` with media_type STORIES and image_url.
     Then `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH` with the creation id.
   - **X**: if there is no active Twitter connection, record it as skipped. Otherwise upload the images,
     post the first item with them, then reply to each previous post in turn.
   - **Reddit**: Composio account `reddit_grame-menald` only. First confirm with
     `proxy_execute("GET", "/api/v1/me", "reddit")` that the `name` is `truthwithdata`; if not, post
     nothing to Reddit. Make Reddit calls one at a time (Reddit rate-limits bursts with HTTP 429; wait
     60 seconds and try once more). Before posting, check `GET /user/truthwithdata/submitted?limit=10`: if a
     post with the same title is already there, record that one instead of posting again (never post the
     same item twice). Then by `kind`:
     - image: in the workbench download `image_urls[0]`, call `REDDIT_PREPARE_MEDIA_UPLOAD` (filename,
       mime_type image/png or image/jpeg), POST the file to `"https:" + args.action` with every field in
       `args.fields` as form data (expect HTTP 201; the image URL is `<Location>` in the XML reply), then
       `proxy_execute("POST", "/api/submit", "reddit", body={}, query_params={"sr": subreddit, "kind": "image",
       "title": title, "url": <Location>, "api_type": "json", "resubmit": "true", "sendreplies": "true"}`
       plus `"flair_id"` when one was found). The parameters must go in `query_params` with `body={}`: a JSON body
       is ignored by Reddit (tested 7 Nov 2026). Success is `{"json": {"errors": [], ...}}`. Image posts don't return the post id: wait about 20 seconds
       and read it from `/user/truthwithdata/submitted?limit=5` by title. If the native image post fails,
       fall back to `REDDIT_CREATE_REDDIT_POST` with kind `link` and `url` = `image_urls[0]`.
     - self: `REDDIT_CREATE_REDDIT_POST` with kind `self`, title, text (and flair_id).
     - link: `REDDIT_CREATE_REDDIT_POST` with kind `link`, title, url (and flair_id).
     Flair: if the item has `flair`, `REDDIT_LIST_SUBREDDIT_POST_FLAIRS` and use the template whose text
     contains it (case-insensitive); if that call fails or nothing matches, post without flair. If the
     submit fails with a flair-required error, pick the closest flair from the list and retry once.
     Then post `first_comment` with `REDDIT_POST_REDDIT_COMMENT` (thing_id `t3_<id>`).
     After about a minute, read the post (`proxy_execute("GET", "/api/info", "reddit",
     query_params={"id": "t3_<id>"})`). If `removed_by_category` is set or it is not visible, still record it
     in `posted.json` (never repost) with `"removed": "<reason>"`, and say so in the summary.
     `ref` = `https://www.reddit.com<permalink>`.
     Finally create a Google Calendar event on Vishal's primary calendar 30 minutes after the slot, 15 minutes,
     titled "TWD: reply to comments on r/<subreddit>", with the post link in the description (not for posts
     on the own profile, u_truthwithdata). Replies are
     Vishal's to write; the poster never replies to anyone.
   - **Newsletter**: if there is no active Kit connection, record it as skipped. Otherwise
     `KIT_CREATE_BROADCAST` with subject, content = text, send_at = `slot_iso` converted to UTC (if that
     is already past, 10 minutes from now), public true, description = the item id.
3. Immediately after each item succeeds (or is skipped for a missing connection), append
   `{id, platform, at, ref}` (plus `"skipped": "<reason>"` when skipped) to `posted.json`, commit to `main`
   with the message `Posted <id>`, then push. Never post an item whose id is already in
   `posted.json`.
4. If an item fails, retry once. If it still fails, leave it out of `posted.json` so the next run that
   day can try again, and report the error.
5. End with a short summary: what was posted (with links), what failed or was skipped and why.

## Review comments (scheduled: three times a day)

Vishal can comment on any open PR in plain English. A scheduled task reads new comments from
`vishalsharma3003` on open PRs, makes the requested change on that PR's branch (re-rendering images and
re-running the checks), pushes, and replies on the PR saying what changed. It never merges.
