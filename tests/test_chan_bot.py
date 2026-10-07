"""Kiem tra nhanh: python tests/test_chan_bot.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import checker as C
import diagnose as D

# Trang chan that: tieu de khop, hoac trang ngan ma noi dung khop.
assert D.la_trang_chan_bot({"title": "Just a moment...", "text_len": 41})
assert D.la_trang_chan_bot({"title": "Attention Required! | Cloudflare", "text_len": 723})
assert D.la_trang_chan_bot({"title": "Security check", "text_len": 93,
                            "snippet": "Enable JavaScript and cookies to continue"})
# Trang that nhac toi reCAPTCHA o chan trang (webtretho, 927 ky tu): khong phai chan.
assert not D.la_trang_chan_bot({"title": "Dang nhap - Cong Dong", "text_len": 927,
                                "snippet": "duoc bao ve boi reCAPTCHA"})

# Trang loi chan cua CloudFront (khong co chu captcha) ma Chromium nhan 403:
# khong duoc ra LINK_BI_GO.
r0 = C.Result(source_url="https://x.mystrikingly.com/blog/a", status="NOT_FOUND",
              rendered="playwright")
sig = {"title": "ERROR", "text_len": 513,
       "snippet": "403 ERROR Request blocked.", "http_render": 403}
assert D.diagnose(r0, sig)[0] == "HTTP_403_CHAN_BOT"
assert D.la_trang_chan_bot({"title": "Human Verification", "text_len": 724})
assert D.la_trang_chan_bot({"title": "ERROR: The request could not be satisfied"})
sig["http_render"] = 200
assert D.diagnose(r0, sig)[0] != "HTTP_403_CHAN_BOT"

# Canonical "//s/" cua raovat49 tro ve chinh trang dang doc.
html = ('<html><head><link rel="canonical" href="https://raovat49.com//s/bai-1">'
        '</head><body>x</body></html>')
r = C.Result(source_url="https://raovat49.com/s/bai-1")
C.analyse(html, "https://raovat49.com/s/bai-1", r, {}, {})
assert r.indexable == "yes", r.note
# Canonical khac that thi van bat.
html2 = html.replace("//s/bai-1", "/s/bai-2")
r2 = C.Result(source_url="https://raovat49.com/s/bai-1")
C.analyse(html2, "https://raovat49.com/s/bai-1", r2, {}, {})
assert r2.indexable == "no"

print("ok")
