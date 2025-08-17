const express = require('express');
const router = express.Router();

let transactions = [
  { id: 1, type: 'sale', amount: 25.0 }
];

router.get('/transactions', (req, res) => {
  res.json(transactions);
});

router.post('/transactions', (req, res) => {
  const transaction = { id: transactions.length + 1, ...req.body };
  transactions.push(transaction);
  res.status(201).json(transaction);
});

module.exports = router;
