const express = require('express');
const router = express.Router();

let items = [
  { id: 1, name: 'Coffee Beans', quantity: 100 }
];

router.get('/', (req, res) => {
  res.json(items);
});

router.post('/', (req, res) => {
  const item = { id: items.length + 1, ...req.body };
  items.push(item);
  res.status(201).json(item);
});

module.exports = router;
