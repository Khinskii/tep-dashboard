import fs from 'fs';
import path from 'path';

export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 's-maxage=60, stale-while-revalidate');

  try {
    const filePath = path.join(process.cwd(), 'live_data.json');
    const data = fs.readFileSync(filePath, 'utf8');
    return res.status(200).send(data);
  } catch (err) {
    return res.status(500).json({ error: "Failed to read live data" });
  }
}
