"""Build only after owner-provided inputs. Never print their values."""
import datetime
import html
import os
import re
import shutil
from pathlib import Path

root = Path(__file__).resolve().parents[1]
out = root / '_site'
names = ('PRIVACY_OFFICER',)
values = {name: os.environ.get(name, '').strip() for name in names}
# The effective date is the date of the approved manual publication in Korea.
values['EFFECTIVE_DATE'] = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).date().isoformat()
if os.environ.get('POLICY_APPROVED') != 'YES' or os.environ.get('PUBLISH_CONFIRMED') != 'YES':
    raise SystemExit('Blocked: legal policy approval and manual publication confirmation required.')
if any(not v or re.search(r'\{\{|\}\}|\[|\]|\b(?:TBD|TODO|pending)\b|미확정|확인 중|승인 필요', v, re.I) for v in values.values()):
    raise SystemExit('Blocked: all approved policy inputs are required without placeholders.')
try:
    if datetime.date.fromisoformat(values['EFFECTIVE_DATE']).isoformat() != values['EFFECTIVE_DATE']:
        raise ValueError()
except ValueError:
    raise SystemExit('Blocked: effective date must be a real ISO date.')
if out.exists(): shutil.rmtree(out)
shutil.copytree(root / 'template', out)
for path in out.rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    for name, value in values.items(): text = text.replace('{{'+name+'}}', html.escape(value, quote=True))
    text = re.sub(r'<aside class="notice" data-review-only>[\s\S]*?</aside>', '', text)
    text = text.replace(' (게시 전 검토본)', '')
    # The private template is intentionally noindex; the approved public policy must not be.
    text = text.replace('<meta name="robots" content="noindex">', '')
    text = text.replace('<p>이 홈페이지 자체에는 광고·분석 스크립트나 입력 폼이 없습니다. 호스팅 접속 정보의 실제 처리와 국외 고지는 배포 전 확인이 필요합니다.</p>', '<p>이 홈페이지 자체에는 광고·분석 스크립트나 입력 폼이 없습니다.</p>')
    text = text.replace('<p lang="en">This homepage has no advertising or analytics scripts or submission forms. Hosting traffic processing and international disclosures require verification before publication.</p>', '<p lang="en">This homepage has no advertising or analytics scripts or submission forms.</p>')
    if re.search(r'\{\{|\}\}|data-review-only|미승인 검토본|Private review only', text):
        shutil.rmtree(out)
        raise SystemExit('Blocked: unresolved review content.')
    path.write_text(text, encoding='utf-8')
print('Build prepared; content intentionally omitted from logs.')
