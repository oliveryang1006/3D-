const express = require('express');
const router = express.Router();

let employees = [
  { id: 1, name: 'Alice', position: 'Barista' }
];

router.get('/employees', (req, res) => {
  res.json(employees);
});

router.post('/employees', (req, res) => {
  const employee = { id: employees.length + 1, ...req.body };
  employees.push(employee);
  res.status(201).json(employee);
});

module.exports = router;
