const express = require('express');
const path = require('path');

const inventory = require('./routes/inventory');
const hr = require('./routes/hr');
const accounting = require('./routes/accounting');

const app = express();
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/inventory', inventory);
app.use('/hr', hr);
app.use('/accounting', accounting);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`ERP server running on port ${PORT}`));
