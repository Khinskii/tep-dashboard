export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  const pin = String(req.body?.pin || '').trim();
  const demos = [
    { client_name: "ООО «Северсталь-Пром» (Заказчик)", pin: "2026", expires_at: "2026-10-01T23:59:59" },
    { client_name: "ООО «ПромМонтаж» (Демонстрация)", pin: "7777", expires_at: "2026-09-25T23:59:59" },
    { client_name: "Тестовый партнер (Истекший срок)", pin: "1111", expires_at: "2026-09-01T00:00:00" }
  ];

  const matched = demos.find(d => d.pin === pin);
  if (!matched) {
    return res.status(200).json({ valid: false, message: "Неверный PIN-код" });
  }

  const now = new Date();
  const expDt = new Date(matched.expires_at);
  if (now > expDt) {
    return res.status(200).json({
      valid: false,
      expired: true,
      client_name: matched.client_name,
      message: `Срок действия демо-доступа для ${matched.client_name} истек.`
    });
  }

  return res.status(200).json({
    valid: true,
    expired: false,
    client_name: matched.client_name,
    expires_at: expDt.toLocaleDateString('ru-RU'),
    message: `Демо-доступ активен до ${expDt.toLocaleDateString('ru-RU')}`
  });
}
