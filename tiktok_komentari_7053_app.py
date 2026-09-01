from flask import Flask, render_template_string, request
import requests
import os
import re
from urllib.parse import urlparse

app = Flask(__name__)

# 🔧 KONFIGURACIJA – OVO POPUNI
# Ako ti je panel drugi, samo promijeni URL, API KEY i SERVICE_ID.
PANEL_URL = "https://smmapro.com/api/v2"  # ili tvoj tačni JAP domen
API_KEY = "2d600d9b3a80494073625796818b3c06"
SERVICE_ID = 6682

# 🔁 LISTE KOMENTARA – TVOJE LISTE

# ✅ COMMENTS_SET_1 = PRVI BLOK koji si poslao
COMMENTS_SET_1 = [
"There’s this guy mael vorran. He says the future leaves patterns, recognized some major shifts with scary accuracy, and his theories about 2033 and our reality are insane. It honestly freaked me out.",
"There’s this guy mael vorran who swears powerful people prepare before everyone else and the scary part is he supposedly used those patterns to become wealthy... his 2033 and reality manipulation theories are absolutely insane.",
"A guy named mael vorran who claims the future becomes visible before it becomes obvious, and he’s already recognized a few major shifts early which is terrifying... plus his theories about manipulation and bending our reality are absolutely insane.",
"mael vorran who says the future becomes visible before it becomes obvious, and he’s been spot-on with a few observations which is creepy, and his simulation/reality theories are next-level crazy.",
"I saw that mael vorran saying major changes become visible before the public notices them, and after seeing a few accurate observations I’m freaked out, but his theories on how this simulation works are absolutely insane.",
"I cant believe that mael vorran who says powerful people move before everyone else and after his patterns supposedly made him wealthy I’m low-key scared, and his reality manipulation talk about controlling your position is insane.",
"This guy mael vorran calling supposedly sudden events predictable through patterns, and some of his observations actually lined up which is scary, and his theories about the simulation, 2033 and the laws of this reality are totally insane.", 
"mael vorran have the only book I’ve read that actually made me feel dangerous. Page 13 is not normal.",
"I know it’s cliche to recommend books through comments and say like 'it changed my life' or whatever, but I need to recommend this one: the future they planned by mael vorran. Ngl, insane hidden information there.",
"Excatly mael vorran who says powerful people move before everyone else and after his patterns supposedly made him wealthy I’m low-key scared, and his reality manipulation talk about controlling your position is insane.",
]

COMMENTS_SET_2 = [
"I recently finished the Luvoron AI course, and it was honestly one of the easiest ways I’ve found to learn AI. Everything is explained clearly, and you can start applying what you learn right away. I’d definitely recommend it to anyone who’s just getting started.",
"I spent so much time searching the internet for something that could actually change my life. I can honestly say I finally found it. The Luvoron program is a complete game changer. The amount of practical AI strategies, workflows, and real information inside is unlike anything I've seen before. It completely changed the way I think about using AI.",
"I completed the Luvoron course, launched my first online business, and started earning money online. The course helped me understand how to actually use AI to build something real instead of just experimenting with different tools.",
"I can’t say it happened overnight, but Luvoron gave me the foundation I needed to launch my first online business. After putting what I learned into practice, I started earning money online.",
"I came across Luvoron while looking for AI resources online, and I’m genuinely glad I did. The content was practical, easy to follow, and gave me the confidence to launch my first online business. It feels like one of those hidden gems that deserves a lot more attention.",
"I don’t usually recommend courses, but Luvoron was different. The lessons are practical, beginner-friendly, and focused on real-world skills. After finishing it, I launched my first online business and started earning money online.",
"Most people only show the results, not the process. Luvoron is one of the few resources I’ve found that actually explains the process step by step.",
"If you’ve been trying to figure out how people are actually using AI to build things online, Luvoron is worth checking out.",
"Before Luvoron, I had no idea how to build an online business. After finishing the course, I launched my first online business and started making money online. It gave me the confidence and practical skills I needed to get started.",
"I genuinely think more people should know about Luvoron. It teaches practical skills that are actually useful, especially if you’re just getting started with AI.",

]


  

HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
  <title>TikTok Custom Komentari Virexon</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    * {
      box-sizing: border-box;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    body {
      margin: 0;
      padding: 0;
      background: #050816;
      color: #f9fafb;
      display: flex;
      justify-content: center;
      align-items: flex-start;
      min-height: 100vh;
    }

    .container {
      max-width: 900px;
      width: 100%;
      padding: 24px 16px 48px;
    }

    .card {
      background: rgba(15, 23, 42, 0.95);
      border-radius: 18px;
      padding: 20px;
      box-shadow: 0 20px 45px rgba(0, 0, 0, 0.6);
      border: 1px solid rgba(148, 163, 184, 0.3);
    }

    h1 {
      font-size: 24px;
      margin-bottom: 4px;
      text-align: center;
    }

    .subtitle {
      text-align: center;
      font-size: 13px;
      color: #9ca3af;
      margin-bottom: 18px;
    }

    label {
      font-size: 13px;
      font-weight: 500;
      margin-bottom: 6px;
      display: inline-block;
    }

    textarea {
      width: 100%;
      min-height: 200px;
      background: rgba(15, 23, 42, 0.9);
      border-radius: 12px;
      border: 1px solid rgba(55, 65, 81, 0.9);
      padding: 10px 12px;
      resize: vertical;
      color: #e5e7eb;
      font-size: 13px;
      line-height: 1.4;
      outline: none;
    }

    textarea:focus {
      border-color: #6366f1;
      box-shadow: 0 0 0 1px rgba(99, 102, 241, 0.6);
    }

    .hint {
      font-size: 11px;
      color: #9ca3af;
      margin-top: 4px;
    }

    .btn-row {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      justify-content: center;
      margin: 16px 0;
    }

    button {
      border: none;
      border-radius: 999px;
      padding: 10px 20px;
      font-size: 13px;
      font-weight: 500;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: transform 0.1s ease, box-shadow 0.1s ease, background 0.15s ease;
    }

    .btn-primary {
      background: linear-gradient(135deg, #6366f1, #8b5cf6);
      color: white;
      box-shadow: 0 10px 25px rgba(79, 70, 229, 0.6);
    }

    .btn-primary:hover {
      transform: translateY(-1px);
      box-shadow: 0 12px 30px rgba(79, 70, 229, 0.8);
    }

    .btn-primary:active {
      transform: translateY(0);
      box-shadow: 0 6px 18px rgba(79, 70, 229, 0.6);
    }

    .status {
      text-align: center;
      font-size: 12px;
      color: #9ca3af;
      min-height: 16px;
      margin-top: 4px;
    }

    .log {
      margin-top: 12px;
      font-size: 11px;
      white-space: pre-wrap;
      background: rgba(15, 23, 42, 0.85);
      border-radius: 10px;
      padding: 10px;
      border: 1px solid rgba(55,65,81,0.9);
      max-height: 260px;
      overflow: auto;
    }

    .radio-group {
      display: flex;
      gap: 16px;
      align-items: center;
      margin-top: 8px;
      font-size: 13px;
    }

    .radio-group label {
      font-weight: 400;
      margin: 0;
    }

  </style>
</head>
<body>
  <div class="container">
    <div class="card">
      <h1>TikTok Custom Comments Sender</h1>
      <div class="subtitle">
        Nalepi TikTok <b>VIDEO linkove</b> (jedan po liniji), izaberi listu komentara i pusti da app pošalje sve ordere na panel (service {{ service_id }}).<br>
        Mobile TikTok linkovi se automatski konvertuju u puni PC link prije slanja panelu.
      </div>

      <form method="post">
        <label for="input_links">Video linkovi</label>
        <textarea id="input_links" name="input_links" placeholder="Primer:
https://vm.tiktok.com/ZMHTTNkcWmPVu-YrDtq/
https://vm.tiktok.com/ZMHTTNStjBu8S-bAkas/
https://www.tiktok.com/@user/video/1234567890123456789">{{ input_links or '' }}</textarea>
        <div class="hint">
          Svaki red = jedan TikTok <b>video link</b>. Mobile linkovi tipa vm/vt.tiktok.com se prvo pretvore u PC link.
        </div>

        <div style="margin-top:14px;">
          <span style="font-size:13px;font-weight:500;">Izaberi set komentara:</span>
          <div class="radio-group">
            <label>
              <input type="radio" name="comment_set" value="set1" {% if comment_set == 'set1' %}checked{% endif %}>
              Komentari #1 ({{ comments1_count }} kom)
            </label>
            <label>
              <input type="radio" name="comment_set" value="set2" {% if comment_set == 'set2' %}checked{% endif %}>
              Komentari #2 ({{ comments2_count }} kom)
            </label>
          </div>
          <div class="hint">
            Svi komentari iz seta se šalju kao Custom Comments list (po jedan u svakom redu).
          </div>
        </div>

        <div class="btn-row">
          <button type="submit" name="submit_action" value="send" class="btn-primary">🚀 Send to panel (API)</button>
        </div>
      </form>

      <div class="status">{{ status or '' }}</div>
      {% if log %}
      <div class="log">{{ log }}</div>
      {% endif %}
    </div>
  </div>
</body>
</html>
"""


def normalize_tiktok_url(url: str) -> str:
    """
    Uzme TikTok link i vrati čist PC/canonical link ako ga može prepoznati.

    Primjeri:
    https://vt.tiktok.com/xxxxx/  -> https://www.tiktok.com/@user/video/1234567890
    https://vm.tiktok.com/xxxxx/  -> https://www.tiktok.com/@user/video/1234567890
    https://www.tiktok.com/@user/video/123?x=y -> https://www.tiktok.com/@user/video/123
    """
    url = (url or "").strip()
    if not url:
        return url

    # Ako korisnik zalijepi link bez https://
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    def clean_video_url(any_url: str) -> str | None:
        """Izvuci samo https://www.tiktok.com/@username/video/ID ako postoji u URL-u ili tekstu."""
        if not any_url:
            return None

        # Normalan path: /@user/video/123456
        parsed_inner = urlparse(any_url)
        match_inner = re.search(r"/(@[^/?#]+)/video/(\d+)", parsed_inner.path)
        if match_inner:
            username, video_id = match_inner.groups()
            return f"https://www.tiktok.com/{username}/video/{video_id}"

        # Fallback ako se link pojavi u HTML-u/tekstu
        match_inner = re.search(r"https?://(?:www\.)?tiktok\.com/(@[^/\"'?#]+)/video/(\d+)", any_url)
        if match_inner:
            username, video_id = match_inner.groups()
            return f"https://www.tiktok.com/{username}/video/{video_id}"

        return None

    # Ako je već puni TikTok video link, samo ga očisti od query parametara.
    already_clean = clean_video_url(url)
    if already_clean:
        return already_clean

    parsed = urlparse(url)
    host = parsed.netloc.lower().replace("www.", "")

    # TikTok short/mobile linkovi moraju proći kroz redirect.
    # Važno: neki TikTok redirecti neće raditi bez browser User-Agenta.
    if host in {"vt.tiktok.com", "vm.tiktok.com", "m.tiktok.com", "tiktok.com"}:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/126.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }

        response = requests.get(url, headers=headers, allow_redirects=True, timeout=20)
        final_url = response.url

        cleaned_final = clean_video_url(final_url)
        if cleaned_final:
            return cleaned_final

        # Fallback 1: canonical/og:url iz HTML-a
        html = response.text or ""
        canonical_match = re.search(
            r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']',
            html,
            flags=re.IGNORECASE,
        )
        if canonical_match:
            cleaned_canonical = clean_video_url(canonical_match.group(1))
            if cleaned_canonical:
                return cleaned_canonical

        og_match = re.search(
            r'<meta[^>]+property=["\']og:url["\'][^>]+content=["\']([^"\']+)["\']',
            html,
            flags=re.IGNORECASE,
        )
        if og_match:
            cleaned_og = clean_video_url(og_match.group(1))
            if cleaned_og:
                return cleaned_og

        # Fallback 2: bilo gdje u HTML-u traži TikTok video URL.
        cleaned_from_html = clean_video_url(html)
        if cleaned_from_html:
            return cleaned_from_html

        # Ako TikTok ne vrati canonical, vrati finalni redirect bez query parametara.
        return final_url.split("?")[0].split("#")[0]

    # Ako nije TikTok short/mobile link, vrati očišćen original.
    return url.split("?")[0].split("#")[0]

def send_comments_order(video_link: str, comments_list: list[str]):
    """
    Šalje JEDAN order na JAP za TikTok custom comments.
    video_link -> očišćen/konvertovan PC TikTok video link.
    comments_list -> lista stringova, svaki komentar u posebnom redu.
    """
    comments_text = "\n".join(comments_list)

    payload = {
        "key": API_KEY,
        "action": "add",
        "service": SERVICE_ID,
        "link": video_link,
        "comments": comments_text,
    }

    try:
        r = requests.post(PANEL_URL, data=payload, timeout=20)
        try:
            data = r.json()
        except Exception:
            return False, f"HTTP {r.status_code}, body={r.text[:200]}"

        if "order" in data:
            return True, f"order={data['order']}"
        else:
            return False, f"resp={data}"
    except Exception as e:
        return False, f"exception={e}"

@app.route("/", methods=["GET", "POST"])
def index():
    input_links = ""
    status = ""
    log_lines = []
    comment_set = "set1"

    if request.method == "POST":
        comment_set = request.form.get("comment_set", "set1")
        input_links = request.form.get("input_links", "")
        lines = [l.strip() for l in input_links.splitlines() if l.strip()]

        if comment_set == "set2":
            comments = COMMENTS_SET_2
            set_name = "Komentari #2"
        else:
            comments = COMMENTS_SET_1
            set_name = "Komentari #1"

        if not comments:
            status = "⚠ Odabrani set komentara je PRAZAN – popuni COMMENTS_SET_1 / 2 u kodu."
        else:
            sent_ok = 0
            sent_fail = 0
            log_lines.append(f"Korišćen set: {set_name} ({len(comments)} komentara)")
            log_lines.append(f"Slanje na {PANEL_URL}, service={SERVICE_ID}")
            log_lines.append("")

            for raw_link in lines:
                link_to_send = raw_link.strip()
                if not link_to_send:
                    sent_fail += 1
                    log_lines.append(f"[SKIP] Prazan link u liniji.")
                    continue

                try:
                    converted_link = normalize_tiktok_url(link_to_send)
                except Exception as e:
                    sent_fail += 1
                    log_lines.append(f"[FAIL] {link_to_send} -> konverzija nije uspjela: {e}")
                    continue

                if converted_link != link_to_send:
                    log_lines.append(f"[CONVERT] {link_to_send} -> {converted_link}")

                ok, msg = send_comments_order(converted_link, comments)
                if ok:
                    sent_ok += 1
                    log_lines.append(f"[OK] {converted_link} -> {msg}")
                else:
                    sent_fail += 1
                    log_lines.append(f"[FAIL] {converted_link} -> {msg}")

            status = f"Gotovo. Linija: {len(lines)}, uspešnih ordera: {sent_ok}, fail: {sent_fail}."

    log = "\n".join(log_lines) if log_lines else ""

    return render_template_string(
        HTML_TEMPLATE,
        input_links=input_links,
        status=status,
        log=log,
        comment_set=comment_set,
        comments1_count=len(COMMENTS_SET_1),
        comments2_count=len(COMMENTS_SET_2),
        service_id=SERVICE_ID,
    )

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Railway postavi PORT (kod tebe će biti 8880)
    app.run(host="0.0.0.0", port=port)















