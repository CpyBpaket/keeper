// Keeper push sender: reads config from ntfy, sends a Web Push notification.
import { setVapidDetails, sendNotification } from 'web-push';

const PUB = process.env.VAPID_PUBLIC;
const PRIV = process.env.VAPID_PRIVATE;
const TOPIC = process.env.NTFY_TOPIC || 'keeper-push-cpybpaket-2026';
const FORCE = process.env.FORCE === 'true';

if (!PUB || !PRIV) {
  console.error('VAPID keys are missing');
  process.exit(1);
}
setVapidDetails('mailto:keeper@example.com', PUB, PRIV);

async function read(kind) {
  const r = await fetch(`https://ntfy.sh/${TOPIC}/json?poll=1`);
  const lines = (await r.text()).trim().split('\n').filter(Boolean);
  let last = null;
  for (const line of lines) {
    try {
      const m = JSON.parse(line);
      if (m.event === 'message' && m.title === kind) last = JSON.parse(m.message);
    } catch (e) { /* ignore */ }
  }
  return last;
}

async function publish(kind, obj) {
  await fetch(`https://ntfy.sh/${TOPIC}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Title': kind },
    body: JSON.stringify(obj)
  });
}

const cfg = await read('config');
if (!cfg || !cfg.subscription) {
  console.log('No subscription yet — nothing to send.');
  process.exit(0);
}

const sent = (await read('sent')) || { count: 0, time: 0 };
const now = Date.now();
const msk = new Date(now + 3 * 3600 * 1000);
const mins = msk.getUTCHours() * 60 + msk.getUTCMinutes();

if (cfg.startTime && cfg.startTime !== '00:00') {
  const [h, m] = cfg.startTime.split(':').map(Number);
  if (mins < h * 60 + m) { console.log('Before start time — skip.'); process.exit(0); }
}
if (!FORCE) {
  if (!cfg.on) { console.log('Disabled — skip.'); process.exit(0); }
  if (cfg.count > 0 && sent.count >= cfg.count) { console.log('Count reached — skip.'); process.exit(0); }
  if (sent.time && now - sent.time < (cfg.interval || 5) * 60000) { console.log('Too soon — skip.'); process.exit(0); }
}

const token = cfg.token === 'random' ? (Math.random() < 0.5 ? 'GRAM' : 'TON') : cfg.token;
const amount = cfg.amount === 'random' ? Math.floor(100 + Math.random() * 901) : Number(cfg.amount);
const body = `Keeper · Получено ${amount} ${token}`;

try {
  await sendNotification(cfg.subscription, JSON.stringify({ title: 'Keeper', body }));
  await publish('sent', { count: (sent.count || 0) + 1, time: now, body });
  console.log('Sent:', body);
} catch (e) {
  console.error('Push failed:', e.statusCode, e.message);
  if (e.statusCode === 410 || e.statusCode === 404) {
    await publish('error', { message: 'Subscription expired' });
  }
  process.exit(1);
}
